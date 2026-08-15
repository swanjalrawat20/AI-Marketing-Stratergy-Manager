import csv
import json
import os
from typing import Any

from agents import function_tool


# ============================================================
# HELPERS
# ============================================================

def _normalize_column_name(name: str) -> str:
    """
    Normalize CSV column names so different naming styles work.

    Examples:
        "Ad Spend" -> "ad_spend"
        "Signups" -> "signups"
        "Conversion Rate" -> "conversion_rate"
    """
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def _to_float(value: Any) -> float:
    """
    Safely convert a value to float.
    """
    if value is None:
        return 0.0

    text = str(value).strip()

    if not text:
        return 0.0

    # Remove common currency / formatting characters.
    text = (
        text
        .replace("₹", "")
        .replace("$", "")
        .replace(",", "")
        .replace("%", "")
    )

    try:
        return float(text)
    except ValueError:
        return 0.0


def _find_column(row: dict, possible_names: list[str]):
    """
    Find the first matching normalized column.
    """
    for name in possible_names:
        normalized = _normalize_column_name(name)

        if normalized in row:
            return normalized

    return None


# ============================================================
# LOAD CSV
# ============================================================

def load_campaign_data(file_path: str) -> dict:
    """
    Read campaign performance CSV and calculate actual metrics.

    Supported concepts include:

    channel
    spend
    visits
    clicks
    impressions
    signups
    conversions
    revenue
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Campaign data file not found: {file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(
                "Campaign CSV does not contain a header row."
            )

        rows = []

        for raw_row in reader:

            normalized_row = {}

            for key, value in raw_row.items():

                if key is None:
                    continue

                normalized_row[
                    _normalize_column_name(key)
                ] = value

            rows.append(normalized_row)

    if not rows:
        raise ValueError(
            "Campaign CSV contains no data rows."
        )

    # --------------------------------------------------------
    # Detect columns
    # --------------------------------------------------------

    channel_column = _find_column(
        rows[0],
        [
            "channel",
            "marketing_channel",
            "source",
            "platform",
        ],
    )

    spend_column = _find_column(
        rows[0],
        [
            "spend",
            "ad_spend",
            "cost",
            "amount_spent",
            "total_spend",
        ],
    )

    visits_column = _find_column(
        rows[0],
        [
            "visits",
            "website_visits",
            "sessions",
            "traffic",
        ],
    )

    clicks_column = _find_column(
        rows[0],
        [
            "clicks",
            "ad_clicks",
        ],
    )

    impressions_column = _find_column(
        rows[0],
        [
            "impressions",
            "views",
        ],
    )

    signups_column = _find_column(
        rows[0],
        [
            "signups",
            "signup",
            "conversions",
            "conversion",
            "customers",
        ],
    )

    revenue_column = _find_column(
        rows[0],
        [
            "revenue",
            "sales",
            "income",
        ],
    )

    # --------------------------------------------------------
    # Validate essential columns
    # --------------------------------------------------------

    if spend_column is None:
        raise ValueError(
            "Campaign CSV must contain a spend/cost column."
        )

    if signups_column is None:
        raise ValueError(
            "Campaign CSV must contain a signups/conversions column."
        )

    # --------------------------------------------------------
    # Overall totals
    # --------------------------------------------------------

    total_spend = 0.0
    total_visits = 0.0
    total_clicks = 0.0
    total_impressions = 0.0
    total_signups = 0.0
    total_revenue = 0.0

    channel_metrics = {}

    for row in rows:

        channel = (
            str(row.get(channel_column, "Unknown"))
            .strip()
            if channel_column
            else "Unknown"
        )

        if not channel:
            channel = "Unknown"

        spend = _to_float(
            row.get(spend_column)
        )

        visits = (
            _to_float(row.get(visits_column))
            if visits_column
            else 0.0
        )

        clicks = (
            _to_float(row.get(clicks_column))
            if clicks_column
            else 0.0
        )

        impressions = (
            _to_float(row.get(impressions_column))
            if impressions_column
            else 0.0
        )

        signups = _to_float(
            row.get(signups_column)
        )

        revenue = (
            _to_float(row.get(revenue_column))
            if revenue_column
            else 0.0
        )

        total_spend += spend
        total_visits += visits
        total_clicks += clicks
        total_impressions += impressions
        total_signups += signups
        total_revenue += revenue

        if channel not in channel_metrics:

            channel_metrics[channel] = {
                "spend": 0.0,
                "visits": 0.0,
                "clicks": 0.0,
                "impressions": 0.0,
                "signups": 0.0,
                "revenue": 0.0,
            }

        channel_metrics[channel]["spend"] += spend
        channel_metrics[channel]["visits"] += visits
        channel_metrics[channel]["clicks"] += clicks
        channel_metrics[channel]["impressions"] += impressions
        channel_metrics[channel]["signups"] += signups
        channel_metrics[channel]["revenue"] += revenue

    # --------------------------------------------------------
    # Overall calculated metrics
    # --------------------------------------------------------

    conversion_rate = (
        total_signups / total_visits
        if total_visits > 0
        else None
    )

    cac = (
        total_spend / total_signups
        if total_signups > 0
        else None
    )

    roas = (
        total_revenue / total_spend
        if total_spend > 0 and total_revenue > 0
        else None
    )

    # --------------------------------------------------------
    # Channel-level metrics
    # --------------------------------------------------------

    channels = []

    for channel, values in channel_metrics.items():

        channel_conversion_rate = (
            values["signups"] / values["visits"]
            if values["visits"] > 0
            else None
        )

        channel_cac = (
            values["spend"] / values["signups"]
            if values["signups"] > 0
            else None
        )

        channel_roas = (
            values["revenue"] / values["spend"]
            if values["spend"] > 0
            and values["revenue"] > 0
            else None
        )

        channels.append(
            {
                "channel": channel,
                "spend": round(values["spend"], 2),
                "visits": round(values["visits"], 2),
                "clicks": round(values["clicks"], 2),
                "impressions": round(
                    values["impressions"],
                    2,
                ),
                "signups": round(values["signups"], 2),
                "conversion_rate": (
                    round(
                        channel_conversion_rate * 100,
                        2,
                    )
                    if channel_conversion_rate is not None
                    else None
                ),
                "cac": (
                    round(channel_cac, 2)
                    if channel_cac is not None
                    else None
                ),
                "revenue": round(
                    values["revenue"],
                    2,
                ),
                "roas": (
                    round(channel_roas, 2)
                    if channel_roas is not None
                    else None
                ),
            }
        )

    # --------------------------------------------------------
    # Best / worst channel
    # --------------------------------------------------------

    channels_with_cac = [
        channel
        for channel in channels
        if channel["cac"] is not None
    ]

    best_channel = None
    worst_channel = None

    if channels_with_cac:

        best_channel = min(
            channels_with_cac,
            key=lambda item: item["cac"],
        )

        worst_channel = max(
            channels_with_cac,
            key=lambda item: item["cac"],
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    result = {
        "source_file": file_path,
        "rows_processed": len(rows),

        "actual": {
            "spend": round(total_spend, 2),
            "visits": round(total_visits, 2),
            "clicks": round(total_clicks, 2),
            "impressions": round(
                total_impressions,
                2,
            ),
            "signups": round(total_signups, 2),

            "conversion_rate": (
                round(
                    conversion_rate * 100,
                    2,
                )
                if conversion_rate is not None
                else None
            ),

            "cac": (
                round(cac, 2)
                if cac is not None
                else None
            ),

            "revenue": round(
                total_revenue,
                2,
            ),

            "roas": (
                round(roas, 2)
                if roas is not None
                else None
            ),
        },

        "channel_performance": channels,

        "best_channel": best_channel,

        "worst_channel": worst_channel,
    }

    return result


# ============================================================
# AGENTS SDK TOOL
# ============================================================

@function_tool
def campaign_data_tool(file_path: str) -> str:
    """
    Read the campaign CSV and calculate actual campaign
    performance metrics.

    The Analytics & Optimization Agent should use this tool
    as the source of truth for actual campaign performance.
    """

    try:

        result = load_campaign_data(file_path)

        return json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )

    except Exception as error:

        return json.dumps(
            {
                "error": str(error),
                "source_file": file_path,
            },
            indent=2,
            ensure_ascii=False,
        )