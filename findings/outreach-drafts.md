# Outreach drafts: DRAFT, NOT SENT

Nothing here has been sent or posted. No agent contacts anyone. Roles and company types only; no named individuals. Finding IDs are unreviewed (see review.md for verdicts).

Note: `findings/kill-criteria.md` and `findings/red-team.md` are currently empty, so no K- or R- IDs exist yet. Questions below are linked to PROPOSED kill criteria (labelled P-K1 to P-K5) that the synthesis step should formalise:
- P-K1: Sellers refuse to release unused or internal knowledge at any realistic price (legal/IP/competitive fear).
- P-K2: No buyer has an identifiable budget or comparable spend for per-query external knowledge.
- P-K3: Buyers will not rely on answers they cannot inspect.
- P-K4: Seller legal/compliance review cost exceeds expected revenue.
- P-K5: Buyers prefer existing channels (marketplaces, clean rooms, expert networks, consortia) with no gap left.

## Target list

### Seller types
1. R&D / innovation heads and data governance leads at mid-size pharma and biotech (including Indian biopharma). Why: failed-experiment knowledge is valuable for AI models (M-011, M-012) but sharing is feared (M-010); India need and fragmentation (M-019, M-020).
2. Materials and chemicals R&D leaders. Why: failures outnumber successes (M-012), chemistry model gains from negatives (M-011).
3. Contract research organisations (CROs) and academic or institute labs with unused results. Why: sit on negative results, possible fewer competitive fears (M-009 shows non-profit pooling precedent, free, which tests willingness to be paid).
4. In-house legal, IP counsel and data-partnership leads at those firms. Why: legal/compliance and IP are the main blockers (M-014, M-015, M-016).

### Buyer types
5. AI/ML platform leads at drug-discovery or materials startups building agents or models. Why: demand signal for failure data (M-011, M-012); buyers are agents.
6. Heads of data procurement or business development at large pharma and chemicals firms already buying external data. Why: they hold comparable spend (marketplaces M-001, clean rooms M-004) and consortium experience (M-007, M-008).
7. Research or competitive-intelligence leads who buy expert-network calls. Why: expert networks at about 800-1,450 USD per call (M-006, low confidence) are the nearest price comparable.
8. Data marketplace and clean-room product or partnership staff (AWS, Snowflake, LiveRamp-type vendors; role only). Why: incumbents that could close the gap (M-002, M-005); tests P-K5.

## Interview-request drafts

All are research requests, not sales pitches.

**Pharma/biotech R&D or data governance lead (seller)**
Hi [Name], I'm researching how companies think about sharing internal research knowledge, such as unused or negative experiment results, with outside parties under strict controls. This is early-stage research and I'm not selling anything. Could I ask [Company]'s perspective in a 25-minute call? I'm mostly interested in what would stop you doing this. Happy to share anonymised findings afterwards. Thanks, [Your name]

**Materials/chemicals R&D leader (seller)**
Hi [Name], I'm researching whether firms like [Company] would ever make parts of their unused experimental knowledge answerable to outside queries without sharing the underlying data. This is research only, not a pitch or a product demo. Could we talk for 25 minutes? Sceptical views are especially welcome. Thanks, [Your name]

**CRO/academic lab (seller)**
Hi [Name], I'm doing research on whether labs hold results that go unused and whether any would be shared for payment under tight controls. This is not a sales pitch. Would you spare 20-25 minutes to tell me how this would or would not work at [Company]? Thanks, [Your name]

**Legal/IP counsel (seller side)**
Hi [Name], I'm researching the legal review a company would need before letting an outside party query its internal knowledge (answers only, no raw data). This is research, not legal-services or sales outreach. Could I ask for 20 minutes on what would block approval at [Company]? Thanks, [Your name]

**AI/ML platform lead (buyer)**
Hi [Name], I'm researching how teams building AI agents get hold of external knowledge they cannot find publicly, and whether they would pay for it. This is research, not a sales pitch. Could I have 25 minutes to learn how [Company] handles this today and what you would not trust? Thanks, [Your name]

**Data procurement / BD lead (buyer)**
Hi [Name], I'm researching how large firms buy external data and knowledge, including budgets and approval. I'm not selling anything. Could I ask [Company] a few questions in a 25-minute call about what you buy today, from whom, and at what cost? Thanks, [Your name]

**Expert-network user / competitive-intelligence lead (buyer)**
Hi [Name], I'm researching how teams spend on expert calls and similar insight sources, and where those fall short. This is research only, no pitch. Could we speak for 20 minutes about how [Company] decides what to buy? Thanks, [Your name]

**Marketplace/clean-room vendor staff**
Hi [Name], I'm researching how data marketplaces and clean rooms handle sellers who want to share knowledge without sharing data. This is not a sales pitch or partnership ask. Could I have 20 minutes to hear where current products fall short? Thanks, [Your name]

## Interview questions

### Sellers
Willingness to sell
1. Has [Company] ever shared or sold unused experiments or internal findings externally? What happened?
2. Which kinds of knowledge could never leave, and which might? Who decides?
3. Would you allow answers to be generated from your knowledge if the buyer never sees raw data? Why or why not?

Blockers and legal/compliance
4. Walk me through the approvals needed. Who reviews (legal, IP, security, compliance), and how long and how costly is it?
5. What contract terms, indemnities or audit rights would you need?
6. What would the cost of preparing the knowledge (structuring, provenance) be, and who would pay? (M-013)

Trust in what you cannot inspect
7. If an answer drawn from your knowledge goes to an AI agent you cannot watch, what would you need to see to feel safe (logs, review before release, caps)?
8. How would you detect or accept that many answers could reveal the underlying data?

Price
9. How would you want to be paid (per query, subscription, revenue share)? What price per answer would make this worth the effort?
10. What internal budget or revenue line would this count against? Any comparable deals?

Falsification (seller)
11. What would make you refuse outright, at any price? (P-K1)
12. Tell me about the last time legal said no to a data-sharing idea. Why? (P-K1, P-K4)
13. If the legal and prep cost were more than the plausible income, would you still do it? What income would you need? (P-K4)
14. Is there anything you already use (consortium, marketplace, free pool) that makes this unnecessary? (P-K5, M-007, M-009)

### Buyers
Willingness to buy
1. Where do you get external knowledge today, and what is missing, especially negative or unused results? (M-011, M-013)
2. Do your agents call outside sources automatically? Who approves a new source?
3. Would you use answers from a source you could not inspect?

Blockers and compliance
4. What would your legal, security or procurement team require before an agent pays for outside answers?
5. What risks come from using answers of unknown provenance in R&D decisions?

Trust in what you cannot inspect
6. What evidence (provenance, confidence, seller reputation, sample tests) would make you trust an answer? What accuracy level would be needed?
7. How would you check an answer was not wrong or stale?

Price
8. What would you pay per query or per answer? What would be too cheap to trust and too expensive to use?
9. Which budget owner approves this? What is the closest comparable spend (expert calls, datasets, clean rooms)? (M-004, M-006)
10. Could an agent spend autonomously within a cap, and what cap?

Falsification (buyer)
11. What would make you refuse to use this at all? (P-K3)
12. Name the last similar purchase you rejected, and why. (P-K2)
13. If you can already get this through a marketplace, clean room, expert call or consortium, what would still make you switch, if anything? (P-K5, M-001, M-005, M-008)
14. If no budget line exists today, who would have to create one, and how likely is that? (P-K2)
