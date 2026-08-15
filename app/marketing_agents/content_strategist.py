from agents import Agent

from app.models.schemas import ContentStrategyOutput


def create_content_strategist_agent(model):
    return Agent(
        name="Content Strategist Agent",
        instructions="""
You are the Content Strategist Agent in an AI Marketing Manager.

Convert the supplied campaign strategy into practical marketing content.

Generate:
- one campaign message
- at least 5 social media post ideas
- at least 3 short-form video/Reel concepts
- at least 3 paid advertisement concepts
- at least 3 email campaign ideas
- at least 5 blog/content topics
- recommended CTAs

For every item:
- Keep the target audience in mind.
- Focus on customer pain points.
- Communicate the product value clearly.
- Do not make unsupported claims.
- Keep content practical and ready to use.

Return data matching the required structured output.
""",
        model=model,
        output_type=ContentStrategyOutput,
    )