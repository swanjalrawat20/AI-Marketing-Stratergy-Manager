# ============================================================
# STEP 2.10 - UNIFIED GROQ WORKFLOW TEST
# ============================================================

from app.services.marketing_workflow import run_marketing_workflow


# ============================================================
# TEST 1 - MARKET RESEARCH
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


# ============================================================
# TEST 2 - MARKETING PLANNER
# ============================================================

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


# ============================================================
# HELPER
# ============================================================

def print_result(result):
    """
    Print the workflow result regardless of whether
    the service returns a dict or an object.
    """

    if isinstance(result, dict):
        selected_tool = result.get("selected_tool")
        last_agent = result.get("last_agent")
        final_output = result.get("final_output", "")
        handoff = result.get("handoff")
    else:
        selected_tool = getattr(result, "selected_tool", None)
        last_agent = getattr(result, "last_agent", None)
        final_output = getattr(result, "final_output", "")
        handoff = getattr(result, "handoff", None)

    print()
    print("SELECTED TOOL")
    print("-" * 60)
    print(selected_tool)

    print()
    print("HANDOFF")
    print("-" * 60)
    print(handoff)

    print()
    print("LAST AGENT")
    print("-" * 60)
    print(last_agent)

    print()
    print("FINAL OUTPUT")
    print("-" * 60)
    print(final_output)

    return selected_tool, last_agent, final_output, handoff


# ============================================================
# TEST 1
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

    result = run_marketing_workflow(
        MARKET_RESEARCH_REQUEST
    )

    selected_tool, last_agent, final_output, handoff = (
        print_result(result)
    )

    expected_tool = "transfer_to_market_research"
    expected_agent = "Market Research"

    routing_pass = (
        selected_tool == expected_tool
        or handoff == expected_tool
    )

    agent_pass = last_agent == expected_agent

    output_pass = bool(final_output and final_output.strip())

    print()
    print("VERIFICATION")
    print("-" * 60)

    print(
        f"Selected tool: "
        f"{'PASS' if routing_pass else 'FAIL'}"
    )

    print(
        f"Last agent: "
        f"{'PASS' if agent_pass else 'FAIL'}"
    )

    print(
        f"Final output: "
        f"{'PASS' if output_pass else 'FAIL'}"
    )

    passed = (
        routing_pass
        and agent_pass
        and output_pass
    )

    print()
    print(
        "TEST 1: "
        + ("PASS" if passed else "FAIL")
    )

    return passed


# ============================================================
# TEST 2
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

    result = run_marketing_workflow(
        MARKETING_PLANNER_REQUEST
    )

    selected_tool, last_agent, final_output, handoff = (
        print_result(result)
    )

    expected_tool = "transfer_to_marketing_planner"
    expected_agent = "Marketing Planner"

    routing_pass = (
        selected_tool == expected_tool
        or handoff == expected_tool
    )

    agent_pass = last_agent == expected_agent

    output_pass = bool(final_output and final_output.strip())

    print()
    print("VERIFICATION")
    print("-" * 60)

    print(
        f"Selected tool: "
        f"{'PASS' if routing_pass else 'FAIL'}"
    )

    print(
        f"Last agent: "
        f"{'PASS' if agent_pass else 'FAIL'}"
    )

    print(
        f"Final output: "
        f"{'PASS' if output_pass else 'FAIL'}"
    )

    passed = (
        routing_pass
        and agent_pass
        and output_pass
    )

    print()
    print(
        "TEST 2: "
        + ("PASS" if passed else "FAIL")
    )

    return passed


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("=" * 60)
    print("STEP 2.10 - UNIFIED GROQ WORKFLOW TEST")
    print("=" * 60)

    print()
    print("Using Groq SDK")
    print("Model: llama-3.3-70b-versatile")

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    research_passed = test_market_research()

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    planner_passed = test_marketing_planner()

    # --------------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("STEP 2.10 VERIFICATION")
    print("=" * 60)

    print(
        f"Market Research workflow: "
        f"{'PASS' if research_passed else 'FAIL'}"
    )

    print(
        f"Marketing Planner workflow: "
        f"{'PASS' if planner_passed else 'FAIL'}"
    )

    all_passed = (
        research_passed
        and planner_passed
    )

    print()

    if all_passed:
        print("=" * 60)
        print("STEP 2.10 COMPLETE - ALL UNIFIED WORKFLOW TESTS PASSED")
        print("=" * 60)
    else:
        print("=" * 60)
        print("STEP 2.10 FAILED - WORKFLOW NEEDS FIXING")
        print("=" * 60)

        raise SystemExit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()