# Synthesis: secure KB gateway (evidence only, no recommendation)

Tags: [S] supported, [P] partly supported (use with the caveat in review.md), [UNREVIEWED] not in review.md (all R- findings and all K- kill criteria). Unsupported and unverifiable findings are excluded from conclusions and listed below. Source of verdicts: `findings/review.md`.

## As of

2026-10-26 (all findings retrieved and reviewed on this date).

| Department | Total | Supported | Partly supported | Unsupported | Unverifiable | Unreviewed |
|---|---|---|---|---|---|---|
| Legal (L-001..L-043) | 43 | 11 | 11 | 4 | 17 | 0 |
| Technical (T-001..T-027) | 27 | 9 | 13 | 1 | 4 | 0 |
| Market (M-001..M-031) | 31 | 6 | 17 | 1 | 7 | 0 |
| Red-team (R-001..R-017) | 17 | 0 | 0 | 0 | 0 | 17 [UNREVIEWED] |
| Kill criteria (K-001..K-010) | 10 | n/a | n/a | n/a | n/a | 10 [UNREVIEWED]; all status open |
| Reviewed total | 101 | 26 | 41 | 6 | 28 | |

Ignored as unsupported: L-006, L-007, L-011, L-039, T-002, M-022.
Ignored as unverifiable (cited page unreadable or finding is a gap or inference only): L-004, L-005, L-012, L-013, L-014, L-015, L-016, L-017, L-018, L-019, L-021, L-026, L-029, L-032, L-035, L-037, L-043, T-008, T-011, T-012, T-014, M-005, M-007, M-013, M-015, M-019, M-020, M-031.
Gap-type findings (L-014, L-016, L-043, T-015, M-013, M-031) are used only under Biggest unknowns.

## Cross-department dependencies

- Legal needs controls that technical cannot yet guarantee. US trade-secret status needs reasonable measures (L-030 [S]) and lawful derivation or reverse engineering is not improper means (L-031 [S]). Agent-driven extraction recovered over 70 percent of a private RAG KB (T-004 [S]) and plans benign-looking queries (T-005 [S]), and query diversity raised extraction under a threshold defense (T-020 [S]). So if technical limits fail, the seller's remaining protection is contract (L-031 [S], M-016 [S], L-001 [S]). The EU equivalent (L-004) is unverifiable.
- Contract-only protection feeds seller cost. Chain of title needs signed written assignments, with India-only and five-year defaults (L-042 [S]); pharma data deals treat ownership as a sticking point (M-026 [P]) and licences carry limited-use and no-resharing terms (M-025 [P]). This links legal review cost to seller willingness (M-016 [S], M-014 [P]).
- Hosting trust shapes both legal and technical design. A sub-1000 USD interposer forges TEE attestation (T-021 [P], T-006 [P]), so confidential computing helps only if the host is physically controlled (T-022 [P], inference). India's cross-border rules (s.16) are not yet commenced and sectoral localisation still applies (L-009 [S]). Both point toward seller-hosted or federated deployment, but the federated-vs-central comparison itself is unverifiable (T-014). Small sellers' ability to host is untested (K-009 [UNREVIEWED]).
- Data-protection law attaches to what answers reveal. DPDP has no stated exemption for commercial data (L-034 [S]), core DPDP duties start about 13 May 2027 (L-008 [S]), and penalty caps reach Rs 250 crore (L-010 [P]). This requires technical output filtering, but LLM-level filters were bypassed at over 90 percent (T-003 [P]) and clean-room DP covers only aggregates, not free-text answers (T-013 [P]). GDPR anonymity is judged by means reasonably likely to be used (L-040 [S]).
- Differential privacy trades accuracy for safety. Noise of order sqrt(n) is needed to stop reconstruction (T-001 [P]); DP use has a contested utility cost (T-026 [S]); a DP synthetic corpus avoids per-query budget burn but the buyer then queries a lossy copy (T-025 [S], inference). Pay-per-query sells accuracy (R-001 [UNREVIEWED]).
- Competition law constrains who may be on both sides. US safe harbours for information sharing and competitor collaboration are withdrawn (L-020 [P], L-038 [S]). Sellers already fear strengthening competitors (M-025 [P]) and pharma sharing today runs through governed consortia (M-008 [S]). Buyer-seller pair vetting as mitigation is analyst inference (L-021 unverifiable).
- Payments depend on legal rails. x402 supports fixed, max-authorise and deferred pricing (T-016 [S]) and CDP reports over 100 million payments (T-017 [P]), but USDC rails and Indian RBI, FEMA and tax treatment are unverified inference (T-017 [P]). Stripe usage billing is a fiat alternative for contracted buyers (T-023 [S]).
- Liability allocation depends on both contract law and technical accuracy. Exclusion clauses are generally enforceable in India (L-025 [P]) but EU Data Act terms limiting liability for gross negligence are blacklisted (L-027 [P]). Indian authority on negligent misstatement for AI output is absent (L-036 [P]) and s.79 safe harbour for a gateway that composes answers is untested (L-022 [P], L-023 [P]).
- Agent-buyer design depends on injection risk. Tool-description poisoning works without the tool being executed (T-007 [P]), results from one MCP server are untrusted input to another (T-010 [P]), and MCP authorization is optional (T-009 [P]). Buyer onboarding then leans on human-approved procurement (R-014 [UNREVIEWED], M-023 [P]).

