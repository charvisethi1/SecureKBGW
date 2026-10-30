# Synthesis: secure KB gateway (evidence only, no recommendation)

Tags: [S] supported, [P] partly supported (use with the caveat in review.md), [UNREVIEWED] not in review.md. Unsupported and unverifiable findings are excluded from conclusions and from the tally, and are listed below. Source of verdicts: `findings/review.md`. Where the review table and a later "Deep-dive" row disagree (M-004, M-045, M-051), the Deep-dive row (the later, more specific one) is used.

## As of

2026-10-30. Legal, technical and market M-001..M-056 were reviewed 2026-10-26 to 2026-10-30. M-057..M-062 and all R- findings are not in review.md.

| Department | Total | Supported | Partly supported | Unsupported | Unverifiable | Unreviewed |
|---|---|---|---|---|---|---|
| Legal (L-001..L-043) | 43 | 11 | 11 | 4 | 17 | 0 |
| Technical (T-001..T-027) | 27 | 9 | 13 | 1 | 4 | 0 |
| Market (M-001..M-062) | 62 | 10 | 31 | 2 | 13 | 6 [UNREVIEWED] (M-057..M-062) |
| Red-team (R-001..R-017) | 17 | 0 | 0 | 0 | 0 | 17 [UNREVIEWED] |
| All findings | 149 | 30 | 55 | 7 | 34 | 23 |
| Kill criteria (K-001..K-010) | 10 | not findings | | | | all 10 cite only R- findings; all status open |

Verdict basis: M-004, M-045 and M-051 are counted as [P] per their Deep-dive rows (the review table first listed them as supported; with those table verdicts the totals would be 33 supported and 52 partly supported). Review-table rows not tied to an ID (AWS analysis rules, AWS DP, AWS C3R, AWS gap assessment) are [S] or [P] Deep-dive rows under the M-004 heading and are cited by topic below.

Excluded as unsupported (7): L-006, L-007, L-011, L-039, T-002, M-022, M-039.
Excluded as unverifiable (34): L-004, L-005, L-012, L-013, L-014, L-015, L-016, L-017, L-018, L-019, L-021, L-026, L-029, L-032, L-035, L-037, L-043, T-008, T-011, T-012, T-014, M-005, M-007, M-013, M-015, M-019, M-020, M-031, M-035, M-036, M-037, M-041, M-043, M-055.
Gap-type findings (L-014, L-016, L-043, T-015, M-013, M-031, M-060, M-061) are used under Biggest unknowns and the competitor section only.

Superseded or corrected (the corrected version is used throughout):
- M-004 is superseded by M-057 [UNREVIEWED]. The 10-minute minimum is PySpark only; Spark SQL is 2.00 USD per CRPU-hour with a 60 second minimum; DP adds 2.00 USD; AWS meters compute, the seller earns nothing, so it is not a per-answer precedent. The M-004 Deep-dive row [P] agrees on every point of this correction.
- M-051 is superseded in part by M-058 [UNREVIEWED]. The source is an August 2024 public-preview post, so it is stale; current docs limit a clean room to ten collaborators and give no GA status or pricing. The M-051 Deep-dive row [P] agrees.
- M-062 [UNREVIEWED] withdraws the 28K USD x402 volume figure (M-039 is [unsupported] in review.md), so x402 volume is unknown, not tiny. It also notes SciFinder is unsupported (M-049 [P]), Elucidata's sources are public and proprietary with India location unconfirmed (M-054 [P]), and the yet2 shutdown is unverified (M-036 unverifiable). The reviewer's notes on M-039, M-049, M-054 and M-036 reach the same conclusions.
- T-006 [P] is refined by T-021 [P]; L-022 [P] by L-028 [P]; M-022 (unsupported) by M-030 [S].

## Cross-department dependencies

