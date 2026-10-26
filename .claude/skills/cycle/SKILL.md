---
name: cycle
description: Run one research cycle for a single department (legal, technical, market, red-team or outreach) and write a dated digest
argument-hint: "<legal|technical|market|red-team|outreach>"
disable-model-invocation: true
---

Run ONE research cycle for the department **$ARGUMENTS**. Follow every rule in CLAUDE.md. Work sequentially and never run subagents in parallel.

## 0. Validate
If `$ARGUMENTS` is not exactly one of `legal`, `technical`, `market`, `red-team`, `outreach`, stop. Print `Usage: /cycle <legal|technical|market|red-team|outreach>` and do nothing else.

## 1. Pick questions
- Read `research/questions.md` and skim the matching findings file(s) in `findings/` (plus `findings/review.md` and `findings/kill-criteria.md`).
- Pick **at most 3** open (unticked) questions for this department. Use the matching section, plus items tagged with this department under "Discovered during research". Prefer questions with no findings yet, then questions whose findings were judged unsupported or unverifiable.
- red-team has no section of its own. Its targets are open kill criteria and the weakest-looking claims across departments.
- outreach has no questions. It drafts or refreshes `findings/outreach-drafts.md` from current market and red-team findings.

## 2. Delegate
Use the Agent tool to delegate to the subagent named `$ARGUMENTS` and wait for it to finish. In the prompt, pass the chosen questions verbatim, today's date (YYYY-MM-DD) and the reminder: at most 5 searches and 8 sources.

## 3. Review (legal, technical and market only)
Delegate to the `reviewer` subagent and wait. Tell it to review only findings in `findings/$ARGUMENTS.md` that are not yet in `findings/review.md`. Skip this step for red-team and outreach.

## 4. Update checkboxes
In `research/questions.md`, tick `[x]` a question only when at least one finding answering it is marked **supported** in `findings/review.md`. Append the supporting IDs in parentheses. Do not tick anything otherwise. Do not delete questions.

## 5. Write the digest
Write `digests/YYYY-MM-DD-$ARGUMENTS.md` using today's date. If that file already exists, append a `## Run 2` (or next number) section instead of overwriting. **Max 300 words** with these sections:
- **New findings** (IDs plus a one-line gist each)
- **Review verdicts** (counts plus any unsupported IDs, or "n/a" for red-team and outreach)
- **Open questions** (what remains for this department)
- **Could make the idea unviable** (anything pointing that way, with IDs and kill-criteria references)

Then print the digest to the console. Only write inside `research/`, `findings/` and `digests/`.
