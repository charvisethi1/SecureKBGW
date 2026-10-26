---
name: digest
description: Run the synthesis subagent across all departments and write a dated summary digest with an evidence tally for and against building
disable-model-invocation: true
---

Produce a cross-department summary. Follow every rule in CLAUDE.md.

## 1. Synthesis
Use the Agent tool to delegate to the `synthesis` subagent and wait for it to finish rewriting `findings/synthesis.md`.

## 2. Write the summary
Read `findings/synthesis.md`, `findings/review.md`, `findings/kill-criteria.md` and `research/questions.md`. Write `digests/YYYY-MM-DD-summary.md` using today's date. **Max 400 words** with these sections:
- **Verified findings by department** (Legal, Technical, Market, Red-team). Show supported IDs plus a one-line gist each, and the count of unreviewed and unsupported findings.
- **Cross-department conflicts** (with IDs)
- **Open questions** (unticked items, most important first)
- **Kill-criteria status** (each K-ID with open, mitigated or confirmed)
- **Evidence tally** (a plain count of supported findings pointing for building vs against building, with the IDs). Mark unreviewed items separately and do not count them.

Give **no recommendations beyond the evidence.** No "you should build" or "you should not build". Then print the summary to the console. Only write inside `findings/` and `digests/`.
