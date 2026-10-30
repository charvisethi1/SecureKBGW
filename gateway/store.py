"""Seller knowledge base: loading, injection quarantine and keyword retrieval."""
import json
import math
import re
from collections import Counter
from dataclasses import dataclass

TOKEN = re.compile(r"[a-z0-9]+")
STOP = frozenset(
    "the and for with that this from was were are has have had not but its into than then "
    "what which when where how why who does did can could would should about".split()
)
# Heuristic only. Catches crude seller-side injection; a determined seller can evade it (K-002).
INJECTION = re.compile(
    r"ignore (all |any )?(previous|prior|above)|disregard (the )?(previous|above|system)|"
    r"you must now|system prompt|<\s*/?\s*(system|assistant|tool)\s*>|call the .{0,30} tool",
    re.I,
)


def tokens(text):
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP and len(t) > 2]


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


@dataclass(frozen=True)
class Doc:
    id: str
    title: str
    text: str


class KnowledgeBase:
    def __init__(self, docs):
        self.quarantined = [d.id for d in docs if INJECTION.search(d.title + " " + d.text)]
        bad = set(self.quarantined)
        self.docs = [d for d in docs if d.id not in bad]
        self._tf = {d.id: Counter(tokens(d.title + " " + d.text)) for d in self.docs}
        df = Counter()
        for tf in self._tf.values():
            df.update(tf.keys())
        n = max(len(self.docs), 1)
        self._idf = {t: math.log(1 + n / c) for t, c in df.items()}

    @classmethod
    def load(cls, path):
        with open(path) as f:
            return cls([Doc(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.docs)

    def search(self, query, k=1):
        """Return [(relevance 0..1, Doc)]. Relevance is the share of query idf mass found in the doc."""
        q = [t for t in set(tokens(query)) if t in self._idf]
        total = sum(self._idf[t] for t in q)
        if not total:
            return []
        scored = []
        for d in self.docs:
            tf = self._tf[d.id]
            hit = sum(self._idf[t] * (1 + math.log(tf[t])) for t in q if t in tf)
            matched = sum(self._idf[t] for t in q if t in tf)
            scored.append((matched / total, hit, d))
        scored.sort(key=lambda s: (s[0], s[1]), reverse=True)
        return [(rel, d) for rel, _, d in scored[:k] if rel > 0]
