"""Direction questions: does the gateway tell "went up" from "went down"?

Each question names a direction (rise or fall, raise or cut, better or worse). tokens() drops
words under three letters, so "up" never reaches retrieval, and nothing treats rise and fall as
opposites. Retrieval can then land on a note about the opposite move, and that answer is charged.

Counts three outcomes:
  right          answered from an acceptable note, and the answer has the expected text
  charged wrong  answered (1 credit taken) but from the wrong note or missing the expected text
  refused        not answered, not charged (a miss, but a free one)

Run: PYTHONPATH=. .venv/bin/python qa/direction.py
"""
from dataclasses import replace
from gateway import DEFAULT, Gateway, KnowledgeBase, Ledger

kb = KnowledgeBase.load("data/market_tech_kb.json")
NVIDIA_UP = {"mkt-nvidia-1-to-3-trillion", "mkt-nvidia-4-and-5-trillion", "mkt-nvidia-gpu-demand", "mkt-nvidia-revenue"}

DIR = [  # (question, acceptable note ids, substring expected in answer)
 # Nvidia: rise vs the DeepSeek fall
 ("Why did Nvidia stock go up so much?", NVIDIA_UP, ""),
 ("How did Nvidia stock rise so fast?", NVIDIA_UP, ""),
 ("When did Nvidia stock go down?", {"mkt-deepseek-selloff"}, "18%"),
 ("Did Nvidia ever lose a lot of value in one day?", {"mkt-deepseek-selloff"}, "$600"),
 # S&P 500: up year vs down year
 ("How much did the S&P 500 go up in 2023?", {"mkt-sp-returns-2022-2025", "mkt-2023-rebound"}, "24.23"),
 ("How much did the S&P 500 go down in 2022?", {"mkt-2022-decline", "mkt-sp-returns-2022-2025"}, "19"),
 ("When did stocks bounce back after the 2022 drop?", {"mkt-2023-rebound"}, "2023"),
 # Fed: raising vs cutting
 ("When did the Fed start raising rates?", {"mkt-fed-hiking-cycle", "mkt-2022-causes"}, "March 2022"),
 ("When did the Fed cut rates to zero?", {"mkt-fed-2020"}, "0.25%"),
 # Others where the note holds both directions or a reversal
 ("Did working from home go down after 2021?", {"tech-remote-work-census"}, "13.8"),
 ("Did GameStop short interest go down?", {"mkt-gamestop-short-interest"}, "15%"),
 ("When did the Magnificent Seven stocks drop?", {"mkt-magnificent-seven-2024"}, "5 August 2024"),
 ("Why did bank stocks go down in March 2023?", {"mkt-svb-response", "mkt-svb-cause", "mkt-svb-collapse"}, ""),
 ("Did the chip shortage get better?", {"tech-chip-shortage"}, "subsided"),
 ("Did Zoom stock go up on its first day?", {"tech-zoom"}, "72%"),
]


def ask(q):
    led = Ledger(); led.add_buyer("k", "k", 9)
    r = Gateway(kb, led, replace(DEFAULT, min_interval_s=0)).query("k", q)
    h = kb.search(q, 1)
    return r, (h[0][1].id if h else None)


right = wrong = refused = 0
for q, want, sub in DIR:
    r, got = ask(q)
    if r.status != "ok":
        refused += 1; tag = "REFUSED"
    elif got in want and sub in r.answer:
        right += 1; tag = "right"
    else:
        wrong += 1; tag = "CHARGED WRONG"
    print(f"  {tag:<13} {q[:50]:<50} got={got}")
print(f"direction questions: {right} right, {wrong} charged wrong, {refused} refused, of {len(DIR)}")
