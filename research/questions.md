# Research questions: secure KB gateway

**Project summary.** A secure knowledge-base gateway where Company A (seller) shares knowledge such as unused experiments and internal findings with Company B (buyer) on a pay-per-query basis. Buyers are AI agents, not humans, and must never receive raw data, only answers to what their query asked. Goal: an honest evidence picture across legal, technical and market fronts to decide whether to build. Home jurisdiction is India. Note EU/US differences.

Rules: tick a box only when the question has at least one finding marked **supported** in `findings/review.md`. Put the supporting finding IDs after the question when ticking, e.g. `(L-003, L-007)`.

## Legal
- [x] Who owns unused experiment data, and can it be licensed? Is there trade-secret risk from query answers? (India first; note EU/US) (L-001, L-030, L-031, L-042)
- [ ] Does a query answer count as licensing, disclosure or a service, and what follows from each?
- [x] DPDP Act (India) and GDPR exposure if answers contain personal data (L-008, L-034, L-040)
- [x] Cross-border transfer rules (DPDP, GDPR) when seller, platform and buyer are in different countries (L-009)
- [ ] Liability for inaccurate answers
- [ ] Contract terms and structure between platform, seller and buyer
- [x] Competition law when competitors exchange information (India CCI, EU Art. 101, US) (L-033, L-038; EU not yet supported)
- [x] Is the platform a neutral intermediary or a data broker, and what does each imply? (L-041 only, California; India s.79 finding L-039 is unsupported, so only partly answered)

## Technical
- [ ] Federated vs centralized architecture for a gateway like this
- [x] Defenses against data reconstruction through many queries (query budgets, rate limits, output caps, anomaly detection), and how well they work (T-004, T-005, T-020, T-025, T-026, T-027)
- [x] Prompt injection, buyer agent attacking the gateway (T-004, T-005)
- [ ] Prompt injection, seller content hijacking buyer agents
- [ ] Clean rooms and confidential computing as building blocks
- [x] Per-query metering and billing (T-016, T-023)
- [ ] Agent-to-agent access protocols (e.g. MCP)
- [x] Current agent-to-agent payment approaches (T-016, T-018, T-023)

## Market
- [x] Existing data marketplaces and clean-room providers, and where they fall short (M-003, M-008)
- [ ] Who would buy "unused experiment" knowledge? Which industries first?
- [ ] Why would a company sell? Incentives and blockers
- [x] Pricing models (per query, subscription, revenue share, outcome-based) (M-004; revenue-share and outcome-based still unsupported)

