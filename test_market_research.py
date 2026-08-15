import asyncio
import os

from dotenv import load_dotenv

from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)

from app.marketing_agents.market_research import create_market_research_agent


# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")


# Disable OpenAI tracing
set_tracing_disabled(True)


# Create Groq client
groq_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


primary_model = OpenAIChatCompletionsModel(
    model="llama-3.1-8b-instant",
    openai_client=groq_client,
)


# Create Market Research Agent
market_research_agent = create_market_research_agent(
    primary_model
)


async def main():

    print("========================================")
    print("MARKET RESEARCH AGENT TEST")
    print("========================================")

    request = """
Research the AI-powered education market for college students aged 18-25.

Focus on:
- current market trends
- student needs
- pain points
- opportunities

Use the web research tool.

Do not invent statistics.
Clearly distinguish facts from assumptions.
"""

    print("\nStarting Market Research Agent...")

    result = await Runner.run(
        market_research_agent,
        request,
    )

    print("\n========================================")
    print("MARKET RESEARCH RESULT")
    print("========================================")

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())