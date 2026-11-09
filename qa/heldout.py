from dataclasses import replace
from gateway import DEFAULT, Gateway, KnowledgeBase, Ledger
kb = KnowledgeBase.load("data/market_tech_kb.json")
ANS = [  # (question, acceptable note ids, substring expected in answer)
 ("What was the Dow's worst day in March 2020?", {"mkt-2020-black-days"}, "12.93"),
 ("Did the market recover by the end of 2020?", {"mkt-2020-crash"}, "November 2020"),
 ("How did the stock market do in 2019?", {"mkt-sp-returns-2019-2021"}, "28.88"),
 ("What percent did the S&P 500 gain in 2023?", {"mkt-sp-returns-2022-2025", "mkt-2023-rebound"}, "24.23"),
 ("Why was Robinhood sued?", {"mkt-gamestop-robinhood"}, "34"),
 ("How high did GameStop stock go?", {"mkt-gamestop-squeeze"}, "483"),
 ("How much did short sellers lose on GameStop?", {"mkt-gamestop-short-interest"}, "$6 billion"),
 ("What was the worst year for bonds?", {"mkt-2022-causes"}, "1994"),
 ("How big was Silicon Valley Bank?", {"mkt-svb-collapse"}, "$209 billion"),
 ("Which banks fell after SVB collapsed?", {"mkt-svb-response"}, "First Republic"),
 ("What is Nvidia's revenue?", {"mkt-nvidia-revenue"}, "billion"),
 ("How many chips are in a car?", {"tech-chip-shortage"}, "1,400"),
 ("What drove the chip shortage in 2021?", {"tech-chip-shortage-causes", "tech-chip-shortage"}, ""),
 ("Who signed the CHIPS Act?", {"tech-chips-act"}, "Biden"),
 ("How many people worked remotely in 2022?", {"tech-remote-work-census"}, "15.2"),
 ("What did Bloom say about remote days?", {"tech-remote-work-hybrid"}, "third"),
 ("Which company laid off 12,000 people?", {"tech-layoffs-google"}, "Google"),
 ("Did Zoom cut jobs?", {"tech-zoom"}, "15%"),
 ("Which cloud provider is biggest?", {"tech-aws-cloud"}, "31%"),
 ("How many users did ChatGPT have after two months?", {"tech-chatgpt-launch"}, "100 million"),
 ("What model did ChatGPT start with?", {"tech-chatgpt-launch"}, "GPT-3.5"),
 ("What happened to Nvidia stock after DeepSeek?", {"mkt-deepseek-selloff"}, "18%"),
 ("How much of the S&P 500 is the Magnificent Seven?", {"mkt-magnificent-seven"}, "29%"),
 ("What AI chip does Nvidia sell and for how much?", {"mkt-nvidia-gpu-demand"}, "$25,000"),
 ("What happened in the markets in 2020?", {"mkt-2020-crash", "mkt-2020-black-days", "mkt-sp-returns-2019-2021"}, ""),
]
OUT = ["Who is the CEO of Nvidia?", "what's Tesla's stock price today", "predict the S&P 500 for 2027",
       "How do I invest in index funds?", "What is bitcoin worth?", "Explain how the Federal Reserve works in detail",
       "Who founded Zoom?", "What is the weather in New York?"]
def ask(q):
    led = Ledger(); led.add_buyer("k","k",9)
    r = Gateway(kb, led, replace(DEFAULT, min_interval_s=0)).query("k", q)
    h = kb.search(q, 1)
    return r, (h[0][1].id if h else None)
ok = 0
for q, want, sub in ANS:
    r, got = ask(q)
    good = r.status == "ok" and got in want and sub in r.answer
    ok += good
    if not good: print(f"  MISS {q[:52]:<52} got={got} status={r.status} {'(answer lacks '+repr(sub)+')' if got in want and r.status=='ok' else ''}")
print(f"held-out answerable: {ok}/{len(ANS)}")
leak = 0
for q in OUT:
    r, got = ask(q)
    leak += r.status == "ok"
    print(f"  {'ANSWERED' if r.status=='ok' else 'refused ':<8} {q:<50} {got if r.status=='ok' else ''}")
print(f"held-out out-of-scope answered: {leak}/{len(OUT)}")
