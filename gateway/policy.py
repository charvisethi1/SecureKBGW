"""Per-buyer limits. Each field maps to a kill criterion or finding it is meant to test."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Policy:
    price_per_query: int = 1  # credits, charged only for answered queries
    max_queries: int = 200  # lifetime query budget per buyer entity (T-027, K-001)
    max_answer_chars: int = 300  # output cap (K-001)
    max_sentences: int = 2  # output cap (K-001)
    min_relevance: float = 0.34  # below this the gateway refuses instead of guessing
    max_revealed_chars: int = 4000  # information budget: new source text shown to an entity (K-001)
    min_interval_s: float = 0.05  # rate limit between queries on one key
    max_question_chars: int = 500  # longer questions are denied


DEFAULT = Policy()
# Roughly what a naive gateway would do: no caps at all. Used as the attack baseline.
UNDEFENDED = Policy(max_queries=10**9, max_answer_chars=10**6, max_sentences=10**6, min_relevance=0.0,
                    max_revealed_chars=10**9, min_interval_s=0.0, max_question_chars=10**9)
STRICT = Policy(max_queries=60, max_answer_chars=200, max_sentences=1, max_revealed_chars=2000)
