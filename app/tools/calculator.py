from agents import function_tool


def calculate_campaign_metrics(
    budget: float,
    signup_target: int,
    campaign_days: int
):
    """Calculate campaign targets and budget metrics."""

    daily_signups = signup_target / campaign_days
    rolling_7_day_signups = daily_signups * 7
    maximum_blended_cac = budget / signup_target
    budget_per_day = budget / campaign_days
    budget_per_signup = budget / signup_target

    return {
        "daily_signups": round(daily_signups, 2),
        "rolling_7_day_signups": round(rolling_7_day_signups, 2),
        "maximum_blended_cac": round(maximum_blended_cac, 2),
        "budget_per_day": round(budget_per_day, 2),
        "budget_per_signup": round(budget_per_signup, 2),
    }


@function_tool
def campaign_metrics_tool(
    budget: float,
    signup_target: int,
    campaign_days: int
):
    """Agent tool for calculating marketing campaign metrics."""

    return calculate_campaign_metrics(
        budget=budget,
        signup_target=signup_target,
        campaign_days=campaign_days,
    )