- Legal needs controls that technical cannot yet guarantee. US trade-secret status needs reasonable measures (L-030 [S]) and reverse engineering or independent derivation is not improper means (L-031 [S]). Agent-driven extraction recovered over 70 percent of a private RAG KB (T-004 [S]), plans benign-looking queries (T-005 [S]) and gains from query diversity under a threshold defense (T-020 [S]). If technical limits fail, the seller's remaining protection is contract (L-001 [S], M-016 [S]). The EU equivalent (L-004) is unverifiable.
- Contract-only protection raises seller cost. Assignment needs a signed writing with India-only and five-year defaults (L-042 [S]); data ownership is a recurring deal sticking point (M-026 [P]); licences carry limited-use and no-resharing terms (M-025 [P]); this links legal review cost to seller willingness (M-016 [S], M-014 [P]).
- Hosting trust shapes legal and technical design. A sub-1000 USD interposer forges TEE attestation (T-021 [P]), so confidential computing helps only if the host is physically controlled (T-022 [P], inference). India's cross-border rules have not commenced and sectoral localisation still applies (L-009 [S]). Both point toward seller-hosted or federated deployment, but the federated-vs-central comparison is unverifiable (T-014) and small sellers' ability to host is untested (K-009 [UNREVIEWED]).
- Data-protection duties attach to what answers reveal. DPDP has no stated exemption for commercial data (L-034 [S]), core duties start about 13 May 2027 (L-008 [S]) and caps reach Rs 250 crore (L-010 [P]). Output filtering is then needed, but LLM-level filters were bypassed at over 90 percent (T-003 [P]) and clean-room DP covers only aggregates (T-013 [P]). Cryptographic computing on AWS cannot run WHERE or SUM on encrypted data (M-059 [UNREVIEWED], consistent with the C3R Deep-dive row [S]). GDPR anonymity is judged by means reasonably likely to be used (L-040 [S]).
- DP trades accuracy for safety. Noise of order sqrt(n) is needed against reconstruction (T-001 [P]); the utility cost of DP is real but contested (T-026 [S]); a DP synthetic corpus avoids per-query budget burn but the buyer queries a lossy copy (T-025 [S], inference), while the demand evidence concerns real failures (M-011 [P], M-028 [P]). R-001 [UNREVIEWED] adds that pay-per-query sells accuracy.
- Competition law constrains who may be on both sides. US safe harbours for information sharing are withdrawn (L-020 [P], L-038 [S]). Sellers fear strengthening competitors (M-025 [P]), and pharma sharing runs through governed consortia (M-008 [S], M-034 [S]). The vetting-of-pairs mitigation is inference only (L-021 unverifiable).
- Payments depend on legal rails. x402 supports fixed, max-authorise and deferred pricing (T-016 [S]), but USDC settlement and Indian RBI, FEMA and tax treatment are unchecked inference (T-017 [P]). Fiat alternatives exist: Stripe usage billing for contracted buyers (T-023 [S]) and Stripe's Machine Payments Protocol with cards or stablecoins (M-050 [S]).
- Liability depends on contract law and technical accuracy. Exclusion clauses are generally enforceable in India (L-025 [P]) but EU Data Act terms limiting liability for gross negligence are blacklisted (L-027 [P]); no Indian authority on negligent misstatement for AI output (L-036 [P]); s.79 for a gateway that composes answers is untested (L-022 [P], L-023 [P]). Technical leakage (T-004 [S]) therefore lands on the operator's contract position.
- Agent-buyer design depends on injection risk and onboarding. Tool-description poisoning works without the tool being executed (T-007 [P]), results from one MCP server are untrusted input to another (T-010 [P]), MCP authorization is optional (T-009 [P]). GLG's connector gates content by entitlement with OAuth or account login (M-045 [P]) and probably needs a client agreement (M-061 [UNREVIEWED]); R-014 [UNREVIEWED] and M-023 [P] point the same way for buyers.

## Conflicts between departments

