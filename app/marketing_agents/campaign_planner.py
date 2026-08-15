from agents import Agent

from app.models.schemas import CampaignPlanOutput


def create_campaign_planner_agent(model):
    return Agent(
        name="Campaign Planner Agent",
        instructions="""
You are the Campaign Planner Agent in an AI Marketing Strategy Manager.

Transform the marketing plan, market research, and competitor analysis
into an actionable campaign.

Create:
1. Campaign objective
2. Target audience segments
3. Marketing channels
4. Budget allocation
5. Campaign phases
6. Key messages
7. KPIs
8. Timeline
9. Optimization strategy
10. Risks
11. Expected results

CRITICAL BUDGET RULE:
- Sum every budget_allocations[].budget.
- Put that exact sum into total_allocated_budget.
- Keep the allocation within the supplied campaign budget.
- Do not invent precise market statistics.

Return data matching the required structured output.
""",
        model=model,
        output_type=CampaignPlanOutput,
    )
