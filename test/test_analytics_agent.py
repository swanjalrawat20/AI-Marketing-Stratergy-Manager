import asyncio
import os

from dotenv import load_dotenv

from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)

from app.marketing_agents.analytics_optimizer import (
    create_analytics_optimizer_agent,
)


async def main():

    print("=" * 50)
    print("ANALYTICS AGENT TEST")
    print("=" * 50)

    load_dotenv()

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is not set."
        )

    set_tracing_disabled(True)

    client = AsyncOpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    model = OpenAIChatCompletionsModel(
        model="llama-3.1-8b-instant",
        openai_client=client,
    )

    analytics_agent = create_analytics_optimizer_agent(
        model
    )

    request = """
Analyze the actual campaign performance data.

The campaign data is located at:

sample_campaign_data.csv

Campaign target:

Product:
AI-powered study assistant

Target audience:
College students aged 18-25

Total campaign budget:
₹50,000

Signup goal:
1,000 signups

Campaign duration:
30 days

IMPORTANT:

Use the campaign data tool to analyze the CSV.

Do not invent actual performance numbers.

Clearly distinguish:

TARGET metrics
from
ACTUAL metrics.

After analyzing the data, provide:

1. Target metrics
2. Actual campaign performance
3. Channel performance
4. Best channel
5. Worst channel
6. Optimization recommendations
7. 7-day optimization plan
"""

    print()
    print("Starting Analytics Agent...")

    result = await Runner.run(
        analytics_agent,
        request,
    )

    print()
    print("=" * 50)
    print("ANALYTICS RESULT")
    print("=" * 50)

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
