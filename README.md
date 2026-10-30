# SecureKBGW

A research workspace for one product question: **should we build a secure knowledge-base gateway?**

Company A (seller) shares knowledge such as unused experiments and internal findings with Company B (buyer) on a **pay-per-query** basis. Buyers are **AI agents**, and they must never receive raw data, only answers to what they asked. Home jurisdiction is India, with EU and US differences noted where they matter.

This repo holds no product code. It holds the evidence: what research agents found on the legal, technical and market fronts, how a reviewer checked it, and how a red team attacked it.

> Legal content is a briefing for a lawyer, not legal advice.

## Where things stand

The first long run (2026-10-26) produced 101 findings plus 17 red-team attacks. The evidence leans **against** building as specified, and all 10 kill criteria are still open. The biggest unknown is whether anyone pays for failed-experiment data. Many findings are only partly supported or unverifiable, so check `findings/review.md` before relying on one.

## Start reading

1. [`digests/2026-10-26-long-run.md`](digests/2026-10-26-long-run.md): short summary of the run
2. [`findings/synthesis.md`](findings/synthesis.md): cross-department picture, conflicts, evidence for and against
3. [`findings/kill-criteria.md`](findings/kill-criteria.md): what would make us stop
4. [`findings/red-team.md`](findings/red-team.md): the strongest attacks
5. [`findings/review.md`](findings/review.md): which findings were verified, and which were not

## Layout

| Path | What it holds |
|---|---|
| `research/questions.md` | Open questions with checkboxes, plus follow-ups discovered during research |
| `findings/` | One file per department (`legal`, `technical`, `market`, `red-team`), plus `review`, `synthesis`, `kill-criteria`, `outreach-drafts` |
| `digests/` | Dated digests and `run-log.md` |
| `logs/` | Headless run logs (gitignored) |
| `.claude/agents/` | Subagents: legal, technical, market, reviewer, red-team, synthesis, outreach |
| `.claude/skills/` | The `/cycle` and `/digest` commands |
| `CLAUDE.md` | The rules every agent follows |

## How it works

- Each finding is one line: `[ID] claim | source URL | confidence | jurisdiction | retrieved date | status`. IDs use the prefixes `L-` legal, `T-` technical, `M-` market, `R-` red-team.
- A claim with no source URL is not a finding.
- Only the reviewer judges findings (supported, partly supported, unsupported, unverifiable), and it records verdicts in `findings/review.md`. A question is ticked only when it has a supported finding.
- Agents look for evidence against the idea as well as for it.
- Outreach is draft-only. Nothing is sent and nobody is contacted.

## Running it

Inside Claude Code, run `/cycle <department>` or `/digest`.

From a shell, one department at a time:

```bash
./run.sh legal        # or technical, market, red-team, outreach, digest
```

`run.sh` uses your Claude subscription login and writes a log to `logs/`. Set `USE_API_KEY=1` to use an API key instead. Python dependencies are managed with `uv` (see `pyproject.toml`).

## MVP prototype

`gateway/` is a seller-hosted, metered query gateway exposed as an MCP server, tested on synthetic data only. Results and limits are in [`research/mvp-results.md`](research/mvp-results.md).

### Quick start (seller)

```bash
./skbgw demo                       # synthetic notes + a demo buyer, prints how the buyer connects
./skbgw serve                      # web UI at http://localhost:8000/ and MCP at /mcp

./skbgw init ./my-notes            # later: load your own folder of .md / .txt / .json notes
./skbgw add-buyer "Acme" -c 50     # one key per buyer, with connect instructions
./skbgw topup "Acme" 100           # add credits
./skbgw report                     # queries, revenue, documents each buyer has seen
```

**Web UI.** Open `http://localhost:8000/`. The *Ask* tab is for buyers (paste a key, ask questions, see cost and credits). The *Seller dashboard* tab takes the admin token that `skbgw serve` prints, and lets you create buyer keys, top up credits, add notes and watch activity. Everything shown from seller notes is rendered as plain text.

The buyer pastes one line into Claude Code (printed by `add-buyer`) and then asks questions in plain English. Beyond localhost, serve behind HTTPS. Do not load real seller data before the legal scoping in `research/implementation-plan.md`.

### Developer commands

```bash
.venv/bin/python scripts/make_synthetic_kb.py 120 > data/synthetic_kb.json   # generate test data
.venv/bin/python -m unittest discover -s tests -t .                          # run tests
.venv/bin/python -m attack.run                                               # extraction attack benchmark
SKBGW_BUYER_KEY=demo-key .venv/bin/python -m gateway.mcp_server              # serve over MCP (stdio)
```

## Next step

The remaining questions can't be settled from the desk. `findings/outreach-drafts.md` has interview requests and questions for eight buyer and seller types, written to test the kill criteria. Review and edit them before any outreach.