- Payment rails exist, buyer demand is unproven. Payment and metering layers are documented and plural (T-016 [S], T-023 [S], M-032 [S], M-050 [S], M-047 [P], M-038 [P]), but agent purchasing is described as still early with no independent evidence (M-023 [P], R-014 [UNREVIEWED]) and actual x402 paid volume is unknown (M-039 unsupported, M-062 [UNREVIEWED]).
- Clean-room precedent versus fit. The earlier reading of AWS Clean Rooms as a pay-per-query precedent (M-004) is corrected: it meters compute and the seller earns nothing (M-057 [UNREVIEWED], M-004 Deep-dive [P]); its DP and C3R handle structured aggregates and joins, not free-form answers (T-013 [P], M-059 [UNREVIEWED]).
- Demand pain versus paid demand. Failed data improves models and is scarce (M-011 [P], M-012 [P], M-028 [P]); duplication waste is quantified (M-021 [S], opinion, 2011); pharma and chemistry buyers pay for curated data and knowledge (M-049 [P], M-054 [P], M-024 [P], M-048 [P]); but the remedies named are free pooling (M-021 [S], M-009 [P]), free access swaps (M-027 [P]) or open repositories (M-029 [P]), and no named buyer of failed or query-level data is evidenced (M-024 [P], R-017 [UNREVIEWED]; M-013 unverifiable).
- Same evidence points both ways on incumbents. Expert networks moving to queryable libraries and agent connectors (M-045 [P], M-046 [P]) show buyers and compliance gating for agent-queryable paid knowledge, and also show an incumbent in the space. Pharma willingness to put proprietary data into privacy-preserving infrastructure (M-008 [S], M-034 [S], M-048 [P]) shows readiness to share, via membership or platform deals, not per-query sales.
- Legal protection depends on controls that are only partly evaluated. Reasonable measures and contract evidence (L-030 [S], L-001 [S]) versus defenses with no complete option (T-019 [P], T-020 [S]), anomaly detection with no adaptive test (T-027 [S]) and no independent adaptive evaluation (T-015 [P]).
- Platform liability for competition. The Supreme Court upheld no hub-and-spoke finding (L-033 [S]) but it predates the 2023 s.3(3) proviso, which is unverifiable (L-017); US and India hub exposure rests only on R-011 and R-012 [UNREVIEWED]; US safe harbours are gone (L-038 [S]).
- Seller-hosting preference versus seller capability. Attestation weakness favours seller-hosted deployment (T-022 [P], T-021 [P]), while sellers face many monetisation barriers and preparation costs (M-014 [P], M-026 [P]); small-seller hosting is untested (K-009 [UNREVIEWED]).
- Timing versus exposure. DPDP core duties and cross-border rules are not in force until about May 2027 (L-008 [S], L-009 [S]); reconstruction and injection risks are documented now (T-004 [S], T-003 [P]).
- Internal review inconsistency. M-004, M-045 and M-051 are [S] in the review table and [P] in Deep-dive rows; the Deep-dive verdicts are used here.

## Competitor landscape

Gap verified or inferred: every gap statement below is inferred from absence on the pages checked. The reviewer states for AWS and Databricks that absence on a few pages is not proof (M-004 gap-assessment row [P]). AWS Data Exchange and AWS Marketplace integration were not checked there, and InfoSum, Habu, Cape Privacy, Innocentive, Wazoku, CRO and CDMO exchanges, and agritech or semiconductor exchanges are not yet covered (questions.md). No finding verifies that a seller-controlled, answer-only, agent-facing paid release of company-internal findings does not exist; M-031 (India) and M-013 are unverifiable and R-017 is [UNREVIEWED].

Closest, in order of overlap with the idea:

1. GLG MCP connector (M-045 [P], deep-dive [P]; pricing gap M-061 [UNREVIEWED]). Verified: an AI assistant queries a customer's expert-call transcripts and GLG's Expert Content Library, with redaction, compliance review, hold approvals, access controls and an in-chat expert call request. Gap: content is human-expert transcripts, not a seller company's unused experiments; no price, billing or per-query agent payment stated; access likely needs a client account (inference). Direction supported by M-046 [P] (Tegus, Third Bridge, AlphaSights libraries and AI answers). Gap is inferred.
2. Databricks and AWS clean rooms.
   - Databricks Clean Rooms (M-051 [P], M-058 [UNREVIEWED], M-060 [UNREVIEWED]). Verified: handles volumes (non-tabular) and approved notebook code; participants cannot see each other's data; limit of ten collaborators; output controls are approval-based, no stated DP or thresholds (Deep-dive [P]); pricing is only "pay as you go" and rates and payer are unknown. Gap: no per-query seller monetisation, no agent buyer, no open market. Inferred.
   - AWS Clean Rooms (M-057 [UNREVIEWED], T-013 [P], M-059 [UNREVIEWED]; analysis-rule and DP Deep-dive rows [S]). Verified: owner-set analysis rules, aggregation thresholds, DP on S3-backed tables, one named querier, compute metered with configurable payer. Gap: seller earns nothing, structured tables only, AWS account needed, no listing or revenue share found. Inferred from the docs reviewed.
   - Snowflake DCR Agent (M-052 [P]) and Duality (M-053 [P]) add agent or LLM interfaces; ad-tech and structured focus, other details unconfirmed. Decentriq (M-037) unverifiable.
