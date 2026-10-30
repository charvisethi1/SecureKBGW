"""The gateway: auth, limits, answering and metering in one call path.

The MVP answerer is extractive (returns capped source sentences). That is deliberately simple
and leaks verbatim text by design within the caps. An LLM answerer can replace `answer_extractive`
later, but paraphrase leakage (K-006) is then untested.
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


def answer_extractive(doc, question, policy):
    q = set(tokens(question))
    ranked = sorted(sentences(doc.text), key=lambda s: len(q & set(tokens(s))), reverse=True)
    out, used = [], 0
    for s in ranked[: policy.max_sentences]:
        if used + len(s) > policy.max_answer_chars:
            s = s[: max(policy.max_answer_chars - used, 0)].rstrip()
        if s:
            out.append(s)
            used += len(s)
    return " ".join(out)


class Gateway:
    def __init__(self, kb: KnowledgeBase, ledger: Ledger, policy: Policy = DEFAULT, clock=time.time):
        self.kb, self.ledger, self.policy, self._clock = kb, ledger, policy, clock
        self._lock = threading.Lock()  # budget checks and the charge must be one atomic step

    def query(self, key, question) -> Result:
        with self._lock:
            return self._query(key, question)

    def _query(self, key, question) -> Result:
        b = self.ledger.buyer(key)
        if b is None:
            return Result("denied", reason="unknown buyer key")
        p, left = self.policy, b["credits"]
        if b["queries"] >= p.max_queries:
            return Result("denied", reason="query budget exhausted", credits_left=left)
        if self._clock() - b["last_ts"] < p.min_interval_s:
            return Result("denied", reason="rate limited", credits_left=left)
        if left < p.price_per_query:
            return Result("denied", reason="insufficient credits", credits_left=left)

        hits = self.kb.search(question, k=1)
        if not hits or hits[0][0] < p.min_relevance:
            self.ledger.record(key, "refused", question)
            return Result("refused", reason="no sufficiently relevant knowledge", credits_left=left)
        _, doc = hits[0]
        seen = self.ledger.docs_seen(key)
        if doc.id not in seen and len(seen) >= p.max_distinct_docs:
            self.ledger.record(key, "refused", question)
            return Result("refused", reason="information budget reached", credits_left=left)

        text = answer_extractive(doc, question, p)
        self.ledger.record(key, "ok", question, doc.id, len(text), p.price_per_query)
        return Result("ok", answer=text, charged=p.price_per_query, credits_left=left - p.price_per_query)
