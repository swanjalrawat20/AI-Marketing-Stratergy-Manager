import asyncio
import json
import os

from dotenv import load_dotenv
from groq import AsyncGroq, RateLimitError


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

client = AsyncGroq(
    api_key=GROQ_API_KEY,
)


# ============================================================
# GROQ MODEL
# ============================================================
#
# IMPORTANT:
# We intentionally hard-code the model here so that an old
# GROQ_MODEL value in .env cannot switch us back to:
#
# llama-3.3-70b-versatile
#
# The 70B model previously exhausted the daily token limit.
#
# ============================================================

MODEL = "llama-3.1-8b-instant"


# ============================================================
# TOKEN SETTINGS
# ============================================================
#
# Keep the end-to-end test lightweight.
#
# Router only needs enough tokens to produce a tool call.
# Specialist only needs enough tokens to produce a useful
# verification response.
#
# ============================================================

ROUTER_MAX_TOKENS = 250
SPECIALIST_MAX_TOKENS = 600


# ============================================================
# SPECIALIST INSTRUCTIONS
# ============================================================

MARKETING_PLANNER_INSTRUCTIONS = """
You are the Marketing Planner specialist.

Create a clear marketing plan based ONLY on the user's
requirements.

Focus on:

1. Campaign objective
2. Target audience
3. Budget allocation
4. Marketing channels
5. Campaign strategy

Important:

- Use only requirements provided by the user.
- Do not invent deadlines, budgets, goals, or constraints.
- If something is not specified, say that it was not specified.
- Return a concise but useful marketing planning response.
- Do not perform unrelated specialist tasks.
"""


MARKET_RESEARCH_INSTRUCTIONS = """
You are the Market Research specialist.

Perform qualitative market research based on the user's
requirements.

Focus on:

1. Target customer segments
2. Customer needs
3. Customer pain points
4. Market trends
5. Market opportunities
6. Potential market challenges
7. Recommended marketing opportunities

Important:

- Do not invent market statistics.
- Do not invent research sources.
- Clearly distinguish qualitative analysis from verified facts.
- Give practical marketing insights.
- Return a concise but useful market research report.
- Do not perform unrelated specialist tasks.
"""


# ============================================================
# MARKETING MANAGER INSTRUCTIONS
# ============================================================

MARKETING_MANAGER_INSTRUCTIONS = """
You are the main Marketing Manager.

Your job is to determine which specialist should handle
the user's request.

You have two specialist tools:

1. transfer_to_market_research

Use this when the user needs:

- market research
- customer segments
- customer needs
- customer pain points
- market trends
- market opportunities
- market risks
- market challenges

2. transfer_to_marketing_planner

Use this when the user needs:

- campaign planning
- campaign objectives
- target audience
- budget allocation
- marketing channels
- marketing strategy

IMPORTANT:

When the request clearly belongs to a specialist,
you MUST call the appropriate transfer tool.

Do NOT answer the specialist request yourself.

Your job is routing only.
"""


# ============================================================
# TOOL DEFINITIONS
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "transfer_to_market_research",
            "description": (
                "Transfer the user's request to the Market Research "
                "specialist. Use for customer segments, customer needs, "
                "customer pain points, market trends, market opportunities, "
                "market risks, and market challenges."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_request": {
                        "type": "string",
                        "description": "The complete user request.",
                    }
                },
                "required": ["user_request"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_marketing_planner",
            "description": (
                "Transfer the user's request to the Marketing Planner "
                "specialist. Use for campaign planning, campaign objectives, "
                "target audience, budget allocation, marketing channels, "
                "and marketing strategy."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_request": {
                        "type": "string",
                        "description": "The complete user request.",
                    }
                },
                "required": ["user_request"],
                "additionalProperties": False,
            },
        },
    },
]


# ============================================================
# GROQ 429 ERROR HELPER
# ============================================================

def format_rate_limit_error(exc: Exception) -> str:
    """
    Convert a Groq rate-limit exception into a readable message.
    """

    message = str(exc)

    retry_text = ""

    if "try again" in message.lower():
        lower_message = message.lower()

        start = lower_message.find("try again")

        if start != -1:
            retry_text = message[start:]

            # Keep only the first sentence when possible.
            if "." in retry_text:
                retry_text = retry_text.split(".")[0] + "."

    if retry_text:
        return retry_text

    return "Please try again later."


