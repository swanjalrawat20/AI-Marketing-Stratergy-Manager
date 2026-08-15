import json
import os
import re
from typing import Any, Callable

from dotenv import load_dotenv
from groq import Groq, RateLimitError


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

# Low-token mode is intended for integration tests.
#
# PowerShell:
#   $env:LOW_TOKEN_MODE="1"
#   python -m app.agents.test_step_2_13
#
# Normal mode:
#   Remove the variable or set it to 0.
LOW_TOKEN_MODE = os.getenv("LOW_TOKEN_MODE", "0").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

# Keep outputs short during integration testing.
ROUTER_MAX_TOKENS = int(
    os.getenv(
        "GROQ_ROUTER_MAX_TOKENS",
        "120" if LOW_TOKEN_MODE else "300",
    )
)

SPECIALIST_MAX_TOKENS = int(
    os.getenv(
        "GROQ_SPECIALIST_MAX_TOKENS",
        "350" if LOW_TOKEN_MODE else "900",
    )
)


# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# 429 / RATE-LIMIT HELPERS
# ============================================================

def _rate_limit_message(error: Exception) -> str:
    """Return a concise, useful message for a Groq 429."""
    text = str(error)

    wait_match = re.search(
        r"try again in\s+([^.]*)",
        text,
        flags=re.IGNORECASE,
    )

    wait_text = (
        wait_match.group(1).strip()
        if wait_match
        else "after the Groq rate-limit window resets"
    )

    return (
        "Groq rate limit reached. "
        f"Please try again {wait_text}. "
        "The workflow itself was routed successfully, but "
        "the specialist response could not be generated."
    )


def _is_rate_limit_error(error: Exception) -> bool:
    return isinstance(error, RateLimitError) or (
        "rate limit" in str(error).lower()
        or "rate_limit_exceeded" in str(error).lower()
        or "429" in str(error)
    )


# ============================================================
# LOCAL ROUTING FALLBACK
# ============================================================

def _local_route(user_request: str) -> str:
    """
    Deterministic fallback used only when the Groq router itself
    is rate-limited.

    This does NOT replace the Groq router during normal operation.
    It simply prevents a daily TPD 429 from destroying the entire
    integration test.
    """
    text = user_request.lower()

    # Most specific routes first.
    analytics_terms = [
        "campaign performance",
        "performance",
        "cost per signup",
        "cost per acquisition",
        "cpa",
        "kpi",
        "underperformance",
        "optimiz",
        "a/b test",
        "ab test",
        "next actions",
        "which channels performed",
    ]

    content_terms = [
        "content strategy",
        "social media ideas",
        "reel",
        "video concepts",
        "ad concepts",
        "email ideas",
        "blog topics",
        "ctas",
        "calls to action",
    ]

    competitor_terms = [
        "competitor",
        "competitors",
        "competitive landscape",
        "competitor analysis",
        "differentiate",
        "market gaps",
        "competitor pricing",
    ]

    research_terms = [
        "market research",
        "customer segments",
        "customer needs",
        "pain points",
        "market trends",
        "market opportunities",
        "market risks",
    ]

    campaign_terms = [
        "campaign execution",
        "campaign phases",
        "campaign timeline",
        "channel strategy",
        "budget allocation",
        "campaign kpis",
        "campaign risks",
        "campaign optimization",
        "actionable campaign",
    ]

    # High-confidence campaign-performance requests belong to the
    # Analytics & Optimization specialist. This must be checked before
    # generic marketing-planner fallback.
    analytics_strong_terms = [
        "analyze campaign performance",
        "analyze my marketing campaign",
        "campaign performance",
        "cost per signup",
        "cost per acquisition",
        "channel performance",
        "areas of underperformance",
        "optimization opportunities",
        "a/b testing",
        "next actions",
    ]

    if any(term in text for term in analytics_strong_terms):
        return "transfer_to_analytics_optimizer"

    # Detailed campaign-execution requests must win over generic
    # optimization/KPI words. A campaign plan can legitimately
    # contain KPIs, optimization, risks, and next steps, but it is
    # still owned by the Campaign Planner.
    campaign_execution_strong_terms = [
        "campaign execution plan",
        "build a campaign",
        "build a campaign plan",
        "create a campaign",
        "create a campaign plan",
        "campaign phases",
        "campaign timeline",
        "campaign execution",
        "actionable campaign",
    ]

    if any(term in text for term in campaign_execution_strong_terms):
        return "transfer_to_campaign_planner"

    if any(term in text for term in content_terms):
        return "transfer_to_content_strategist"

    if any(term in text for term in competitor_terms):
        return "transfer_to_competitor_analysis"

    if any(term in text for term in research_terms):
        return "transfer_to_market_research"

    # Campaign planning is checked after the strong campaign guard
    # above, but before the generic marketing-planner fallback.
    if any(term in text for term in campaign_terms):
        return "transfer_to_campaign_planner"

    return "transfer_to_marketing_planner"


