# AI-Marketing-Stratergy-Manager

OpenAI Agents SDK – Summer School '26 Capstone Project

AI Marketing Manager is a multi-agent marketing workspace that helps users create, review, store, and analyze marketing campaigns through specialized AI agents, external tools, persistent memory, structured outputs, and a human approval workflow.

The project is implemented as a Streamlit application with Python and integrates Groq for LLM generation, optional Tavily web research, SQLite persistence, Pydantic validation, and campaign analytics.

📌 Project Overview

Marketing teams often need to perform several tasks before and after launching a campaign:

Understand the target audience and market

Research competitors and trends

Build a campaign strategy

Plan channels, budget and timelines

Create content directions

Analyze campaign performance

Revise strategies based on human feedback

Doing these tasks manually can be time-consuming and inconsistent.

AI Marketing Manager combines these responsibilities into a single AI-assisted workspace where specialized agents and tools handle different parts of the marketing workflow.

🎯 Objectives

The main objectives of the project are to:

Build a practical multi-agent AI marketing system.

Separate marketing responsibilities among specialized agents.

Integrate tools/APIs into the agent workflow.

Provide structured and validated AI outputs.

Maintain persistent campaign memory and history.

Include a human-in-the-loop approval and revision process.

Analyze real campaign-performance CSV data.

Generate optimization recommendations from campaign metrics.

Provide an easy-to-use Streamlit interface.

Demonstrate agent routing and handoff concepts using the OpenAI Agents SDK ecosystem.

✨ Key Features

🤖 Multi-Agent Marketing System

The project contains six specialist marketing agents:

Agent

Responsibility

Marketing Planner

Creates high-level marketing plans, goals, audiences, budget direction and KPIs

Market Research Agent

Identifies customer segments, needs, pain points, trends, opportunities and challenges

Competitor Analysis Agent

Studies competitors, strengths, weaknesses, market gaps and positioning opportunities

Campaign Planner Agent

Builds executable campaigns with channels, budget allocation, phases, KPIs and timelines

Content Strategist Agent

Develops content direction, messaging, themes and content ideas

Analytics & Optimization Agent

Reviews campaign performance and generates optimization recommendations

🔄 End-to-End Workflow

User
  │
  ▼
Campaign Details / Request
  │
  ▼
Marketing Manager / Router
  │
  ├──────────────► Marketing Planner
  ├──────────────► Market Research
  ├──────────────► Competitor Analysis
  ├──────────────► Campaign Planner
  ├──────────────► Content Strategist
  └──────────────► Analytics & Optimization
                         │
                         ▼
                  Structured Output
                         │
                         ▼
                  Human Approval
                    │         │
                 Approve     Revise
                    │         │
                    ▼         └──────► Regenerate
             Final Strategy
                    │
                    ▼
              Campaign Analytics
                    │
                    ▼
             Optimization Advice

🧠 Agent Routing & Handoffs

The project includes a Marketing Manager routing layer that identifies the intent of a request and transfers it to the appropriate specialist.

Examples:

"Create a marketing plan"
        ↓
Marketing Planner

"Research customer pain points"
        ↓
Market Research Agent

"Analyze our competitors"
        ↓
Competitor Analysis Agent

"Build a campaign execution plan"
        ↓
Campaign Planner Agent

"Give me social media content ideas"
        ↓
Content Strategist Agent

"Analyze campaign performance"
        ↓
Analytics & Optimization Agent

The routing implementation also includes a deterministic local fallback for selected routing cases when the LLM router is rate-limited.

🛠️ Tools & APIs

The project contains reusable tools implemented with agent function-tool patterns.

Current tools

Web Research Tool – performs optional web research through Tavily.

Competitor Research Tool – supports competitor research.

Campaign Data Tool – loads and processes campaign-performance data.

Campaign Metrics / Calculator Tool – calculates campaign metrics.

File Reader Tool – reads supported local campaign files.

External technologies