# ============================================================
# ROUTE REQUEST
# ============================================================

async def route_request(user_request: str):
    """
    Send the user request to the Marketing Manager router.

    The router MUST select one of the specialist transfer tools.
    """

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": MARKETING_MANAGER_INSTRUCTIONS,
                },
                {
                    "role": "user",
                    "content": user_request,
                },
            ],
            tools=TOOLS,
            tool_choice="required",
            temperature=0,
            max_tokens=ROUTER_MAX_TOKENS,
        )

    except RateLimitError as exc:
        print()
        print("GROQ RATE LIMIT ERROR DURING ROUTING")
        print(format_rate_limit_error(exc))
        return None, None, "rate_limit"

    message = response.choices[0].message

    if not message.tool_calls:
        raise RuntimeError(
            "Marketing Manager did not produce a tool call."
        )

    tool_call = message.tool_calls[0]

    tool_name = tool_call.function.name

    try:
        arguments = json.loads(
            tool_call.function.arguments
        )

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Invalid tool arguments: "
            f"{tool_call.function.arguments}"
        ) from exc

    return tool_name, arguments, "success"


# ============================================================
# RUN SPECIALIST
# ============================================================

async def run_specialist(
    specialist_name: str,
    user_request: str,
):
    """
    Execute the specialist selected by the Marketing Manager.
    """

    if specialist_name == "transfer_to_market_research":

        instructions = MARKET_RESEARCH_INSTRUCTIONS
        agent_name = "Market Research"

    elif specialist_name == "transfer_to_marketing_planner":

        instructions = MARKETING_PLANNER_INSTRUCTIONS
        agent_name = "Marketing Planner"

    else:

        raise RuntimeError(
            f"Unknown specialist tool: {specialist_name}"
        )

    try:

        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": user_request,
                },
            ],
            temperature=0.2,
            max_tokens=SPECIALIST_MAX_TOKENS,
        )

    except RateLimitError as exc:

        error_message = format_rate_limit_error(exc)

        fallback_output = (
            f"[{agent_name}] Groq rate limit reached. "
            f"{error_message}\n"
            "The routing workflow itself was successful, "
            "but the specialist response could not be generated."
        )

        return agent_name, fallback_output, "rate_limit"

    final_output = response.choices[0].message.content

    if not final_output:

        raise RuntimeError(
            f"{agent_name} returned an empty response."
        )

    return agent_name, final_output, "success"


# ============================================================
# RUN INDIVIDUAL TEST
# ============================================================

async def run_test(
    test_number: int,
    title: str,
    user_request: str,
    expected_tool: str,
    expected_agent: str,
):
    print()
    print("=" * 60)
    print(f"TEST {test_number} - {title}")
    print("=" * 60)

    print()
    print(f"Groq model: {MODEL}")

    print()
    print(f"Router max tokens: {ROUTER_MAX_TOKENS}")

    print(
        f"Specialist max tokens: {SPECIALIST_MAX_TOKENS}"
    )

    print()
    print("User request:")
    print()
    print(user_request)

    # ========================================================
    # ROUTING
    # ========================================================

    print()
    print("-" * 60)
    print("MARKETING MANAGER ROUTING")
    print("-" * 60)

    tool_name, arguments, route_status = await route_request(
        user_request
    )

    if route_status == "rate_limit":

        print()
        print("ROUTING: FAIL")
        print("Reason: Groq rate limit.")

        return False

    print()
    print("Selected tool:")
    print(tool_name)

    print()
    print("Tool arguments:")
    print(
        json.dumps(
            arguments,
            ensure_ascii=False,
            indent=2,
        )
    )

    # ========================================================
    # VERIFY ROUTING
    # ========================================================

    if tool_name != expected_tool:

        print()
        print("ROUTING: FAIL")
        print(f"Expected: {expected_tool}")
        print(f"Actual:   {tool_name}")

        return False

    print()
    print("ROUTING: PASS")

    # ========================================================
    # SPECIALIST EXECUTION
    # ========================================================

    print()
    print("-" * 60)
    print("SPECIALIST EXECUTION")
    print("-" * 60)

    forwarded_request = arguments.get(
        "user_request",
        user_request,
    )

    (
        agent_name,
        final_output,
        specialist_status,
    ) = await run_specialist(
        tool_name,
        forwarded_request,
    )

    print()
    print("LAST AGENT")
    print(agent_name)

    print()
    print("-" * 60)
    print("FINAL SPECIALIST OUTPUT")
    print("-" * 60)

    print()
    print(final_output)

    # ========================================================
    # VERIFY SPECIALIST
    # ========================================================

    execution_pass = (
        agent_name == expected_agent
        and specialist_status == "success"
    )

    print()
    print("-" * 60)

    if execution_pass:

        print("SPECIALIST EXECUTION: PASS")

        print()
        print(f"Expected agent: {expected_agent}")
        print(f"Actual agent:   {agent_name}")

    else:

        print("SPECIALIST EXECUTION: FAIL")

        print()
        print(f"Expected agent: {expected_agent}")
        print(f"Actual agent:   {agent_name}")

        if specialist_status == "rate_limit":

            print()
            print(
                "NOTE: Specialist could not execute because "
                "Groq rate limit was reached."
            )

    return execution_pass


