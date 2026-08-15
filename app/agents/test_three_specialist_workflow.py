# ============================================================
# STEP 2.11 - THREE SPECIALIST UNIFIED WORKFLOW TEST
# ============================================================

from app.agents.handoff_agents import run_marketing_manager
import os


# ============================================================
# CONFIGURATION
# ============================================================

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


# ============================================================
# TEST REQUESTS
# ============================================================

MARKET_RESEARCH_REQUEST = """
I am launching an AI-powered study assistant for college students.

Before creating a campaign, I need to understand:

- who the main customer segments are
- what students need
- their major pain points
- current market trends
- market opportunities
- potential market risks

Please research the market and provide useful marketing insights.
"""


MARKETING_PLANNER_REQUEST = """
I want to launch a marketing campaign for an
AI-powered study assistant.

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
"""


CAMPAIGN_ANALYST_REQUEST = """
Analyze my marketing campaign performance.

I spent ₹50,000 and received 1,000 signups.

I want to understand:

- campaign performance
- cost per signup
- which channels performed best
- areas of underperformance
- optimization opportunities
- recommended next actions

If channel-level data is not provided, clearly state
that it cannot be determined.
"""


# ============================================================
# OUTPUT HELPERS
# ============================================================

def print_result(result):
    print()
    print("SELECTED TOOL")
    print("-" * 60)
    print(result.get("selected_tool"))

    print()
    print("HANDOFF")
    print("-" * 60)
    print(result.get("handoff"))

    print()
    print("LAST AGENT")
    print("-" * 60)
    print(result.get("last_agent"))

    print()
    print("FINAL OUTPUT")
    print("-" * 60)
    print(result.get("final_output"))


# ============================================================
# VERIFICATION
# ============================================================

def verify_result(
    result,
    expected_tool,
    expected_agent,
):
    selected_tool = result.get("selected_tool")
    handoff = result.get("handoff")
    last_agent = result.get("last_agent")
    final_output = result.get("final_output") or ""

    tool_pass = (
        selected_tool == expected_tool
        or handoff == expected_tool
    )

    agent_pass = last_agent == expected_agent

    output_pass = len(final_output.strip()) > 0

    print()
    print("VERIFICATION")
    print("-" * 60)

    print(
        "Selected tool: "
        + ("PASS" if tool_pass else "FAIL")
    )

    print(
        "Last agent: "
        + ("PASS" if agent_pass else "FAIL")
    )

    print(
        "Final output: "
        + ("PASS" if output_pass else "FAIL")
    )

    return tool_pass and agent_pass and output_pass


# ============================================================
# TEST 1 - MARKET RESEARCH
# ============================================================

def test_market_research():
    print()
    print("=" * 60)
    print("TEST 1 - MARKET RESEARCH WORKFLOW")
    print("=" * 60)

    print()
    print("USER REQUEST")
    print("-" * 60)
    print(MARKET_RESEARCH_REQUEST)

    print()
    print("RUNNING WORKFLOW")
    print("-" * 60)

    result = run_marketing_manager(
        MARKET_RESEARCH_REQUEST
    )

    print_result(result)

    passed = verify_result(
        result,
        "transfer_to_market_research",
        "Market Research",
    )

    print()
    print(
        "TEST 1: "
        + ("PASS" if passed else "FAIL")
    )

    return passed


# ============================================================
# TEST 2 - MARKETING PLANNER
# ============================================================

def test_marketing_planner():
    print()
    print("=" * 60)
    print("TEST 2 - MARKETING PLANNER WORKFLOW")
    print("=" * 60)

    print()
    print("USER REQUEST")
    print("-" * 60)
    print(MARKETING_PLANNER_REQUEST)

    print()
    print("RUNNING WORKFLOW")
    print("-" * 60)

    result = run_marketing_manager(
        MARKETING_PLANNER_REQUEST
    )

    print_result(result)

    passed = verify_result(
        result,
        "transfer_to_marketing_planner",
        "Marketing Planner",
    )

    print()
    print(
        "TEST 2: "
        + ("PASS" if passed else "FAIL")
    )

    return passed


# ============================================================
# TEST 3 - CAMPAIGN ANALYST
# ============================================================

def test_campaign_analyst():
    print()
    print("=" * 60)
    print("TEST 3 - CAMPAIGN ANALYST WORKFLOW")
    print("=" * 60)

    print()
    print("USER REQUEST")
    print("-" * 60)
    print(CAMPAIGN_ANALYST_REQUEST)

    print()
    print("RUNNING WORKFLOW")
    print("-" * 60)

    result = run_marketing_manager(
        CAMPAIGN_ANALYST_REQUEST
    )

    print_result(result)

    passed = verify_result(
        result,
        "transfer_to_campaign_analyst",
        "Campaign Analyst",
    )

    print()
    print(
        "TEST 3: "
        + ("PASS" if passed else "FAIL")
    )

    return passed


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("=" * 60)
    print("STEP 2.11 - THREE SPECIALIST UNIFIED WORKFLOW TEST")
    print("=" * 60)

    print()
    print("Using Groq SDK")
    print(f"Model: {GROQ_MODEL}")

    research_pass = test_market_research()

    planner_pass = test_marketing_planner()

    analyst_pass = test_campaign_analyst()

    print()
    print("=" * 60)
    print("STEP 2.11 VERIFICATION")
    print("=" * 60)

    print(
        "Market Research: "
        + ("PASS" if research_pass else "FAIL")
    )

    print(
        "Marketing Planner: "
        + ("PASS" if planner_pass else "FAIL")
    )

    print(
        "Campaign Analyst: "
        + ("PASS" if analyst_pass else "FAIL")
    )

    all_passed = (
        research_pass
        and planner_pass
        and analyst_pass
    )

    print()

    if all_passed:
        print("=" * 60)
        print(
            "STEP 2.11 COMPLETE - "
            "ALL THREE SPECIALIST WORKFLOWS PASSED"
        )
        print("=" * 60)
    else:
        print("=" * 60)
        print(
            "STEP 2.11 FAILED - "
            "ONE OR MORE SPECIALIST WORKFLOWS FAILED"
        )
        print("=" * 60)

        raise SystemExit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
    