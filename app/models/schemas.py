from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# ============================================================
# COMMON CONFIG
# ============================================================

class StrictBaseModel(BaseModel):
    """
    Base model for all structured outputs.

    extra="forbid" prevents the model from silently returning
    fields that were not defined in the schema.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


# ============================================================
# 1. MARKETING PLANNER
# ============================================================

class MarketingPlanOutput(StrictBaseModel):
    """Structured high-level plan produced by the Marketing Planner."""

    product_or_service: str = Field(
        min_length=1,
        description="Product or service being marketed.",
    )

    target_audience: str = Field(
        min_length=1,
        description="Primary target audience.",
    )

    marketing_goal: str = Field(
        min_length=1,
        description="Primary measurable marketing goal.",
    )

    budget: float = Field(
        ge=0,
        description="Total marketing budget.",
    )

    timeline_days: int = Field(
        gt=0,
        description="Campaign duration in days.",
    )

    recommended_marketing_direction: list[str] = Field(
        min_length=1,
        description="Recommended strategic marketing directions.",
    )


# ============================================================
# 2. MARKET RESEARCH
# ============================================================

class MarketResearchOutput(StrictBaseModel):
    """Structured market research findings."""

    target_segments: list[str] = Field(
        min_length=1,
        description="Relevant target market segments.",
    )

    customer_needs: list[str] = Field(
        min_length=1,
        description="Important customer needs.",
    )

    pain_points: list[str] = Field(
        min_length=1,
        description="Major customer pain points.",
    )

    market_trends: list[str] = Field(
        default_factory=list,
        description="Relevant market trends.",
    )

    opportunities: list[str] = Field(
        min_length=1,
        description="Potential market opportunities.",
    )

    challenges: list[str] = Field(
        min_length=1,
        description="Potential market challenges.",
    )

    recommended_approach: list[str] = Field(
        min_length=1,
        description="Recommended approach based on research.",
    )

    assumptions: list[str] = Field(
        default_factory=list,
        description="Assumptions made when research data is unavailable.",
    )

    sources: list[str] = Field(
        default_factory=list,
        description="URLs or source descriptions when research sources are available.",
    )


# ============================================================
# 3. COMPETITOR ANALYSIS
# ============================================================

class CompetitorProfile(StrictBaseModel):
    """One competitor or competitor category."""

    name: str = Field(
        min_length=1,
        description="Competitor name.",
    )

    competitor_type: str = Field(
        min_length=1,
        description="Direct, indirect, or category competitor.",
    )

    offering: str = Field(
        default="",
        description="Main product/service offering.",
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Competitor strengths.",
    )

    weaknesses: list[str] = Field(
        default_factory=list,
        description="Competitor weaknesses.",
    )

    pricing_or_offer: Optional[str] = Field(
        default=None,
        description="Known pricing, subscription, or offer information.",
    )


class CompetitorAnalysisOutput(StrictBaseModel):
    """Structured competitor analysis."""

    competitors: list[CompetitorProfile] = Field(
        min_length=1,
        description="Identified competitors.",
    )

    customer_expectations: list[str] = Field(
        default_factory=list,
        description="Customer expectations inferred from the competitive landscape.",
    )

    market_gaps: list[str] = Field(
        default_factory=list,
        description="Potential gaps in the existing market.",
    )

    differentiation_opportunities: list[str] = Field(
        min_length=1,
        description="Ways the product can differentiate itself.",
    )

    recommended_positioning: str = Field(
        min_length=1,
        description="Recommended market positioning.",
    )

    assumptions: list[str] = Field(
        default_factory=list,
        description="Assumptions made where competitor information is incomplete.",
    )

    sources: list[str] = Field(
        default_factory=list,
        description="URLs or source descriptions used for competitor analysis.",
    )


# ============================================================
# 4. CAMPAIGN PLANNER
# ============================================================

class ChannelBudget(StrictBaseModel):
    """Budget assigned to one marketing channel."""

    channel: str = Field(
        min_length=1,
        description="Marketing channel.",
    )

    budget: float = Field(
        ge=0,
        description="Budget allocated to this channel.",
    )

    rationale: str = Field(
        default="",
        description="Reason for allocating this amount to the channel.",
    )


class CampaignPhase(StrictBaseModel):
    """One phase of the campaign timeline."""

    phase: str = Field(
        min_length=1,
        description="Campaign phase name.",
    )

    days: str = Field(
        min_length=1,
        description="Days covered by this campaign phase.",
    )

    activities: list[str] = Field(
        min_length=1,
        description="Activities performed during this phase.",
    )


class CampaignPlanOutput(StrictBaseModel):
    """Structured executable campaign plan."""

    objective: str = Field(
        min_length=1,
        description="Primary campaign objective.",
    )

    target_audience_segments: list[str] = Field(
        min_length=1,
        description="Target audience segments.",
    )

    channels: list[str] = Field(
        min_length=1,
        description="Recommended marketing channels.",
    )

    budget_allocations: list[ChannelBudget] = Field(
        min_length=1,
        description="Budget allocated across marketing channels.",
    )

    campaign_phases: list[CampaignPhase] = Field(
        min_length=1,
        description="Campaign execution phases.",
    )

    key_messages: list[str] = Field(
        min_length=1,
        description="Core campaign messages.",
    )

    kpis: list[str] = Field(
        min_length=1,
        description="Key performance indicators.",
    )

    timeline: list[str] = Field(
        min_length=1,
        description="Important campaign timeline milestones.",
    )

    optimization_strategy: list[str] = Field(
        min_length=1,
        description="Campaign optimization strategy.",
    )

    risks: list[str] = Field(
        default_factory=list,
        description="Known campaign risks.",
    )

    expected_results: list[str] = Field(
        default_factory=list,
        description="Expected campaign outcomes.",
    )

    total_allocated_budget: float = Field(
        ge=0,
        description="Total of all channel budget allocations.",
    )

    @model_validator(mode="after")
    def validate_budget_total(self) -> "CampaignPlanOutput":
        """
        Ensure the declared total budget matches the sum
        of individual channel allocations.
        """

        calculated = sum(
            item.budget
            for item in self.budget_allocations
        )

        if abs(calculated - self.total_allocated_budget) > 0.01:
            raise ValueError(
                "total_allocated_budget must equal the sum "
                "of budget_allocations."
            )

        return self


# ============================================================
# 5. CONTENT STRATEGIST
# ============================================================

class ContentItem(StrictBaseModel):
    """Reusable content idea."""

    title: str = Field(
        min_length=1,
        description="Content title.",
    )

    concept: str = Field(
        min_length=1,
        description="Description of the content idea.",
    )

    audience_pain_point: str = Field(
        default="",
        description="Audience pain point addressed by the content.",
    )

    call_to_action: str = Field(
        default="",
        description="Call to action.",
    )


class AdvertisementConcept(StrictBaseModel):
    """Paid advertisement concept."""

    name: str = Field(
        min_length=1,
        description="Advertisement concept name.",
    )

    ad_copy: str = Field(
        min_length=1,
        description="Advertisement copy.",
    )

    call_to_action: str = Field(
        min_length=1,
        description="Advertisement call to action.",
    )


class EmailCampaignIdea(StrictBaseModel):
    """Email campaign concept."""

    subject: str = Field(
        min_length=1,
        description="Email subject.",
    )

    purpose: str = Field(
        min_length=1,
        description="Purpose of the email.",
    )

    call_to_action: str = Field(
        min_length=1,
        description="Email call to action.",
    )


class ContentStrategyOutput(StrictBaseModel):
    """Structured content strategy."""

    campaign_message: str = Field(
        min_length=1,
        description="Core campaign message.",
    )

    social_media_posts: list[ContentItem] = Field(
        min_length=5,
        description="Social media content ideas.",
    )

    short_form_videos: list[ContentItem] = Field(
        min_length=3,
        description="Short-form video ideas.",
    )

    advertisements: list[AdvertisementConcept] = Field(
        min_length=3,
        description="Paid advertisement concepts.",
    )

    email_campaigns: list[EmailCampaignIdea] = Field(
        min_length=3,
        description="Email campaign ideas.",
    )

    blog_topics: list[str] = Field(
        min_length=5,
        description="Recommended blog topics.",
    )

    recommended_ctas: list[str] = Field(
        min_length=1,
        description="Recommended calls to action.",
    )


# ============================================================
# 6. ANALYTICS
# ============================================================

class ChannelPerformance(StrictBaseModel):
    """Actual performance for one campaign channel."""

    channel: str = Field(
        min_length=1,
        description="Marketing channel.",
    )

    spend: float = Field(
        ge=0,
        description="Actual spend.",
    )

    visits: float = Field(
        ge=0,
        description="Number of visits generated.",
    )

    signups: float = Field(
        ge=0,
        description="Number of signups generated.",
    )

    cac: Optional[float] = Field(
        default=None,
        ge=0,
        description="Cost per signup.",
    )

    conversion_rate: Optional[float] = Field(
        default=None,
        ge=0,
        description="Signup conversion rate.",
    )


class AnalyticsOptimizationOutput(StrictBaseModel):
    """Structured analytics and optimization result."""

    # --------------------------------------------------------
    # TARGET METRICS
    # --------------------------------------------------------

    signup_target: int = Field(
        ge=0,
        description="Target number of signups.",
    )

    campaign_days: int = Field(
        gt=0,
        description="Campaign duration.",
    )

    total_budget: float = Field(
        ge=0,
        description="Total campaign budget.",
    )

    daily_signup_target: float = Field(
        ge=0,
        description="Required average daily signups.",
    )

    rolling_7_day_signup_target: float = Field(
        ge=0,
        description="Required rolling seven-day signups.",
    )

    maximum_blended_cac: float = Field(
        ge=0,
        description="Maximum acceptable blended CAC.",
    )

    budget_per_day: float = Field(
        ge=0,
        description="Average daily budget.",
    )

    budget_per_signup: float = Field(
        ge=0,
        description="Budget available per target signup.",
    )

    # --------------------------------------------------------
    # ACTUAL METRICS
    # --------------------------------------------------------

    actual_spend: Optional[float] = Field(
        default=None,
        ge=0,
        description="Actual campaign spend.",
    )

    actual_visits: Optional[float] = Field(
        default=None,
        ge=0,
        description="Actual campaign visits.",
    )

    actual_signups: Optional[float] = Field(
        default=None,
        ge=0,
        description="Actual signups.",
    )

    actual_revenue: Optional[float] = Field(
        default=None,
        ge=0,
        description="Actual campaign revenue.",
    )

    actual_conversion_rate: Optional[float] = Field(
        default=None,
        ge=0,
        description="Actual signup conversion rate.",
    )

    actual_cac: Optional[float] = Field(
        default=None,
        ge=0,
        description="Actual blended CAC.",
    )

    actual_roas: Optional[float] = Field(
        default=None,
        ge=0,
        description="Actual return on ad spend.",
    )

    actual_roi: Optional[float] = Field(
        default=None,
        description="Actual return on investment.",
    )

    # --------------------------------------------------------
    # CHANNEL PERFORMANCE
    # --------------------------------------------------------

    channel_performance: list[ChannelPerformance] = Field(
        default_factory=list,
        description="Performance breakdown by channel.",
    )

    best_channel: Optional[str] = Field(
        default=None,
        description="Best performing channel.",
    )

    worst_channel: Optional[str] = Field(
        default=None,
        description="Worst performing channel.",
    )

    # --------------------------------------------------------
    # ANALYSIS
    # --------------------------------------------------------

    executive_summary: str = Field(
        min_length=1,
        description="Executive summary of campaign performance.",
    )

    funnel_analysis: list[str] = Field(
        default_factory=list,
        description="Marketing funnel observations.",
    )

    budget_optimization: list[str] = Field(
        default_factory=list,
        description="Budget optimization recommendations.",
    )

    kpi_analysis: list[str] = Field(
        default_factory=list,
        description="KPI analysis.",
    )

    ab_testing_recommendations: list[str] = Field(
        default_factory=list,
        description="Recommended A/B tests.",
    )

    risk_detection: list[str] = Field(
        default_factory=list,
        description="Detected campaign risks.",
    )

    seven_day_optimization_plan: list[str] = Field(
        default_factory=list,
        description="Seven-day optimization plan.",
    )

    final_recommendation: str = Field(
        min_length=1,
        description="Final optimization recommendation.",
    )

    # --------------------------------------------------------
    # VALIDATORS
    # --------------------------------------------------------

    @field_validator("actual_roas")
    @classmethod
    def validate_roas_non_negative(
        cls,
        value: Optional[float],
    ) -> Optional[float]:
        if value is not None and value < 0:
            raise ValueError(
                "actual_roas cannot be negative."
            )

        return value


# ============================================================
# 7. COMPLETE WORKFLOW OUTPUT
# ============================================================

class MarketingWorkflowOutput(StrictBaseModel):
    """
    Complete structured result of the marketing workflow.

    This will become particularly useful later when we implement:
    - shared CampaignContext
    - SQLite memory
    - human approval
    - revision loop
    - Gradio UI
    - final report generation
    """

    marketing_plan: MarketingPlanOutput

    market_research: MarketResearchOutput

    competitor_analysis: CompetitorAnalysisOutput

    campaign_plan: CampaignPlanOutput

    content_strategy: ContentStrategyOutput

    analytics_optimization: AnalyticsOptimizationOutput

    workflow_status: str = Field(
        default="completed",
        description="Current workflow status.",
    )

    approval_status: str = Field(
        default="pending",
        description="Human approval status.",
    )

    revision_requested: bool = Field(
        default=False,
        description="Whether the human reviewer requested a revision.",
    )

    revision_feedback: Optional[str] = Field(
        default=None,
        description="Human feedback for revision.",
    )