# QA report: public demo (tech and US stocks sample)

Run against the code on `main` plus the uncommitted fixes described below. Scripts are in `qa/`; run them with `PYTHONPATH=. .venv/bin/python qa/<name>.py` (`live.py` takes `QA_URL=<base url>`).

## Headline numbers
| Check | First run | After fixes |
|---|---|---|
| Expected-answer questions (57, tuned set) | 43 correct | 57 correct (inflated: data was tuned to these) |
| Out-of-scope / junk questions answered (15) | 2 | 0 |
| **Held-out questions (25 new phrasings)** | **18 correct (72%)** | 22 (88%) after fixing, no longer unseen |
| Held-out out-of-scope answered (8) | 1 | 0 |
| 20,000 random questions | 0 exceptions, 0 over-cap answers, 0 text from outside the notes, budget respected | unchanged |
| Slowest single query | 8 ms | |
| Attack suite | 2 broken, 1 partial, 8 held | unchanged |
| Unit tests | 28 passing | 28 passing |

The honest accuracy figure is the **72% first-pass held-out score**. Expect real visitors to land somewhere between that and the tuned figure, and expect new phrasings to find new misses.

## Bugs found and fixed (locally, not yet deployed)
1. **Synonym and word-form misses.** "launched" vs "released", "SVB" vs "Silicon Valley Bank", "Fed" vs "Federal Reserve", "raise" vs "raised", "withdraw" vs "withdrew", "sued" vs "lawsuits". Fixed with word folding and a small alias list.
2. **Right note, wrong sentence.** Notes that covered several topics (layoffs for four companies, Nvidia milestones) returned the wrong figures. Fixed by splitting notes and ranking sentences by rarity.
3. **Typos refused.** "nividia", "chatgtp" are now repaired to the single close word.
4. **Non-English and emoji ignored.** A Chinese question plus "2022" was answered from "2022" alone. Unknown scripts now count as unknown words.
5. **One shared word was enough.** "capital of France" matched "Melvin Capital". Now two matching words are required when a question has two or more.
6. **Source line outranked content and answers were cut mid-word.** Source lines are now attribution only; trimming happens at word boundaries.
7. **Investment questions got a generic answer.** "Should I buy Nvidia stock?" is now refused with a clear reason. "What is Tesla's stock price today?" is refused because the notes have no live prices.
8. **A real defect the unit tests missed in the earlier build:** a request with no Authorization header crashed instead of returning 401 (fixed earlier).

## Known limitations (not fixed)
- Keyword matching only. Multi-topic questions ("compare Amazon and Meta layoffs") return one note, which is misleading.
- Numbers in questions are weak signals ("Which company laid off 12,000 people?" returns Meta).
- Three held-out questions still pick the wrong sentence inside the right note.
- The notes were summarised from Wikipedia pages by an automated fetch and not hand-verified.
- The extraction weaknesses in `research/mvp-attack-results.md` are unchanged (many entities, injection filter).

## Live site (https://securekbgw.onrender.com), checked before the fixes were deployed
- Healthy and fast: config 0.3 s, answers about 0.3 s p50.
- Security headers present (CSP, nosniff), no open CORS, admin routes 404, MCP 401 without a key and 405 on GET.
- Demo key limit works (third key from one IP refused).
- It runs the previous code, so it still answers "Should I buy Nvidia stock?". Deploy the fixes to change that.
- A first live attempt at the malformed-request and concurrency tests was flawed (no key, credits already spent). The same tests were re-run against a local copy of the current code: no server errors, rate limit held under 100 parallel requests, credits never negative.

## Not tested
- **The UI in a real browser.** Layout, dark mode, the new scope banner and phone view have not been looked at. The page script parses and the ids match, nothing more.
- Real concurrent users at scale, Render cold-start timing, and MCP clients.
- An LLM answerer and LLM-driven attackers.
