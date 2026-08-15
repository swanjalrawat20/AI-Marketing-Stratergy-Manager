import asyncio
import os

from dotenv import load_dotenv

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)

from app.tools.competitor_research import competitor_research


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not configured in .env")

set_tracing_disabled(True)


# Groq client
groq_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


# Use the smaller model because your 70B model
# is currently close to its daily token limit.
model = OpenAIChatCompletionsModel(
    model="llama-3.1-8b-instant",
    openai_client=groq_client,
)


# Temporary test agent
competitor_test_agent = Agent(
    name="Competitor Research Test Agent",

    instructions="""
    You are testing the competitor research tool.

    When asked to research competitors, use the
    competitor_research tool.

    Summarize the research clearly.

    Do not invent competitor statistics.
    Distinguish web evidence from assumptions.
    """,

    model=model,

    tools=[
        competitor_research
    ],
)


async def main():

    print("========================================")
    print("COMPETITOR RESEARCH TOOL TEST")
    print("========================================")

    print(
        "Tavily API key loaded:",
        bool(os.getenv("TAVILY_API_KEY"))
    )

    request = """
    Research competitors for an AI-powered study
    assistant targeting college students aged 18-25.

    Identify relevant competitors and summarize:

    - competitor name
    - what they offer
    - strengths
    - weaknesses
    - possible differentiation opportunities

    Use the competitor research tool.
    """

    print("\nStarting Competitor Research Agent...")

    result = await Runner.run(
        competitor_test_agent,
        request,
    )

    print("\n========================================")
    print("COMPETITOR RESEARCH RESULT")
    print("========================================")

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
