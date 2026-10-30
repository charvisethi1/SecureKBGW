"""The gateway: auth, limits, answering and metering in one call path.

The MVP answerer is extractive (returns capped source sentences). That is deliberately simple
and leaks verbatim text by design within the caps. An LLM answerer can replace `build_answer`
later, but paraphrase leakage (K-006) is then untested.

The information budget counts characters of source text newly shown to a buyer entity, so asking
the same document many ways cannot reveal more than the budget, and extra keys issued to the same
entity share it. Entities themselves are whatever the seller issues keys to; nothing here verifies
that two entities are not the same attacker (K-001).
"""
import threading
import time
from dataclasses import dataclass

from .ledger import Ledger
from .policy import DEFAULT, Policy
from .store import KnowledgeBase, sentences, tokens


@dataclass(frozen=True)
class Result:
    status: str  # ok | refused | denied
    answer: str = ""
    reason: str = ""
    charged: int = 0
    credits_left: int = 0


def build_answer(doc, question, policy, seen, remaining):
    """Pick up to max_sentences most relevant sentences. Sentences the entity has already seen are
    free; new ones must fit in `remaining` chars. Returns (text, [(idx, chars)] newly revealed)."""
    q = set(tokens(question))
    sents = sentences(doc.text)
    order = sorted(range(len(sents)), key=lambda i: len(q & set(tokens(sents[i]))), reverse=True)
    out, new, used = [], [], 0
    for i in order:
        if len(out) >= policy.max_sentences:
            break
        s = sents[i]
        is_new = (doc.id, i) not in seen
        if is_new and len(s) > remaining:
            continue
        s = s[: max(policy.max_answer_chars - used, 0)].rstrip()
        if not s:
            break
        out.append(s)
        used += len(s)
        if is_new:
            new.append((i, len(sents[i])))
            remaining -= len(sents[i])
    return " ".join(out), new


class Gateway:
    def __init__(self, kb: KnowledgeBase, ledger: Ledger, policy: Policy = DEFAULT, clock=time.time):
        self.kb, self.ledger, self.policy, self._clock = kb, ledger, policy, clock
        self._lock = threading.Lock()  # budget checks and the charge must be one atomic step

    def set_kb(self, kb):
        with self._lock:
            self.kb = kb

    def query(self, key, question) -> Result:
        with self._lock:
            return self._query(key, question)

    def _query(self, key, question) -> Result:
        b = self.ledger.buyer(key)
        if b is None:
            return Result("denied", reason="unknown buyer key")
        p, left = self.policy, b["credits"]
        if len(question) > p.max_question_chars:
            return Result("denied", reason="question too long", credits_left=left)
        if self.ledger.entity_queries(b["entity"]) >= p.max_queries:
            return Result("denied", reason="query budget exhausted", credits_left=left)
        if b["last_ts"] and self._clock() - b["last_ts"] < p.min_interval_s:
            return Result("denied", reason="rate limited", credits_left=left)
        if left < p.price_per_query:
            return Result("denied", reason="insufficient credits", credits_left=left)

        hits = self.kb.search(question, k=1)
        if not hits or hits[0][0] < p.min_relevance:
            self.ledger.record(key, "refused", question)
            return Result("refused", reason="no sufficiently relevant knowledge", credits_left=left)
        _, doc = hits[0]
        seen, used_chars = self.ledger.revealed(b["entity"])
        text, new = build_answer(doc, question, p, seen, p.max_revealed_chars - used_chars)
        if not text:
            self.ledger.record(key, "refused", question)
            return Result("refused", reason="information budget reached", credits_left=left)
        self.ledger.record(key, "ok", question, doc.id, len(text), p.price_per_query, new)
        return Result("ok", answer=text, charged=p.price_per_query, credits_left=left - p.price_per_query)
