<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/LangGraph-Stateful_Agent-00A67E?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/Playwright-Browser_Automation-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector_Memory-FF6F00?style=for-the-badge&logo=databricks&logoColor=white" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/n8n-Workflow_Orchestration-EA4B71?style=for-the-badge&logo=n8n&logoColor=white" alt="n8n"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

# 🤖 Autonomous Browser Automation Agent

> **An intelligent, self-correcting AI agent that autonomously navigates websites, interacts with web elements, extracts information, and completes multi-step browser tasks using reasoning, planning, and memory.**

Unlike traditional automation scripts that follow rigid, predefined steps and break at the slightest UI change, this project leverages **Agentic AI** — combining LLM-powered reasoning, dynamic planning, tool calling, and self-correction — to build a browser agent that **adapts** to changing web pages and **recovers** from failures autonomously.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [How It Works — The ReAct Loop](#-how-it-works--the-react-loop)
- [Tech Stack](#-tech-stack)
- [Component Deep Dive](#-component-deep-dive)
- [Example Use Cases](#-example-use-cases)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Running the Project](#-running-the-project)
- [API Reference — Available Tools](#-api-reference--available-tools)
- [Workflow Orchestration with n8n](#-workflow-orchestration-with-n8n)
- [Memory Architecture](#-memory-architecture)
- [Error Handling & Self-Correction](#-error-handling--self-correction)
- [Performance Considerations](#-performance-considerations)
- [Security Best Practices](#-security-best-practices)
- [Troubleshooting](#-troubleshooting)
- [Skills Demonstrated](#-skills-demonstrated)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

The **Autonomous Browser Automation Agent** is a production-grade Agentic AI system that goes beyond simple chatbot interactions into **real-world autonomous execution environments**. It can:

- 🌐 **Navigate** complex, multi-page websites autonomously
- 🧠 **Reason** about what actions to take based on the current page state
- 🔧 **Use tools** dynamically (click, type, scroll, extract, screenshot)
- 📝 **Plan** multi-step workflows and decompose complex goals into sub-tasks
- 🔄 **Self-correct** by reflecting on failures and replanning on-the-fly
- 💾 **Remember** past interactions using vector-based long-term memory
- 📊 **Extract** structured data from websites intelligently

### Why Agentic AI for Browser Automation?

| Aspect | Traditional Scripts (Selenium/etc.) | This Agentic Approach |
|---|---|---|
| **Adaptability** | ❌ Breaks on UI changes | ✅ Adapts via LLM reasoning |
| **Error Recovery** | ❌ Fails and stops | ✅ Reflects, retries, replans |
| **Planning** | ❌ Fixed linear steps | ✅ Dynamic multi-step planning |
| **Learning** | ❌ No memory | ✅ Vector memory across sessions |
| **Maintenance** | ❌ Constant script updates | ✅ Self-healing automation |
| **Complex Tasks** | ❌ Requires manual scripting | ✅ Natural language instructions |

---

## ✨ Key Features

### 🧠 Core Intelligence
- **AI-Powered Task Planning** — The LLM decomposes high-level goals into executable sub-tasks
- **ReAct Reasoning Loop** — Iterative Thought → Action → Observation cycle for robust execution
- **Dynamic Tool Selection** — The agent autonomously decides which browser tool to invoke
- **Contextual Decision Making** — Actions are based on real-time analysis of page content and state

### 🌐 Browser Automation
- **Autonomous Navigation** — Navigate across pages, handle redirects, manage tabs
- **Element Interaction** — Click buttons, fill forms, select dropdowns, handle modals
- **Data Extraction** — Scrape structured and unstructured data from any web page
- **Screenshot Capture** — Visual logging of browser state at every step for debugging
- **Cross-Browser Support** — Works with Chromium, Firefox, and WebKit engines

### 🔄 Resilience & Self-Correction
- **Error Detection** — Automatic identification of failed actions and unexpected states
- **Reflection Engine** — Post-failure analysis to understand why an action failed
- **Retry Mechanisms** — Intelligent retry with alternative strategies, not blind repetition
- **Dynamic Replanning** — Complete plan revision when the original approach is unviable

### 💾 Memory & State
- **Short-Term Memory** — Conversation history and session context via LangGraph checkpointing
- **Long-Term Memory** — Persistent vector storage in ChromaDB for cross-session knowledge
- **Semantic Retrieval** — Embedding-based memory lookup for relevant past experiences
- **State Persistence** — Full agent state serialization for pause/resume capabilities

### 🔗 Workflow Orchestration
- **n8n Integration** — Visual workflow design for complex multi-agent pipelines
- **Trigger-Based Execution** — Schedule or event-driven agent invocation
- **Multi-Agent Coordination** — Chain multiple specialized agents for complex tasks
- **External Service Integration** — Connect to databases, APIs, and notification systems

### 📈 Monitoring & Observability
- **LangSmith Tracing** — Full agent decision trace for debugging and optimization
- **Step-by-Step Logging** — Detailed logs of every reasoning step and action taken
- **Performance Metrics** — Track execution time, token usage, and success rates
- **Visual Debugging** — Screenshot timeline of the agent's browser interactions

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                    (Natural Language Goal)                           │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    LLM REASONING AGENT                              │
│               (Groq / Llama 3 — The "Brain")                        │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │   Thought    │→ │   Action     │→ │     Observation           │  │
│  │  (Reasoning) │  │ (Tool Call)  │  │  (Page State Analysis)    │  │
│  └──────┬───────┘  └──────────────┘  └───────────────────────────┘  │
│         │                                          │                │
│         └──────────← ReAct Loop ←──────────────────┘                │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     PLANNING ENGINE                                 │
│                                                                     │
│  ┌────────────────────┐  ┌────────────────────────────────────────┐  │
│  │ Task Decomposition │  │  Dynamic Plan Adjustment               │  │
│  │ (Goal → Sub-tasks) │  │  (Replan on failure/new info)          │  │
│  └────────────────────┘  └────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TOOL LAYER                                     │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Navigate  │ │ Click    │ │  Type    │ │ Extract  │ │Screenshot│  │
│  │  URL     │ │ Element  │ │  Text    │ │  Data    │ │ Capture  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Scroll   │ │ Wait     │ │  Select  │ │ Upload   │ │  Back /  │  │
│  │  Page    │ │ Element  │ │ Dropdown │ │  File    │ │ Forward  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 BROWSER CONTROLLER (Playwright)                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │  • Chromium / Firefox / WebKit Engine Support                  │ │
│  │  • Headless & Headful Mode                                    │ │
│  │  • Auto-Waiting for Element Readiness                         │ │
│  │  • Isolated Browser Contexts (Parallel Execution)             │ │
│  │  • Network Interception & Request Mocking                     │ │
│  │  • DOM Snapshot & Accessibility Tree Access                   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   OBSERVATION LAYER                                  │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐   │
│  │  DOM Analysis   │  │  Text Extraction │  │  Screenshot       │   │
│  │  & Parsing      │  │  & Structuring   │  │  Comparison       │   │
│  └─────────────────┘  └──────────────────┘  └───────────────────┘   │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────┬─────────────────────────────┐
│       REFLECTION ENGINE               │      MEMORY SYSTEM          │
│                                       │                             │
│  ┌─────────────────────────────────┐  │  ┌───────────────────────┐  │
│  │ • Analyze failure root cause    │  │  │ Short-Term Memory     │  │
│  │ • Generate correction strategy  │  │  │ (LangGraph State)     │  │
│  │ • Evaluate alternative paths    │  │  ├───────────────────────┤  │
│  │ • Update confidence scores      │  │  │ Long-Term Memory      │  │
│  └─────────────────────────────────┘  │  │ (ChromaDB Vectors)    │  │
│                                       │  └───────────────────────┘  │
└───────────────────────────┬───────────┴─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    OUTPUT & INTEGRATION                              │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  Final   │ │  JSON    │ │  n8n     │ │ LangSmith│ │  FastAPI  │  │
│  │  Report  │ │  Export  │ │ Webhook  │ │  Trace   │ │ Endpoint  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 How It Works — The ReAct Loop

The agent follows the **ReAct (Reasoning + Acting)** pattern, which is the fundamental control loop that transforms a static LLM into an autonomous agent. Instead of attempting to solve a problem in one shot, the agent iterates until the goal is achieved:

```
┌─────────────────────────────────────────────────────┐
│                    USER GOAL                         │
│       "Find the cheapest flight from NYC to LA"     │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
     ┌────→│   💭 THOUGHT          │
     │     │   (LLM Reasoning)     │
     │     │                       │
     │     │ "I need to navigate   │
     │     │  to a flight search   │
     │     │  website first."      │
     │     └───────────┬───────────┘
     │                 │
     │                 ▼
     │     ┌───────────────────────┐
     │     │   ⚡ ACTION           │
     │     │   (Tool Execution)    │
     │     │                       │
     │     │ navigate_to_url(      │
     │     │   "google.com/flights"│
     │     │ )                     │
     │     └───────────┬───────────┘
     │                 │
     │                 ▼
     │     ┌───────────────────────┐
     │     │   👁️ OBSERVATION      │
     │     │   (Result Analysis)   │
     │     │                       │
     │     │ "Page loaded. I see   │
     │     │  search fields for    │
     │     │  origin, destination, │
     │     │  and dates."          │
     │     └───────────┬───────────┘
     │                 │
     │                 ▼
     │     ┌───────────────────────┐
     │     │   🔄 CONTINUE?        │
     │     │                       │
     │  YES│ Goal achieved? ───── NO ──→ Loop Back
     │     │                       │          │
     │     └───────────┬───────────┘          │
     │                 │                      │
     └─────────────────┘──────────────────────┘
                       │
                  (When YES)
                       │
                       ▼
           ┌───────────────────────┐
           │   ✅ FINAL OUTPUT     │
           │   Structured result   │
           │   with extracted data │
           └───────────────────────┘
```

### Detailed Step Walkthrough

| Step | Phase | What Happens | Example |
|------|-------|-------------|---------|
| 1 | **Thought** | LLM analyzes the goal and current state | *"I need to search for flights. Let me navigate to a travel site."* |
| 2 | **Action** | Agent selects and executes a tool | `navigate_to_url("google.com/flights")` |
| 3 | **Observation** | System captures the result and page state | *"Page loaded successfully. Search form is visible."* |
| 4 | **Thought** | LLM reasons about next steps | *"Now I need to enter NYC as origin and LA as destination."* |
| 5 | **Action** | Agent fills in the form fields | `type_text(selector="#origin", text="NYC")` |
| 6 | **Observation** | System confirms the action result | *"Text entered. Autocomplete suggestions appeared."* |
| ... | **Loop** | Continues until goal is achieved or max iterations reached | *Selects dates, clicks search, extracts results...* |
| N | **Output** | Final structured result is returned | *"Cheapest flight: $149, Delta, 5h 30m, departing 8:00 AM"* |

---

## 🛠 Tech Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|---|---|---|---|
| **LLM** | Groq / Llama 3 | Latest | Reasoning, planning, and decision-making engine |
| **Agent Framework** | LangGraph | ≥0.2.x | Stateful graph-based agent orchestration with cycles and branching |
| **Tool Integration** | LangChain | ≥0.2.x | Tool calling, prompt templates, output parsing, and chain composition |
| **Browser Engine** | Playwright | ≥1.40.x | Cross-browser automation with auto-waiting and network interception |
| **Vector Memory** | ChromaDB | ≥0.4.x | Persistent embedding-based long-term memory storage |
| **Workflow Engine** | n8n | Latest | Visual workflow orchestration, scheduling, and external integrations |
| **Observability** | LangSmith | Latest | Agent tracing, debugging, evaluation, and performance monitoring |
| **API Layer** | FastAPI | ≥0.100.x | RESTful API for programmatic agent invocation |
| **Runtime** | Python | 3.10+ | Core implementation language |
| **Containerization** | Docker | Latest | Reproducible deployment and environment isolation |

### Why These Technologies?

<details>
<summary><b>🧠 Groq / Llama 3 — Lightning-Fast Inference</b></summary>

Groq provides **ultra-low-latency inference** for Llama 3 models, making real-time browser agent reasoning practical. With inference speeds of 500+ tokens/second, the agent can make rapid decisions without the latency bottleneck that plagues cloud-hosted LLMs. Llama 3's strong instruction-following and tool-calling capabilities make it ideal for agentic applications.

</details>

<details>
<summary><b>📊 LangGraph — Stateful Agent Orchestration</b></summary>

LangGraph is purpose-built for **stateful, multi-step agentic workflows** with cycles. Unlike simple LangChain chains that are linear and stateless, LangGraph provides:
- **Graph-based state machines** with nodes, edges, and conditional routing
- **Built-in checkpointing** for conversation persistence and pause/resume
- **Human-in-the-loop** capabilities for agent supervision
- **Streaming support** for real-time agent status updates
- **First-class support for cycles** — essential for the ReAct loop

</details>

<details>
<summary><b>🌐 Playwright — Modern Browser Automation</b></summary>

Playwright surpasses Selenium with its **modern architecture**:
- **Direct WebSocket connections** to the browser (bypassing the slower HTTP-based WebDriver protocol)
- **Auto-waiting** for elements to be actionable — dramatically reduces flakiness
- **Isolated browser contexts** — run parallel sessions without state interference
- **Cross-browser support** — Chromium, Firefox, and WebKit from a single API
- **Network interception** — mock/modify requests for testing edge cases
- **Trace Viewer** — full timeline recordings with DOM snapshots for debugging

</details>

<details>
<summary><b>💾 ChromaDB — Semantic Vector Memory</b></summary>

ChromaDB provides the agent's **long-term memory** through embedding-based storage:
- **Semantic similarity search** — retrieve relevant past experiences, not just exact matches
- **Persistent storage** — memories survive across sessions and restarts
- **Namespace support** — organize memories by task type, user, or domain
- **Lightweight & local** — no external service dependencies for development

</details>

<details>
<summary><b>🔗 n8n — Visual Workflow Orchestration</b></summary>

n8n enables **complex multi-agent pipeline orchestration** with 70+ AI nodes:
- **AI Agent Node** — autonomous tool selection driven by LLM reasoning
- **Multi-agent systems** — chain specialized agents with branching and conditional logic
- **400+ integrations** — connect to databases, APIs, email, Slack, and more
- **Visual workflow designer** — build and debug complex pipelines without code
- **Trigger-based execution** — schedule, webhook, or event-driven agent invocation

</details>

---

## 🔬 Component Deep Dive

### 1. LLM Reasoning Agent

The reasoning agent is the **central intelligence** of the system. It receives the current state (page content, action history, memory context) and produces structured decisions:

```python
# Conceptual example — Agent reasoning step
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation history
    current_url: str                          # Current browser URL
    page_content: str                         # Extracted page text
    screenshots: list[str]                    # Base64 screenshot history
    plan: list[str]                           # Current task plan
    memory_context: list[str]                 # Retrieved long-term memories

# The agent node processes state and returns tool calls
def agent_node(state: AgentState) -> AgentState:
    # LLM analyzes state and decides next action
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### 2. Planning Engine

The planning engine handles **task decomposition** — breaking high-level goals into actionable steps:

```
User Goal: "Research and compare the top 3 laptops under $1000"

Decomposed Plan:
├── Step 1: Navigate to a tech review website
├── Step 2: Search for "best laptops under $1000"
├── Step 3: Extract top 3 laptop names and prices
├── Step 4: For each laptop:
│   ├── Step 4.1: Navigate to product page
│   ├── Step 4.2: Extract specifications
│   └── Step 4.3: Extract user ratings
├── Step 5: Compare specifications side-by-side
└── Step 6: Generate summary report with recommendation
```

### 3. Browser Controller (Playwright)

Playwright manages the actual browser instance with enterprise-grade reliability:

```python
# Browser initialization with optimal settings
async with async_playwright() as p:
    browser = await p.chromium.launch(
        headless=True,            # Run without visible UI
        args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    )
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 ...',
        locale='en-US'
    )
    page = await context.new_page()
```

### 4. Reflection Engine

When an action fails, the reflection engine **analyzes the failure** and suggests corrections:

```
Failed Action: click_element(selector="#buy-now-btn")
Error: Element not found

Reflection Analysis:
├── Possible Cause: Button may have a different selector on this page version
├── Alternative Strategy 1: Search by text content "Buy Now"
├── Alternative Strategy 2: Search by role (button) with accessible name
├── Alternative Strategy 3: Take screenshot and analyze visually
└── Selected: Strategy 1 — click_element(text="Buy Now")
```

---

## 💡 Example Use Cases

### 🔍 Web Research Agent
Automate complex research tasks that would take hours manually.

| Task | Actions | Output |
|------|---------|--------|
| Topic Research | Search multiple sources, navigate articles, extract key points | Structured research summary |
| Competitive Analysis | Visit competitor websites, extract pricing and features | Comparison spreadsheet |
| News Aggregation | Monitor news sites, extract headlines and summaries | Daily news digest |

### 🛒 E-Commerce Automation
Intelligent shopping assistant that adapts to different e-commerce platforms.

| Task | Actions | Output |
|------|---------|--------|
| Price Comparison | Search products across multiple stores, extract prices | Best deal recommendation |
| Price Monitoring | Periodically check prices, detect drops | Price alert notification |
| Spec Extraction | Navigate product pages, extract detailed specifications | Structured product database |

### 📝 Job Application Assistant
Streamline the job search and application process.

| Task | Actions | Output |
|------|---------|--------|
| Job Search | Search portals, filter by criteria, extract listings | Curated job list |
| Form Filling | Navigate to application pages, fill in personal details | Completed applications |
| Application Tracking | Visit portal dashboards, extract application statuses | Status tracking spreadsheet |

### 📊 Analytics & Reporting
Automate data collection from web dashboards and portals.

| Task | Actions | Output |
|------|---------|--------|
| Dashboard Scraping | Login to analytics platforms, navigate to reports | Extracted metrics dataset |
| Report Download | Authenticate, navigate to downloads, save reports | Downloaded PDF/CSV files |
| KPI Monitoring | Check dashboards periodically, extract key metrics | Timeseries KPI database |

### 🧪 QA & Testing Agent
Intelligent quality assurance that goes beyond scripted tests.

| Task | Actions | Output |
|------|---------|--------|
| Workflow Validation | Navigate critical user journeys, verify expected outcomes | Pass/fail test report |
| Regression Testing | Compare current UI state with baseline screenshots | Visual diff report |
| Accessibility Audit | Check ARIA labels, contrast ratios, keyboard navigation | Accessibility compliance report |
| Load Testing | Execute user flows under various conditions | Performance metrics report |

---

## 📁 Project Structure

```
browser-automation-agent/
│
├── 📄 main.py                     # Application entry point
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env                        # Environment variables (not in git)
├── 📄 .env.example                # Template for environment variables
├── 📄 Dockerfile                  # Container configuration
├── 📄 docker-compose.yml          # Multi-service orchestration
├── 📄 README.md                   # This file
│
├── 📁 agent/                      # Core agent implementation
│   ├── 📄 __init__.py
│   ├── 📄 graph.py                # LangGraph state machine definition
│   ├── 📄 state.py                # Agent state schema (TypedDict)
│   ├── 📄 nodes.py                # Graph node functions (agent, tools, reflect)
│   ├── 📄 edges.py                # Conditional edge routing logic
│   └── 📄 prompts.py              # System prompts and prompt templates
│
├── 📁 tools/                      # Browser automation tools
│   ├── 📄 __init__.py
│   ├── 📄 navigation.py           # URL navigation, back/forward, tab management
│   ├── 📄 interaction.py          # Click, type, select, scroll, upload
│   ├── 📄 extraction.py           # Text extraction, data scraping, parsing
│   ├── 📄 screenshot.py           # Screenshot capture and comparison
│   └── 📄 validation.py           # Page state validation and assertions
│
├── 📁 memory/                     # Memory management
│   ├── 📄 __init__.py
│   ├── 📄 short_term.py           # LangGraph checkpointer configuration
│   ├── 📄 long_term.py            # ChromaDB vector store integration
│   └── 📄 embeddings.py           # Sentence transformer embedding config
│
├── 📁 planning/                   # Task planning and decomposition
│   ├── 📄 __init__.py
│   ├── 📄 planner.py              # Goal → sub-task decomposition
│   └── 📄 replanner.py            # Dynamic plan adjustment on failure
│
├── 📁 reflection/                 # Error analysis and self-correction
│   ├── 📄 __init__.py
│   ├── 📄 analyzer.py             # Failure root cause analysis
│   └── 📄 corrector.py            # Strategy generation for recovery
│
├── 📁 api/                        # FastAPI REST interface
│   ├── 📄 __init__.py
│   ├── 📄 routes.py               # API endpoint definitions
│   ├── 📄 schemas.py              # Request/response Pydantic models
│   └── 📄 middleware.py           # Auth, CORS, rate limiting
│
├── 📁 workflows/                  # n8n workflow definitions
│   ├── 📄 research_agent.json     # Web research workflow
│   ├── 📄 price_monitor.json      # E-commerce monitoring workflow
│   └── 📄 qa_testing.json         # Automated QA workflow
│
├── 📁 config/                     # Configuration files
│   ├── 📄 settings.py             # Application settings
│   ├── 📄 logging.py              # Logging configuration
│   └── 📄 browser.py              # Playwright browser settings
│
├── 📁 logs/                       # Execution logs (gitignored)
│   ├── 📁 screenshots/            # Captured screenshots
│   ├── 📁 traces/                 # LangSmith trace exports
│   └── 📁 runs/                   # Per-run execution logs
│
└── 📁 tests/                      # Test suite
    ├── 📄 test_agent.py           # Agent integration tests
    ├── 📄 test_tools.py           # Tool unit tests
    ├── 📄 test_memory.py          # Memory system tests
    └── 📄 test_planning.py        # Planning engine tests
```

---

## ⚙ Installation & Setup

### Prerequisites

| Requirement | Minimum Version | Check Command |
|---|---|---|
| Python | 3.10+ | `python --version` |
| pip | 23.0+ | `pip --version` |
| Node.js (for n8n) | 18+ | `node --version` |
| Docker (optional) | 20.0+ | `docker --version` |
| Git | 2.30+ | `git --version` |

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/browser-automation-agent.git
cd browser-automation-agent
```

### Step 2: Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browser Engines

```bash
# Install all supported browsers
playwright install

# Or install specific browsers only
playwright install chromium
playwright install firefox
playwright install webkit
```

### Step 5: (Optional) Install n8n for Workflow Orchestration

```bash
npm install -g n8n
```

### Step 6: (Optional) Docker Setup

```bash
# Build the Docker image
docker build -t browser-agent .

# Or use Docker Compose for multi-service setup
docker-compose up -d
```

---

## 🔐 Configuration

### Environment Variables

Create a `.env` file in the project root (use `.env.example` as a template):

```env
# ═══════════════════════════════════════════════
# LLM Configuration
# ═══════════════════════════════════════════════
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama3-70b-8192
TEMPERATURE=0.1
MAX_TOKENS=4096

# ═══════════════════════════════════════════════
# LangChain / LangSmith Configuration
# ═══════════════════════════════════════════════
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=browser-automation-agent

# ═══════════════════════════════════════════════
# Browser Configuration
# ═══════════════════════════════════════════════
BROWSER_HEADLESS=true
BROWSER_TIMEOUT=30000
BROWSER_VIEWPORT_WIDTH=1920
BROWSER_VIEWPORT_HEIGHT=1080

# ═══════════════════════════════════════════════
# Memory Configuration
# ═══════════════════════════════════════════════
CHROMADB_PERSIST_DIR=./data/chromadb
EMBEDDING_MODEL=all-MiniLM-L6-v2

# ═══════════════════════════════════════════════
# Agent Configuration
# ═══════════════════════════════════════════════
MAX_ITERATIONS=25
RETRY_LIMIT=3
SCREENSHOT_ON_EVERY_STEP=true

# ═══════════════════════════════════════════════
# API Configuration
# ═══════════════════════════════════════════════
API_HOST=0.0.0.0
API_PORT=8000
API_KEY=your_api_key_here
```

### Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | *Required* | API key for Groq LLM inference |
| `MODEL_NAME` | `llama3-70b-8192` | LLM model identifier |
| `TEMPERATURE` | `0.1` | LLM temperature (lower = more deterministic) |
| `MAX_TOKENS` | `4096` | Maximum tokens per LLM response |
| `LANGCHAIN_TRACING_V2` | `true` | Enable LangSmith tracing |
| `BROWSER_HEADLESS` | `true` | Run browser without visible UI |
| `BROWSER_TIMEOUT` | `30000` | Max wait time for page load (ms) |
| `MAX_ITERATIONS` | `25` | Maximum ReAct loop iterations |
| `RETRY_LIMIT` | `3` | Max retries per failed action |
| `SCREENSHOT_ON_EVERY_STEP` | `true` | Capture screenshot after each action |

---

## 🚀 Running the Project

### Quick Start

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Run the agent
python main.py
```

### Run with FastAPI Server

```bash
# Start the API server
uvicorn api.routes:app --host 0.0.0.0 --port 8000 --reload
```

### Run with Docker

```bash
# Using Docker
docker run -it --env-file .env browser-agent

# Using Docker Compose (includes n8n + ChromaDB)
docker-compose up
```

### Example API Request

```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "goal": "Search for the latest AI news on TechCrunch and extract the top 5 headlines",
    "max_iterations": 15,
    "headless": true
  }'
```

---

## 🔧 API Reference — Available Tools

The agent has access to the following browser automation tools, which it selects autonomously based on the task:

### Navigation Tools

| Tool | Parameters | Description |
|---|---|---|
| `navigate_to_url` | `url: str` | Navigate to a specific URL |
| `go_back` | — | Navigate to the previous page |
| `go_forward` | — | Navigate to the next page |
| `refresh_page` | — | Reload the current page |
| `open_new_tab` | `url: str` | Open a URL in a new browser tab |
| `switch_tab` | `index: int` | Switch to a specific tab by index |

### Interaction Tools

| Tool | Parameters | Description |
|---|---|---|
| `click_element` | `selector: str` | Click on a web element |
| `type_text` | `selector: str, text: str` | Type text into an input field |
| `select_dropdown` | `selector: str, value: str` | Select an option from a dropdown |
| `scroll_page` | `direction: str, amount: int` | Scroll the page up/down |
| `hover_element` | `selector: str` | Hover over an element |
| `upload_file` | `selector: str, path: str` | Upload a file to a file input |
| `press_key` | `key: str` | Press a keyboard key (Enter, Tab, etc.) |

### Extraction Tools

| Tool | Parameters | Description |
|---|---|---|
| `extract_text` | `selector: str` | Extract text content from an element |
| `extract_all_text` | — | Extract all visible text from the page |
| `extract_links` | `selector: str` | Extract all hyperlinks from the page |
| `extract_table` | `selector: str` | Extract a table into structured data |
| `get_page_title` | — | Get the current page title |
| `get_current_url` | — | Get the current page URL |

### Observation Tools

| Tool | Parameters | Description |
|---|---|---|
| `take_screenshot` | `full_page: bool` | Capture a screenshot of the viewport or full page |
| `get_page_state` | — | Get the current DOM state summary |
| `wait_for_element` | `selector: str, timeout: int` | Wait for an element to appear |
| `check_element_exists` | `selector: str` | Check if an element exists on the page |

---

## 🔗 Workflow Orchestration with n8n

n8n enables complex, multi-step automation pipelines that go beyond single agent runs:

### Example Workflow: Automated Price Monitoring

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Schedule   │────→│   Browser    │────→│   Compare    │
│   Trigger    │     │   Agent      │     │   Prices     │
│  (Daily 9AM) │     │  (Extract    │     │  (vs. last   │
│              │     │   prices)    │     │   run)       │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                    ┌─────────────┴─────────────┐
                                    │                           │
                              Price Dropped?              No Change
                                    │                           │
                                    ▼                           ▼
                          ┌──────────────┐           ┌──────────────┐
                          │ Send Alert   │           │   Log to     │
                          │ (Slack/Email)│           │   Database   │
                          └──────────────┘           └──────────────┘
```

### n8n Capabilities Used

| Feature | Usage in This Project |
|---|---|
| **AI Agent Node** | Wraps the browser agent for no-code invocation |
| **Schedule Trigger** | Periodic execution of monitoring tasks |
| **Webhook Trigger** | On-demand agent invocation via HTTP |
| **Database Nodes** | Store extracted data in PostgreSQL/MySQL |
| **Notification Nodes** | Send alerts via Slack, Email, or Telegram |
| **Conditional Nodes** | Route workflow based on extracted data values |
| **Subworkflows** | Modular, reusable workflow components |

---

## 🧠 Memory Architecture

The agent employs a **dual-memory system** that mirrors human short-term and long-term memory:

```
┌─────────────────────────────────────────────────────────────┐
│                     MEMORY SYSTEM                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │           SHORT-TERM MEMORY (Session)                 │    │
│  │                                                       │    │
│  │  • Managed by LangGraph Checkpointer                 │    │
│  │  • Stores: message history, current URL,             │    │
│  │    action log, screenshots, active plan              │    │
│  │  • Scope: Single session / thread                    │    │
│  │  • Persistence: In-memory or SQLite                  │    │
│  │  • Purpose: Maintain context within a task           │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │           LONG-TERM MEMORY (Cross-Session)            │    │
│  │                                                       │    │
│  │  • Powered by ChromaDB + Sentence Transformers       │    │
│  │  • Stores: successful strategies, extracted facts,   │    │
│  │    website navigation patterns, error resolutions    │    │
│  │  • Scope: Cross-session, cross-task                  │    │
│  │  • Retrieval: Semantic similarity search             │    │
│  │  • Purpose: Learn from past experiences              │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │           MEMORY WORKFLOW                             │    │
│  │                                                       │    │
│  │  1. Agent receives task                               │    │
│  │  2. Query long-term memory for similar past tasks    │    │
│  │  3. Inject relevant memories as context              │    │
│  │  4. Execute task with enriched context               │    │
│  │  5. On success: store strategy in long-term memory   │    │
│  │  6. On failure: store failure analysis for avoidance │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛡 Error Handling & Self-Correction

The agent implements a **three-tier error handling strategy**:

### Tier 1: Automatic Retry
Simple transient errors (network timeouts, element not yet loaded) are retried automatically with exponential backoff.

### Tier 2: Reflection & Strategy Change
When retries fail, the **Reflection Engine** activates:
1. **Analyze** — What went wrong? (element not found, page structure changed, authentication required)
2. **Hypothesize** — Why did it fail? (selector outdated, element behind modal, page not fully loaded)
3. **Correct** — Try an alternative approach (different selector strategy, scroll to element, wait longer)

### Tier 3: Dynamic Replanning
When the entire approach is unviable, the **Planning Engine** generates a new plan:
- Original plan: Navigate via sidebar menu → *Sidebar doesn't exist on mobile layout*
- New plan: Use the hamburger menu → Navigate to target page

```
Error Flow:
                    Action Failed
                         │
                         ▼
              ┌─────────────────────┐
              │  Retry (Tier 1)?    │──── Yes ──→ Retry with backoff
              │  (Transient error?) │
              └──────────┬──────────┘
                         │ No
                         ▼
              ┌─────────────────────┐
              │  Reflect (Tier 2)?  │──── Yes ──→ Alternative strategy
              │  (Known pattern?)   │
              └──────────┬──────────┘
                         │ No
                         ▼
              ┌─────────────────────┐
              │  Replan (Tier 3)    │──── Yes ──→ New execution plan
              │  (Approach invalid?)│
              └──────────┬──────────┘
                         │ No (max retries exceeded)
                         ▼
              ┌─────────────────────┐
              │  Graceful Failure   │
              │  (Report + Logs)    │
              └─────────────────────┘
```

---

## ⚡ Performance Considerations

| Optimization | Implementation | Impact |
|---|---|---|
| **Headless Mode** | Run browser without UI rendering | 2x–15x faster execution |
| **Isolated Contexts** | Separate browser contexts per task | Parallel execution without interference |
| **Lazy Screenshots** | Capture only on significant state changes | Reduced I/O overhead |
| **Token Optimization** | Minimize page content sent to LLM | Lower latency, reduced cost |
| **Connection Pooling** | Reuse browser instances across tasks | Faster task initialization |
| **Embedding Cache** | Cache frequently-used embeddings | Faster memory retrieval |
| **Streaming Responses** | Stream LLM output as it generates | Lower perceived latency |

### Resource Requirements

| Environment | CPU | RAM | Disk | Notes |
|---|---|---|---|---|
| **Development** | 2+ cores | 4 GB | 2 GB | Headful mode for debugging |
| **Production** | 4+ cores | 8 GB | 5 GB | Headless, concurrent tasks |
| **Docker** | 4+ cores | 8 GB | 10 GB | Includes browser binaries |

---

## 🔒 Security Best Practices

| Practice | Description |
|---|---|
| **API Key Management** | All secrets stored in `.env`, never committed to version control |
| **Input Sanitization** | Validate all user inputs before passing to browser tools |
| **Sandboxed Execution** | Browser runs in isolated contexts with restricted permissions |
| **Network Restrictions** | Optional allowlist for permitted domains |
| **PII Scrubbing** | Remove personally identifiable information from logs and memory |
| **Rate Limiting** | API rate limiting to prevent abuse |
| **Authentication** | API key-based authentication for the FastAPI endpoints |
| **Docker Isolation** | Run in containerized environment for OS-level isolation |

---

## 🐛 Troubleshooting

<details>
<summary><b>Playwright browsers not installed</b></summary>

```bash
# Error: Browser not found
# Solution: Install browser binaries
playwright install

# If permission issues on Linux:
sudo playwright install-deps
playwright install
```

</details>

<details>
<summary><b>Groq API rate limiting</b></summary>

```
# Error: 429 Too Many Requests
# Solution: Reduce request frequency or upgrade API plan

# In .env, increase delay between requests:
LLM_REQUEST_DELAY=1.0  # seconds between API calls
```

</details>

<details>
<summary><b>ChromaDB persistence errors</b></summary>

```bash
# Error: Database locked or corrupted
# Solution: Clear and reinitialize the database

rm -rf ./data/chromadb
python -c "import chromadb; client = chromadb.PersistentClient('./data/chromadb')"
```

</details>

<details>
<summary><b>Element not found errors during automation</b></summary>

```
# The agent handles this automatically via the Reflection Engine,
# but if it persists:

# 1. Increase browser timeout in .env:
BROWSER_TIMEOUT=60000

# 2. Enable screenshots on every step for debugging:
SCREENSHOT_ON_EVERY_STEP=true

# 3. Check LangSmith traces for the agent's reasoning
```

</details>

<details>
<summary><b>Docker: Browser crashes inside container</b></summary>

```bash
# Increase shared memory size
docker run --shm-size=1gb browser-agent

# Or in docker-compose.yml:
services:
  agent:
    shm_size: '1gb'
```

</details>

<details>
<summary><b>LangSmith traces not appearing</b></summary>

```bash
# Verify environment variables are set:
echo $LANGCHAIN_API_KEY
echo $LANGCHAIN_TRACING_V2

# Ensure tracing is enabled:
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=browser-automation-agent
```

</details>

---

## 📋 Required Dependencies

```txt
# Core Agent Framework
langchain>=0.2.0
langgraph>=0.2.0
langchain-community>=0.2.0
langchain-groq>=0.1.0

# Browser Automation
playwright>=1.40.0

# Memory & Embeddings
chromadb>=0.4.0
sentence-transformers>=2.2.0

# API & Web Framework
fastapi>=0.100.0
uvicorn>=0.24.0

# Utilities
python-dotenv>=1.0.0
pydantic>=2.0.0

# Monitoring
langsmith>=0.1.0

# Data Processing
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

---

## 🏆 Skills Demonstrated

| Category | Skills |
|---|---|
| **Agentic AI** | ReAct reasoning loops, autonomous decision-making, tool calling, self-correction |
| **LLM Engineering** | Prompt engineering, structured output parsing, temperature tuning, token optimization |
| **Agent Orchestration** | LangGraph state machines, conditional routing, checkpointing, streaming |
| **Browser Automation** | Playwright mastery, DOM manipulation, network interception, cross-browser testing |
| **Memory Systems** | Vector databases, semantic retrieval, embedding models, memory lifecycle management |
| **System Design** | Modular architecture, separation of concerns, scalable patterns, API design |
| **DevOps** | Docker containerization, CI/CD readiness, environment management, logging |
| **Workflow Automation** | n8n pipeline design, trigger-based execution, multi-service integration |

---

## 🔮 Future Enhancements

| Enhancement | Description | Priority |
|---|---|---|
| **Vision-Enabled Navigation** | Use multimodal LLMs to analyze screenshots and annotated bounding boxes for precise element targeting | 🔴 High |
| **Multi-Agent Orchestration** | Supervisor agent delegating to specialized worker agents (research, extraction, validation) | 🔴 High |
| **Human-in-the-Loop** | LangGraph interrupt points for human approval before critical actions (e.g., form submission, purchases) | 🟡 Medium |
| **Streaming UI** | Real-time web dashboard showing agent's browser view, reasoning steps, and action log | 🟡 Medium |
| **MCP Integration** | Model Context Protocol support for external AI agents to invoke the browser agent | 🟡 Medium |
| **Parallel Execution** | Run multiple browser contexts concurrently for tasks like price comparison across sites | 🟢 Low |
| **Fine-Tuned Models** | Train specialized smaller models on browser automation datasets for faster inference | 🟢 Low |
| **Browser Extension** | Chrome extension for triggering the agent directly from the browser | 🟢 Low |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code style
- Add type hints to all function signatures
- Write docstrings for all public functions
- Include unit tests for new tools and features
- Update this README for any new capabilities

---

## 📝 Resume Description

> Developed an **Autonomous Browser Automation Agent** using **LangGraph**, **LangChain**, and **Playwright** capable of multi-step web navigation, intelligent task planning using the **ReAct reasoning loop**, memory-aware execution via **ChromaDB** vector storage, and dynamic error recovery through **reflection and retry mechanisms**. Integrated **n8n** for visual workflow orchestration and **LangSmith** for full agent observability. Designed a modular, production-grade architecture with **FastAPI** endpoints, **Docker** containerization, and a dual short-term/long-term memory system for cross-session learning.

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>Built with ❤️ using Agentic AI, LangGraph, LangChain, Playwright & ChromaDB</b>
  <br/>
  <i>Demonstrating how AI agents can move beyond chatbots into real-world autonomous execution</i>
</p>
