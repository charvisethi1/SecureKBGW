# Implementation plan (DRAFT for review)

Status: draft. Nothing here is built, sent or filed. Legal items are for a lawyer to confirm, not advice. Evidence IDs point to `findings/`; many are partly supported or unverified, and the competitor gap is inferred, not verified (`findings/synthesis.md`).

## Principle
The evidence leans against building as specified, and all 10 kill criteria are open. So the plan is ordered to **kill the idea cheaply or prove the riskiest assumption first**, spending the least money and doing the least legal work until demand is shown. Each phase ends with a go/no-go gate.

## Phase 0: Decide scope and prepare a lawyer brief (about 1 week, no engineering)
- Pick a beachhead: one narrow vertical and one seller type (e.g. pharma/biotech or specialty chemicals, mid-size sellers without consortium access; M-007, M-024, M-031).
- Reconcile `findings/review.md` (M-004, M-045, M-051 listed supported but downgraded in the deep-dive rows) and review M-057..M-062 and R-001..R-017.
- Package `findings/legal.md` "Questions for a lawyer" as a short brief. **Do not commission further legal research or draft contracts yet.** One scoping call with an Indian IP/data lawyer is the only legal step in this phase.

**Gate:** a one-paragraph product definition and a named beachhead.

## Phase 1: Demand test, no code (3-4 weeks; tests K-003, K-007, K-010)
- Edit and use `findings/outreach-drafts.md`. Send nothing without your approval; you send them yourself.
- Target 10 seller-side and 10 buyer-side interviews. Ask about willingness to sell, willingness to pay, price, and procurement for agent buyers.
- Track against the falsification questions already in the draft.
- Test an alternative the evidence favours: data-for-access swaps instead of cash (TuneLab-style, M-027).

**Gate (go):** at least 3 sellers say they would list specific material, and at least 2 buyers name a budget or a concrete price. **Gate (stop or pivot):** nobody names a price, or sellers refuse on trade-secret fear.

## Phase 2: Technical spike (4-6 weeks; tests K-001, K-002, K-006, K-009; start only after Phase 1 go)
Build the smallest thing that can fail:
- **Seller-hosted answerer** over a small synthetic knowledge base, exposed as an MCP server (avoids the TEE trust problem for small sellers; T-021, T-022).
- **Defenses to measure, not assume:** per-buyer query budgets, output caps, query-stream anomaly detection (T-027), and DP on a synthetic copy (T-025).
- **Red-team harness:** replay RAG-extraction attacks (RAGCrawler-style, T-004, T-005) against the gateway and report how much leaks under each defense.
- **Injection tests** both ways (seller content to buyer agent, buyer agent to gateway).
- Metering/billing stub only (x402 or Stripe Meters; T-016, T-023). No real money.

**Gate:** a number. If an adaptive extractor recovers more than an agreed threshold of the KB within a realistic budget while answers stay useful, K-001 is confirmed and the design must change or stop.

## Phase 3: Legal structuring (only after Phases 1-2 pass)
This is where legal work becomes major. Do it with counsel, in this order:
1. Licence vs service vs disclosure characterisation (no supported findings yet).
2. Competition-law review of a gateway linking competitors (hub-and-spoke; L-017..L-021, R-011, R-012, K-008).
3. DPDP/GDPR position if any answer can carry personal data (L-008, L-013; DPDP core duties start about 13 May 2027).
4. Liability allocation, disclaimers, insurance (K-005; no Indian authority found, L-026, L-036).
5. Three-way contract (platform, seller, buyer) and chain-of-title for seller data (L-042, L-043).
6. Payment rails and cross-border rules for an Indian entity (stablecoin/x402 questions, FEMA/RBI).

**Gate:** counsel confirms a structure that is not designed out by competition or liability risk.

## Phase 4: Paid pilot (8-12 weeks)
- One seller, 2-3 buyers, fiat billing, human-approved procurement, manual review of every answer category.
- Measure: answer quality as judged by buyers (K-004), repeat queries, price acceptance, leakage incidents.

## Phase 5: Build decision
Decide with the kill-criteria table updated from real evidence, not desk research.

## Kill-criteria map
| Criterion | Tested in |
|---|---|
| K-001, K-006 reconstruction and paraphrase leakage | Phase 2 |
| K-002 injection | Phase 2 |
| K-003 too few sellers, K-007 nobody pays | Phase 1 |
| K-004 unverifiable answer quality | Phase 4 |
| K-005 liability, K-008 hub exposure | Phase 3 |
| K-009 TEE dependence | Phase 2 (seller-hosted design) |
| K-010 agent procurement | Phase 1, then Phase 4 |

## Open decisions for you
1. Beachhead vertical and seller type.
2. Cash per query vs credits/swap as the first offer.
3. Seller-hosted (default in this plan) vs platform-hosted architecture.
4. Whether to run Phase 1 at all, given the current tally (20 for, 50 against among reviewed findings).