## Conflicts between departments

- Payment rails exist, buyer demand is unproven. Metering and agent-payment flows are documented (T-016 [S], T-023 [S], M-004 [S] as a metered precedent), but agent purchasing is described as still early with no independent evidence (M-023 [P], R-014 [UNREVIEWED]).
- Clean-room precedent versus fit. AWS Clean Rooms is a working metered pay-per-use precedent (M-004 [S]), but its DP supports only user-level aggregates, not natural-language answers (T-013 [P]).
- Demand pain versus paid demand. Failed data improves models and is scarce (M-011 [P], M-012 [P], M-028 [P]) and duplication waste is quantified (M-021 [S], opinion, 2011), but the quoted remedies are free pooling (M-021 [S], M-009 [P]) or free access swaps (M-027 [P], M-029 [P]), and no paying buyer is evidenced (M-024 [P], R-017 [UNREVIEWED]; M-013 unverifiable).
- Platform liability for competition. The Supreme Court upheld no hub-and-spoke finding for Ola/Uber (L-033 [S]), but it predates the 2023 s.3(3) proviso (L-033 [S] caveat); the proviso itself (L-017) is unverifiable; US and India hub-and-spoke exposure is asserted only in R-011 and R-012 [UNREVIEWED].
- Defense evidence is mixed within technical. Similarity thresholds of 0.5 to 0.7 cut retrieval extraction near zero at a recall cost (T-019 [P]) and stream anomaly detection reported 0.3 percent false positives (T-027 [S], model-extraction setting, no adaptive attacker), versus coverage-planning attackers (T-005 [S]) and diversity raising extraction (T-020 [S]). Independent adaptive evaluation is missing (T-015 [P]).
- Synthetic-corpus DP versus the product's value. T-025 [S] avoids per-query budget burn; the value proposition rests on real failure data (M-011 [P]).
- Timing versus exposure. DPDP core duties are not in force until about May 2027 (L-008 [S]) and cross-border rules likewise (L-009 [S]), while reconstruction and injection risks are documented now (T-004 [S], T-003 [P]).

## Evidence for building