# ============================================================
# COMMON SPECIALIST RUNNER
# ============================================================

def _run_specialist(
    specialist_name: str,
    instructions: str,
    user_request: str,
) -> str:
    """Run one specialist using the Groq SDK with 429 handling."""

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
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

        return response.choices[0].message.content or ""

    except Exception as error:
        if _is_rate_limit_error(error):
            return (
                f"[{specialist_name}] "
                f"{_rate_limit_message(error)}"
            )

        # Do not hide non-429 programming/API errors.
        raise


# ============================================================
# SPECIALIST 1: MARKETING PLANNER
# ============================================================

def marketing_planner(user_request: str) -> str:
    return _run_specialist(
        "Marketing Planner",
        """
You are the Marketing Planner specialist.

Create a practical marketing plan from the user's requirements.

Focus on:
1. Campaign objective
2. Target audience
3. Budget allocation
4. Marketing channels
5. Campaign strategy
6. KPIs
7. Timeline when provided

Rules:
- Use only requirements provided by the user.
- Do not invent deadlines, budgets, goals, or constraints.
- If something is not specified, say that it was not specified.
- Keep the plan practical and concise.
- Do not perform detailed competitor analysis.
- Do not perform campaign performance analysis.
""",
        user_request,
    )


# ============================================================
# SPECIALIST 2: MARKET RESEARCH
# ============================================================

def market_research(user_request: str) -> str:
    return _run_specialist(
        "Market Research",
        """
You are the Market Research specialist.

Analyze the user's marketing requirements.

Focus on:
1. Target customer segments
2. Customer needs
3. Customer pain points
4. Market trends
5. Market opportunities
6. Potential market risks
7. Recommended marketing opportunities

Rules:
- Base the analysis on the user's request.
- Do not invent precise statistics.
- Do not invent research sources.
- Clearly distinguish qualitative analysis from verified facts.
- If information is missing, say that it was not provided.
- Provide practical marketing insights.
- Do not create a detailed campaign plan unless requested.
""",
        user_request,
    )


# ============================================================
# SPECIALIST 3: COMPETITOR ANALYSIS
# ============================================================

def competitor_analysis(user_request: str) -> str:
    return _run_specialist(
        "Competitor Analysis",
        """
You are the Competitor Analysis specialist.

Analyze the competitive landscape relevant to the user's
product, service, market, or campaign.

Focus on:
1. Direct competitors
2. Indirect competitors
3. Competitor offerings
4. Competitor strengths
5. Competitor weaknesses
6. Pricing or offer information when supplied or known
7. Market positioning
8. Customer expectations
9. Market gaps
10. Differentiation opportunities
11. Recommended positioning

Rules:
- Do not invent precise competitor statistics.
- Do not claim a price is current unless the user supplied it
  or it is clearly presented as an assumption.
- Clearly distinguish known information from assumptions.
- If competitor information is insufficient, say so.
- Do not create the campaign plan itself.
""",
        user_request,
    )


