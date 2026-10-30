# MVP results (Phase 2 spike, synthetic data only)

What exists: a seller-hosted gateway (`gateway/`) with buyer keys, per-query credit metering, an audit log, output caps, a per-buyer query budget, an information budget (distinct source docs per buyer), a rate limit, relevance-based refusal, and a heuristic quarantine for seller docs containing prompt-injection phrases. It is exposed as an MCP server with one `ask` tool (`gateway/mcp_server.py`). Nine unit tests pass, including an MCP round trip.

Test data is 120 generated "failed experiment" notes. No real seller data has been used, and none should be until a lawyer has scoped the seller licence.

## Extraction test (`python -m attack.run`)
| policy | attacker | queries used | KB sentences recovered | honest-buyer utility |
|---|---|---|---|---|
| undefended | crawler | 143 | 23.8% | 100% |
| undefended | crawler + ID enumeration | 465 | 100% | 100% |
| default | crawler | 109 | 15.8% | 100% |
| default | crawler + ID enumeration | 191 | 15.5% | 100% |
| strict | either | 61 | 3.5% | 100% |

## What this does and does not show
- **Shows:** with no limits, a simple attacker that notices identifiers recovers 100% of the KB in 465 queries. The information budget caps a single key at about 25 of 120 docs (about 21% at most). Limits work against one honest-looking key.
- **Does not show:** that the defense holds in real conditions.
  - **Many keys.** The cap is per key. Five keys would recover about five times as much, so the cap only helps if buyer accounts are identity-verified and linked. Untested.
  - **Paraphrase leakage (K-006).** The answerer is extractive, so it leaks verbatim text within the caps. An LLM answerer has not been built or attacked.
  - **Attacker strength.** The attackers are crude keyword attackers, not the LLM agents in T-004 and T-005.
  - **Utility score.** The 100% figure is too easy: honest buyers ask 8 direct questions each, and the test never hits the doc cap. A buyer who legitimately needs more than 25 docs is blocked. That is the real product tradeoff.
  - **Injection filter.** It is a regex heuristic, so K-002 stays open.
- **Kill-criteria effect (provisional):** K-001 not confirmed on synthetic data with one key, and not mitigated either. Nothing else moved.

## Market entry, as far as it can go without sending anything
- The MVP can be demoed to a seller or buyer interviewee today through any MCP client.
- Interview requests and questions are in `findings/outreach-drafts.md`. Nothing has been sent. Approving, editing and sending them is your step.
- Before a real seller's data goes in: one lawyer scoping call on licence versus service and chain of title (see `research/implementation-plan.md`, Phase 3).
- Billing is credits only. There is no payment rail, no seller onboarding and no identity checks.