Reviewed [S] or [P] only. 14 findings.
- L-008 [S]: core DPDP duties not in force until about 13 May 2027.
- L-033 [S]: Supreme Court found no hub-and-spoke cartel for ride-hailing platforms (pre-2023 amendment).
- L-025 [P]: exclusion and limitation clauses are generally enforceable in India, with caveats.
- T-016 [S]: x402 flow supports per-query pricing modes including settle-actual-usage.
- T-023 [S]: Stripe usage-based billing (Meters, Metronome) exists for contracted buyers.
- T-024 [P]: per-tool paid MCP monetisation is being built in practice (no adoption figures).
- T-025 [S]: DP synthetic RAG corpus avoids per-query privacy-budget accumulation.
- T-027 [S]: query-window anomaly detection reported 0.3 percent false positives (model-extraction setting, self-reported).
- M-002 [P]: marketplace listings are data products, with no answer-only listing seen (inference).
- M-003 [S]: AWS Data Exchange and Databricks coverage gaps for niche providers (single competitor-written source).
- M-004 [S]: AWS Clean Rooms provides a metered, per-second, configurable-payer precedent.
- M-011 [P]: a model tuned on failures plus successes outperformed successes only.
- M-012 [P]: 2026 perspective says databases omit failed experiments and AI is overconfident.
- M-028 [P]: negative chemical datasets are often inaccessible or not machine-readable.

## Evidence against building

Reviewed [S] or [P]: 35 findings.

Legal (13)
- L-001 [S]: India has no trade-secret statute, protection rests on contract and confidence.
- L-002 [P]: confidence can be implied; express buyer limits needed (inference).
- L-003 [P]: s.27 Contract Act may constrain buyer-use restrictions (inference part unverified).
- L-010 [P]: DPDP penalty caps up to Rs 250 crore for security failures.
- L-020 [P]: DOJ information-sharing safety zones withdrawn in 2023.
- L-023 [P]: s.79 protects third-party content; gateway composing answers likely outside (inference).
- L-027 [P]: EU Data Act unfair-terms test on B2B data terms.
- L-030 [S]: US trade secret needs reasonable measures.
- L-031 [S]: reverse engineering or independent derivation is not improper means.
- L-034 [S]: DPDP public-data exclusion is narrow, no stated B2B exemption.
- L-038 [S]: FTC and DOJ withdrew collaboration guidelines in Dec 2024.
- L-041 [S]: California Delete Act data-broker registration could reach consumer personal data answers (applicability inference).
- L-042 [S]: copyright assignment needs a signed writing, defaults to five years and India only.

Technical (12)
- T-001 [P]: reconstruction needs noise of order sqrt(n); rate limits alone not shown sufficient (inference).
- T-003 [P]: 12 prompt-injection defenses bypassed at over 90 percent.
- T-004 [S]: agent attack recovered over 70 percent of private RAG content.
- T-005 [S]: RAGCrawler plans benign-looking coverage queries.
- T-006 [P]: sub-1000 USD interposer extracts TEE keys.
- T-007 [P]: tool-description poisoning hijacks agents without tool execution.
- T-010 [P]: MCP server results are untrusted input to other servers.
- T-013 [P]: clean-room DP limited to S3 user-level aggregates.
- T-020 [S]: query diversity raises extraction under threshold defense.
- T-021 [P]: TEE.fail forges attestation quotes; Intel and AMD treat as out of scope.
- T-022 [P]: attestation unreliable without physical control, favours seller-hosted (inference).
- T-026 [S]: DP utility cost is real but contested (Census critique).

Market (10)
- M-008 [S]: pharma data collaboration already runs through Apheris-style consortia.
- M-010 [P]: companies prefer sharing successes; later-stage findings stay proprietary.
- M-014 [P]: 21 data-monetisation challenges in established firms.
- M-016 [S]: traditional IP gives limited data protection, contracts are central.
- M-023 [P]: agent purchasing still early, no independent evidence of private-data buying.
- M-024 [P]: pharma data deals are platform-scale, no per-query or failed-data pricing seen.
- M-025 [P]: seller restrictions on resharing and fear of empowering competitors.
- M-026 [P]: data ownership is a recurring deal sticking point.
- M-027 [P]: Lilly TuneLab offers free access in exchange for federated updates.
- M-029 [P]: Open Reaction Database accepts failed reactions (cost to user unverified).