# ============================================================
# SPECIALIST 4: CAMPAIGN PLANNER
# ============================================================

def campaign_planner(user_request: str) -> str:
    return _run_specialist(
        "Campaign Planner",
        """
You are the Campaign Planner specialist.

Turn the user's marketing requirements into an actionable
campaign execution plan.

Focus on:
1. Campaign objective
2. Target audience segments
3. Marketing channels
4. Budget allocation
5. Campaign phases
6. Key messages
7. KPIs
8. Timeline
9. Optimization strategy
10. Campaign risks
11. Expected results

Rules:
- Use only the budget and goals supplied by the user.
- Do not invent a budget when none is supplied.
- If budget allocation is proposed, make sure it does not
  exceed the supplied total budget.
- Do not invent guaranteed results.
- Clearly label assumptions.
""",
        user_request,
    )


# ============================================================
# SPECIALIST 5: CONTENT STRATEGIST
# ============================================================

def content_strategist(user_request: str) -> str:
    return _run_specialist(
        "Content Strategist",
        """
You are the Content Strategist specialist.

Create practical marketing content based on the user's
product, audience, campaign, and positioning.

Focus on:
1. Core campaign message
2. Social media post ideas
3. Short-form video/Reel concepts
4. Paid advertisement concepts
5. Email campaign ideas
6. Blog/content topics
7. Calls to action
8. Content themes

Rules:
- Keep the target audience in mind.
- Address real customer pain points from the request.
- Communicate product value clearly.
- Do not make unsupported performance claims.
- Keep ideas practical and ready to use.
- If campaign details are missing, state the assumptions used.
""",
        user_request,
    )


# ============================================================
# SPECIALIST 6: ANALYTICS & OPTIMIZATION
# ============================================================

def analytics_optimizer(user_request: str) -> str:
    return _run_specialist(
        "Analytics & Optimization",
        """
You are the Analytics & Optimization specialist.

Analyze the user's marketing campaign performance or
optimization request.

Focus on:
1. Campaign performance
2. KPIs
3. Cost per signup/acquisition when possible
4. Conversion performance
5. Channel performance
6. Areas of underperformance
7. Optimization opportunities
8. Recommended next actions
9. A/B testing
10. Budget optimization

Critical rules:
- Calculate metrics only when enough information is provided.
- Never invent channel-level data.
- Never invent impressions, clicks, visits, revenue, CAC,
  conversion rates, or ROI.
- If channel-level data is missing, clearly state that
  channel performance cannot be determined.
- If revenue is missing, do not calculate ROAS.
- Clearly distinguish calculated metrics from recommendations.
- If actual campaign data is unavailable, explain what data
  is needed for deeper analysis.
""",
        user_request,
    )


# ============================================================
# HANDOFF TOOL DEFINITIONS
# ============================================================

def _handoff_tool(name: str, description: str) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    "user_request": {
                        "type": "string",
                        "description": "The complete original user request.",
                    }
                },
                "required": ["user_request"],
                "additionalProperties": False,
            },
        },
    }


MARKETING_PLANNER_TOOL = _handoff_tool(
    "transfer_to_marketing_planner",
    "Transfer to Marketing Planner for campaign objectives, "
    "target audience, budget allocation, channels, strategy, "
    "KPIs, and planning.",
)

MARKET_RESEARCH_TOOL = _handoff_tool(
    "transfer_to_market_research",
    "Transfer to Market Research for customer segments, "
    "customer needs, pain points, market trends, opportunities, "
    "risks, and market insights.",
)

COMPETITOR_ANALYSIS_TOOL = _handoff_tool(
    "transfer_to_competitor_analysis",
    "Transfer to Competitor Analysis for direct and indirect "
    "competitors, competitor strengths, weaknesses, positioning, "
    "market gaps, and differentiation opportunities.",
)

