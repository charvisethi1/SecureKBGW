import random, string, time
from dataclasses import replace
from gateway import DEFAULT, Gateway, KnowledgeBase, Ledger
from gateway.store import sentences

kb = KnowledgeBase.load("data/market_tech_kb.json")
vocab = list(kb.idf)
src = {d.id: d.text for d in kb.docs}
rng = random.Random(42)
pol = replace(DEFAULT, min_interval_s=0.0, max_queries=10**9)
led = Ledger(); led.add_buyer("k", "k", 10**9, entity="e")
gw = Gateway(kb, led, pol)
junk_alpha = string.ascii_letters + string.digits + " .,!?$%&-'\"()/\\\n\t\x00" + "éñ股😀"

def rand_q():
    kind = rng.random()
    if kind < 0.35:   # real words, shuffled
        return " ".join(rng.choice(vocab) for _ in range(rng.randint(1, 8)))
    if kind < 0.6:    # real words with one-letter damage
        w = rng.choice(vocab); i = rng.randrange(len(w))
        return w[:i] + rng.choice(string.ascii_lowercase) + w[i + 1:] + " " + rng.choice(vocab)
    if kind < 0.8:    # pure junk
        return "".join(rng.choice(junk_alpha) for _ in range(rng.randint(0, 120)))
    if kind < 0.9:    # long
        return " ".join(rng.choice(vocab) for _ in range(rng.randint(50, 90)))[:500]
    return rng.choice(["", " ", "\n", "a", "I", "%", "'; DROP TABLE buyers;--", "<script>alert(1)</script>", "{{7*7}}", "${jndi:ldap://x}"])

n, ok, errors, over, foreign, slow = 20000, 0, [], 0, 0, 0.0
t0 = time.time()
for i in range(n):
    q = rand_q()
    t = time.time()
    try:
        r = gw.query("k", q)
    except Exception as e:
        errors.append((q[:40], repr(e)[:80])); continue
    slow = max(slow, time.time() - t)
    if r.status == "ok":
        ok += 1
        body = r.answer
        # strip the attribution tail and clipped marker, then every sentence must come from some note
        for s in sentences(body):
            s0 = s.rstrip("…").strip()
            if not any(s0 in txt or s0.startswith("Source") for txt in src.values()):
                foreign += 1
        content = body.split(" Source")[0]
        if len(content) > pol.max_answer_chars + 2:
            over += 1
_, used = led.revealed("e")
print(f"{n} random questions in {time.time()-t0:.1f}s, slowest single query {slow*1000:.0f} ms")
print(f"answered {ok}, exceptions {len(errors)}, over-cap answers {over}, sentences not in any note {foreign}")
print(f"revealed {used} chars, budget {pol.max_revealed_chars}: {'OK' if used <= pol.max_revealed_chars else 'EXCEEDED'}")
for e in errors[:5]: print("  EXC", e)
