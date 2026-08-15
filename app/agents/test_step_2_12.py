from app.agents.handoff_agents import run_marketing_manager


# ============================================================
# TEST DATA
# ============================================================

MARKET_RESEARCH_REQUEST = """
I am launching an AI-powered study assistant for college students.

I need to understand:

- customer segments
- customer needs
- customer pain points
- market trends
- market opportunities
- potential market risks

Please perform market research and provide useful marketing insights.
"""


MARKETING_PLANNER_REQUEST = """
I want to launch a marketing campaign for an AI-powered study
assistant.

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
# TEST HELPER
# ============================================================

def run_test(
    test_number: int,
    name: str,
    user_request: str,
    expected_tool: str,
    expected_agent: str,
) -> bool:

    print()
    print("=" * 60)
    print(f"TEST {test_number} - {name}")
    print("=" * 60)

    print()
    print("USER REQUEST")
    print("-" * 60)
    print(user_request)

    print()
    print("RUNNING WORKFLOW")
    print("-" * 60)

    result = run_marketing_manager(user_request)

    selected_tool = result.get("selected_tool")
    last_agent = result.get("last_agent")
    final_output = result.get("final_output", "")

    print()
    print("SELECTED TOOL")
    print("-" * 60)
    print(selected_tool)

    print()
    print("LAST AGENT")
    print("-" * 60)
    print(last_agent)

    print()
    print("FINAL OUTPUT")
    print("-" * 60)
    print(final_output)

    tool_pass = selected_tool == expected_tool
    agent_pass = last_agent == expected_agent
    output_pass = bool(final_output.strip())

    print()
    print("VERIFICATION")
    print("-" * 60)

    print(
        "Selected tool:",
        "PASS" if tool_pass else "FAIL",
    )

    print(
        "Last agent:",
        "PASS" if agent_pass else "FAIL",
    )

    print(
        "Final output:",
        "PASS" if output_pass else "FAIL",
    )

    passed = (
        tool_pass
        and agent_pass
        and output_pass
    )

    print()
    print(
        f"TEST {test_number}: "
        f"{'PASS' if passed else 'FAIL'}"
    )

    return passed


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("STEP 2.12 - THREE SPECIALIST UNIFIED WORKFLOW TEST")
    print("=" * 60)

    print()
    print("Using Groq SDK")
    print("Model: llama-3.3-70b-versatile")

    results = []

    # ========================================================
    # TEST 1
    # ========================================================

    results.append(
        run_test(
            test_number=1,
            name="MARKET RESEARCH",
            user_request=MARKET_RESEARCH_REQUEST,
            expected_tool="transfer_to_market_research",
            expected_agent="Market Research",
        )
    )

    # ========================================================
    # TEST 2
    # ========================================================

    results.append(
        run_test(
            test_number=2,
            name="MARKETING PLANNER",
            user_request=MARKETING_PLANNER_REQUEST,
            expected_tool="transfer_to_marketing_planner",
            expected_agent="Marketing Planner",
        )
    )

    # ========================================================
    # TEST 3
    # ========================================================

    results.append(
        run_test(
            test_number=3,
            name="CAMPAIGN ANALYST",
            user_request=CAMPAIGN_ANALYST_REQUEST,
            expected_tool="transfer_to_campaign_analyst",
            expected_agent="Campaign Analyst",
        )
    )

    # ========================================================
    # FINAL VERIFICATION
    # ========================================================

    print()
    print("=" * 60)
    print("STEP 2.12 VERIFICATION")
    print("=" * 60)

    print(
        "Market Research:",
        "PASS" if results[0] else "FAIL",
    )

    print(
        "Marketing Planner:",
        "PASS" if results[1] else "FAIL",
    )

    print(
        "Campaign Analyst:",
        "PASS" if results[2] else "FAIL",
    )

    all_passed = all(results)

    print()

    if all_passed:
        print("=" * 60)
        print("STEP 2.12 COMPLETE - ALL TESTS PASSED")
        print("=" * 60)
    else:
        print("=" * 60)
        print("STEP 2.12 FAILED - CHECK THE FAILED TEST")
        print("=" * 60)

        raise SystemExit(1)


if __name__ == "__main__":
    main()