CAMPAIGN_PLANNER_TOOL = _handoff_tool(
    "transfer_to_campaign_planner",
    "Transfer to Campaign Planner for an actionable campaign "
    "including channels, budget allocation, phases, KPIs, "
    "timeline, messaging, risks, and optimization.",
)

CONTENT_STRATEGIST_TOOL = _handoff_tool(
    "transfer_to_content_strategist",
    "Transfer to Content Strategist for campaign messaging, "
    "social posts, short-form videos, advertisements, emails, "
    "content topics, and CTAs.",
)

ANALYTICS_OPTIMIZER_TOOL = _handoff_tool(
    "transfer_to_analytics_optimizer",
    "Transfer to Analytics and Optimization for campaign "
    "performance, KPIs, acquisition cost, channel analysis, "
    "underperformance, optimization, testing, and next actions.",
)


# ============================================================
# ALL SIX ROUTING TOOLS
# ============================================================

ROUTING_TOOLS = [
    MARKETING_PLANNER_TOOL,
    MARKET_RESEARCH_TOOL,
    COMPETITOR_ANALYSIS_TOOL,
    CAMPAIGN_PLANNER_TOOL,
    CONTENT_STRATEGIST_TOOL,
    ANALYTICS_OPTIMIZER_TOOL,
]


# ============================================================
# SPECIALIST MAP
# ============================================================

SPECIALIST_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "transfer_to_marketing_planner": marketing_planner,
    "transfer_to_market_research": market_research,
    "transfer_to_competitor_analysis": competitor_analysis,
    "transfer_to_campaign_planner": campaign_planner,
    "transfer_to_content_strategist": content_strategist,
    "transfer_to_analytics_optimizer": analytics_optimizer,
}


SPECIALIST_NAMES: dict[str, str] = {
    "transfer_to_marketing_planner": "Marketing Planner",
    "transfer_to_market_research": "Market Research",
    "transfer_to_competitor_analysis": "Competitor Analysis",
    "transfer_to_campaign_planner": "Campaign Planner",
    "transfer_to_content_strategist": "Content Strategist",
    "transfer_to_analytics_optimizer": "Analytics & Optimization",
}


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_handoff_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> str:
    user_request = arguments.get("user_request", "")

    if not user_request:
        return "Error: user_request was not provided."

    specialist = SPECIALIST_FUNCTIONS.get(tool_name)

    if specialist is None:
        return f"Error: unknown handoff tool: {tool_name}"

    return specialist(user_request)


# ============================================================
# MARKETING MANAGER
# ============================================================

