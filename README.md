
# 🤖 AI Marketing Manager

> **OpenAI Agents SDK – Summer School '26 Capstone Project**

AI Marketing Manager is a multi-agent marketing strategy and analytics platform that helps users create, review, store, and analyze marketing campaigns using specialized AI agents, external tools, persistent memory, structured outputs, and human approval.

The application is built with Python and Streamlit and integrates AI agents, web research, campaign analytics, SQLite memory, and a human-in-the-loop workflow.

---

## 📌 Project Overview

Marketing teams need to perform multiple activities before and after launching a campaign, including:

- Market research
- Customer analysis
- Competitor analysis
- Marketing strategy creation
- Campaign planning
- Content planning
- Performance analysis
- Campaign optimization

Performing these tasks manually can be time-consuming and inconsistent.

**AI Marketing Manager** brings these activities together into a single AI-powered workspace.

Instead of relying on one general-purpose AI assistant, the system uses multiple specialized agents. Each agent is responsible for a specific marketing task and can use relevant tools and campaign context.

---

# 🎯 Problem Statement

Traditional marketing campaign planning involves collecting information from multiple sources, analyzing competitors, designing strategies, creating content plans, and monitoring performance.

This creates several challenges:

- Time-consuming manual research
- Fragmented marketing workflows
- Difficulty maintaining campaign context
- Inconsistent strategy generation
- Limited automation
- Manual analysis of campaign performance
- Lack of structured AI outputs
- Need for human review before final decisions

The proposed system addresses these challenges through a **multi-agent AI architecture**.

---

# 🎯 Objectives

The main objectives of the project are:

1. Build a practical multi-agent AI marketing system.
2. Divide marketing responsibilities among specialized AI agents.
3. Implement agent routing and handoffs.
4. Integrate external tools and APIs.
5. Generate structured and validated AI outputs.
6. Maintain persistent campaign memory.
7. Implement human approval and revision workflows.
8. Analyze campaign-performance data.
9. Generate AI-powered optimization recommendations.
10. Provide an easy-to-use Streamlit interface.

---

# ✨ Key Features

## 🤖 Multi-Agent AI System

The project contains six specialized marketing agents.

| Agent | Responsibility |
|---|---|
| **Marketing Planner** | Creates high-level marketing plans, goals, target audience and KPIs |
| **Market Research Agent** | Researches customer segments, trends, opportunities and pain points |
| **Competitor Analysis Agent** | Analyzes competitors, positioning, strengths, weaknesses and market gaps |
| **Campaign Planner Agent** | Creates campaign plans including channels, timelines, budgets and KPIs |
| **Content Strategist Agent** | Develops content direction, messaging and content ideas |
| **Analytics & Optimization Agent** | Analyzes campaign performance and generates optimization recommendations |

---

# 🏗️ Multi-Agent Architecture

```text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │ Marketing Manager │
                 │      / Router     │
                 └─────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   Marketing Planner  Market Research  Competitor Analysis
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                  Campaign Planner
                           │
                           ▼
                  Content Strategist
                           │
                           ▼
             Analytics & Optimization
                           │
                           ▼
                    Final Output
                           │
                           ▼
                   Human Approval
                      │       │
                  Approve   Revise
                      │       │
                      ▼       ▼
                  Final     Feedback
                 Strategy      │
                              ▼
                       Regenerate
````

---

# 🔄 End-to-End Workflow

```text
Campaign Input
      │
      ▼
Marketing Manager / Router
      │
      ▼
Specialized AI Agent
      │
      ├── Market Research
      ├── Competitor Analysis
      ├── Campaign Planning
      ├── Content Strategy
      └── Analytics
      │
      ▼
Tools / APIs
      │
      ▼
Structured Output
      │
      ▼
Human Review
      │
 ┌────┴────┐
 │         │
Approve   Revise
 │         │
 ▼         ▼
Final    Feedback
Output     │
           ▼
       Regenerate
```

---

# 🧠 Agent Routing & Handoffs

The Marketing Manager acts as the central routing layer.

It identifies the user's request and directs it to the appropriate specialist agent.

### Example

```text
"Create a marketing plan"
        ↓
Marketing Planner
```

```text
"Research customer pain points"
        ↓
Market Research Agent
```

```text
"Analyze our competitors"
        ↓
Competitor Analysis Agent
```

```text
"Create a campaign execution plan"
        ↓
Campaign Planner Agent
```

```text
"Give me social media content ideas"
        ↓
