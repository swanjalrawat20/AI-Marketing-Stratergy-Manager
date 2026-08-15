import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from app.agents.handoff_agents import run_marketing_manager


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = Groq(
    api_key=GROQ_API_KEY,
)


# ============================================================
# MARKETING WORKFLOW
# ============================================================

def run_marketing_workflow(
    user_request: str,
) -> dict[str, Any]:
    """
    Public service entry point for the marketing workflow.

    The workflow uses the Groq SDK and delegates routing to
    the Marketing Manager.

    The Marketing Manager selects either:

    - Marketing Planner
    - Market Research

    The selected specialist then executes the request.
    """

    if not user_request or not user_request.strip():
        raise ValueError("user_request cannot be empty")

    result = run_marketing_manager(user_request)

    return {
        "user_request": user_request,
        "handoff": result.get("handoff"),
        "last_agent": result.get("last_agent"),
        "final_output": result.get("final_output", ""),
    }


# ============================================================
# SIMPLE WORKFLOW TEST
# ============================================================

if __name__ == "__main__":

    test_request = """
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

    print()
    print("=" * 60)
    print("GROQ NATIVE MARKETING WORKFLOW TEST")
    print("=" * 60)
    print()
    print("Using Groq SDK")
    print(f"Model: {GROQ_MODEL}")

    print()
    print("=" * 60)
    print("USER REQUEST")
    print("=" * 60)
    print()
    print(test_request)

    result = run_marketing_workflow(test_request)

    print()
    print("=" * 60)
    print("MARKETING MANAGER ROUTING")
    print("=" * 60)
    print()

    print("HANDOFF:")
    print(result["handoff"])

    print()
    print("LAST AGENT:")
    print(result["last_agent"])

    print()
    print("=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print()

    print(result["final_output"])

    print()
    print("=" * 60)
    print("WORKFLOW TEST COMPLETE")
    print("=" * 60)