import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app.agents.handoff_agents import (
    marketing_manager_agent,
    market_research_agent,
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")


# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


# ============================================================
# GROQ MODEL
# ============================================================

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


# ============================================================
# SPECIALIST ROUTING TOOLS
# ============================================================

ROUTING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "transfer_to_marketing_planner",
            "description": (
                "Transfer the request to the Marketing Planner "
                "specialist when the user needs campaign planning, "
                "campaign objectives, budget allocation, marketing "
                "channels, or marketing strategy."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Why the Marketing Planner is needed.",
                    }
                },
                "required": ["reason"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_market_research",
            "description": (
                "Transfer the request to the Market Research "
                "specialist when the user needs customer segments, "
                "customer needs, customer pain points, market trends, "
                "market opportunities, or market risks."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Why Market Research is needed.",
                    }
                },
                "required": ["reason"],
                "additionalProperties": False,
            },
        },
    },
]


# ============================================================
# MAIN TEST
# ============================================================

async def main():

    print()
    print("=" * 60)
    print("STEP 2.5 - MARKET RESEARCH HANDOFF TEST")
    print("=" * 60)
    print()

    print("Starting Marketing Manager...")
    print()

    user_request = """
I want to launch a marketing campaign.

Product:
AI-powered study assistant

Target audience:
College students aged 18-25

Budget:
₹50,000

Signup goal:
1,000 users

I specifically need market research.

Please hand this request to the Market Research specialist.

The Market Research specialist should analyse:

1. Target customer segments
2. Customer needs
3. Customer pain points
4. Market trends
5. Market opportunities
6. Potential challenges
7. Recommended marketing opportunities

Do not create the full campaign plan.
I want to test the Market Research handoff.
"""


    # ========================================================
    # STEP 1 - MARKETING MANAGER ROUTING
    # ========================================================

    manager_response = await groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": marketing_manager_agent.instructions,
            },
            {
                "role": "user",
                "content": user_request,
            },
        ],
        tools=ROUTING_TOOLS,
        tool_choice="auto",
    )

    manager_message = manager_response.choices[0].message


    # ========================================================
    # STEP 2 - CHECK ROUTING RESULT
    # ========================================================

    if not manager_message.tool_calls:
        print("Marketing Manager did not select a specialist.")
        print()
        print("Manager response:")
        print(manager_message.content)
        return


    tool_call = manager_message.tool_calls[0]

    selected_tool = tool_call.function.name

    print("MARKETING MANAGER ROUTING")
    print("-" * 60)
    print("Selected tool:", selected_tool)
    print()


    # ========================================================
    # STEP 3 - MARKET RESEARCH SPECIALIST
    # ========================================================

    if selected_tool == "transfer_to_market_research":

        print("Transferring to Market Research...")
        print()

        specialist_response = await groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": market_research_agent.instructions,
                },
                {
                    "role": "user",
                    "content": user_request,
                },
            ],
        )

        final_output = specialist_response.choices[0].message.content

        last_agent = market_research_agent.name


    # ========================================================
    # STEP 4 - MARKETING PLANNER SPECIALIST
    # ========================================================

    elif selected_tool == "transfer_to_marketing_planner":

        print("Transferring to Marketing Planner...")
        print()

        specialist_response = await groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": marketing_planner_agent.instructions,
                },
                {
                    "role": "user",
                    "content": user_request,
                },
            ],
        )

        final_output = specialist_response.choices[0].message.content

        last_agent = marketing_planner_agent.name


    # ========================================================
    # UNKNOWN TOOL
    # ========================================================

    else:

        print("Unknown routing tool:", selected_tool)
        return


    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print()
    print("=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print()

    print(final_output)

    print()
    print("=" * 60)
    print("LAST AGENT")
    print("=" * 60)
    print()

    print(last_agent)

    print()
    print("=" * 60)
    print("STEP 2.5 COMPLETE")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())