# ============================================================
# MAIN
# ============================================================

async def main():

    print()
    print("=" * 60)
    print("STEP 2.8 - GROQ NATIVE END-TO-END TEST")
    print("=" * 60)

    print()
    print("Using Groq SDK")

    print()
    print(f"Model: {MODEL}")

    print()
    print("Low-token test configuration enabled.")

    print(
        f"Router max tokens: {ROUTER_MAX_TOKENS}"
    )

    print(
        f"Specialist max tokens: {SPECIALIST_MAX_TOKENS}"
    )

    # ========================================================
    # TEST 1 - MARKET RESEARCH
    # ========================================================

    research_request = """
I am launching an AI-powered study assistant for college students.

Before creating a campaign, I need to understand:

- who the main customer segments are
- what students need
- their major pain points
- current market trends
- market opportunities
- potential market risks

Please research the market and provide useful marketing insights.
""".strip()

    research_pass = await run_test(
        test_number=1,
        title="MARKET RESEARCH END-TO-END",
        user_request=research_request,
        expected_tool="transfer_to_market_research",
        expected_agent="Market Research",
    )

    # ========================================================
    # TEST 2 - MARKETING PLANNER
    # ========================================================

    planner_request = """
I want to launch a marketing campaign for an AI-powered
study assistant.

Target audience:
College students aged 18-25

Budget:
₹50,000

Signup goal:
1,000 users

Create a marketing plan covering:

1. Campaign objective
2. Target audience
3. Budget allocation
4. Marketing channels
5. Campaign strategy
""".strip()

    planner_pass = await run_test(
        test_number=2,
        title="MARKETING PLANNER END-TO-END",
        user_request=planner_request,
        expected_tool="transfer_to_marketing_planner",
        expected_agent="Marketing Planner",
    )

    # ========================================================
    # FINAL VERIFICATION
    # ========================================================

    print()
    print("=" * 60)
    print("STEP 2.8 VERIFICATION")
    print("=" * 60)

    print()
    print(
        "Market Research end-to-end:",
        "PASS" if research_pass else "FAIL",
    )

    print(
        "Marketing Planner end-to-end:",
        "PASS" if planner_pass else "FAIL",
    )

    print()

    # ========================================================
    # SUCCESS
    # ========================================================

    if research_pass and planner_pass:

        print("=" * 60)
        print(
            "STEP 2.8 COMPLETE - "
            "ALL END-TO-END TESTS PASSED"
        )
        print("=" * 60)

    # ========================================================
    # FAILURE
    # ========================================================

    else:

        print("=" * 60)
        print(
            "STEP 2.8 FAILED - "
            "END-TO-END FLOW NEEDS FIXING"
        )
        print("=" * 60)

        raise SystemExit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())