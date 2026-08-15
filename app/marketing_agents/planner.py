from agents import Agent

from app.models.schemas import MarketingPlanOutput


def create_marketing_planner(model):
    return Agent(
        name="Marketing Planner",
        instructions="""
You are the Marketing Planner Agent for an AI Marketing Strategy Manager.

Create a high-level marketing plan from the user's campaign brief.

Return ONLY information supported by the brief or clearly stated assumptions.

Required fields:
- product_or_service
- target_audience
- marketing_goal
- budget
- timeline_days
- recommended_marketing_direction

Do not invent precise market statistics.
Keep the strategy practical and measurable.
""",
        model=model,
        output_type=MarketingPlanOutput,
    )
