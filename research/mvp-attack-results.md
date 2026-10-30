# MVP attack results (synthetic data, 120 notes)

Reproduce: `python -m attack.suite` (in-process), `python -m attack.run` (benchmark), plus the curl checks described below against `./skbgw serve`. Authorised testing of our own prototype only.

Round 1 found three serious breaks. Round 2 applied fixes and re-ran the same attacks.

## Before and after (`attack/suite.py`)
| attack | round 1 | round 2 (after fixes) |
|---|---|---|
| 1 key enumerating IDs | HELD, 12% | HELD, 12% |
| 5 keys, same buyer entity | not tested | **HELD**, 12% (shared limits) |
| 5 keys, 5 separate entities | BROKEN, 60% | **still BROKEN**, 59% |
| re-asking docs in 5 different ways | BROKEN, 100% of the 25 reachable docs verbatim | **HELD**, 12% of KB text (4000-char budget) |
| junk words plus one real token | BROKEN, answered | **HELD**, refused |
| burst rate, one key | PARTIAL, about 4,500 queries/s | **HELD**, 1 of 200 served in a burst (0.05s limit) |
| 1 MB and malformed questions | HELD, no length cap | HELD, 500-char cap |
| 8 threads racing on 10 credits | HELD | HELD (charged exactly 10) |
| forged keys, SQL injection | HELD | HELD |
| hostile seller notes (injection) | BROKEN, regex caught 1 of 10 | **still BROKEN**, 1 of 10 |
| answered vs refused reveals what the seller researched | PARTIAL | **still PARTIAL** |

Benchmark (`attack.run`), default policy: the ID-enumerating crawler now recovers 12.0% of the KB (was 15.5%). With no limits it recovers 100%.

HTTP (live server): no key, wrong key, SQL-injection key, `Basic` scheme and path traversal give 401; malformed JSON 400; a 10 MB body 413; 300 random keys 0 successes. `GET` and `DELETE` on `/mcp` now return 405 instead of holding the connection open.

## What the fixes changed
1. **Information budget counts content, not documents.** Each buyer entity may be shown at most 4,000 characters of new source text. Re-showing text it already has costs nothing. Rewording questions cannot extract more.
2. **Limits are per buyer entity.** Keys with the same `--entity` share the query count and the content budget.
3. **Relevance counts unknown words against the question.** Junk padding no longer lets one real word through.
4. **Rate limit (0.05s per key), 500-character question cap, POST-only HTTP.**

## What is still open
- **Many entities.** Five keys under five names still recover 59% of the KB. Nothing stops one attacker holding several entities. This needs real identity checks and contracts, so it is a business control, not code. K-001 remains open.
- **Raw data is still shown.** Within the budget the buyer receives verbatim source sentences. The "no raw data" promise is only true as "a capped amount of raw text".
- **Injection (K-002).** The regex filter catches 1 of 10 evasions. Do not rely on it. Answers carry `content_type: untrusted_seller_data` as a convention only.
- **Existence oracle.** Answered versus refused tells a buyer what the seller has researched.
- **Utility is under-tested.** Honest buyers score 100% on an easy test. A buyer who legitimately needs more than the budget (4,000 characters, about 10% of this KB) is cut off. Whether that is commercially acceptable is a question for the demand interviews.
- **Not tested:** an LLM answerer (K-006), LLM-driven attackers, a seller changing notes after sale, HTTPS deployment.
