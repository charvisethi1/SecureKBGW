"""The gateway: auth, limits, answering and metering in one call path.

The MVP answerer is extractive (returns capped source sentences). That is deliberately simple
and leaks verbatim text by design within the caps. An LLM answerer can replace `build_answer`
later, but paraphrase leakage (K-006) is then untested.

The information budget counts characters of source text newly shown to a buyer entity, so asking
the same document many ways cannot reveal more than the budget, and extra keys issued to the same
entity share it. Entities themselves are whatever the seller issues keys to; nothing here verifies
that two entities are not the same attacker (K-001).
"""
import re
import threading
import time
from dataclasses import dataclass

from .ledger import Ledger
from .policy import DEFAULT, Policy
from .store import KnowledgeBase, sentences, tokens


# Questions asking what to do with money. The sample only reports what happened, with sources.
ADVICE = re.compile(r"\b(should i|shall i|is it (a )?good (time|idea) to|worth (buying|investing)|buy or sell|"
                    r"good investment|price target|financial advice|investment advice)\b", re.I)
ADVICE_REASON = "this demo does not give investment advice"
# The notes are history, not a feed. Asking for a price "today" cannot be answered truthfully from them.
LIVE = re.compile(r"\b(today|right now|currently|at the moment|this week|live)\b.*\b(price|quote|trading|worth)\b|"
                  r"\b(price|quote|trading|worth)\b.*\b(today|right now|currently|at the moment|this week)\b|"
                  r"\b(current|latest|live) (stock |share )?(price|quote)\b", re.I)
LIVE_REASON = "this demo has no live prices"


@dataclass(frozen=True)
class Result:
    status: str  # ok | refused | denied
    answer: str = ""
    reason: str = ""
    charged: int = 0
    credits_left: int = 0


def _clip(s, room):
    """Cut at a word boundary and mark the cut; the result is never longer than `room`."""
    if len(s) <= room:
        return s
    cut = s[: max(room - 1, 0)].rsplit(" ", 1)[0].rstrip(" ,;:")
    return (cut + "\u2026") if cut else ""


def build_answer(doc, question, policy, seen, remaining, idf=None):
    """Pick up to max_sentences of the most relevant sentences, returned in reading order.
    Sentences the entity has already seen are free; new ones must fit in `remaining` chars.
    Returns (text, [(idx, chars)] newly revealed)."""
    q, idf = set(tokens(question)), idf or {}
    sents = sentences(doc.text)
    # A trailing "Source: ..." line is attribution, not content: it is not ranked, not budgeted,
    # and is appended to any answer drawn from this document.
    source = sents.pop() if sents and re.match(r"sources?:", sents[-1], re.I) else ""

    def score(i):
        return sum(idf.get(t, 1.0) for t in q & set(tokens(sents[i])))

    picked, new, used = [], [], 0
    for i in sorted(range(len(sents)), key=lambda i: (-score(i), i)):
        if len(picked) >= policy.max_sentences:
            break
        s = sents[i]
        is_new = (doc.id, i) not in seen
        room = policy.max_answer_chars - used
        if (is_new and len(s) > remaining) or room <= 0 or (picked and len(s) > room):
            continue  # whole sentences only after the first; the first may be clipped
        text = _clip(s, room)
        if not text:
            continue
        picked.append((i, text))
        used += len(text)
        if is_new:
            new.append((i, len(s)))
            remaining -= len(s)
    out = [t for _, t in sorted(picked)]
    if out and source:
        out.append(source)
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

        if ADVICE.search(question):
            self.ledger.record(key, "refused", question)
            return Result("refused", reason=ADVICE_REASON, credits_left=left)
        if LIVE.search(question):
            self.ledger.record(key, "refused", question)
            return Result("refused", reason=LIVE_REASON, credits_left=left)
        hits = self.kb.search(question, k=1)
        if not hits or hits[0][0] < p.min_relevance:
            self.ledger.record(key, "refused", question)
            return Result("refused", reason="no sufficiently relevant knowledge", credits_left=left)
        _, doc = hits[0]
        seen, used_chars = self.ledger.revealed(b["entity"])
        text, new = build_answer(doc, question, p, seen, p.max_revealed_chars - used_chars, self.kb.idf)
        if not text:
            self.ledger.record(key, "refused", question)
            return Result("refused", reason="information budget reached", credits_left=left)
        self.ledger.record(key, "ok", question, doc.id, len(text), p.price_per_query, new)
        return Result("ok", answer=text, charged=p.price_per_query, credits_left=left - p.price_per_query)