Content Strategist Agent
```

```text
"Analyze campaign performance"
        ↓
Analytics & Optimization Agent
```

This approach allows each agent to focus on a clearly defined responsibility.

---

# 🛠️ Tools & APIs

The project integrates multiple tools and services to extend agent capabilities.

## Main Tools

### 🔎 Web Research Tool

Used for collecting external market and research information.

### 🏢 Competitor Research Tool

Used for competitor-related research and analysis.

### 📊 Campaign Data Tool

Used to load and process campaign-performance data.

### 🧮 Calculator / Metrics Tool

Used for calculating marketing performance metrics.

### 📄 File Reader Tool

Used to read supported campaign-related files.

---

# 🔌 External Technologies

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| **OpenAI Agents SDK** | Agent and tool architecture  |
| **Groq**              | LLM inference                |
| **Tavily**            | Web research                 |
| **Streamlit**         | User interface               |
| **SQLite**            | Persistent memory            |
| **Pydantic**          | Structured output validation |
| **Plotly**            | Data visualization           |
| **Pandas**            | Data processing              |
| **Pytest**            | Testing                      |
| **python-dotenv**     | Environment configuration    |

---

# 📊 Analytics & Optimization

The system supports campaign-performance analysis using CSV data.

Typical campaign fields may include:

```text
channel
spend
cost
visits
sessions
clicks
impressions
signups
conversions
revenue
```

The system can calculate and analyze metrics such as:

* Total spend
* Clicks
* Impressions
* Visits
* Signups / conversions
* Conversion rate
* Cost per acquisition
* ROAS
* Channel performance

### Analytics Flow

```text
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
Analytics Agent
     │
     ▼
Optimization Recommendations
```

---

# 👤 Human-in-the-Loop

Human approval is an important part of the application.

AI-generated strategies are reviewed by the user before they are considered final.

```text
AI Generates Strategy
        │
        ▼
   Human Review
     /       \
    /         \
Approve       Revise
  │             │
  ▼             ▼
Final        Feedback
Strategy        │
                ▼
        Regenerate Strategy
                │
                ▼
          Human Review
```

This provides greater control over AI-generated marketing decisions.

---

# 🧠 Memory & Context Management

The application uses SQLite-based persistent memory to store campaign-related information.

The memory system can maintain:

* Campaign information
* Campaign context
* Previous outputs
* Campaign history
* Strategy versions
* Approval information
* Revision information

Example:

```text
Campaign
   │
   ▼
Campaign Context
   │
   ▼
Agent Execution
   │
   ▼
SQLite Memory
   │
   ├── Campaign History
   ├── Previous Strategy
   ├── User Context
   └── Approval / Revision Data
```

This allows the system to maintain context across interactions.

---

# 📋 Structured Outputs

The project uses Pydantic models to validate important AI outputs.

Structured outputs help ensure that agents return predictable and machine-readable information.

Examples include:

* Marketing Plan Output
* Market Research Output
* Competitor Analysis Output
* Campaign Plan Output

Instead of relying only on free-form text, structured schemas make the agent workflow more reliable.

---

# 🖥️ Application Interface

The Streamlit application provides an interactive workspace for the marketing workflow.

## Main Areas

### Campaigns

Create and manage marketing campaigns.

### AI Strategy Studio

Generate AI-powered marketing strategies.

### Approval Center

Review, approve, or request revisions to generated strategies.

### Analytics

Upload campaign data and analyze performance.

### Campaign Memory

View stored campaign context and information.

### Campaign History

Review previous campaign activities and generated outputs.

---

# 📁 Project Structure

```text
AI Marketing Manager/
│
├── app/
│   │
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
│
├── tests/
│
├── sample_campaign.txt
├── sample_campaign_data.csv
├── run_app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Marketing-Manager.git
cd AI-Marketing-Manager
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
TAVILY_API_KEY=your_tavily_api_key
```

If additional API keys are required by your local configuration, add them to `.env`.

### ⚠️ IMPORTANT

Never upload `.env` to GitHub.

Never expose:

```text
API Keys
Passwords
Access Tokens
Secret Keys
```

The repository should contain only placeholder values.

---

# ▶️ Run the Application

From the project root:

```bash
python run_app.py
```

Or run Streamlit directly:

```bash
streamlit run app/ui/myapp.py
```

The application will open in your browser.

---

# 🧪 Testing

Run the test suite with:

```bash
pytest -q
```

Individual components can also be tested separately.

Examples:

```bash
python test_calculate.py
```

```bash
python test_campaign_data.py
```

```bash
python test_market_research.py
```

```bash
python test_competitor_research.py
```

```bash
python test_file_reader.py
```

```bash
python test_web_research.py
```

API-based tests require valid environment variables.

---

# 📄 Sample Data

The project includes sample files that can be used for testing.

```text
sample_campaign.txt
sample_campaign_data.csv
```

The sample campaign data can be used to demonstrate the analytics workflow.

---

# 🧩 Technology Stack

```text
Frontend / UI
    ↓
