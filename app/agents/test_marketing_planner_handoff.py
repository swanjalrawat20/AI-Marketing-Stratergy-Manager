import asyncio
import os

from dotenv import load_dotenv
from groq import AsyncGroq

from app.agents.handoff_agents import (
    marketing_manager_agent,
    marketing_planner_agent,
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")


# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = AsyncGroq(
    api_key=GROQ_API_KEY,
)


# ============================================================
# HANDOFF TOOLS
# ============================================================

handoff_tools = [
    {
        "type": "function",
        "function": {
            "name": "transfer_to_marketing_planner",
            "description": (
                "Transfer the current request to the Marketing "
                "Planner specialist. Use this when the user needs "
                "campaign planning, campaign objectives, target "
                "audience, budget allocation, marketing channels, "
                "or campaign strategy."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_market_research",
            "description": (
                "Transfer the current request to the Market Research "
                "specialist. Use this when the user needs market "
                "research, customer segments, customer needs, "
                "customer pain points, market trends, market "
                "opportunities, or market risks."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
]


# ============================================================
# USER REQUEST
# ============================================================

USER_REQUEST = """
I want to launch a marketing campaign.

Product:
AI-powered study assistant

Target audience:
College students aged 18-25

Budget:
₹50,000

Signup goal:
1,000 users

I need a complete marketing plan.

The Marketing Planner must create:

1. Campaign objective
2. Target audience
3. Budget allocation
4. Marketing channels
5. Campaign strategy

This is a Marketing Planner handoff test.
"""


# ============================================================
# MAIN
# ============================================================

async def main():

    print()
    print("=" * 60)
    print("STEP 2.6 - MARKETING PLANNER HANDOFF TEST")
    print("=" * 60)
    print()

    print("Starting Marketing Manager...")
    print()

    print(f"Groq model: {GROQ_MODEL}")
    print()

    # ========================================================
    # STEP 1
    # MARKETING MANAGER DECIDES WHICH SPECIALIST TO USE
    # ========================================================

    manager_messages = [
        {
            "role": "system",
            "content": marketing_manager_agent.instructions,
        },
        {
            "role": "user",
            "content": USER_REQUEST,
        },
    ]

    manager_response = await groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=manager_messages,
        tools=handoff_tools,
        tool_choice={
            "type": "function",
            "function": {
                "name": "transfer_to_marketing_planner",
            },
        },
    )

    manager_message = manager_response.choices[0].message

    print("MARKETING MANAGER ROUTING")
    print("-" * 60)

    # ========================================================
    # CHECK TOOL CALL
    # ========================================================

    if not manager_message.tool_calls:

        print("ERROR: Marketing Manager did not create a handoff.")
        print()

        if manager_message.content:
            print("Manager response:")
            print(manager_message.content)

        return

    tool_call = manager_message.tool_calls[0]

    selected_tool = tool_call.function.name

    print(f"Selected tool: {selected_tool}")
    print()

    # ========================================================
    # STEP 2
    # EXECUTE HANDOFF
    # ========================================================

    if selected_tool == "transfer_to_marketing_planner":

        print("Transferring to Marketing Planner...")
        print()

        planner_messages = [
            {
                "role": "system",
                "content": marketing_planner_agent.instructions,
            },
            {
                "role": "user",
                "content": USER_REQUEST,
            },
        ]

        planner_response = await groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=planner_messages,
        )

        final_output = planner_response.choices[0].message.content

        last_agent = marketing_planner_agent.name

    elif selected_tool == "transfer_to_market_research":

        print("ERROR: Wrong specialist selected.")
        print()
        print(
            "Expected: transfer_to_marketing_planner"
        )

        return

    else:

        print(f"ERROR: Unknown handoff: {selected_tool}")

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

    # ========================================================
    # LAST AGENT
    # ========================================================

    print()
    print("=" * 60)
    print("LAST AGENT")
    print("=" * 60)
    print()

    print(last_agent)

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 60)
    print("STEP 2.6 COMPLETE")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())