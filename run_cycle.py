import asyncio, datetime, os, sys
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ResultMessage

# Pro-subscription mode: make sure no API key is picked up by accident.
# To use an API key later, run with USE_API_KEY=1 and set ANTHROPIC_API_KEY.
if not os.getenv("USE_API_KEY"):
    os.environ.pop("ANTHROPIC_API_KEY", None)

FORMAT = ("Record each finding as: claim | source URL | confidence (high/med/low) | "
          "jurisdiction (legal only) | date retrieved. Never record a claim without a source. "
          "Append to your file; do not repeat earlier findings.")
LEAN = "Keep it lean: at most 5 searches and 8 sources per run. Prefer primary sources."
WEB = ["WebSearch", "WebFetch", "Read", "Write"]

AGENTS = {
    "legal": AgentDefinition(
        description="Legal research: IP/trade secrets, data protection (India DPDP, GDPR), contracts, liability, competition law.",
        prompt=f"You are a legal research analyst. Prefer statutes and official sources; mark anything unverified. "
               f"This is a briefing for a lawyer, not legal advice. Write to findings/legal.md. {FORMAT} {LEAN}",
        tools=WEB, model="sonnet"),
    "technical": AgentDefinition(
        description="Technical research: secure KB gateways, clean rooms, query metering, extraction defenses, agent-access protocols.",
        prompt=f"You are a technical research analyst. Write to findings/technical.md. {FORMAT} {LEAN}",
        tools=WEB, model="sonnet"),
    "market": AgentDefinition(
        description="Market research: existing data marketplaces, demand, supply incentives, pricing, competitors.",
        prompt=f"You are a market research analyst. Write to findings/market.md. {FORMAT} {LEAN}",
        tools=WEB, model="sonnet"),
    "red-team": AgentDefinition(
        description="Attacks the idea: data extraction via queries, prompt injection, liability, the no-seller problem.",
        prompt=f"Find the strongest reasons this product fails or leaks data. Write to findings/red-team.md. {LEAN}",
        tools=["Read", "WebSearch", "Write"], model="sonnet"),
    "outreach": AgentDefinition(
        description="Drafts interview requests to potential buyers and sellers. Draft only; never sends.",
        prompt="Draft short outreach messages into findings/outreach-drafts.md for the founder to approve.",
        tools=["Read", "Write"], model="sonnet"),  # no send tools, by design
}
REVIEWER = AgentDefinition(
    description="Verifies new findings: opens each cited source and checks the claim is supported.",
    prompt="Check each NEW finding against its cited source. Write verdicts (supported / unsupported / "
           "unverifiable) to findings/review.md. Be strict, especially on legal claims. Max 8 sources per run.",
    tools=["Read", "WebFetch", "Write"], model="sonnet")

async def main():
    focus = sys.argv[1] if len(sys.argv) > 1 else ""
    if focus not in AGENTS:
        sys.exit(f"Usage: python run_cycle.py [{'|'.join(AGENTS)}]")
    active = {focus: AGENTS[focus]}
    review = focus in ("legal", "technical", "market")
    if review:
        active["reviewer"] = REVIEWER

    today = datetime.date.today().isoformat()
    steps = (f"Delegate to the '{focus}' subagent and wait for it to finish"
             + (", then run the 'reviewer' on the new findings" if review else "") + ". ")
    prompt = (f"Today is {today}. Read research/questions.md and skim the existing files in findings/. "
              f"Pick at most 3 open questions in the '{focus}' area that are not yet answered. {steps}"
              f"Use only these subagents. Then write digests/{today}-{focus}.md (max 300 words): "
              "new verified findings, open questions, and anything that could make the idea unviable.")

    async for msg in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="sonnet",
            allowed_tools=["Read", "Write", "Glob", "Grep", "WebSearch", "WebFetch", "Agent"],
            permission_mode="acceptEdits",
            agents=active,
            max_turns=30,
            max_budget_usd=2.0,  # estimated-cost safety stop
            env={"CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1",
                 "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS": "2"},
        ),
    ):
        if isinstance(msg, ResultMessage):
            print(f"{msg.subtype} | est. cost ${msg.total_cost_usd}")

asyncio.run(main())