3. Agent payment layers: x402 (T-016 [S], T-017 [P], M-038 [P]), Stripe MPP (M-050 [S]), Nevermined (M-032 [S]), Skyfire (M-047 [P]), AP2 (T-018 [S], early-stage), Cloudflare Pay Per Crawl (M-017 [P]), MCP monetisation models (M-040 [S]). Verified: per-call, dynamic and deferred charging for APIs, datasets and MCP servers exist; no private-knowledge or R&D seller is named (M-050). Gap: none provides answer-only output control, seller release review or curation (M-032 finding, reviewer calls the "off-the-shelf" framing the analyst's). Inferred. Volume and fees unknown (M-062 [UNREVIEWED]). MCPay, Apify and similar are unverifiable (M-041).
4. Pharma consortia and federated platforms: Apheris (M-008 [S], M-034 [S]), Owkin (M-048 [P]), Lilly TuneLab (M-027 [P]), CAMD (M-009 [P]). MELLODDY (M-007) is unverifiable. Verified: members keep data in place and receive pooled-data models; TuneLab is free access for federated updates. Gap: closed membership, model outputs, no per-query access for outsiders; inferred from descriptions. "Closer substitute than marketplaces" is analyst inference (M-034 review note).
5. Data marketplaces and exchanges: Snowflake Marketplace (M-001 [P], M-002 [P]), Dawex (M-033 [S]), AWS Data Exchange and Databricks Marketplace (M-003 [S], single competitor-written source). Verified: usage and subscription pricing is common. Gap: dataset delivery rather than controlled answers (M-002 [P], M-033, inference). Datarade (M-035) and yet2 (M-036) are unverifiable.
6. Knowledge bases and curators: Reaxys (M-049 [P]; SciFinder unsupported per M-062 [UNREVIEWED]), Elucidata (M-054 [P]; India link unconfirmed). Gap: published or curated sources; no evidence of company-internal failed experiments (M-049).
7. India: AIKosh (M-022 unsupported, M-030 [S] self-correction, 316 datasets only), CSIR portal (M-056 [P]), Finarkein (M-044 [P]); Account Aggregator (M-043) and Innoplexus (M-055) unverifiable. India gap: no Indian R&D data seller or exchange confirmed (M-031 unverifiable).

Remaining gap, stated at the level the evidence allows: the combination of (a) seller-controlled answer-only release, (b) unstructured company-internal unused findings, (c) per-answer seller revenue and (d) an agent buyer on an open market is not described on any page the reviewer read for the products above. The components (billing, clean-room governance, agent connectors, expert-library AI answers) each exist. All of this is inferred, not verified.

## Evidence for building

Reviewed [S] or [P] only. 20 findings (9 [S], 11 [P]). No [UNREVIEWED] finding points this way. The classification is mine.
- L-008 [S]: core DPDP duties not in force until about 13 May 2027.
- L-009 [S]: India cross-border transfer rules not yet commenced; restrict-by-notification model (sectoral rules still apply).
- L-033 [S]: Supreme Court upheld no hub-and-spoke finding against ride-hailing platforms (pre-2023 amendment).
- T-016 [S]: x402 flow supports fixed, max-authorise and deferred per-use pricing.
- T-023 [S]: Stripe usage billing (Meters, Metronome) exists for contracted buyers.
- T-024 [P]: per-tool paid MCP monetisation is being built (no adoption figures).
- T-025 [S]: DP synthetic RAG corpus avoids per-query privacy-budget accumulation (lossy copy caveat).
- T-027 [S]: query-window anomaly detection reported 0.3 percent false positives (model-extraction setting, no adaptive test).
- M-011 [P]: a model tuned on failures plus successes outperformed successes only.
- M-012 [P]: 2026 perspective says databases omit failed experiments and AI is overconfident (ten-to-one ratio not on page).
- M-018 [P]: IndiaAI working group recommended flexible pricing for non-personal data (earlier draft policy with pricing was scrapped).
- M-021 [S]: about 7 billion USD a year said to be wasted repeating experiments (opinion, 2011; remedy proposed is free pooling).
- M-024 [P]: pharma pays for AI data at platform scale (no per-query or failed-data pricing).
- M-028 [P]: negative chemical datasets are often inaccessible or not machine-readable.
- M-040 [S]: per-call or outcome pricing fits agent buyers; billable answer definition is open.
- M-042 [P]: dedicated negative-result outlets have narrowed, so supply is unused (also a caution on demand).
- M-046 [P]: expert networks are moving from calls to queryable libraries and AI answers.
- M-048 [P]: large pharma pays for federated access to data at source (Sanofi-Owkin 2021).
- M-049 [P]: institutions pay for curated reaction knowledge (Reaxys), and are price-sensitive.
- M-054 [P]: pharma customers use a curated-data vendor (India location unconfirmed, pricing undisclosed).

## Evidence against building

Reviewed [S] or [P]: 50 findings (17 [S], 33 [P]). Plus 17 [UNREVIEWED] red-team findings. The classification is mine.

Legal (14)
- L-001 [S]: India has no trade-secret statute; protection rests on contract and confidence.
- L-003 [P]: s.27 Contract Act may limit buyer-use restrictions (inference part unverified).
- L-010 [P]: DPDP penalty caps up to Rs 250 crore for security failures.
- L-020 [P]: DOJ information-sharing safety zones withdrawn (2023).
- L-022 [P]: s.79 test unsettled (Amway, 2020).
- L-023 [P]: s.79 protects third-party content; a gateway composing answers likely outside (inference).
- L-025 [P]: liability caps valid generally but with limits; commentary on consumer contracts.
- L-027 [P]: EU Data Act unfair-terms test on B2B data terms.
- L-030 [S]: US trade secret needs reasonable measures.
- L-031 [S]: reverse engineering or independent derivation is not improper means.
- L-034 [S]: DPDP public-data exclusion is narrow; no B2B exemption stated.
- L-036 [P]: no Indian authority on negligent misstatement or AI-output disclaimers.
- L-038 [S]: FTC and DOJ withdrew collaboration guidelines (Dec 2024).
- L-042 [S]: copyright assignment needs a signed writing; five-year and India-only defaults.

Technical (16)
- T-001 [P]: reconstruction needs noise of order sqrt(n); rate limits alone not shown sufficient (inference).
- T-003 [P]: 12 injection defenses bypassed at over 90 percent.
- T-004 [S]: agent attack recovered over 70 percent of private RAG content.
- T-005 [S]: RAGCrawler plans benign-looking coverage queries.
- T-007 [P]: tool-description poisoning hijacks agents without tool execution.
- T-009 [P]: MCP authorization optional; spec version may be superseded.
- T-010 [P]: MCP results from one server are untrusted input to others.
- T-013 [P]: clean-room DP limited to S3 user-level aggregates.
- T-015 [P]: independent evaluation of auditing and rate limits not found.
- T-017 [P]: x402 settlement relies on USDC; Indian treatment unchecked.
- T-018 [S]: AP2 is early-stage sample code.
- T-019 [P]: no single RAG-extraction defense is complete.
- T-020 [S]: query diversity raises extraction under threshold defense.
- T-021 [P]: TEE.fail forges attestation quotes; Intel and AMD treat as out of scope.
- T-022 [P]: attestation unreliable without physical control (inference).
- T-026 [S]: DP utility cost real but contested.

Market (20)
- M-008 [S]: Apheris-style consortia already serve pharma data collaboration.
- M-009 [P]: CAMD pooled failed-trial data via a nonprofit (free access not stated).
- M-010 [P]: companies prefer sharing successes; later-stage findings stay proprietary.
- M-014 [P]: 21 data-monetisation challenges in established firms.
- M-016 [S]: traditional IP gives limited data protection; contracts central.
- M-023 [P]: agent purchasing still early; no independent evidence of private-data buying.
- M-025 [P]: sellers restrict resharing and fear empowering competitors.
- M-026 [P]: data ownership is a recurring deal sticking point.
- M-027 [P]: Lilly TuneLab gives free access for federated updates.
- M-029 [P]: Open Reaction Database accepts failed reactions (free status unconfirmed).
- M-032 [S]: payment gating and per-request pricing for APIs, datasets and models already exists (Nevermined).
- M-033 [S]: usage pricing is common in data exchanges (Dawex).
- M-034 [S]: pharma federated networks are expanding fast (ADMET, AISB).
- M-038 [P]: x402 per-call and deferred scheme exists (deferred is a proposal).
- M-045 [P]: GLG MCP connector is an agent-queryable paid-knowledge incumbent.
- M-047 [P]: Skyfire is another agent identity and payment rail.
- M-050 [S]: Stripe MPP; the agent-payment layer is crowded and backed by a major processor.
- M-051 [P]: Databricks Clean Rooms covers non-tabular data (stale source; see M-058).
- M-052 [P]: Snowflake DCR Agent adds a conversational agent interface.
- M-053 [P]: Duality lists LLM inference and an assistant agent.

Red-team [UNREVIEWED] (17), attacks by design
- R-001: accurate answers at scale permit reconstruction (cf. T-001 [P]).
- R-002: differencing attacks are practical; Diffix-style noise was attacked.
- R-003: indirect prompt injection through retrieved text (cf. T-007 [P], T-010 [P]).
- R-004: LLM paraphrase can leak content (low confidence).
- R-005: data marketplace cold start and non-excludability (low confidence).
- R-006: marketplace buyers see only description and price (trust gap).
- R-007: R&D sharing without reasonable measures risks trade-secret status (cf. L-030 [S]).
- R-008: DPDP Rs 250 crore exposure; role allocation unresolved (cf. L-010 [P]).
- R-009: Moffatt v Air Canada, operator liable for chatbot answer (Canada, not binding in India).
- R-010: Azure DataMarket, Kasabi, Infochimps, Streamr failed on demand.
- R-011: US hub-and-spoke algorithm cases (cases not read).
- R-012: India 2023 facilitator exposure (statute not read).
- R-013: free community MCP servers substitute public chemistry and literature data.
- R-014: enterprise agent buying needs human approval; figures unverified at origin.
- R-015: EU Data Act pushes toward more data access (applicability date unconfirmed).
- R-016: TEE attestation forgeable; a hosted multi-tenant promise cannot rest on it (builds on T-021 [P], T-022 [P]).
- R-017: no evidence of payment for failed data (draws on M-024 [P], M-028 [P]).

## Tally: findings for versus against

Counts are of findings, not weights, and many findings overlap. Classification is mine. Excluded from the tally: unsupported, unverifiable, M-057..M-062 (corrections and gaps, used in the competitor section), kill criteria (not findings) and 15 reviewed findings not classed either way (L-002, L-024, L-028, L-040, L-041, T-006 superseded by T-021, M-001, M-002, M-003, M-004 superseded by M-057, M-006, M-017, M-030, M-044, M-056).

| Group | For | Against |
|---|---|---|
| Reviewed [S] | 9 | 17 |
| Reviewed [P] | 11 | 33 |
| Reviewed total | 20 | 50 |
| [UNREVIEWED] red-team | 0 | 17 |
| All | 20 | 67 |

Reviewed [S]/[P] total 85 = 20 for + 50 against + 15 not classed. Red-team findings are attacks by design, which skews the "against" count. Without them: 20 for, 50 against.

## Kill-criteria status

Source: `findings/kill-criteria.md` (updated 2026-10-26). Result: 0 confirmed, 0 mitigated, 10 open. Every criterion cites only [UNREVIEWED] red-team findings. The reviewed findings below bear on them but are not cited by the file and do not change status. No criterion cites the competitor findings M-032..M-056.

| ID | Condition (short) | Red-team basis | Reviewed findings bearing on it | Status |
|---|---|---|---|---|
| K-001 | No scheme blocks reconstruction yet keeps answers useful | R-001, R-002 | Attack: T-001 [P], T-004 [S], T-005 [S], T-020 [S]. Defense: T-019 [P], T-025 [S], T-026 [S], T-027 [S]. T-015 [P]: no independent adaptive evaluation | open |
| K-002 | Injection both ways not defensible beyond heuristics | R-003 | T-003 [P], T-007 [P], T-009 [P], T-010 [P]; T-008 unverifiable | open |
| K-003 | Too few credible sellers | R-005, R-007, R-010 | M-010 [P], M-014 [P], M-016 [S], M-025 [P], M-026 [P], L-030 [S]; M-031 unverifiable | open |
| K-004 | Buyers cannot verify answer quality | R-006, R-013 | No reviewed finding addresses it | open |
| K-005 | Liability cannot be allocated at acceptable cost | R-008, R-009 | L-010 [P], L-023 [P], L-025 [P], L-027 [P], L-036 [P]; L-035 unverifiable | open |
| K-006 | LLM answerer leaks via paraphrase | R-004 | No reviewed finding addresses it directly | open |
| K-007 | No named buyer pays for failed data at query level | R-017, R-013, R-010 | M-024 [P], M-027 [P], M-028 [P], M-029 [P], M-021 [S]; paying adjacent buyers: M-049 [P], M-054 [P], M-045 [P]; M-013, M-031 unverifiable | open |
| K-008 | Hub exposure cannot be designed out | R-011, R-012 | L-033 [S] (pre-amendment), L-038 [S], L-020 [P]; L-017, L-019, L-021 unverifiable | open |
| K-009 | Security depends on TEEs on hardware seller does not control | R-016 | T-021 [P], T-022 [P]; T-014 unverifiable | open |
| K-010 | Agents cannot be onboarded without human-approved procurement | R-014 | M-023 [P], M-045 [P]; M-061 [UNREVIEWED] (GLG likely needs client agreement); M-039 unsupported | open |

## Biggest unknowns

Top-level questions in `research/questions.md` with no ticked box (9 of 20 unticked) and discovered questions (28, all unticked), restricted to those with no [S] finding.
- Licence vs disclosure vs service: only L-007 (unsupported).
- Liability for inaccurate answers: only L-025 [P], L-036 [P]; R-009 [UNREVIEWED]; L-026 unverifiable.
- Platform-seller-buyer contract structure: L-027 [P] only; L-029 unverifiable.
- Federated vs centralised architecture: T-022 [P] is inference; T-014 unverifiable.
- Seller content hijacking buyer agents, and MCP as access protocol: only [P] (T-007, T-009, T-010); T-008 unverifiable.
- Clean rooms and confidential computing as building blocks: at ID level only [P] (T-013, T-021, T-022, M-051); AWS rule, DP and C3R Deep-dive rows are [S] but sit under M-004, which questions.md does not cite for this box.
- Who would buy unused-experiment knowledge, and a named payer for failed data: M-011, M-012, M-028 [P] show need; M-013 unverifiable; R-017 [UNREVIEWED].
- Why a company would sell: blockers have M-016 [S] and M-010, M-014, M-025, M-026 [P]; no [S] finding on seller incentives.
- Whether the competitor gap is real: inferred only (see competitor landscape); GLG, Databricks and AWS Data Exchange pricing and listing terms unknown (M-061, M-060 [UNREVIEWED]); InfoSum, Habu, Wazoku and others uncovered.
- x402 and agent-payment actual volume: unknown (M-039 unsupported, M-062 [UNREVIEWED]); enterprise permission for agents to buy: M-023 [P], R-014 [UNREVIEWED].
- Independent adaptive evaluation of query auditing, caps and anomaly detection: T-015 [P]; T-020 [S] narrows it; T-027 [S] has no adaptive test.
- DP on free-text answers at usable utility: T-013 [P] (aggregates only), T-025 [S] (lossy copy, inference).
- Ownership and licensability of unused experiment data: L-006 unsupported, L-043 unverifiable; L-042 [S] covers assignment formalities only.
- India Competition Act s.3(3) effect and EU Art. 101: L-017, L-019, L-021 unverifiable; EU competition is not supported at all.
- EU trade-secret reasonable steps and US state UTSA: L-004, L-005, L-014, L-032 unverifiable.
- DPDP and GDPR primary texts: L-011 unsupported; L-012, L-013, L-035 unverifiable.
- IT Act s.79 for AI-composed answers: L-023 [P] inference; L-039 unsupported.
- Indian crypto, RBI and FEMA treatment of stablecoin settlement: T-017 [P] (flagged inference).
- Indian sellers of R&D data: M-031 unverifiable.

Observations on `research/questions.md` (not edited by this analyst):
- The ticked pricing-models box cites M-004, now [P] per its Deep-dive row and corrected by M-057 [UNREVIEWED]. Other [S] pricing findings remain (M-032, M-033, M-040), and the box note says revenue-share and outcome-based were unsupported; M-040 [S] now describes outcome-based billing as a model but no seller precedent is evidenced.
- The unticked "Why would a company sell" box now has M-016 [S] on blockers; the incentives half has no [S] finding.
- The ticked first Legal box rests on L-001, L-030, L-031, L-042 [S], which do not answer collaborator ownership (L-006 unsupported, L-043 unverifiable).