Groq API – LLM inference used by the current runtime workflow.

Tavily – optional web research.

OpenAI Agents SDK – agent/tool abstractions and project agent architecture.

SQLite – persistent local campaign memory.

Streamlit – application interface.

Plotly – analytics visualizations.

Pydantic – structured output validation.

📊 Analytics

The application supports CSV-based campaign analytics.

Typical supported fields include:

channel
spend / cost
visits / sessions
clicks
impressions
signups / conversions
revenue

The application can calculate metrics such as:

Spend

Clicks

Impressions

Visits

Signups / conversions

Conversion rate

Cost per acquisition / signup

ROAS when revenue is available

Channel-level performance

Example:

Campaign CSV
     │
     ▼
Data Processing
     │
     ▼
Metric Calculation
     │
     ▼
Performance Analysis
     │
     ▼
AI Optimization Recommendations

👤 Human-in-the-Loop Approval

AI-generated strategies are not treated as automatically final.

The application provides an approval workflow:

AI Strategy Generated
        │
        ▼
   Human Review
     /       \
    /         \
Approve       Revise
  │             │
  ▼             ▼
Final       Feedback
Strategy       │
               ▼
       Revised Strategy
               │
               ▼
         Human Review

This helps keep the system controllable and allows a human reviewer to check the strategy before final approval.

🧠 Persistent Memory

Campaign information and history are stored locally using SQLite.

The memory layer can store:

Campaign information

Campaign outputs

User context

Metadata

Campaign history

Strategy versions

Approval/revision information

Default database:

data/marketing_memory.db

The database is intentionally excluded from Git commits through .gitignore because it contains local runtime data.

📋 Structured Outputs

The project uses Pydantic schemas to validate important agent outputs.

Examples include:

MarketingPlanOutput

MarketResearchOutput

CompetitorAnalysisOutput

CampaignPlanOutput

Structured schemas help ensure that generated outputs contain the expected fields and reduce malformed responses.

The base schema configuration also forbids unexpected fields where applicable.

🖥️ Application Pages

The Streamlit application provides the following main areas:

Campaigns

Create and manage campaign information.

AI Strategy Studio

Generate an AI-powered marketing strategy from the selected campaign.

Approval Center

Review, approve, or request revisions to generated strategies.

Analytics

Upload campaign-performance data and analyze KPIs.

Campaign Memory

Inspect persistent campaign context and stored information.

Campaign History

Review previous campaign activity and strategy/approval history.

📁 Project Structure

AI Marketing Manager/
│
├── app/
│   ├── agents/
│   │   └── handoff_agents.py
│   │
│   ├── approval/
│   │   ├── approval.py
│   │   ├── human_approval.py
│   │   └── workflow_integration.py
│   │
│   ├── marketing_agents/
│   │   ├── planner.py
│   │   ├── market_research.py
│   │   ├── competitor_analysis.py
│   │   ├── campaign_planner.py
│   │   ├── content_strategist.py
│   │   └── analytics_optimizer.py
│   │
│   ├── memory/
│   │   └── memory_manager.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── services/
│   │   └── marketing_workflow.py
│   │
│   ├── tools/
│   │   ├── calculator.py
│   │   ├── campaign_data.py
│   │   ├── competitor_research.py
│   │   ├── file_reader.py
│   │   └── web_research.py
│   │
│   └── ui/
│       ├── myapp.py
│       └── campaigns.json
│
├── data/
│   └── marketing_memory.db
│
├── tests/
│   └── test_memory_manager.py
│
├── sample_campaign.txt
├── sample_campaign_data.csv
├── run_app.py
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/AI-Marketing-Manager.git
cd AI-Marketing-Manager

Replace YOUR_USERNAME with your GitHub username.

2. Create a virtual environment

Windows PowerShell

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

🔐 Environment Variables

Create a local .env file in the project root.

Example:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
TAVILY_API_KEY=your_tavily_api_key

