import asyncio
import os

from dotenv import load_dotenv

from agents import Runner, RunConfig
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from app.agents.handoff_agents import marketing_manager_agent


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")


groq_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


groq_model = OpenAIChatCompletionsModel(
    model=os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile",
    ),
    openai_client=groq_client,
)


async def main():

    print()
    print("========================================")
    print("STEP 2.4 - REAL HANDOFF EXECUTION TEST")
    print("========================================")
    print()

    print("Starting Marketing Manager...")
    print()

    result = await Runner.run(
        marketing_manager_agent,

        """
I want to launch a marketing campaign for my product.

My budget is ₹50,000.

My signup goal is 1,000 users.

Help me create the campaign plan.
""",

        run_config=RunConfig(
            model=groq_model,
        ),
    )

    print()
    print("========================================")
    print("FINAL OUTPUT")
    print("========================================")
    print()

    print(result.final_output)

    print()
    print("========================================")
    print("LAST AGENT")
    print("========================================")
    print()

    print(result.last_agent.name)

    print()
    print("========================================")
    print("STEP 2.4 COMPLETE")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(main())