Red-team [UNREVIEWED] (17), all attacks by design
- R-001: accurate answers at scale permit reconstruction (cf. T-001 [P]).
- R-002: differencing attacks practical; Diffix-style noise attacked.
- R-003: indirect prompt injection via retrieved text (cf. T-007 [P], T-010 [P]).
- R-004: LLM paraphrase can leak content (low confidence, theoretical for RAG).
- R-005: data marketplace cold start and non-excludability (low confidence).
- R-006: marketplace buyers see only description and price, a trust gap.
- R-007: R&D sharing without reasonable measures risks trade-secret status (cf. L-030 [S]).
- R-008: DPDP Rs 250 crore exposure, role allocation unresolved (cf. L-010 [P]).
- R-009: Moffatt v Air Canada, operator held liable for chatbot answer (Canada, not binding in India).
- R-010: Azure DataMarket, Kasabi, Infochimps, Streamr marketplaces failed on demand.
- R-011: US hub-and-spoke algorithm cases (Third Circuit Cendyn, Yardi), cases not read.
- R-012: India 2023 facilitator exposure (commentary, statute not read).
- R-013: free community MCP servers substitute for public chemistry and literature data.
- R-014: enterprise agent-buying needs human approval; figures unverified at origin (extends M-023 [P]).
- R-015: EU Data Act pushes toward more data access (applicability date unconfirmed).
- R-016: TEE attestation forgeable, hosted multi-tenant security promise cannot rest on it (builds on T-021 [P], T-022 [P]).
- R-017: no evidence of payment for failed data (draws on M-024 [P], M-028 [P]).

### Kill-criteria status [UNREVIEWED]

None is mitigated or confirmed in `findings/kill-criteria.md`; all ten are open as written. Reviewed findings that bear on each are shown for context only and do not change status.

| ID | Condition (short) | Red-team basis | Reviewed findings bearing on it | Status |
|---|---|---|---|---|
| K-001 | No scheme blocks reconstruction yet keeps answers useful | R-001, R-002 | Attack side T-001 [P], T-004 [S], T-005 [S], T-020 [S]; defense side T-019 [P], T-027 [S], T-025 [S]; T-015 [P] says independent adaptive evaluation is missing | open |
| K-002 | Injection both ways cannot be defended beyond heuristics | R-003 | T-003 [P], T-007 [P], T-010 [P]; T-008 unverifiable | open |
| K-003 | Too few credible sellers | R-005, R-007, R-010 | M-010 [P], M-014 [P], M-016 [S], M-025 [P], M-026 [P], L-030 [S]; M-031 unverifiable | open |
| K-004 | Buyers cannot verify answer quality | R-006, R-013 | No reviewed finding addresses it | open |
| K-005 | Liability cannot be allocated at acceptable cost | R-008, R-009 | L-010 [P], L-023 [P], L-025 [P], L-027 [P], L-036 [P]; L-035 unverifiable | open |
| K-006 | LLM answerer leaks via paraphrase | R-004 | No reviewed finding addresses it directly | open |
| K-007 | No named buyer pays for failed data at query level | R-017, R-013, R-010 | M-024 [P], M-027 [P], M-028 [P], M-029 [P]; M-013 and M-031 unverifiable | open |
| K-008 | Hub exposure cannot be designed out | R-011, R-012 | L-033 [S] (pre-amendment), L-038 [S], L-020 [P]; L-017, L-019, L-021 unverifiable | open |
| K-009 | Security depends on TEEs on hardware seller does not control | R-016 | T-006 [P], T-021 [P], T-022 [P]; T-014 unverifiable | open |
| K-010 | Agents cannot be onboarded without human-approved procurement | R-014 | M-023 [P] | open |

## Tally: findings for versus against

Counts are of findings, not weights. The for/against/neutral classification is mine, based on each finding's direction; gap findings and corrections are excluded. Red-team findings are attacks by design, which skews any count.