Streamlit
    ↓
Python Application
    ↓
OpenAI Agents SDK
    ↓
Specialized AI Agents
    ↓
Tools / APIs
    ↓
Groq + Tavily
    ↓
SQLite Memory
    ↓
Analytics & Structured Outputs
```

---

# 🏆 Capstone Requirement Mapping

| Capstone Requirement | Implementation                                                                |
| -------------------- | ----------------------------------------------------------------------------- |
| Problem Analysis     | AI-assisted marketing planning and analytics                                  |
| Multi-Agent Design   | Six specialized AI agents                                                     |
| Agent Architecture   | Central Marketing Manager + specialist agents                                 |
| Agent Roles          | Planner, Research, Competitor, Campaign, Content, Analytics                   |
| Agent Handoffs       | Routing and specialist-agent handoffs                                         |
| Minimum 5 Tools/APIs | Research, competitor research, file reader, campaign data, calculator/metrics |
| Memory / Context     | SQLite Memory Manager                                                         |
| Structured Outputs   | Pydantic schemas                                                              |
| Human Approval       | Approval Center + revision workflow                                           |
| Error Handling       | Validation, fallback handling and logging                                     |
| Session Persistence  | Campaign memory/history                                                       |
| Analytics            | Campaign CSV analysis                                                         |
| UI                   | Streamlit application                                                         |

---

# 🔒 Security

The project is intended for educational and portfolio purposes.

Recommended security practices:

* Keep API keys inside `.env`.
* Never commit `.env`.
* Never commit `.venv`.
* Do not expose API keys in screenshots.
* Use sample/synthetic data in public repositories.
* Do not upload private campaign information.
* Rotate credentials if they are accidentally exposed.

---

# 🚀 Future Enhancements

The project can be extended with:

* Retrieval-Augmented Generation (RAG)
* Vector database integration
* Parallel agent execution
* Reflection and self-review
* Multimodal inputs
* PDF/document understanding
* Production database
* User authentication
* Role-based access
* Cloud deployment
* Advanced A/B testing
* Real-time dashboards
* Automated campaign execution
* Production monitoring and observability
* Advanced marketing-platform integrations

---

# 📸 Screenshots

Add your application screenshots inside a folder named:

```text
screenshots/
```

Recommended screenshots:

```text
screenshots/
│
├── dashboard.png
├── campaigns.png
├── strategy-studio.png
├── approval-center.png
├── analytics.png
├── channel-performance.png
├── campaign-memory.png
└── campaign-history.png
```


# 💡 Why This Project?

AI Marketing Manager demonstrates how multiple specialized AI agents can collaborate to solve a real-world business problem.

Instead of using a single AI chatbot, the project separates responsibilities into specialized agents:

```text
Planning
   +
Research
   +
Competitor Analysis
   +
Campaign Planning
   +
Content Strategy
   +
Analytics
   ↓
AI Marketing Manager
```

The project combines:

**Multi-Agent Architecture**

*

**Agent Routing & Handoffs**

*

**Tools & APIs**

*

**Structured Outputs**

*

**Persistent Memory**

*

**Human Approval**

*

**Analytics**

to create a practical AI-powered marketing assistant.

---

# 👨‍💻 Author

## Swanjal Rawat

**B.Tech Computer Science & Engineering**

**Summer School '26 – OpenAI Agents SDK Capstone Project**

---

# ⭐ Project Summary

**AI Marketing Manager** is a multi-agent AI platform designed to support the complete marketing campaign lifecycle.

It uses specialized AI agents for planning, research, competitor analysis, campaign planning, content strategy, and analytics.

The platform combines AI agent orchestration with external tools, persistent memory, structured outputs, analytics, and human approval.

This project demonstrates practical applications of **AI Agents, LLM orchestration, tool calling, memory management, structured outputs, human-in-the-loop systems, and AI-powered analytics.**

---


