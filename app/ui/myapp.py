from __future__ import annotations

import os
import sys
import re
import json
from datetime import datetime, timezone
from pathlib import Path
from html import escape

import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv


# ============================================================
# PROJECT PATH / ENVIRONMENT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Marketing Manager",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================
st.markdown(
    """
<style>

:root {
    --bg: #F7F3ED;
    --surface: #FFFDF9;
    --surface-soft: #F2EAE1;
    --border: #E5D8CB;

    --primary: #C96A3D;
    --primary-dark: #AA542F;
    --primary-light: #F3D4C2;

    --text: #211A16;
    --muted: #81756D;

    --success: #3d7826;
    --warning: #C58A3A;
    --danger: #8a5a19;

    --sidebar: #2E2520;
    --sidebar-border: #443831;
}


/* ============================================================
   APP
   ============================================================ */

.stApp {
    background: var(--bg);
    color: var(--text);
}

.main .block-container {
    max-width: 1500px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}


/* ============================================================
   REMOVE STREAMLIT CHROME
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--sidebar-border);
}

section[data-testid="stSidebar"] > div {
    background: var(--sidebar);
}

section[data-testid="stSidebar"] * {
    color: #211A16;
}

section[data-testid="stSidebar"] .stButton {
    width: 100%;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 42px;

    background: transparent;
    border: 0;

    color: #D9CEC5;

    text-align: left;

    border-radius: 9px;

    padding: 9px 12px;

    font-size: 13px;
    font-weight: 600;

    margin: 2px 0;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #40342D;
    color: #FFFFFF;
    border: 0;
}

section[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none;
}


/* ============================================================
   BRAND
   ============================================================ */

.brand {
    padding: 10px 8px 26px 8px;
}

.brand-icon {
    width: 42px;
    height: 42px;

    background: var(--primary);

    border-radius: 13px;

    display: inline-flex;
    align-items: center;
    justify-content: center;

    font-size: 18px;
    font-weight: 700;

    margin-right: 10px;

    vertical-align: middle;
}

.brand-name {
    display: inline-block;

    vertical-align: middle;

    font-size: 17px;
    font-weight: 800;

    letter-spacing: -0.3px;
}

.brand-subtitle {
    color: #B9AAA0;

    font-size: 9px;

    margin-left: 54px;
    margin-top: -5px;

    letter-spacing: 0.9px;
}


/* ============================================================
   SIDEBAR SECTIONS
   ============================================================ */

.sidebar-section {
    color: #A99589;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 1.7px;

    margin: 24px 8px 8px 8px;

    text-transform: uppercase;
}


/* ============================================================
   SIDEBAR STATUS
   ============================================================ */

.system-status {
    margin-top: 28px;

    padding: 13px;

    border: 1px solid #51443C;

    border-radius: 12px;

    background: #382E28;

    font-size: 11px;
}

.status-dot {
    display: inline-block;

    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #7F9D6F;

    margin-right: 7px;
}


/* ============================================================
   PAGE HEADER
   ============================================================ */

.top-header {
    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    margin-bottom: 28px;
}

.eyebrow {
    color: var(--primary);

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.8px;

    text-transform: uppercase;

    margin-bottom: 7px;
}

.page-title {
    color: var(--text);

    font-size: 32px;

    line-height: 1.1;

    font-weight: 800;

    letter-spacing: -1.1px;
}

.page-description {
    color: var(--muted);

    font-size: 13px;

    margin-top: 7px;
}

.user-chip {
    background: var(--surface);

    border: 1px solid var(--border);

    padding: 9px 14px;

    border-radius: 30px;

    color: var(--text);

    font-size: 12px;

    font-weight: 600;

    box-shadow: 0 4px 14px rgba(80, 55, 40, 0.05);
}


/* ============================================================
   CARDS
   ============================================================ */

.section-card {
    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 16px;

    padding: 21px;

    box-shadow: 0 5px 18px rgba(80, 55, 40, 0.04);
}

.card-title {
    color: var(--text);

    font-size: 15px;

    font-weight: 800;
}

.card-subtitle {
    color: var(--muted);

    font-size: 11px;

    margin-top: 4px;

    margin-bottom: 14px;
}


/* ============================================================
   KPI
   ============================================================ */

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 21px;
    min-height: 130px;
    box-shadow: 0 5px 18px rgba(80, 55, 40, 0.04);
}

.metric-label {
    color: #211A16 !important;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.4px;
    margin-bottom: 11px;
}

.metric-value {
    color: #211A16 !important;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.8px;
}

.metric-change {
    font-size: 10px;
    margin-top: 8px;
    color: var(--success);
    font-weight: 700;
}
/* ============================================================
   WORKFLOW
   ============================================================ */

.workflow-item {
    display: flex;

    align-items: center;

    padding: 11px 0;

    border-bottom: 1px solid var(--border);
}

.workflow-item:last-child {
    border-bottom: none;
}

.workflow-icon {
    width: 29px;
    height: 29px;

    border-radius: 50%;

    background: var(--surface-soft);

    display: flex;

    align-items: center;
    justify-content: center;

    margin-right: 11px;

    font-size: 11px;

    font-weight: 800;

    color: var(--primary);
}

.workflow-name {
    font-size: 12px;

    font-weight: 650;

    color: var(--text);
}

.workflow-status {
    margin-left: auto;

    font-size: 10px;

    color: var(--success);

    font-weight: 700;
}


/* ============================================================
   CAMPAIGN ROW
   ============================================================ */

.campaign-row {
    display: flex;

    align-items: center;

    padding: 14px 0;

    border-bottom: 1px solid var(--border);
}

.campaign-row:last-child {
    border-bottom: none;
}

.campaign-name {
    color: var(--text);

    font-size: 13px;

    font-weight: 750;
}

.campaign-meta {
    color: var(--muted);

    font-size: 10px;

    margin-top: 3px;
}

.campaign-budget {
    margin-left: auto;

    margin-right: 18px;

    color: var(--text);

    font-size: 12px;

    font-weight: 750;
}


/* ============================================================
   BADGES
   ============================================================ */

.badge-approved,
.badge-pending,
.badge-revision {
    display: inline-block;

    padding: 5px 9px;

    border-radius: 20px;

    font-size: 9px;

    font-weight: 800;
}

.badge-approved {
    background: #E4ECDD;
    color: #557047;
}

.badge-pending {
    background: #F5E6CE;
    color: #996B2F;
}

.badge-revision {
    background: #F3DCD3;
    color: #9D5239;
}


/* ============================================================
   QUICK ACTION / ENGINE
   ============================================================ */

.quick-action,
.strategy-engine {
    background: var(--primary);

    color: white;

    border-radius: 16px;

    padding: 21px;

    box-shadow: 0 9px 25px rgba(201, 106, 61, 0.18);
}

.quick-action-title,
.engine-title {
    color: white;

    font-size: 16px;

    font-weight: 800;
}

.quick-action-text,
.engine-text {
    color: #FBE9DE;

    font-size: 11px;

    line-height: 1.5;

    margin-top: 6px;
}


/* ============================================================
   STRATEGY STEPS
   ============================================================ */

.strategy-steps {
    display: flex;

    align-items: center;

    margin-top: 22px;
}

.strategy-step {
    display: flex;

    align-items: center;

    flex: 1;

    min-width: 0;
}

.step-number {
    width: 24px;
    height: 24px;

    flex-shrink: 0;

    border-radius: 50%;

    background: rgba(255,255,255,0.18);

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 10px;

    font-weight: 800;
}

.step-label {
    margin-left: 9px;

    color: white;

    font-size: 10px;

    font-weight: 700;

    white-space: nowrap;
}

.step-line {
    height: 1px;

    background: rgba(255,255,255,0.35);

    flex: 1;

    margin: 0 12px;
}


/* ============================================================
   DETAIL FIELDS
   ============================================================ */

.detail-label {
    color: var(--muted);

    font-size: 11px;

    margin-bottom: 5px;
}

.detail-value {
    color: var(--text);

    font-size: 13px;

    font-weight: 500;
}

.detail-block {
    margin-bottom: 20px;
}

.detail-block:last-child {
    margin-bottom: 0;
}

/* Streamlit metric text */
[data-testid="stMetric"] {
    color: #211A16 !important;
}

[data-testid="stMetricLabel"] {
    color: #6B4226 !important;
}

[data-testid="stMetricValue"] {
    color: #211A16 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #6B4226 !important;
}


/* ============================================================
   STREAMLIT TABLE — FORCE DARK TEXT ON LIGHT PANEL
   ============================================================ */

[data-testid="stTable"] {
    color: #211A16 !important;
}

[data-testid="stTable"] table {
    color: #211A16 !important;
    background: #FFFDF9 !important;
}

[data-testid="stTable"] th,
[data-testid="stTable"] td {
    color: #211A16 !important;
    background: #FFFDF9 !important;
}

[data-testid="stTable"] th *,
[data-testid="stTable"] td *,
[data-testid="stTable"] p,
[data-testid="stTable"] span,
[data-testid="stTable"] div {
    color: #211A16 !important;
}


/* ============================================================
   CHECKLIST
   ============================================================ */

.check-item {
    display: flex;

    align-items: center;

    padding: 11px 0;

    border-bottom: 1px solid var(--border);
}

.check-item:last-child {
    border-bottom: none;
}

.check-icon {
    width: 28px;
    height: 28px;

    border-radius: 50%;

    background: var(--surface-soft);

    color: var(--primary);

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 11px;

    margin-right: 11px;
}

.check-name {
    color: var(--text);

    font-size: 12px;

    font-weight: 650;
}

.check-status {
    margin-left: auto;

    font-size: 10px;

    font-weight: 700;
}


/* ============================================================
   ALERTS
   ============================================================ */

.success-box {
    background: #DDF1DB;

    border: 1px solid #B9DEB5;

    color: #4F8050;

    padding: 12px 14px;

    border-radius: 9px;

    font-size: 12px;
}

.info-box {
    background: #DDEAF6;

    border: 1px solid #C3D9EA;

    color: #4A79A8;

    padding: 12px 14px;

    border-radius: 9px;

    font-size: 12px;
}

.warning-box {
    background: #b58326;

    border: 1px solid #EBD4AE;

    color: #9A6C2F;

    padding: 12px 14px;

    border-radius: 9px;

    font-size: 12px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    min-height: 40px;

    border-radius: 10px;

    border: 1px solid var(--border);

    background: var(--surface);

    color: var(--text);

    font-weight: 650;

    font-size: 12px;
}

.stButton > button:hover {
    border-color: var(--primary);

    color: var(--primary);

    background: var(--surface);
}

.stButton > button:focus {
    box-shadow: 0 0 0 1px var(--primary);
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 900px) {

    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .page-title {
        font-size: 27px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# PROFESSIONAL BROWN + CREAM UI OVERRIDES
# ============================================================
# UI-only changes: no campaign/analytics/workflow logic is changed.
st.markdown(
    """
    <style>
    :root {
        --cream-bg: #F6EFE6;
        --cream-card: #FFFDF8;
        --cream-soft: #EFE2D3;
        --brown-deep: #3A2418;
        --brown: #6B4226;
        --brown-mid: #8A5A38;
        --brown-light: #B88A63;
        --brown-border: #DCC7B3;
        --brown-text: #2B1C14;
        --brown-muted: #765F50;
    }

    /* Overall page */
    .stApp {
        background: var(--cream-bg) !important;
        color: var(--brown-text) !important;
    }

    .main .block-container {
        max-width: 1550px !important;
        padding-top: 2.5rem !important;
        padding-bottom: 4rem !important;
        padding-left: 3.5rem !important;
        padding-right: 3.5rem !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background: var(--brown-deep) !important;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid #523524 !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        min-height: 50px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        font-weight: 750 !important;
        letter-spacing: 0.1px !important;
        border-radius: 12px !important;
        color: #F9F1E8 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        color: #543724 !important;
        background: #FFFDF8 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:focus {
        box-shadow: 0 0 0 2px #B88A63 !important;
    }

    .brand {
        padding: 14px 10px 30px 10px !important;
    }

    .brand-icon {
        width: 48px !important;
        height: 48px !important;
        background: #9A673F !important;
        font-size: 21px !important;
    }

    .brand-name {
        font-size: 22px !important;
        font-weight: 850 !important;
        color: #FFF9F1 !important;
    }

    .brand-subtitle {
        font-size: 11px !important;
        color: #D7C0AC !important;
        letter-spacing: 1.5px !important;
    }

    .sidebar-section {
        font-size: 11px !important;
        color: #C6A991 !important;
        letter-spacing: 1.9px !important;
        margin-top: 27px !important;
        margin-bottom: 10px !important;
    }

    .system-status {
        font-size: 13px !important;
        padding: 16px !important;
        background: #463025 !important;
        border-color: #654534 !important;
    }

    /* Page headings */
    .page-title {
        font-size: 42px !important;
        line-height: 1.05 !important;
        font-weight: 900 !important;
        letter-spacing: -1.4px !important;
        color: var(--brown-deep) !important;
    }

    .eyebrow {
        font-size: 12px !important;
        font-weight: 850 !important;
        letter-spacing: 2px !important;
        color: var(--brown) !important;
    }

    .page-description {
        font-size: 15px !important;
        color: var(--brown-muted) !important;
        line-height: 1.55 !important;
        max-width: 850px !important;
    }

    .user-chip {
        font-size: 13px !important;
        font-weight: 750 !important;
        color: var(--brown-deep) !important;
        border-color: var(--brown-border) !important;
        background: var(--cream-card) !important;
    }

    /* Cards and section headings */
    .section-card,
    .metric-card {
        background: var(--cream-card) !important;
        border-color: var(--brown-border) !important;
        box-shadow: 0 8px 24px rgba(72, 43, 26, 0.07) !important;
    }

    .section-card {
        border-radius: 18px !important;
        padding: 25px !important;
    }

    .card-title {
        font-size: 18px !important;
        font-weight: 850 !important;
        color: var(--brown-deep) !important;
    }

    .card-subtitle {
        font-size: 13px !important;
        line-height: 1.5 !important;
        color: var(--brown-muted) !important;
    }

    /* Detail labels become obvious field headings */
    .detail-label {
        font-size: 13px !important;
        font-weight: 800 !important;
        color: var(--brown) !important;
        text-transform: none !important;
        margin-bottom: 7px !important;
    }

    .detail-value {
        font-size: 15px !important;
        line-height: 1.55 !important;
        color: var(--brown-text) !important;
    }

    .detail-block {
        padding: 10px 0 !important;
        margin-bottom: 10px !important;
    }

    /* KPI cards */
    .metric-card {
        min-height: 145px !important;
        padding: 24px !important;
        border-radius: 18px !important;
    }

    .metric-label {
        font-size: 12px !important;
        font-weight: 850 !important;
        color: var(--brown-muted) !important;
        letter-spacing: 0.7px !important;
    }

    .metric-value {
        font-size: 34px !important;
        font-weight: 900 !important;
        color: var(--brown-deep) !important;
    }

    .metric-change {
        font-size: 12px !important;
    }

    /* Buttons */
    .stButton > button {
        min-height: 46px !important;
        border-radius: 12px !important;
        border: 1px solid var(--brown-border) !important;
        background: var(--cream-card) !important;
        color: var(--brown-deep) !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        padding: 10px 18px !important;
    }

    .stButton > button:hover {
        background: #F0E1D2 !important;
        border-color: var(--brown) !important;
        color: var(--brown-deep) !important;
    }

    /* Inputs - applies automatically if/when Streamlit input widgets are present */
    label,
    [data-testid="stWidgetLabel"] p {
        font-size: 14px !important;
        font-weight: 800 !important;
        color: var(--brown-deep) !important;
    }

    input,
    textarea,
    [data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: var(--brown-border) !important;
        background: #FFFCF7 !important;
        color: var(--brown-text) !important;
    }

    input:focus,
    textarea:focus {
        border-color: var(--brown) !important;
        box-shadow: 0 0 0 1px var(--brown) !important;
    }

    /* Helpful text beneath fields */
    [data-testid="InputInstructions"],
    .stTextInput small,
    .stNumberInput small,
    .stTextArea small {
        font-size: 12px !important;
        color: var(--brown-muted) !important;
    }

    /* Workflow/checklist */
    .workflow-name,
    .check-name {
        font-size: 14px !important;
        font-weight: 750 !important;
    }

    .workflow-status,
    .check-status {
        font-size: 12px !important;
        font-weight: 800 !important;
    }

    /* Campaign rows */
    .campaign-name {
        font-size: 15px !important;
        font-weight: 850 !important;
    }

    .campaign-meta {
        font-size: 12px !important;
    }

    .campaign-budget {
        font-size: 14px !important;
    }

    /* Badges */
    .badge-approved,
    .badge-pending,
    .badge-revision {
        font-size: 10px !important;
        padding: 6px 11px !important;
        letter-spacing: 0.5px !important;
    }

    /* Brown strategy/action panels */
    .quick-action,
    .strategy-engine {
        background: linear-gradient(135deg, #6B4226, #8A5A38) !important;
        border-radius: 18px !important;
        box-shadow: 0 12px 30px rgba(86, 51, 30, 0.20) !important;
    }

    .quick-action-title,
    .engine-title {
        font-size: 19px !important;
        font-weight: 850 !important;
    }

    .quick-action-text,
    .engine-text {
        font-size: 13px !important;
        line-height: 1.6 !important;
    }

    /* Alerts */
    .success-box,
    .info-box,
    .warning-box {
        font-size: 13px !important;
        line-height: 1.55 !important;
        padding: 14px 16px !important;
        border-radius: 11px !important;
    }

    /* Plotly area */
    .js-plotly-plot {
        border-radius: 16px !important;
        overflow: hidden !important;
    }

    /* Mobile */
    @media (max-width: 900px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .page-title {
            font-size: 32px !important;
        }

        section[data-testid="stSidebar"] .stButton > button {
            font-size: 15px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "campaign_status" not in st.session_state:
    st.session_state.campaign_status = "Pending Review"

if "strategy_generated" not in st.session_state:
    st.session_state.strategy_generated = False

if "approved" not in st.session_state:
    st.session_state.approved = False


# ============================================================
# HTML HELPER
# ============================================================

def html(content: str) -> None:
    """
    Render HTML safely through Streamlit's HTML renderer.

    Do NOT use markdown code fences inside these strings.
    """
    st.html(content)



# ============================================================
# HELPERS
# ============================================================

def html(content: str) -> None:
    st.html(content)


def navigate(page: str) -> None:
    st.session_state.page = page


PERSISTENCE_FILE = Path(__file__).resolve().parent / "campaigns.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_performance() -> dict:
    return {
        "signups": 0, "visitors": 0, "spend": 0.0, "revenue": 0.0,
        "channels": {}, "analytics_ai_output": "", "analytics_ai_agent": "",
    }


def _prepare_campaign_for_storage(campaign: dict) -> dict:
    stored = dict(campaign)
    stored["performance"] = dict(stored.get("performance") or _default_performance())
    stored["performance"]["channels"] = dict(stored["performance"].get("channels") or {})
    stored["strategy_history"] = list(stored.get("strategy_history") or [])
    stored["feedback_history"] = list(stored.get("feedback_history") or [])
    stored["approval_history"] = list(stored.get("approval_history") or [])
    return stored


def load_persistent_campaigns() -> list[dict]:
    if not PERSISTENCE_FILE.exists():
        return []
    try:
        raw = json.loads(PERSISTENCE_FILE.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        return [_prepare_campaign_for_storage(item) for item in raw if isinstance(item, dict) and item.get("name")]
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return []


def save_persistent_campaigns(campaigns: list[dict]) -> None:
    safe = [_prepare_campaign_for_storage(item) for item in campaigns if isinstance(item, dict)]
    PERSISTENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = PERSISTENCE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(PERSISTENCE_FILE)


def _persist_current_campaign() -> None:
    campaigns = st.session_state.setdefault("campaigns", [])
    active = st.session_state.get("campaign")
    if not active:
        return
    active = _prepare_campaign_for_storage(active)
    active["updated_at"] = _utc_now()
    st.session_state.campaign = active
    st.session_state.current_campaign = active.copy()
    for i, item in enumerate(campaigns):
        if item.get("name") == active.get("name"):
            campaigns[i] = active.copy()
            break
    else:
        campaigns.append(active.copy())
    save_persistent_campaigns(campaigns)


def reset_strategy_state() -> None:
    st.session_state.strategy_generated = False
    st.session_state.approved = False
    st.session_state.strategy_output = ""
    st.session_state.selected_agent = ""
    st.session_state.handoff = ""
    st.session_state.approval_workflow = None
    st.session_state.revision_feedback = ""
    st.session_state.show_revision_box = False
    st.session_state.campaign_status = "Draft"
    st.session_state.last_error = ""


def normalise_campaign(
    name: str,
    product: str,
    audience: str,
    budget: float,
    signup_target: int,
    duration_days: int,
    channels: list[str],
) -> dict:
    daily = signup_target / duration_days
    weekly = daily * 7
    cac = budget / signup_target
    per_day = budget / duration_days

    goal = f"Acquire {signup_target:,} signups"

    return {
        "name": name.strip(),
        "product": product.strip(),
        "goal": goal,
        "audience": audience.strip(),
        "budget": f"₹{budget:,.0f}",
        "budget_value": float(budget),
        "signup_target": int(signup_target),
        "duration": f"{duration_days} days",
        "duration_days": int(duration_days),
        "channels": ", ".join(channels),
        "channel_list": channels,
        "daily_signup_target": daily,
        "weekly_signup_target": weekly,
        "maximum_cac": cac,
        "budget_per_day": per_day,
        "budget_per_signup": cac,
        # Actual performance is entered later from the Analytics page.
        # It is deliberately kept separate from AI-generated strategy data.
        "performance": _default_performance(),
        "strategy_history": [],
        "feedback_history": [],
        "approval_history": [],
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
def store_campaign(campaign: dict) -> None:
    """Save one canonical campaign to session state and durable JSON storage."""
    campaigns = st.session_state.setdefault("campaigns", [])
    existing = next((item for item in campaigns if item.get("name") == campaign.get("name")), None)
    if existing:
        if existing.get("performance"):
            campaign["performance"] = existing["performance"]

        for key in ("strategy_history", "feedback_history", "approval_history"):
            if key not in campaign:
                campaign[key] = list(existing.get(key) or [])

    campaign.setdefault("status", "Draft")
    campaign.setdefault("approved", False)
    campaign.setdefault("strategy_output", "")
    campaign.setdefault("strategy_history", [])
    campaign.setdefault("feedback_history", [])
    campaign.setdefault("approval_history", [])
    campaign.setdefault("performance", _default_performance())
    campaign["updated_at"] = _utc_now()
    st.session_state.campaign = campaign.copy()
    st.session_state.current_campaign = campaign.copy()
    existing_index = next((i for i, item in enumerate(campaigns) if item.get("name") == campaign.get("name")), None)
    if existing_index is None:
        campaigns.append(campaign.copy())
    else:
        campaigns[existing_index] = campaign.copy()
    st.session_state.selected_campaign_name = campaign["name"]
    save_persistent_campaigns(campaigns)
def build_strategy_request(feedback: str = "") -> str:
    c = st.session_state.campaign

    previous_strategy = str(
        st.session_state.get("strategy_output", "")
        or c.get("strategy_output", "")
        or ""
    ).strip()

    request = f"""
Create a practical marketing strategy for this campaign.

CAMPAIGN:
Name: {c["name"]}
Product / Service: {c["product"]}
Target Audience: {c["audience"]}
Campaign Goal: {c["goal"]}
Budget: {c["budget"]}
Campaign Duration: {c["duration"]}
Channels: {c["channels"]}
Signup Target: {c["signup_target"]:,}
Maximum CAC: ₹{c["maximum_cac"]:.2f}

IMPORTANT:
Keep the campaign constraints above unchanged.

"""

    if previous_strategy:
        request += f"""
PREVIOUS STRATEGY
-----------------
{previous_strategy}
-----------------

This is a REVISION of the previous strategy.

Do not create an unrelated strategy.
Preserve useful parts of the previous strategy unless the reviewer
specifically asks for them to change.
HARD RULES:
1. Apply ONLY the changes explicitly requested in the human feedback.
2. Preserve every other value and section from the previous strategy.
3. Never replace, rebalance, or recalculate a budget unless explicitly requested.
4. Never change a channel allocation unless explicitly requested.
5. Never change the target audience unless explicitly requested.
6. Never change the signup target unless explicitly requested.
7. Never change the campaign duration unless explicitly requested.
8. Never change CAC/CPA unless explicitly requested.
9. Never remove an existing KPI unless explicitly requested.
10. Never add a new audience segment unless explicitly requested.
11. If the feedback says "keep unchanged", that value is LOCKED.
12. If the feedback says "exactly", reproduce that value exactly.
13. Preserve the previous strategy's structure and terminology wherever possible.
14. Return the COMPLETE revised strategy.
 
Apply the reviewer feedback directly to the PREVIOUS STRATEGY.

Only make the requested changes.
Everything not mentioned in the feedback must remain unchanged.
The final output must contain the requested changes.
Do not merely describe the changes.
"""

    request += """
Please cover:

1. Campaign objective
2. Target audience
3. Budget allocation
4. Recommended marketing channels
5. Campaign strategy
6. Positioning
7. KPIs
8. Timeline
9. Measurement approach
10. Key risks and assumptions

This strategy will be reviewed by a human before approval.
Do not present projections as guaranteed results.
"""

    if feedback.strip():
        request += f"""

HUMAN REVIEWER FEEDBACK
-----------------------
{feedback.strip()}
-----------------------

Apply the reviewer feedback directly to the strategy.
The final output must actually contain the requested changes.
Do not merely mention the feedback.
"""

    return request.strip()


def run_existing_marketing_workflow(request: str) -> dict:
    from app.services.marketing_workflow import run_marketing_workflow

    return run_marketing_workflow(request)


def create_approval_workflow(strategy: str):
    from app.approval.workflow_integration import ApprovalWorkflow

    c = st.session_state.campaign

    return ApprovalWorkflow(
        strategy=strategy,
        metadata={
            "campaign": c["name"],
            "product": c["product"],
            "goal": c["goal"],
        },
        reviewer="project_owner",
    )

def generate_strategy(feedback: str = "") -> bool:
    request = build_strategy_request(feedback)

    st.session_state.last_error = ""

    try:
        with st.spinner(
            "Marketing Manager is routing the campaign and generating the strategy..."
        ):
            result = run_existing_marketing_workflow(request)

        if not isinstance(result, dict):
            raise RuntimeError(
                "The existing marketing workflow did not return a dictionary."
            )

        output = str(result.get("final_output", "") or "").strip()

        if not output:
            raise RuntimeError(
                "The existing marketing workflow returned an empty strategy."
            )

        st.session_state.strategy_output = output
        st.session_state.selected_agent = str(
            result.get("last_agent", "") or ""
        )
        st.session_state.handoff = str(
            result.get("handoff", "") or ""
        )
        st.session_state.strategy_generated = True
        st.session_state.approved = False
        st.session_state.campaign_status = "Pending Review"
        st.session_state.approval_workflow = create_approval_workflow(output)

        # Persist every generated version, including human-feedback revisions.
        c = st.session_state.campaign
        history = c.setdefault("strategy_history", [])
        revision = len(history) + 1

        history.append({
            "revision": revision,
            "generated_at": _utc_now(),
            "feedback": feedback.strip(),
            "strategy": output,
        })

        if feedback.strip():
            c.setdefault("feedback_history", []).append({
                "revision": revision,
                "submitted_at": _utc_now(),
                "feedback": feedback.strip(),
                "status": "submitted",
            })

        c["strategy_output"] = output

        # Keep the updated campaign object in session state
        # before persisting it.
        st.session_state.campaign = c

        update_campaign_status("Pending Review", output)
        _persist_current_campaign()

        return True

    except Exception as exc:
        st.session_state.last_error = str(exc)
        return False


def update_campaign_status(
    status: str,
    strategy: str | None = None,
) -> None:
    c = st.session_state.campaign
    c["status"] = status
    if strategy is not None:
        c["strategy_output"] = strategy
    c["approved"] = bool(st.session_state.get("approved", False))
    c["updated_at"] = _utc_now()
    st.session_state.campaign = c
    campaigns = st.session_state.setdefault("campaigns", [])
    for i, item in enumerate(campaigns):
        if item.get("name") == c.get("name"):
            campaigns[i] = c.copy()
            break
    else:
        campaigns.append(c.copy())
    save_persistent_campaigns(campaigns)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_CAMPAIGN = {
    "name": "AI Study Assistant Launch",
    "product": "AI-powered Study Assistant",
    "goal": "Acquire 1,000 signups",
    "audience": "College students aged 18-25",
    "budget": "₹50,000",
    "budget_value": 50000.0,
    "signup_target": 1000,
    "duration": "30 days",
    "duration_days": 30,
    "channels": "Instagram, Content Marketing",
    "channel_list": ["Instagram", "Content Marketing"],
    "daily_signup_target": 33.33,
    "weekly_signup_target": 233.33,
    "maximum_cac": 50.0,
    "budget_per_day": 1666.67,
    "budget_per_signup": 50.0,
    "status": "Draft",
    "approved": False,
    "strategy_output": "",
}

defaults = {
    "page": "Dashboard",
    "campaign": DEFAULT_CAMPAIGN.copy(),
    "current_campaign": DEFAULT_CAMPAIGN.copy(),
    "campaigns": [],
    "selected_campaign_name": DEFAULT_CAMPAIGN["name"],
    "campaign_status": "Draft",
    "strategy_generated": False,
    "approved": False,
    "strategy_output": "",
    "selected_agent": "",
    "handoff": "",
    "approval_workflow": None,
    "revision_feedback": "",
    "show_revision_box": False,
    "last_error": "",
    "analytics_ai_output": "",
    "analytics_ai_agent": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    html(
        """
        <div class="brand">
            <span class="brand-icon">◉</span>
            <span class="brand-name">AI Marketing</span>
            <div class="brand-subtitle">STRATEGY MANAGER</div>
        </div>
        """
    )

    html('<div class="sidebar-section">Overview</div>')

    if st.button("◈  Dashboard", use_container_width=True):
        navigate("Dashboard")
        st.rerun()

    html('<div class="sidebar-section">Campaigns</div>')

    if st.button("✦  Campaigns", use_container_width=True):
        navigate("Campaigns")
        st.rerun()

    if st.button("✧  AI Strategy Studio", use_container_width=True):
        navigate("Strategy Studio")
        st.rerun()

    if st.button("✓  Approval Center", use_container_width=True):
        navigate("Approval Center")
        st.rerun()

    html('<div class="sidebar-section">Insights</div>')

    if st.button("◒  Analytics", use_container_width=True):
        navigate("Analytics")
        st.rerun()

    if st.button("◉  Campaign Memory", use_container_width=True):
        navigate("Memory")
        st.rerun()

    if st.button("☷  Campaign History", use_container_width=True):
        navigate("History")
        st.rerun()

    html('<div class="sidebar-section">System</div>')

    if st.button("⚙  Settings", use_container_width=True):
        navigate("Settings")
        st.rerun()

    backend_ready = bool(os.getenv("GROQ_API_KEY"))

    html(
        f"""
        <div class="system-status">
            <span class="status-dot"></span>
            {"System operational" if backend_ready else "API key not configured"}
            <br>
            <span style="color:#9F9188;font-size:10px;">
                AI Marketing Manager
            </span>
        </div>
        """
    )


# ============================================================
# COMMON HEADER
# ============================================================

def page_header(
    eyebrow: str,
    title: str,
    description: str,
    chip: str | None = None,
) -> None:
    chip_html = (
        f'<div class="user-chip">{escape(chip)}</div>'
        if chip
        else ""
    )

    html(
        f"""
        <div class="top-header">
            <div>
                <div class="eyebrow">{escape(eyebrow)}</div>
                <div class="page-title">{escape(title)}</div>
                <div class="page-description">{escape(description)}</div>
            </div>
            {chip_html}
        </div>
        """
    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():
    page_header(
        "Marketing Overview",
        "Hii!! I am Your Marketing Manager 👋",
        "Here's what's happening across your marketing campaigns.",
        "● Swanjal Rawat",
    )

    total = len(st.session_state.campaigns)

    cards = [
        ("TOTAL CAMPAIGNS", str(max(total, 1)), "Current workspace"),
        ("TOTAL SIGNUPS", f'{st.session_state.campaign["signup_target"]:,}', "Current target"),
        ("TOTAL SPEND", st.session_state.campaign["budget"], "Current budget"),
        (
            "MAX. CAC",
            f'₹{st.session_state.campaign["maximum_cac"]:.2f}',
            "Budget / signup",
        ),
    ]

    cols = st.columns(4)

    for column, card in zip(cols, cards):
        with column:
            html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{card[0]}</div>
                    <div class="metric-value">{card[1]}</div>
                    <div class="metric-change">{card[2]}</div>
                </div>
                """
            )

    st.write("")

    left, right = st.columns([1.65, 1])

    with left:
        html(
            """
            <div class="section-card">
                <div class="card-title">Campaign Performance</div>
                <div class="card-subtitle">
                    Target signups across the campaign duration
                </div>
            </div>
            """
        )

        c = st.session_state.campaign
        days = c["duration_days"]
        weekly_target = c["weekly_signup_target"]

        points = min(6, max(2, (days + 6) // 7))
        x = [f"Week {i}" for i in range(1, points + 1)]
        y = [round(weekly_target * i, 1) for i in range(1, points + 1)]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers",
                line=dict(color="#602104", width=3),
                marker=dict(color="#121211", size=7),
                fill="tozeroy",
                fillcolor="rgba(201,106,61,0.08)",
            )
        )

        fig.update_layout(
    height=280,
    margin=dict(l=10, r=10, t=10, b=10),

    paper_bgcolor="#FFFDF9",
    plot_bgcolor="#FFFDF9",

    # Main chart text
    font=dict(
        family="Arial",
        color="#211A16",
        size=13,
    ),

    # X axis
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(
            color="#211A16",
            size=12,
        ),
        linecolor="#E5D8CB",
    ),

    # Y axis
    yaxis=dict(
        showgrid=True,
        gridcolor="#EDE3DA",
        zeroline=False,
        tickfont=dict(
            color="#211A16",
            size=12,
        ),
        linecolor="#E5D8CB",
    ),

    showlegend=False,
)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        specialist = (
            st.session_state.selected_agent
            if st.session_state.strategy_generated
            else "Waiting for generation"
        )

        strategy_status = (
            "Generated"
            if st.session_state.strategy_generated
            else "Pending"
        )

        approval_status = (
            "Approved"
            if st.session_state.approved
            else (
                "Pending"
                if st.session_state.strategy_generated
                else "Not started"
            )
        )

        html(
            f"""
            <div class="section-card">
                <div class="card-title">AI Workflow</div>
                <div class="card-subtitle">
                    Current strategy generation pipeline
                </div>

                <div class="workflow-item">
                    <div class="workflow-icon">✓</div>
                    <div class="workflow-name">Marketing Manager</div>
                    <div class="workflow-status">Ready</div>
                </div>

                <div class="workflow-item">
                    <div class="workflow-icon">
                        {"✓" if st.session_state.strategy_generated else "●"}
                    </div>
                    <div class="workflow-name">{escape(specialist)}</div>
                    <div class="workflow-status">
                        {"Complete" if st.session_state.strategy_generated else "Pending"}
                    </div>
                </div>

                <div class="workflow-item">
                    <div class="workflow-icon">
                        {"✓" if st.session_state.strategy_generated else "●"}
                    </div>
                    <div class="workflow-name">Strategy</div>
                    <div class="workflow-status">{strategy_status}</div>
                </div>

                <div class="workflow-item">
                    <div class="workflow-icon">●</div>
                    <div class="workflow-name">Human Approval</div>
                    <div class="workflow-status">{approval_status}</div>
                </div>
            </div>
            """
        )

    st.write("")

    left, right = st.columns([1.65, 1])

    with left:
        html(
            """
            <div class="section-card">
                <div class="card-title">Recent Campaigns</div>
                <div class="card-subtitle">
                    Campaigns created during this workspace session
                </div>
            """
        )

        if not st.session_state.campaigns:
            html(
                '<div class="info-box">No campaigns created yet.</div></div>'
            )
        else:
            for item in reversed(st.session_state.campaigns[-5:]):
                status = item.get("status", "Draft")
                badge = (
                    "badge-approved"
                    if status == "Approved"
                    else (
                        "badge-revision"
                        if status == "Revision Required"
                        else "badge-pending"
                    )
                )

                html(
                    f"""
                    <div class="campaign-row">
                        <div>
                            <div class="campaign-name">
                                {escape(item["name"])}
                            </div>
                            <div class="campaign-meta">
                                {escape(item["audience"])} · {item["signup_target"]:,} signup goal
                            </div>
                        </div>
                        <div class="campaign-budget">
                            {escape(item["budget"])}
                        </div>
                        <span class="{badge}">
                            {escape(status.upper())}
                        </span>
                    </div>
                    """
                )

            html("</div>")

    with right:
        html(
            """
            <div class="quick-action">
                <div class="quick-action-title">Create a new campaign</div>
                <div class="quick-action-text">
                    Create campaign inputs and immediately use the same
                    campaign in AI Strategy Studio.
                </div>
            </div>
            """
        )

        st.write("")

        if st.button("＋  Create a new Campaigns", use_container_width=True):
            navigate("Campaigns")
            st.rerun()


# ============================================================
# CAMPAIGNS
# ============================================================

def campaigns():
    page_header(
        "Campaign Management",
        "Campaigns",
        "Create and manage marketing campaigns powered by your AI workflow.",
    )

    current = st.session_state.campaign

    if st.session_state.campaign_status != "Draft":
        html(
            f"""
            <div class="success-box">
                Current campaign:
                <strong>{escape(current["name"])}</strong>
                · status:
                <strong>{escape(st.session_state.campaign_status)}</strong>
            </div>
            """
        )
        st.write("")

    html(
        """
        <div class="section-card">
            <div class="card-title">Create / Edit Campaign</div>
            <div class="card-subtitle">
                Fill in the campaign details. The saved campaign is the
                exact object used by AI Strategy Studio.
            </div>
        </div>
        """
    )

    st.write("")

    default_channels = current.get(
        "channel_list",
        ["Instagram", "Content Marketing"],
    )

    channel_options = [
        "Instagram",
        "Facebook",
        "LinkedIn",
        "YouTube",
        "Google Ads",
        "Content Marketing",
        "Email Marketing",
        "Influencer Marketing",
    ]

    with st.form("create_campaign_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            campaign_name = st.text_input(
                "Campaign Name",
                value=current.get("name", ""),
                placeholder="e.g. AI Study Assistant Launch",
            )

            product = st.text_input(
                "Product / Service",
                value=current.get("product", ""),
                placeholder="e.g. AI-powered study assistant",
            )

            target_audience = st.text_area(
                "Target Audience",
                value=current.get("audience", ""),
                placeholder="e.g. College students aged 18-25",
                height=100,
            )

        with col2:
            budget = st.number_input(
                "Total Budget (₹)",
                min_value=1.0,
                value=float(current.get("budget_value", 50000)),
                step=1000.0,
            )

            signup_target = st.number_input(
                "Signup Target",
                min_value=1,
                value=int(current.get("signup_target", 1000)),
                step=100,
            )

            campaign_days = st.number_input(
                "Campaign Duration (days)",
                min_value=1,
                value=int(current.get("duration_days", 30)),
                step=1,
            )

        selected_channels = st.multiselect(
            "Marketing Channels",
            options=channel_options,
            default=[
                item
                for item in default_channels
                if item in channel_options
            ],
        )

        submitted = st.form_submit_button(
            "Create / Update Campaign →",
            use_container_width=True,
        )

    if not submitted:
        return

    if not campaign_name.strip():
        st.error("Please enter a campaign name.")
        return

    if not product.strip():
        st.error("Please enter the product or service.")
        return

    if not target_audience.strip():
        st.error("Please enter the target audience.")
        return

    if not selected_channels:
        st.error("Please select at least one marketing channel.")
        return

    if budget <= 0:
        st.error("Budget must be greater than ₹0.")
        return

    if signup_target <= 0:
        st.error("Signup target must be greater than 0.")
        return

    if campaign_days <= 0:
        st.error("Campaign duration must be greater than 0 days.")
        return

    campaign = normalise_campaign(
        name=campaign_name,
        product=product,
        audience=target_audience,
        budget=float(budget),
        signup_target=int(signup_target),
        duration_days=int(campaign_days),
        channels=selected_channels,
    )

    # ========================================================
    # THE CRITICAL FIX
    # ========================================================
    # Previously:
    #     session_state.current_campaign = {...}
    #
    # But Strategy Studio read:
    #     session_state.campaign
    #
    # Therefore the form appeared to work while Strategy Studio
    # continued showing the old campaign.
    #
    # store_campaign() updates BOTH and keeps one canonical object.
    # ========================================================

    store_campaign(campaign)
    reset_strategy_state()

    st.success(
        f'Campaign "{campaign["name"]}" created successfully.'
    )

    st.write("")

    html(
        f"""
        <div class="section-card">
            <div class="card-title">Campaign Created</div>
            <div class="card-subtitle">
                This exact campaign is now loaded into AI Strategy Studio.
            </div>

            <div class="campaign-row">
                <div>
                    <div class="campaign-name">
                        {escape(campaign["name"])}
                    </div>
                    <div class="campaign-meta">
                        {escape(campaign["audience"])}
                    </div>
                </div>

                <div class="campaign-budget">
                    {escape(campaign["budget"])}
                </div>

                <span class="badge-pending">READY</span>
            </div>
        </div>
        """
    )

    st.write("")
    st.markdown("### Campaign Targets")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Daily Signups",
            f'{campaign["daily_signup_target"]:.1f}',
        )

    with m2:
        st.metric(
            "7-Day Target",
            f'{campaign["weekly_signup_target"]:.1f}',
        )

    with m3:
        st.metric(
            "Maximum CAC",
            f'₹{campaign["maximum_cac"]:.2f}',
            
        )

    with m4:
        st.metric(
            "Budget / Day",
            f'₹{campaign["budget_per_day"]:,.2f}',
        )

    st.write("")

    if st.button(
        "Open AI Strategy Studio →",
        use_container_width=True, 
    ):
        navigate("AI Strategy Studio")
        st.rerun()


# ============================================================
# STRATEGY STUDIO
# ============================================================

def strategy_studio():
    page_header(
        "AI Strategy",
        "AI Strategy Studio",
        "Review the current campaign before running the existing AI workflow.",
        "✦ AI Workspace",
    )

    c = st.session_state.campaign

    html(
        f"""
        <div class="success-box">
            <strong>Active campaign:</strong>
            {escape(c["name"])}
            · This is the same campaign saved from the Campaigns page.
        </div>
        """
    )

    st.write("")

    left, right = st.columns(2)

    with left:
        html(
            f"""
            <div class="section-card">
                <div class="card-title">Campaign</div>

                <div class="detail-block" style="margin-top:28px;">
                    <div class="detail-value" style="font-weight:750;">
                        {escape(c["name"])}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Product / Service</div>
                    <div class="detail-value">
                        {escape(c["product"])}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Campaign Goal</div>
                    <div class="detail-value">
                        {escape(c["goal"])}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Signup Target</div>
                    <div class="detail-value">
                        {c["signup_target"]:,}
                    </div>
                </div>
            </div>
            """
        )

    with right:
        html(
            f"""
            <div class="section-card">
                <div class="card-title">Campaign Parameters</div>

                <div class="detail-block" style="margin-top:28px;">
                    <div class="detail-label">Target Audience</div>
                    <div class="detail-value">
                        {escape(c["audience"])}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Budget</div>
                    <div class="detail-value">
                        {escape(c["budget"])}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Duration</div>
                    <div class="detail-value">
                        {escape(c["duration"])}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Channels</div>
                    <div class="detail-value">
                        {escape(c["channels"])}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Maximum CAC</div>
                    <div class="detail-value">
                        ₹{c["maximum_cac"]:.2f}
                    </div>
                </div>
            </div>
            """
        )

    st.write("")

    html(
        """
        <div class="strategy-engine">
            <div class="engine-title">AI Strategy Engine</div>
            <div class="engine-text">
                Your campaign is ready. Generate the strategy, then
                review it in the Approval Center.
            </div>

            <div class="strategy-steps">
                <div class="strategy-step">
                    <div class="step-number">1</div>
                    <div class="step-label">Campaign Input</div>
                    <div class="step-line"></div>
                </div>

                <div class="strategy-step">
                    <div class="step-number">2</div>
                    <div class="step-label">Marketing Manager</div>
                    <div class="step-line"></div>
                </div>

                <div class="strategy-step">
                    <div class="step-number">3</div>
                    <div class="step-label">Strategy</div>
                    <div class="step-line"></div>
                </div>

                <div class="strategy-step">
                    <div class="step-number">4</div>
                    <div class="step-label">Human Approval</div>
                </div>
            </div>
        </div>
        """
    )

    st.write("")

    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("← Back to Campaigns", use_container_width=True):
            navigate("Campaigns")
            st.rerun()

    with b2:
        if st.button("✎ Edit Campaign", use_container_width=True):
            navigate("Campaigns")
            st.rerun()

    with b3:
        if st.button("✦ Generate AI Strategy", use_container_width=True):
            success = generate_strategy()

            if success:
                navigate("Approval Center")
                st.rerun()

    if st.session_state.last_error:
        st.write("")
        html(
            f"""
            <div class="warning-box">
                <strong>AI workflow error:</strong><br>
                {escape(st.session_state.last_error)}
            </div>
            """
        )

    if st.session_state.strategy_generated:
        st.write("")
        html(
            f"""
            <div class="success-box">
                ✓ Strategy generated by the existing backend workflow.
                Specialist:
                {escape(st.session_state.selected_agent or "Unknown")}.
            </div>
            """
        )


# ============================================================
# APPROVAL CENTER
# ============================================================

def approval_center():
    page_header(
        "Human Review",
        "Approval Center",
        "Review the actual AI-generated campaign strategy before approval.",
    )

    workflow = st.session_state.approval_workflow

    if not st.session_state.strategy_generated or workflow is None:
        html(
            """
            <div class="info-box">
                No generated strategy is waiting for review.
                Open AI Strategy Studio and generate a strategy first.
            </div>
            """
        )

        st.write("")

        if st.button(
            "✦ Open AI Strategy Studio",
            use_container_width=True,
        ):
            navigate("Strategy Studio")
            st.rerun()

        return

    approved = st.session_state.approved

    badge = (
        '<span class="badge-approved">APPROVED</span>'
        if approved
        else '<span class="badge-pending">PENDING REVIEW</span>'
    )

    status_text = (
        "Strategy approved and ready for execution."
        if approved
        else "Strategy generated · Awaiting human approval"
    )

    html(
        f"""
        <div class="section-card">
            <div class="card-title">
                {escape(st.session_state.campaign["name"])}
            </div>

            <div class="card-subtitle">
                {escape(status_text)}
            </div>

            <div style="margin-top:28px;">
                {badge}
            </div>
        </div>
        """
    )

    st.write("")

    left, right = st.columns([1.55, 1])

    with left:
        html(
            """
            <div class="section-card">
                <div class="card-title">Generated Strategy</div>
                <div class="card-subtitle">
                    Actual output returned by the existing Marketing Manager workflow
                </div>
            </div>
            """
        )

        with st.container(border=True):
            st.markdown(st.session_state.strategy_output)

        if st.session_state.selected_agent:
            html(
                f"""
                <div class="backend-meta">
                    Routed specialist:
                    {escape(st.session_state.selected_agent)}
                    &nbsp;·&nbsp;
                    Handoff:
                    {escape(st.session_state.handoff or "n/a")}
                </div>
                """
            )

    with right:
        human_status = "Approved" if approved else "Required"
        human_color = "#31621E" if approved else "#AE7A30"

        html(
            f"""
            <div class="section-card">
                <div class="card-title">Review Checklist</div>

                <div class="check-item">
                    <div class="check-icon">✓</div>
                    <div class="check-name">Campaign inputs</div>
                    <div class="check-status" style="color:#31621E;">
                        Ready
                    </div>
                </div>

                <div class="check-item">
                    <div class="check-icon">✓</div>
                    <div class="check-name">AI workflow</div>
                    <div class="check-status" style="color:#31621E;">
                        Complete
                    </div>
                </div>

                <div class="check-item">
                    <div class="check-icon">✓</div>
                    <div class="check-name">Strategy</div>
                    <div class="check-status" style="color:#31621E;">
                        Generated
                    </div>
                </div>

                <div class="check-item">
                    <div class="check-icon">●</div>
                    <div class="check-name">Human approval</div>
                    <div class="check-status" style="color:{human_color};">
                        {human_status}
                    </div>
                </div>
            </div>
            """
        )

    st.write("")

    if not approved:
        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button(
                "✓ Approve Strategy",
                use_container_width=True,
            ):
                try:
                    workflow.approve(
                        feedback="Approved by project owner."
                    )

                    st.session_state.approved = True
                    st.session_state.campaign_status = "Approved"
                    st.session_state.campaign.setdefault("approval_history", []).append({
                        "approved_at": _utc_now(),
                        "feedback": "Approved by project owner.",
                        "status": "Approved",
                    })
                    update_campaign_status("Approved")
                    _persist_current_campaign()
                    st.rerun()

                except Exception as exc:
                    st.error(
                        f"Approval workflow error: {exc}"
                    )

        with b2:
            if st.button(
                "↻ Request Revision",
                use_container_width=True,
            ):
                st.session_state.show_revision_box = True
                st.rerun()

        with b3:
            if st.button(
                "← Back to Strategy Studio",
                use_container_width=True,
            ):
                navigate("Strategy Studio")
                st.rerun()

        if st.session_state.show_revision_box:
            st.write("")

            html(
                """
                <div class="section-card">
                    <div class="card-title">Request a revision</div>
                    <div class="card-subtitle">
                        Tell the AI workflow what should be changed.
                    </div>
                </div>
                """
            )

            feedback = st.text_area(
                "Revision feedback",
                value=st.session_state.revision_feedback,
                placeholder=(
                    "Example: Make the positioning more specific to "
                    "college students and provide a clearer budget allocation."
                ),
                height=130,
                key="revision_feedback_input",
            )

            rb1, rb2 = st.columns(2)

            with rb1:
                if st.button(
                    "Generate Revised Strategy",
                    use_container_width=True,
                ):
                    if not feedback.strip():
                        st.warning(
                            "Please enter revision feedback first."
                        )
                    else:
                        try:
                            if st.button(
                                "Generate Revised Strategy",
                                key="revision_generate_button",
                                use_container_width=True,
                                ):
                                feedback_text = feedback.strip()
                                if not feedback_text:
                                    st.warning("Please enter revision feedback first.")
                                else:
                                    success = generate_strategy(feedback=feedback_text)
                                    if success:
                                     st.session_state.show_revision_box = False
                                     st.session_state.revision_feedback = ""
                                     st.session_state.campaign_status = "Pending Review"
                                    st.rerun()

                            success = generate_strategy(
                                feedback=feedback.strip()
                            )

                            if success:
                                st.session_state.show_revision_box = False
                                st.session_state.revision_feedback = ""
                                st.rerun()

                        except Exception as exc:
                            st.error(
                                f"Revision workflow error: {exc}"
                            )

            with rb2:
                if st.button(
                    "Cancel Revision",
                    use_container_width=True,
                ):
                    st.session_state.show_revision_box = False
                    st.rerun()

    else:
        b1, b2 = st.columns(2)

        with b1:
            st.button(
                "✓ Strategy Approved",
                use_container_width=True,
                disabled=True,
            )

        with b2:
            if st.button(
                "← Back to Strategy Studio",
                use_container_width=True,
            ):
                navigate("Strategy Studio")
                st.rerun()

        st.write("")

        html(
            """
            <div class="success-box">
                ✓ Strategy approved successfully through the existing
                human approval workflow.
            </div>
            """
        )


# ============================================================
# ANALYTICS
# ============================================================

def _safe_float(value, default=0.0):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return default


def _safe_int(value, default=0):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return default


def _format_currency(value):
    return f"₹{value:,.2f}"


def _get_campaign_performance(campaign):
    performance = campaign.setdefault(
        "performance",
        {
            "signups": 0,
            "visitors": 0,
            "spend": 0.0,
            "revenue": 0.0,
            "channels": {},
            "analytics_ai_output": "",
            "analytics_ai_agent": "",
        },
    )

    performance.setdefault("signups", 0)
    performance.setdefault("visitors", 0)
    performance.setdefault("spend", 0.0)
    performance.setdefault("revenue", 0.0)
    performance.setdefault("channels", {})
    performance.setdefault("analytics_ai_output", "")
    performance.setdefault("analytics_ai_agent", "")

    return performance


def _load_campaign_into_session(campaign):
    """
    Make the selected campaign the canonical active campaign.

    Analytics, Strategy Studio, Approval Center and Campaign Memory all
    read st.session_state.campaign, so changing a campaign here keeps the
    whole application synchronized.
    """
    selected = _prepare_campaign_for_storage(campaign)

    st.session_state.campaign = selected
    st.session_state.current_campaign = selected.copy()
    st.session_state.selected_campaign_name = selected.get("name", "")

    st.session_state.campaign_status = selected.get("status", "Draft")
    st.session_state.approved = bool(selected.get("approved", False))

    strategy = str(selected.get("strategy_output", "") or "").strip()
    st.session_state.strategy_output = strategy
    st.session_state.strategy_generated = bool(strategy)

    # Specialist/handoff metadata is session-only in the current data model.
    # Clear it when loading another campaign so old workflow metadata cannot
    # appear beside a different campaign.
    st.session_state.selected_agent = ""
    st.session_state.handoff = ""
    st.session_state.approval_workflow = None
    st.session_state.show_revision_box = False
    st.session_state.revision_feedback = ""
    st.session_state.last_error = ""

    if strategy:
        try:
            st.session_state.approval_workflow = create_approval_workflow(
                strategy
            )
        except Exception:
            st.session_state.approval_workflow = None


# Load durable campaign history once per Streamlit session.
if not st.session_state.get("persistence_loaded", False):
    persisted_campaigns = load_persistent_campaigns()
    st.session_state.campaigns = persisted_campaigns
    if persisted_campaigns:
        preferred = st.session_state.get("selected_campaign_name", "")
        selected = next(
            (x for x in persisted_campaigns if x.get("name") == preferred),
            persisted_campaigns[-1],
        )
        _load_campaign_into_session(selected)
    else:
        st.session_state.campaign = DEFAULT_CAMPAIGN.copy()
        st.session_state.current_campaign = DEFAULT_CAMPAIGN.copy()
    st.session_state.persistence_loaded = True


def _select_analytics_campaign():
    """
    Let Analytics choose any campaign created in the current session.

    The selected campaign is also loaded as the application's active
    campaign so Memory, Strategy Studio and Approval Center stay aligned.
    """
    campaigns_list = st.session_state.get("campaigns", [])

    if not campaigns_list:
        return st.session_state.campaign

    campaign_names = [
        item.get("name", f"Campaign {index + 1}")
        for index, item in enumerate(campaigns_list)
    ]

    current_name = st.session_state.get("selected_campaign_name", "")
    if current_name not in campaign_names:
        current_name = campaign_names[0]

    current_index = campaign_names.index(current_name)

    selected_name = st.selectbox(
        "Select Campaign",
        options=campaign_names,
        index=current_index,
        key="analytics_campaign_selector",
    )

    selected_campaign = next(
        (
            item
            for item in campaigns_list
            if item.get("name") == selected_name
        ),
        None,
    )

    if selected_campaign is None:
        selected_campaign = campaigns_list[current_index]

    if st.session_state.get("selected_campaign_name") != selected_campaign.get(
        "name"
    ):
        _load_campaign_into_session(selected_campaign)

    else:
        # Always refresh the active object from the campaign collection.
        # This prevents Analytics from displaying a stale copy.
        _load_campaign_into_session(selected_campaign)

    html(
        f"""
        <div class="success-box" style="margin-top:10px;">
            <strong>Active campaign:</strong>
            {escape(selected_campaign.get("name", ""))}
            &nbsp;·&nbsp; Analytics is showing this campaign's own
            performance data.
        </div>
        """
    )

    return st.session_state.campaign


def _save_campaign_performance(performance):
    c = st.session_state.campaign
    c["performance"] = performance
    st.session_state.campaign = c
    st.session_state.current_campaign = c.copy()

    campaigns = st.session_state.setdefault("campaigns", [])
    for i, item in enumerate(campaigns):
        if item.get("name") == c.get("name"):
            campaigns[i] = c.copy()
            break
    else:
        campaigns.append(c.copy())
    save_persistent_campaigns(campaigns)


def _deterministic_analytics_fallback(campaign: dict, performance: dict) -> str:
    signups = _safe_int(performance.get("signups"))
    visitors = _safe_int(performance.get("visitors"))
    spend = _safe_float(performance.get("spend"))
    revenue = _safe_float(performance.get("revenue"))
    conversion = (signups / visitors * 100) if visitors else None
    cac = (spend / signups) if signups else None
    roas = (revenue / spend) if spend and revenue else None
    rows = []
    for name, data in (performance.get("channels") or {}).items():
        ch_spend = _safe_float(data.get("spend"))
        ch_signups = _safe_int(data.get("signups"))
        ch_cac = ch_spend / ch_signups if ch_signups else None
        rows.append(
            f"- {name}: spend {_format_currency(ch_spend)}, "
            f"signups {ch_signups:,}, CAC "
            f"{_format_currency(ch_cac) if ch_cac is not None else 'not available'}"
        )
    channel_text = "\n".join(rows) if rows else "- No channel performance data supplied."
    return f"""### Deterministic Analytics Review

The AI analytics provider was unavailable, so this review was generated from the saved actual performance values. No missing metric has been invented.

#### Configured Targets
- Signup target: {campaign["signup_target"]:,}
- Campaign duration: {campaign["duration_days"]} days
- Maximum target CAC: {_format_currency(campaign["maximum_cac"])}
- Configured budget: {campaign["budget"]}

#### Actual Performance
- Actual signups: {signups:,}
- Actual visitors: {visitors:,}
- Actual spend: {_format_currency(spend)}
- Actual revenue: {_format_currency(revenue)}
- Actual conversion rate: {f"{conversion:.2f}%" if conversion is not None else "not available"}
- Actual CAC: {_format_currency(cac) if cac is not None else "not available"}
- Actual ROAS: {f"{roas:.2f}x" if roas is not None else "not available"}

#### Channel Performance
{channel_text}

#### Recommendations
1. Compare actual CAC with the maximum target CAC before increasing spend.
2. Shift budget toward channels with lower observed CAC and meaningful signup volume.
3. Collect channel-level visitors and revenue if channel conversion rate or ROAS is required.
""".strip()


def analytics():
    page_header(
        "Performance Insights",
        "Analytics",
        "Track configured targets against actual campaign performance.",
    )

    # ------------------------------------------------------------
    # CAMPAIGN SELECTOR
    # ------------------------------------------------------------
    c = _select_analytics_campaign()
    performance = _get_campaign_performance(c)

    # Widget keys must include the campaign name. Otherwise Streamlit can
    # reuse the previous campaign's input state after the user switches
    # campaigns.
    campaign_key = re.sub(
        r"[^a-zA-Z0-9_]+",
        "_",
        c.get("name", "campaign"),
    ).strip("_").lower() or "campaign"

    # ------------------------------------------------------------
    # CONFIGURED TARGETS
    # ------------------------------------------------------------
    cards = [
        (
            "SIGNUP TARGET",
            f'{c["signup_target"]:,}',
            "Campaign target",
        ),
        (
            "CAMPAIGN DAYS",
            str(c["duration_days"]),
            "Configured duration",
        ),
        (
            "MAX. CAC",
            _format_currency(c["maximum_cac"]),
            "Maximum target CAC",
        ),
        (
            "BUDGET / DAY",
            _format_currency(c["budget_per_day"]),
            "Configured spend",
        ),
    ]

    cols = st.columns(4)

    for col, card in zip(cols, cards):
        with col:
            html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{card[0]}</div>
                    <div class="metric-value">{card[1]}</div>
                    <div class="metric-change">{card[2]}</div>
                </div>
                """
            )

    st.write("")

    # ------------------------------------------------------------
    # ACTUAL CAMPAIGN PERFORMANCE INPUTS
    # ------------------------------------------------------------
    html(
        """
        <div class="section-card">
            <div class="card-title">Actual Campaign Performance</div>
            <div class="card-subtitle">
                Enter real campaign data. These values are stored with the
                campaign and are never treated as AI-generated projections.
            </div>
        </div>
        """
    )

    st.write("")

    input_cols = st.columns(4)

    with input_cols[0]:
        actual_signups = st.number_input(
            "Actual Signups",
            min_value=0,
            value=_safe_int(performance.get("signups")),
            step=1,
            key=f"analytics_actual_signups_{campaign_key}",
        )

    with input_cols[1]:
        actual_visitors = st.number_input(
            "Actual Visitors",
            min_value=0,
            value=_safe_int(performance.get("visitors")),
            step=1,
            key=f"analytics_actual_visitors_{campaign_key}",
        )

    with input_cols[2]:
        actual_spend = st.number_input(
            "Actual Spend (₹)",
            min_value=0.0,
            value=_safe_float(performance.get("spend")),
            step=100.0,
            key=f"analytics_actual_spend_{campaign_key}",
        )

    with input_cols[3]:
        actual_revenue = st.number_input(
            "Actual Revenue (₹)",
            min_value=0.0,
            value=_safe_float(performance.get("revenue")),
            step=100.0,
            key=f"analytics_actual_revenue_{campaign_key}",
        )

    if st.button(
        "Save Performance Data →",
        use_container_width=True,
        key=f"save_actual_campaign_performance_{campaign_key}",
    ):
        performance["signups"] = int(actual_signups)
        performance["visitors"] = int(actual_visitors)
        performance["spend"] = float(actual_spend)
        performance["revenue"] = float(actual_revenue)
        _save_campaign_performance(performance)

        # New actual data invalidates this campaign's old AI review.
        performance["analytics_ai_output"] = ""
        performance["analytics_ai_agent"] = ""
        st.success("Actual campaign performance saved.")
        st.rerun()

    # ------------------------------------------------------------
    # CALCULATED ACTUAL METRICS
    # ------------------------------------------------------------
    actual_signups = _safe_int(performance.get("signups"))
    actual_visitors = _safe_int(performance.get("visitors"))
    actual_spend = _safe_float(performance.get("spend"))
    actual_revenue = _safe_float(performance.get("revenue"))

    conversion_rate = (
        (actual_signups / actual_visitors) * 100
        if actual_visitors > 0
        else None
    )

    actual_cac = (
        actual_spend / actual_signups
        if actual_signups > 0
        else None
    )

    roas = (
        actual_revenue / actual_spend
        if actual_spend > 0 and actual_revenue > 0
        else None
    )

    target_progress = (
        (actual_signups / c["signup_target"]) * 100
        if c["signup_target"] > 0
        else 0
    )

    if actual_cac is None:
        cac_status = "No actual CAC yet."
    elif actual_cac <= c["maximum_cac"]:
        cac_status = (
            f"CAC is within target at {_format_currency(actual_cac)} "
            f"versus a maximum of {_format_currency(c['maximum_cac'])}."
        )
    else:
        cac_status = (
            f"CAC is above target at {_format_currency(actual_cac)} "
            f"versus a maximum of {_format_currency(c['maximum_cac'])}."
        )

    st.write("")

    metric_cols = st.columns(4)

    metric_values = [
        (
            "ACTUAL SIGNUPS",
            f"{actual_signups:,}",
            f"{target_progress:.1f}% of target",
        ),
        (
            "CONVERSION RATE",
            f"{conversion_rate:.2f}%" if conversion_rate is not None else "—",
            "Actual signups / visitors",
        ),
        (
            "ACTUAL CAC",
            _format_currency(actual_cac) if actual_cac is not None else "—",
            "Actual spend / signup",
        ),
        (
            "ROAS",
            f"{roas:.2f}x" if roas is not None else "—",
            "Revenue / spend",
        ),
    ]

    for col, metric in zip(metric_cols, metric_values):
        with col:
            html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{metric[0]}</div>
                    <div class="metric-value">{metric[1]}</div>
                    <div class="metric-change">{metric[2]}</div>
                </div>
                """
            )

    if actual_signups == 0 and actual_visitors == 0 and actual_spend == 0:
        html(
            """
            <div class="info-box" style="margin-top:15px;">
                Performance status: No actual performance data has been
                recorded yet. The target metrics above are configuration
                values, not campaign results.
            </div>
            """
        )
    else:
        html(
            f"""
            <div class="info-box" style="margin-top:15px;">
                <strong>Performance status:</strong>
                Signup progress: {actual_signups:,} of
                {c["signup_target"]:,} ({target_progress:.1f}%).
                {escape(cac_status)}
            </div>
            """
        )

    # ------------------------------------------------------------
    # CHANNEL PERFORMANCE
    # ------------------------------------------------------------
    st.write("")
    html(
        """
        <div class="section-card">
            <div class="card-title">Channel Performance</div>
            <div class="card-subtitle">
                Enter channel-level actual spend and signups when available.
                Channel CAC is calculated only from these real values.
            </div>
        </div>
        """
    )

    st.write("")

    selected_channels = c.get("channel_list") or []
    stored_channels = performance.setdefault("channels", {})

    # Always make the three commonly tested channels available when they
    # are part of the campaign. For other campaigns, use the selected list.
    channels_to_show = []
    for channel in selected_channels:
        if channel not in channels_to_show:
            channels_to_show.append(channel)

    if not channels_to_show:
        channels_to_show = ["Instagram", "YouTube", "LinkedIn"]

    for channel in channels_to_show:
        stored_channels.setdefault(
            channel,
            {"spend": 0.0, "signups": 0},
        )

    channel_input_values = {}

    # Two-column rows: spend and signups for each channel.
    for row_start in range(0, len(channels_to_show), 2):
        row_channels = channels_to_show[row_start:row_start + 2]
        cols = st.columns(2)

        for col, channel in zip(cols, row_channels):
            with col:
                data = stored_channels[channel]
                safe_key = re.sub(
                    r"[^a-zA-Z0-9_]+",
                    "_",
                    channel,
                ).strip("_").lower()

                st.markdown(
                    f"**{escape(channel)}**",
                    unsafe_allow_html=True,
                )

                spend = st.number_input(
                    f"{channel} — Spend (₹)",
                    min_value=0.0,
                    value=_safe_float(data.get("spend")),
                    step=100.0,
                    key=f"channel_spend_{safe_key}",
                )

                signups = st.number_input(
                    f"{channel} — Signups",
                    min_value=0,
                    value=_safe_int(data.get("signups")),
                    step=1,
                    key=f"channel_signups_{safe_key}",
                )

                channel_input_values[channel] = {
                    "spend": float(spend),
                    "signups": int(signups),
                }

    if st.button(
        "Save Channel Performance →",
        use_container_width=True,
        key=f"save_channel_performance_{campaign_key}",
    ):
        performance["channels"] = channel_input_values
        _save_campaign_performance(performance)

        performance["analytics_ai_output"] = ""
        performance["analytics_ai_agent"] = ""
        st.success("Channel performance saved.")
        st.rerun()

    # ------------------------------------------------------------
    # REPORTED CHANNEL KPIs
    # ------------------------------------------------------------
    st.write("")

    html(
        """
        <div class="section-card">
            <div class="card-title">Reported Channel KPIs</div>
            <div class="card-subtitle">
                These are calculations from the channel data you entered.
                No channel visitors, revenue, conversion rate, or ROAS are
                assumed when those values were not supplied.
            </div>
        </div>
        """
    )

    channel_rows = []
    for channel in channels_to_show:
        data = stored_channels.get(channel, {})
        spend = _safe_float(data.get("spend"))
        signups = _safe_int(data.get("signups"))
        channel_cac = spend / signups if signups > 0 else None

        channel_rows.append(
            {
                "Channel": channel,
                "Spend": _format_currency(spend),
                "Signups": f"{signups:,}",
                "CAC": (
                    _format_currency(channel_cac)
                    if channel_cac is not None
                    else "—"
                ),
            }
        )

    if channel_rows:
        st.table(channel_rows)

    # ------------------------------------------------------------
    # AI PERFORMANCE REVIEW
    # ------------------------------------------------------------
    st.write("")

    if st.button(
        "✦ Generate AI Performance Review",
        use_container_width=True,
        key=f"generate_analytics_review_{campaign_key}",
    ):
        channel_summary = []

        for channel in channels_to_show:
            data = stored_channels.get(channel, {})
            spend = _safe_float(data.get("spend"))
            signups = _safe_int(data.get("signups"))
            channel_cac = spend / signups if signups > 0 else None

            channel_summary.append(
                f"- {channel}: "
                f"spend {_format_currency(spend)}, "
                f"signups {signups:,}, "
                f"CAC "
                f"{_format_currency(channel_cac) if channel_cac is not None else 'not available'}"
            )

        performance_request = f"""
Analyze the ACTUAL performance of this marketing campaign.

Campaign: {c["name"]}
Product: {c["product"]}
Target audience: {c["audience"]}

CONFIGURED TARGETS:
- Signup target: {c["signup_target"]:,}
- Campaign duration: {c["duration_days"]} days
- Maximum target CAC: {_format_currency(c["maximum_cac"])}
- Configured budget: {c["budget"]}

ACTUAL CAMPAIGN DATA:
- Actual signups: {actual_signups:,}
- Actual visitors: {actual_visitors:,}
- Actual spend: {_format_currency(actual_spend)}
- Actual revenue: {_format_currency(actual_revenue)}
- Actual conversion rate: {
    f"{conversion_rate:.2f}%"
    if conversion_rate is not None
    else "not available"
}
- Actual CAC: {
    _format_currency(actual_cac)
    if actual_cac is not None
    else "not available"
}
- Actual ROAS: {
    f"{roas:.2f}x"
    if roas is not None
    else "not available"
}

ACTUAL CHANNEL DATA:
{chr(10).join(channel_summary)}

IMPORTANT DATA RULES:
1. Use ONLY the actual numbers supplied above.
2. Do NOT invent visitors, impressions, clicks, revenue, conversion rates,
   or ROAS for individual channels.
3. Channel CAC is spend divided by channel signups when signups are greater
   than zero.
4. Do NOT calculate a channel conversion rate because channel visitors are
   not collected on this page.
5. Do NOT calculate channel ROAS because channel revenue is not collected.
6. Clearly separate configured targets from actual results.
7. If a metric is unavailable, say "not available" rather than estimating it.

Provide:
1. Executive performance assessment.
2. KPI analysis against the configured target.
3. Actual campaign funnel interpretation.
4. Channel observations based only on supplied channel spend, signups and CAC.
5. Areas of underperformance.
6. Three concrete optimization actions.
7. Additional data that should be collected next.
8. Final recommendation.

Do not invent metrics or assumptions.
""".strip()

        try:
            with st.spinner("Analyzing actual campaign performance..."):
                result = run_existing_marketing_workflow(
                    performance_request
                )

            output = str(
                result.get("final_output", "") or ""
            ).strip()

            if not output:
                raise RuntimeError(
                    "The analytics workflow returned an empty result."
                )

            performance["analytics_ai_output"] = output
            performance["analytics_ai_agent"] = str(
                result.get(
                    "last_agent",
                    "Analytics & Optimization",
                )
                or "Analytics & Optimization"
            )
            _save_campaign_performance(performance)

            st.rerun()

        except Exception:
            fallback_output = _deterministic_analytics_fallback(c, performance)
            performance["analytics_ai_output"] = fallback_output
            performance["analytics_ai_agent"] = "Deterministic Analytics Fallback"
            _save_campaign_performance(performance)
            st.warning(
                "AI performance review was unavailable, so a deterministic review "
                "was generated from the saved actual campaign data."
            )
            st.rerun()

    analytics_ai_output = str(
        performance.get("analytics_ai_output", "") or ""
    ).strip()
    analytics_ai_agent = str(
        performance.get(
            "analytics_ai_agent",
            "Analytics & Optimization",
        )
        or "Analytics & Optimization"
    )

    if analytics_ai_output:
        st.write("")

        html(
            f"""
            <div class="section-card">
                <div class="card-title">AI Performance Review</div>
                <div class="card-subtitle">
                    Generated from actual performance data.
                    Specialist:
                    {escape(analytics_ai_agent)}
                </div>
            </div>
            """
        )

        with st.container(border=True):
            st.markdown(analytics_ai_output)

    # ------------------------------------------------------------
    # CURRENT CAMPAIGN INSIGHT
    # ------------------------------------------------------------
    st.write("")

    html(
        f"""
        <div class="section-card">
            <div class="card-title">Current Campaign Insight</div>
            <div class="card-subtitle">
                Configuration and actual performance are intentionally shown
                separately.
            </div>

            <div class="detail-block" style="margin-top:25px;">
                <div class="detail-label">Campaign</div>
                <div class="detail-value">
                    {escape(c["name"])}
                </div>
            </div>

            <div class="detail-block">
                <div class="detail-label">Status</div>
                <div class="detail-value">
                    {escape(st.session_state.campaign_status)}
                </div>
            </div>

            <div class="detail-block">
                <div class="detail-label">Data integrity note</div>
                <div class="detail-value">
                    Target values come from campaign configuration.
                    Actual signups, conversion rate, CAC and ROAS are
                    calculated only from performance data entered by the user.
                    Channel CAC is calculated only from channel spend and
                    channel signups. Missing values are displayed as — rather
                    than estimated.
                </div>
            </div>
        </div>
        """
    )


# ============================================================

# MEMORY
# ============================================================

def memory():
    page_header(
        "Persistent Context",
        "Campaign Memory",
        "View the campaign context currently supplied to the AI workflow.",
    )

    c = st.session_state.campaign

    html(
        f"""
        <div class="section-card">
            <div class="card-title">Campaign Memory</div>
            <div class="card-subtitle">
                Current context available to the AI Marketing Manager
            </div>

            <div class="detail-block" style="margin-top:25px;">
                <div class="detail-label">Campaign</div>
                <div class="detail-value">
                    {escape(c["name"])}
                </div>
            </div>

            <div class="detail-block">
                <div class="detail-label">Primary audience</div>
                <div class="detail-value">
                    {escape(c["audience"])}
                </div>
            </div>

            <div class="detail-block">
                <div class="detail-label">Preferred channels</div>
                <div class="detail-value">
                    {escape(c["channels"])}
                </div>
            </div>

            <div class="detail-block">
                <div class="detail-label">Current product</div>
                <div class="detail-value">
                    {escape(c["product"])}
                </div>
            </div>

            <div class="detail-block">
                <div class="detail-label">Goal</div>
                <div class="detail-value">
                    {escape(c["goal"])}
                </div>
            </div>
        </div>
        """
    )


# ============================================================
# HISTORY
# ============================================================

def history():
    page_header(
        "Campaign Archive",
        "Campaign History",
        "View campaigns and their saved strategy/review history. This data survives application restarts.",
    )

    campaigns_list = st.session_state.campaigns

    if not campaigns_list:
        html(
            """
            <div class="info-box">
                No campaign history exists in the current session yet.
            </div>
            """
        )
        return

    for index, item in enumerate(reversed(campaigns_list)):
        status = item.get("status", "Draft")

        badge_class = (
            "badge-approved"
            if status == "Approved"
            else (
                "badge-revision"
                if status == "Revision Required"
                else "badge-pending"
            )
        )

        html(
            f"""
            <div class="section-card" style="margin-bottom:12px;">
                <div class="campaign-row">
                    <div>
                        <div class="campaign-name">
                            {escape(item["name"])}
                        </div>
                        <div class="campaign-meta">
                            {escape(item["product"])}
                            · {escape(item["duration"])}
                            · {escape(item["audience"])}
                        </div>
                    </div>

                    <div class="campaign-budget">
                        {escape(item["budget"])}
                    </div>

                    <span class="{badge_class}">
                        {escape(status.upper())}
                    </span>
                </div>
            </div>
            """
        )

        strategy_versions = item.get("strategy_history") or []
        feedback_versions = item.get("feedback_history") or []
        approval_versions = item.get("approval_history") or []
        st.caption(
            f"Strategy revisions: {len(strategy_versions)} · "
            f"Human feedback entries: {len(feedback_versions)} · "
            f"Approval events: {len(approval_versions)}"
        )

        if strategy_versions:
            with st.expander("View saved strategy / revision history"):
                for version in strategy_versions:
                    st.markdown(
                        f"**Revision {version.get('revision', '?')}** · {version.get('generated_at', '')}"
                    )
                    if version.get("feedback"):
                        st.caption(f"Human feedback: {version['feedback']}")
                    st.markdown(version.get("strategy", ""))

        if feedback_versions:
            with st.expander("View human feedback history"):
                for entry in feedback_versions:
                    st.markdown(
                        f"**Revision {entry.get('revision', '?')}** · "
                        f"{entry.get('submitted_at', '')}: {entry.get('feedback', '')}"
                    )

        if st.button(
            "Open Campaign",
            key=f"open_history_{index}",
            use_container_width=True,
        ):
            _load_campaign_into_session(item)
            strategy = item.get("strategy_output", "")

            if strategy:
                st.session_state.strategy_output = strategy
                st.session_state.strategy_generated = True
            else:
                st.session_state.strategy_output = ""
                st.session_state.strategy_generated = False

            st.session_state.approved = bool(item.get("approved", False))
            st.session_state.campaign_status = item.get(
                "status",
                "Draft",
            )

            if st.session_state.strategy_generated:
                try:
                    st.session_state.approval_workflow = (
                        create_approval_workflow(
                            st.session_state.strategy_output
                        )
                    )
                except Exception:
                    st.session_state.approval_workflow = None

            navigate("Strategy Studio")
            st.rerun()


# ============================================================
# SETTINGS
# ============================================================

def settings():
    page_header(
        "System Configuration",
        "Settings",
        "Manage application and AI configuration.",
    )

    groq_configured = bool(os.getenv("GROQ_API_KEY"))
    model_name = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile",
    )

    left, right = st.columns(2)

    with left:
        html(
            f"""
            <div class="section-card">
                <div class="card-title">AI Configuration</div>

                <div class="detail-block" style="margin-top:25px;">
                    <div class="detail-label">Marketing Manager</div>
                    <div class="detail-value">
                        {"Connected" if groq_configured else "Not configured"}
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Existing Workflow</div>
                    <div class="detail-value">
                        app.services.marketing_workflow
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Model</div>
                    <div class="detail-value">
                        {escape(model_name)}
                    </div>
                </div>
            </div>
            """
        )

    with right:
        html(
            """
            <div class="section-card">
                <div class="card-title">Workspace</div>

                <div class="detail-block" style="margin-top:25px;">
                    <div class="detail-label">Workspace</div>
                    <div class="detail-value">
                        AI Marketing Manager
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">User Role</div>
                    <div class="detail-value">
                        Project Owner
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-label">Approval Workflow</div>
                    <div class="detail-value">
                        HumanApproval / ApprovalWorkflow
                    </div>
                </div>
            </div>
            """
        )


# ============================================================
# ROUTER
# ============================================================

if st.session_state.page == "Dashboard":
    dashboard()

elif st.session_state.page == "Campaigns":
    campaigns()

elif st.session_state.page == "Strategy Studio":
    strategy_studio()

elif st.session_state.page == "Approval Center":
    approval_center()

elif st.session_state.page == "Analytics":
    analytics()

elif st.session_state.page == "Memory":
    memory()

elif st.session_state.page == "History":
    history()

elif st.session_state.page == "Settings":
    settings()

else:
    dashboard()