| Group | For | Against | Neutral or context |
|---|---|---|---|
| Legal reviewed (22 [S]/[P]) | 3 | 13 | 6 |
| Technical reviewed (22 [S]/[P]) | 5 | 12 | 5 |
| Market reviewed (23 [S]/[P]) | 6 | 10 | 7 |
| Reviewed total (67) | 14 | 35 | 18 |
| of which [S] only (26) | 8 | 13 | 5 |
| of which [P] only (41) | 6 | 22 | 13 |
| Red-team [UNREVIEWED] (17) | 0 | 17 | 0 |
| Kill criteria [UNREVIEWED] (10) | n/a | 10 open, 0 mitigated, 0 confirmed | n/a |

Neutral or context IDs: L-009, L-040, L-022, L-024, L-028, L-036, T-018, T-009, T-015, T-017, T-019, M-021, M-030, M-001, M-006, M-009, M-017, M-018.

## Biggest unknowns

Questions in `research/questions.md` with no [S] finding yet, plus gaps flagged in the findings.
- Whether a query answer is a licence, disclosure or service: only L-007 (unsupported) addresses it.
- Liability for inaccurate answers: only L-025 [P], L-036 [P] and L-026 (unverifiable); no Indian authority on AI output.
- Platform-seller-buyer contract structure: L-027 [P] only; L-029 unverifiable.
- Ownership and licensability of unused experiment data: L-006 unsupported, L-043 unverifiable; only the assignment formalities are supported (L-042 [S]).
- Federated versus centralised architecture: T-014 unverifiable, T-022 [P] is inference.
- Seller content hijacking buyer agents, and MCP as an access protocol: only [P] findings (T-007, T-009, T-010); T-008 unverifiable.
- Clean rooms and confidential computing as building blocks: only [P] findings (T-013, T-006, T-021, T-022).
- Independent adaptive evaluation of query auditing, caps and anomaly detection: T-015 [P], T-020 [S] narrows the gap, T-027 [S] lacks an adaptive test.
- DP on free-text answers at usable utility: T-013 [P] (aggregates only), T-025 [S] (lossy synthetic copy, inference).
- Who would pay for unused or failed-experiment knowledge: M-011, M-012, M-028 [P] show need; M-013 unverifiable; R-017 [UNREVIEWED] finds no payer.
- Whether Indian sellers have ever sold R&D data: M-031 unverifiable.
- Buyer-side answer quality verification (K-004) and paraphrase leakage (K-006): no reviewed finding.
- Enterprise approval of autonomous agent purchases: M-023 [P], R-014 [UNREVIEWED].
- India Competition Act 2023 s.3(3) effect and EU Art. 101 text: L-017, L-019, L-021 unverifiable.
- EU trade-secret reasonable-steps and reconstruction risk: L-004, L-005 unverifiable; US state UTSA and EU/US data-broker regimes beyond California not researched (L-014 unverifiable, L-041 [S] covers California only).
- DPDP and GDPR primary texts: L-011 unsupported, L-012, L-013, L-035 unverifiable.
- IT Act s.79 for AI-composed answers: L-023 [P] inference; L-039 (unsupported) is excluded because it presented a draft as in force.
- Indian crypto, RBI and FEMA treatment of stablecoin settlement: flagged inference in T-017 [P].

Housekeeping observations on `research/questions.md` (not edited by this analyst):
- The ticked first Legal box rests on L-001 [S], which covers only the absence of a trade-secret statute; ownership (L-006 unsupported) and answer-leakage risk (L-005 unverifiable) are not supported.
- The ticked DPDP/GDPR box rests on L-008 [S], which covers commencement timing; L-011 is unsupported and L-012 and L-013 are unverifiable. L-034 [S] and L-040 [S] now add support on public-data exclusion and the Recital 26 test.
- Unticked boxes that now have at least one [S] finding: competition law (L-033, L-038), data broker (L-041, California only), per-query metering (T-016, T-023), agent payments (T-016, T-018), existing marketplaces (M-003, M-004, M-008), why a company would sell (M-016), pricing models (M-004).
