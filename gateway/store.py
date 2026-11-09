"""Seller knowledge base: loading, injection quarantine and keyword retrieval."""
import json
import math
import re
from collections import Counter
from dataclasses import dataclass

TOKEN = re.compile(r"[a-z0-9]+")
STOP = frozenset(
    "the and for with that this from was were are has have had not but its into than then "
    "what which when where how why who does did can could would should about "
    "tell everything anything please give show details information know happened off much many".split()
)
# Heuristic only. Catches crude seller-side injection; a determined seller can evade it (K-002).
INJECTION = re.compile(
    r"ignore (all |any )?(previous|prior|above)|disregard (the )?(previous|above|system)|"
    r"you must now|system prompt|<\s*/?\s*(system|assistant|tool)\s*>|call the .{0,30} tool",
    re.I,
)


def _norm(t):
    """Crude word-form folding so raise/raised/raising and layoff/layoffs meet. Not a real stemmer;
    it only needs to be consistent between documents and questions."""
    if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
        t = t[:-1]
    if len(t) > 5 and t.endswith("ing"):
        t = t[:-3]
    elif len(t) > 4 and t.endswith("ed"):
        t = t[:-2]
    if len(t) > 3 and t.endswith("e"):
        t = t[:-1]
    return t


# Word forms that mean the same thing for retrieval. Keys are already folded by _norm; a value is
# the list of folded tokens it expands to, on both the document and the question side.
ALIAS = {
    "lay": ["layoff"], "laid": ["layoff"],
    "launch": ["releas"], "debut": ["releas"],
    "svb": ["silicon", "valley", "bank"], "fed": ["federal", "reserve"],
    "gme": ["gamestop"], "wfh": ["work", "home"],
    # irregular forms and near-synonyms that real questions use
    "withdrew": ["withdraw"], "sued": ["lawsuit"], "sue": ["lawsuit"], "fell": ["fall"], "ros": ["ris"], "depositor": ["deposit"], "worth": ["valuation"],
}


def tokens(text):
    out = []
    for t in TOKEN.findall(text.lower()):
        if t in STOP or not (len(t) > 2 or t.isdigit()):
            continue
        t = _norm(t)
        out.extend(ALIAS.get(t, [t]))
    return out


def _near(a, b):
    """True if a and b differ by one insertion, deletion, substitution or adjacent swap."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    if len(a) == len(b):
        return a[i + 1:] == b[i + 1:] or (a[i] == b[i + 1] and a[i + 1] == b[i] and a[i + 2:] == b[i + 2:])
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    return short[i:] == long_[i + 1:]


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

    @property
    def idf(self):
        return self._idf

    def search(self, query, k=1):
        """Return [(relevance 0..1, Doc)]. Relevance is the share of query idf mass found in the doc."""
        words = set(tokens(query))
        words = {self._repair(w) for w in words}
        # Runs of non-ASCII characters (other languages, emoji) cannot match this English corpus. Count
        # them as unknown words so they cannot be silently ignored.
        foreign = len(re.findall(r"[^\x00-\x7f]+", query))
        q = [t for t in words if t in self._idf]
        n_words = len(words) + foreign
        mean_idf = sum(self._idf.values()) / max(len(self._idf), 1)
        total = sum(self._idf[t] for t in q) + (n_words - len(q)) * mean_idf
        if not q:
            return []
        scored = []
        for d in self.docs:
            tf = self._tf[d.id]
            hit = sum(self._idf[t] * (1 + math.log(tf[t])) for t in q if t in tf)
            found = [t for t in q if t in tf]
            matched = sum(self._idf[t] for t in found)
            # With two or more words, one shared word is a coincidence ("capital" in "Melvin Capital").
            enough = len(found) >= min(2, n_words)
            scored.append((matched / total if enough else 0.0, hit, d))
        scored.sort(key=lambda s: (s[0], s[1]), reverse=True)
        return [(rel, d) for rel, _, d in scored[:k] if rel > 0]

    def _repair(self, w):
        """Fix a one-character typo ('nividia') by mapping an unknown word to the single close known word."""
        if w in self._idf or len(w) < 6:
            return w
        close = [v for v in self._idf if len(v) >= 5 and _near(w, v)]
        return close[0] if len(close) == 1 else w