If another API key is required by a particular tool or local configuration, add it to .env as well.

⚠️ Security

Never commit .env to GitHub.

The repository .gitignore excludes:

.env
.venv/
data/*.db
__pycache__/

If an API key has ever been accidentally exposed, revoke/rotate it before publishing the repository.

▶️ Run the Application

From the project root:

python run_app.py

Alternatively:

streamlit run app/ui/myapp.py

The application will open in your browser through Streamlit.

🧪 Testing

The project contains unit and integration-style tests for several components.

Run:

pytest -q

Individual tests can also be run, for example:

python test_calculate.py
python test_campaign_data.py
python test_market_research.py
python test_competitor_research.py
python test_file_reader.py
python test_web_research.py

Some tests depend on external APIs and valid credentials.

For API-based tests, make sure the relevant keys are configured in .env.

📄 Sample Data

The repository includes:

sample_campaign.txt
sample_campaign_data.csv

These can be used to test campaign creation and analytics functionality without creating a dataset from scratch.

🧩 Technology Stack

Technology

Purpose

Python

Core application language

OpenAI Agents SDK

Agent/tool architecture

Groq

LLM inference

Tavily

Optional web research

Streamlit

Web interface

SQLite

Persistent memory

Pydantic

Structured output validation

Plotly

Analytics visualization

Pandas / CSV processing

Campaign data analysis

Pytest

Testing

python-dotenv

Environment configuration

🏗️ Capstone Requirement Mapping

Requirement

Project Implementation

Problem Analysis

AI-assisted marketing planning and analytics problem

Multi-Agent Design

Six specialized marketing agents

Agent Roles

Planner, Research, Competitor, Campaign, Content, Analytics

Agent Handoffs

Marketing Manager routing and specialist transfer

Minimum 5 Tools/APIs

Web research, competitor research, file reader, campaign data, calculator/metrics

Memory / Context

SQLite MemoryManager

Structured Outputs

Pydantic schemas

Human Approval

Approval Center + revision workflow

Error Handling

Validation, rate-limit handling and fallback routing

Session Persistence

Campaign memory/history

Analytics

CSV-based campaign performance analysis

UI

Streamlit workspace

🔒 Security Considerations

This project is designed for local development and academic/portfolio demonstration.

Recommended practices:

Keep API keys in .env.

Never commit secrets.

Keep .venv outside Git tracking.

Do not upload local SQLite databases containing private data.

Use synthetic/sample campaign data for public repositories.

Rotate any accidentally exposed credentials.

🚀 Future Enhancements

Possible future improvements include:

Retrieval-Augmented Generation (RAG) with a dedicated vector database.

Parallel execution of independent specialist agents.

More advanced reflection/self-review loops.

Multimodal campaign inputs such as images and PDFs.

Production database instead of local SQLite.

Authentication and role-based access.

Cloud deployment.

Automated campaign execution through external marketing platforms.

More advanced experiment/A-B testing support.

Real-time marketing dashboards.

Observability, tracing and production-level logging.

📸 Recommended Screenshots

For the project documentation and GitHub README, add screenshots such as:

screenshots/
├── dashboard.png
├── campaigns.png
├── strategy-studio.png
├── approval-center.png
├── analytics.png
├── channel-performance.png
├── campaign-memory.png
└── campaign-history.png


👨‍💻 Author

Swanjal Rawat

B.Tech Computer Science & Engineering
Summer School '26 – OpenAI Agents SDK Capstone Project

⭐ Project Summary

AI Marketing Manager demonstrates how specialized AI agents can work together to support a complete marketing workflow.

Instead of relying on one general-purpose chatbot, the system separates responsibilities across marketing planning, market research, competitor analysis, campaign planning, content strategy, and analytics.

The combination of:

Multi-Agent Routing + Tools/APIs + Structured Outputs + Memory + Human Approval + Analytics

makes the project suitable as a portfolio demonstration of practical AI-agent engineering.

