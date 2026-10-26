# Kill criteria (conditions that would make the idea unviable)

Format: - [K-NNN] condition | evidence IDs | status: open / mitigated / confirmed | updated YYYY-MM-DD

- [K-001] No query-limiting or noise scheme exists that blocks reconstruction and differencing yet keeps answers useful enough to sell | R-001, R-002 | status: open | updated 2026-10-26
- [K-002] Seller content cannot be prevented from hijacking buyer agents, or buyer agents from manipulating the gateway, with a defense better than heuristics | R-003 | status: open | updated 2026-10-26
- [K-003] Fewer than a handful of credible sellers will list R&D knowledge (trade secret fear, cold start) | R-005, R-007, R-010 | status: open | updated 2026-10-26
- [K-004] Buyers cannot verify answer quality before paying and will not pay for unverifiable answers | R-006, R-013 | status: open | updated 2026-10-26
- [K-005] Liability for wrong or leaking answers cannot be allocated by contract or insurance at an acceptable cost (DPDP penalties, misrepresentation) | R-008, R-009 | status: open | updated 2026-10-26
- [K-006] LLM-based answerer leaks seller content through paraphrase beyond what the gateway can detect | R-004 | status: open | updated 2026-10-26
- [K-007] No named buyer pays for failed or unused-experiment knowledge at query level (only free pools, synthetic negatives, platform-scale licences exist) | R-017, R-013, R-010 | status: open | updated 2026-10-26
- [K-008] Hub exposure: competitor sellers and buyers exchanging non-public R&D signals through one gateway triggers hub-and-spoke or facilitator liability (US, India) that cannot be designed out | R-011, R-012 | status: open | updated 2026-10-26
- [K-009] Security promise depends on TEEs or attestation on hardware the seller does not control, which is defeated by cheap physical attacks, forcing seller-hosted deployment that small sellers cannot run | R-016 | status: open | updated 2026-10-26
- [K-010] Agent buyers cannot be onboarded without human-approved procurement and security review, so no autonomous pay-per-query volume materialises | R-014 | status: open | updated 2026-10-26
