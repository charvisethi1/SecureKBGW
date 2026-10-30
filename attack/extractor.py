"""Adaptive extraction attack and honest-buyer utility benchmark.

The attacker only sees answers. It crawls by querying content words it has not yet tried, taken from
answers it already received (the RAGCrawler idea, T-005, in a crude keyword form). This is a weak
attacker: a good result here is necessary, not sufficient (K-001, K-006).
"""
import random
import re
from collections import deque

from gateway import Gateway, KnowledgeBase, Ledger, Policy
from gateway.store import sentences, tokens

SEEDS = ["failure", "yield", "catalyst", "experiment", "reaction", "temperature", "recommended", "batch"]


def _fresh(kb, policy, credits=10**9):
    ledger = Ledger()
    ledger.add_buyer("k", "b", credits)
    return Gateway(kb, ledger, policy), ledger


ID = re.compile(r"\b([A-Z]{2,5})-(\d{4})\b")


def run_attack(kb: KnowledgeBase, policy: Policy, max_rounds=2000, enumerate_ids=False):
    """enumerate_ids=True adds the obvious smart move: once an answer shows an ID like EXP-0042,
    query its neighbours directly. Real attackers will notice identifiers."""
    gw, _ = _fresh(kb, policy)
    truth = {s for d in kb.docs for s in sentences(d.text)}
    got, tried, frontier = set(), set(), deque(SEEDS)
    rounds = 0
    while frontier and rounds < max_rounds:
        term = frontier.popleft()
        if term in tried:
            continue
        tried.add(term)
        rounds += 1
        r = gw.query("k", term)
        if r.status == "denied":
            break
        for s in sentences(r.answer):
            if s in truth:
                got.add(s)
        if enumerate_ids:
            for pre, num in ID.findall(r.answer):
                for n in range(max(int(num) - 3, 0), int(num) + 4):
                    frontier.appendleft(f"What happened in {pre}-{n:04d}?")
        for t in tokens(r.answer):
            if t not in tried:
                frontier.append(t)
    return {"queries": rounds, "sentences_recovered": len(got) / len(truth)}


def utility(kb: KnowledgeBase, policy: Policy, buyers=20, per_buyer=8, seed=1):
    """Honest buyers ask about a real experiment code and its failure cause. Scored on whether the
    answer contains the stated failure cause sentence."""
    rng = random.Random(seed)
    ok = total = 0
    for _ in range(buyers):
        gw, _ = _fresh(kb, policy)
        for d in rng.sample(kb.docs, per_buyer):
            code = d.id
            want = next(s for s in sentences(d.text) if "failure cause" in s)
            r = gw.query("k", f"What was the main failure cause for {code}?")
            total += 1
            ok += r.status == "ok" and want in r.answer
    return ok / total