def run_marketing_manager(user_request: str) -> dict[str, Any]:
    """
    Full six-agent unified handoff workflow.

    The Marketing Manager routes the request to exactly one
    of six specialist agents.

    429 handling:
    - If the Groq router is rate-limited, use a deterministic
      local routing fallback.
    - If the specialist is rate-limited, return a readable
      fallback message instead of crashing.

    This is especially useful when Groq's daily TPD quota has
    been exhausted during integration testing.
    """

    if not user_request or not user_request.strip():
        raise ValueError("user_request cannot be empty")

    messages = [
        {
            "role": "system",
            "content": """
You are the Marketing Manager and workflow router.

Your ONLY job is to identify which one specialist should
handle the user's request and transfer the complete original
request to that specialist.

AVAILABLE SPECIALISTS
=====================

1. MARKETING PLANNER
Use for:
- high-level marketing plans
- campaign objectives
- target audience
- budget planning
- marketing direction
- general marketing strategy

2. MARKET RESEARCH
Use for:
- customer segments
- customer needs
- customer pain points
- market trends
- market opportunities
- market risks
- market research

3. COMPETITOR ANALYSIS
Use for:
- competitors
- competitor comparison
- competitor strengths/weaknesses
- competitor pricing/offers
- market positioning
- market gaps
- differentiation

4. CAMPAIGN PLANNER
Use for:
- executable campaign planning
- channel strategy
- detailed budget allocation
- campaign phases
- campaign timeline
- KPIs
- campaign messaging
- campaign execution

5. CONTENT STRATEGIST
Use for:
- social media content
- ad concepts
- email campaigns
- blog topics
- content calendars
- campaign messaging
- video/Reel ideas
- CTAs

6. ANALYTICS & OPTIMIZATION
Use for:
- campaign performance
- KPIs and metrics
- cost per signup/acquisition
- conversion performance
- channel performance
- underperformance
- optimization
- A/B testing
- recommended next actions
- campaign improvement

ROUTING RULES
=============

- Use exactly ONE handoff tool.
- Pass the COMPLETE original user request.
- Do not perform specialist work yourself.
- Do not answer the user's request directly.
- Route immediately.
- Do not call multiple specialists.
- Prefer the most specific specialist when multiple categories
  appear in the request.
- For actual performance/optimization questions, use
  Analytics & Optimization.
- For detailed campaign execution plans, use Campaign Planner.
- For general/high-level campaign plans, use Marketing Planner.
""",
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=ROUTING_TOOLS,
            tool_choice="required",
            temperature=0.0,
            max_tokens=ROUTER_MAX_TOKENS,
        )

    except Exception as error:
        if _is_rate_limit_error(error):
            # The router cannot make a Groq request, so use the
            # local deterministic router for this run.
            tool_name = _local_route(user_request)

            specialist_output = execute_handoff_tool(
                tool_name,
                {"user_request": user_request},
            )

            return {
                "selected_tool": tool_name,
                "last_agent": SPECIALIST_NAMES.get(
                    tool_name,
                    "Marketing Manager",
                ),
                "final_output": specialist_output,
                "handoff": tool_name,
                "router_fallback": True,
                "rate_limited": True,
            }

        raise

    message = response.choices[0].message

    if not message.tool_calls:
        # Normally impossible because tool_choice="required".
        # Keep this safe fallback for unexpected SDK/model behavior.
        tool_name = _local_route(user_request)

        return {
            "selected_tool": tool_name,
            "last_agent": SPECIALIST_NAMES.get(
                tool_name,
                "Marketing Manager",
            ),
            "final_output": (
                "Router returned no tool call. "
                "A local routing fallback selected the specialist."
            ),
            "handoff": tool_name,
            "router_fallback": True,
            "rate_limited": False,
        }

    # The router is instructed to call exactly one tool.
    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name

    # Protect against an unexpected tool name.
    if tool_name not in SPECIALIST_FUNCTIONS:
        tool_name = _local_route(user_request)

    try:
        arguments = json.loads(
            tool_call.function.arguments or "{}"
        )
    except json.JSONDecodeError:
        arguments = {
            "user_request": user_request,
        }

    # Always preserve the original request.
    if not arguments.get("user_request"):
        arguments["user_request"] = user_request

    specialist_output = execute_handoff_tool(
        tool_name,
        arguments,
    )

    return {
        "selected_tool": tool_name,
        "last_agent": SPECIALIST_NAMES.get(
            tool_name,
            "Marketing Manager",
        ),
        "final_output": specialist_output,
        "handoff": tool_name,
        "router_fallback": False,
        "rate_limited": (
            specialist_output.startswith("[")
            and "rate limit reached" in specialist_output.lower()
        ),
    }


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":
    test_request = """
I want to analyze my marketing campaign performance.

I spent ₹50,000 and received 1,000 signups.

Tell me the campaign performance,
cost per signup,
channel performance,
optimization opportunities,
and recommended next actions.
"""

    result = run_marketing_manager(test_request)

    print("=" * 60)
    print("STEP 2.13 - FULL SIX-AGENT HANDOFF WORKFLOW")
    print("=" * 60)
    print()
    print("LOW TOKEN MODE:")
    print(LOW_TOKEN_MODE)
    print()
    print("SELECTED TOOL:")
    print(result["selected_tool"])
    print()
    print("LAST AGENT:")
    print(result["last_agent"])
    print()
    print("FINAL OUTPUT:")
    print("-" * 60)
    print(result["final_output"])