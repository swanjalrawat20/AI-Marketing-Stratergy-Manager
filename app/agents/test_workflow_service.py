from app.services.marketing_workflow import run_marketing_workflow
import os
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


# ============================================================
# TEST REQUEST
# ============================================================

USER_REQUEST = """
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
# MAIN TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("STEP 2.9 - MARKETING WORKFLOW SERVICE TEST")
    print("=" * 60)

    print()
    print("Using Groq SDK")
    print(f"Model: {GROQ_MODEL}")

    print()
    print("USER REQUEST")
    print("-" * 60)
    print(USER_REQUEST)

    print()
    print("RUNNING WORKFLOW")
    print("-" * 60)

    result = run_marketing_workflow(USER_REQUEST)

    # ========================================================
    # RESULT VALIDATION
    # ========================================================

    if not isinstance(result, dict):
        raise TypeError(
            "run_marketing_workflow() must return a dictionary."
        )

    # ========================================================
    # SELECTED TOOL
    # ========================================================

    print()
    print("SELECTED TOOL")
    print("-" * 60)

    selected_tool = result.get(
        "selected_tool",
        result.get("handoff"),
    )

    print(selected_tool)

    # ========================================================
    # LAST AGENT
    # ========================================================

    print()
    print("LAST AGENT")
    print("-" * 60)

    last_agent = result.get(
        "last_agent",
        "Unknown",
    )

    print(last_agent)

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print()
    print("FINAL OUTPUT")
    print("-" * 60)

    final_output = result.get(
        "final_output",
        "",
    )

    print(final_output)

    # ========================================================
    # VERIFICATION
    # ========================================================

    print()
    print("=" * 60)
    print("STEP 2.9 VERIFICATION")
    print("=" * 60)

    expected_tool = "transfer_to_marketing_planner"
    expected_agent = "Marketing Planner"

    routing_pass = selected_tool == expected_tool
    agent_pass = last_agent == expected_agent
    output_pass = bool(final_output.strip())

    print()
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

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()

    if routing_pass and agent_pass and output_pass:

        print("=" * 60)
        print("STEP 2.9 COMPLETE - WORKFLOW SERVICE TEST PASSED")
        print("=" * 60)

    else:

        print("=" * 60)
        print("STEP 2.9 FAILED")
        print("=" * 60)

        print()
        print("Expected tool:")
        print(expected_tool)

        print()
        print("Actual tool:")
        print(selected_tool)

        print()
        print("Expected agent:")
        print(expected_agent)

        print()
        print("Actual agent:")
        print(last_agent)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()