## Discovered during research
<!-- Agents append follow-up questions here as: - [ ] (Department) question -->
- [ ] (Legal) What US law (DTSA, state UTSA) governs trade-secret loss through aggregated query answers, and is there any case law on derived-output leakage in any jurisdiction? (L-005, L-014)
- [ ] (Legal) Fetch primary texts of the DPDP Act 2023 (s.3, s.8, Schedule), DPDP Rules 2025 Rule 15, GDPR Arts. 4, 28, 44-49 and verify L-008 to L-013 against them
- [ ] (Legal) Can the seller assign or licence experiment data that includes third-party (CRO, collaborator, funder) contributions, and what chain-of-title evidence is needed in India? (L-006)
- [ ] (Market) Does any company currently pay for failed-experiment or negative-result data (named buyer, price, contract)? None found in M-011 to M-013.
- [ ] (Market) Why would a consortium (MELLODDY, Apheris) participant prefer pay-per-query sales over consortium membership, and is there outcome-based or revenue-share precedent in R&D data licensing? (M-007, M-008)
- [ ] (Market) Which Indian companies (pharma CDMOs, agritech, materials) have publicly sold or licensed R&D data, and what did the IndiaAI Datasets Platform actually launch? (M-018)
- [ ] (Technical) Is there independent evaluation of defenses (DP-RAG, output caps, query auditing, anomaly detection) against adaptive agent extractors like RAG-Thief and RAGCrawler? (T-004, T-005, T-015)
- [ ] (Technical) Can DP be applied to free-text answers about unstructured experiment knowledge at usable utility, given that clean-room DP only supports aggregates? (T-013)
- [ ] (Technical) Fetch the TEE.fail paper and Intel/AMD advisories to confirm T-006, and assess whether a seller-hosted gateway with attestation is realistic for small sellers
- [ ] (Legal) Has any court or regulator (India, EU, US) addressed whether AI-composed answers fall within intermediary safe harbour (IT Act s.79 or EU DSA)? (L-022, L-023)
- [ ] (Legal) Read the official CCI Samir Agrawal order and EU Horizontal Guidelines text on information exchange and data pools, and check FTC position after 2023 (L-018, L-019, L-020)
- [ ] (Legal) Indian authority on negligent misstatement and enforceability of AI-output disclaimers (L-026)
- [ ] (Market) Would sellers prefer data-for-access swaps (Lilly TuneLab style) to cash per query, and can a gateway offer a credit or barter mode? (M-027)
- [ ] (Market) Read the AIKosh dataset-contribution terms (EOI PDF was an unreadable image) to confirm whether commercial use and monetisation are barred for contributed datasets. (M-022, M-030)
- [ ] (Market) Is there any independent data (not vendor-written) on enterprises allowing AI agents to purchase third-party data autonomously, and what approval controls apply? (M-023)
- [ ] (Market) Is there a mid-market or non-pharma segment (materials, agritech, chemicals, semiconductor process) where sellers lack consortium access and would pay for query-level answers, with named interviews or surveys? (M-024, M-027, M-031)
- [ ] (Legal) Is paying or receiving x402 stablecoin (USDC) micropayments across borders permitted and how is it taxed or reported for an Indian company (RBI, FEMA, Income Tax VDA rules)? Fiat alternatives such as Stripe/UPI/card rails may be needed. (T-017)
- [ ] (Technical) Is there any adaptive-attacker evaluation of query-stream anomaly detection or per-buyer information-budget limits against RAGCrawler-style coverage-planning agents on a knowledge base? (T-020, T-027)
- [ ] (Technical) What are the primary specs for x402 (headers, facilitator trust, settlement finality) and AP2/ACP mandates, and does any of them support deferred or invoiced B2B settlement rather than per-call crypto? (T-016, T-018)
- [ ] (Legal) Obtain readable official texts (gazette or India Code) for DPDP Act s.3 and s.16, Copyright Act 1957 s.17 and s.19, and the Samir Agrawal judgment (PDFs on api.sci.gov.in and PRS were unreadable via fetch). (L-033 to L-035, L-042)
- [ ] (Legal) Does the Competition Act 2023 s.3(3) proviso, as applied by CCI since 2024, reach an information-exchange platform whose users do not communicate directly? Any CCI order after the amendment? (L-017, L-033)
- [ ] (Legal) What do US state laws other than California (Vermont, Texas, Oregon) and any EU rule say about data brokers, and does non-personal B2B experiment data fall outside all of them? (L-041)
- [ ] (Red-team) Read the Cornell/Third Circuit Cendyn opinion and the 2023 Competition Act s.3(3) text to test whether a query-only gateway with no cross-seller data pooling avoids the hub-and-spoke "rim". (R-011, R-012)
- [ ] (Red-team) Verify the Deloitte, Gartner and Ardent figures in R-014 at origin, and find any independent evidence of enterprises permitting agents to pay for third-party data. (R-014, M-023)
- [ ] (Market) GLG already ships an MCP connector for agent queries over expert transcripts (M-045): can its customers or GLG be shown to pay for, or accept, seller-contributed corporate findings, and what does GLG charge for the connector or library access?
- [ ] (Market) Why did the yet2 online marketplace shut down in 2018 and what do its "Why Online IP Marketplaces Fail" post and other post-mortems (Ocean Tomo, Innocentive-style platforms) say about cold-start and trust problems? The page returned 403. (M-036)
- [ ] (Market) Do Databricks Clean Rooms or Snowflake DCR (with agent interface) offer per-query seller pricing or marketplace listing for unstructured content, and can a seller restrict output to answers only? Read primary pricing and docs. (M-051, M-052)
- [ ] (Market) Not yet covered: InfoSum, Habu, Cape Privacy, Innocentive/Wazoku, CRO or CDMO data-sharing, agritech and semiconductor data exchanges (for example Covalent or Sematech-type), and Indian CDMO or pharma-association data initiatives. Which are real competitors?
