import os

from dotenv import load_dotenv

from app.agents.handoff_agents import (
    run_marketing_manager,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


# ============================================================
# TEST 1
# ============================================================

def test_market_research():

    print()
    print("=" * 60)
    print("TEST 1 - MARKET RESEARCH ROUTING")
    print("=" * 60)

    request = """
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

    print()
    print("Groq model:", MODEL)

    print()
    print("User request:")
    print(request)

    print()
    print("-" * 60)

    result = run_marketing_manager(request)

    print()
    print("FINAL OUTPUT")
    print("-" * 60)
    print(result["final_output"])

    print()
    print("HANDOFF")
    print("-" * 60)
    print(result["handoff"])

    print()
    print("LAST AGENT")
    print("-" * 60)
    print(result["last_agent"])

    passed = (
        result["handoff"]
        == "transfer_to_market_research"
        and
        result["last_agent"]
        == "Market Research"
    )

    print()
    print(
        "TEST 1:",
        "PASS" if passed else "FAIL",
    )

    return passed


# ============================================================
# TEST 2
# ============================================================

def test_marketing_planner():

    print()
    print("=" * 60)
    print("TEST 2 - MARKETING PLANNER ROUTING")
    print("=" * 60)

    request = """
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
"""

    print()
    print("Groq model:", MODEL)

    print()
    print("User request:")
    print(request)

    print()
    print("-" * 60)

    result = run_marketing_manager(request)

    print()
    print("FINAL OUTPUT")
    print("-" * 60)
    print(result["final_output"])

    print()
    print("HANDOFF")
    print("-" * 60)
    print(result["handoff"])

    print()
    print("LAST AGENT")
    print("-" * 60)
    print(result["last_agent"])

    passed = (
        result["handoff"]
        == "transfer_to_marketing_planner"
        and
        result["last_agent"]
        == "Marketing Planner"
    )

    print()
    print(
        "TEST 2:",
        "PASS" if passed else "FAIL",
    )

    return passed


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("STEP 2.7 - GROQ NATIVE SPECIALIST ROUTING TEST")
    print("=" * 60)

    print()
    print("Using Groq SDK")
    print("Model:", MODEL)

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    research_pass = test_market_research()

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    planner_pass = test_marketing_planner()

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("STEP 2.7 VERIFICATION")
    print("=" * 60)

    print()
    print(
        "Market Research routing:",
        "PASS" if research_pass else "FAIL",
    )

    print(
        "Marketing Planner routing:",
        "PASS" if planner_pass else "FAIL",
    )

    print()

    if research_pass and planner_pass:

        print("=" * 60)
        print("STEP 2.7 COMPLETE - ALL ROUTING TESTS PASSED")
        print("=" * 60)

    else:

        print("=" * 60)
        print("STEP 2.7 FAILED")
        print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()