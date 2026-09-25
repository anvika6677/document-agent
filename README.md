# 📄 Autonomous AI Document Generation Agent

An enterprise-ready, stateful multi-agent system built with **LangGraph**, **FastAPI**, **Tavily Search API**, and **OpenRouter LLMs**. The agent plans document outlines, conducts real-time web research, synthesizes technical content, and automatically compiles production-ready Microsoft Word documents (`.docx`) with formal citations.
📈 System Evolution & Architecture Journey
This system transitioned through three distinct engineering phases, moving from a simple procedural prototype to a production-grade state machine.

Phase 1: Baseline Prototype (v1.0)
Architecture: Linear procedural script (orchestrator.py).

Control Flow: Sequential method execution (Planner -> Worker -> Writer).

Data Handling: Ephemeral local variables and return tuples.

Limitations: Prone to hallucinating on current events due to lack of web grounding; strict JSON parsing crashed whenever models returned markdown code fences or conversational text.

Phase 2: Tool Integration & RAG Engine (v2.0)
Search Grounding: Integrated Tavily AI Search API for real-time fact retrieval.

Automated Citations: Designed an automated bibliography compiler that formats in-text citations and creates a formal "References & Sources Cited" section with source domains and retrieval dates.

Parser Resilience: Implemented regex pattern matching and json.JSONDecoder().raw_decode() in utils/json_parser.py to prevent "Extra data" errors caused by trailing LLM commentary.

Phase 3: Stateful Multi-Agent System (v3.0 - Current)
Architecture: Compiled LangGraph StateGraph state machine (graph_orchestrator.py).

Data Contract: Centralized, typed AgentState (TypedDict) shared across isolated nodes.

Separation of Concerns: Split tasks into dedicated graph nodes (planner_node, researcher_node, writer_node, docx_node).

Model Failover: Added dynamic fallback routing across OpenRouter models to absorb 404 endpoint drops and rate limits without halting pipeline execution.

⚖️ Architectural Shift: Before vs. After LangGraph
Plaintext
BEFORE (Procedural Pipeline):
User Request ──> orchestrator.py ──> PlannerAgent() ──(tuples)──> WorkerAgent() ──(dict)──> DocumentWriter()
[Limitation: Rigid sequential execution, coupled responsibilities, no audit trail]

AFTER (LangGraph State Machine):
                      ┌──────────────────────────────────────────────┐
                      │            TypedDict: AgentState             │
                      │  (request, plan, context, sources, docs)    │
                      └──────┬──────────────┬──────────────┬─────────┘
                             │              │              │
                             ▼              ▼              ▼
[START] ──> [planner_node] ──┴─> [researcher_node] ───────┴─> [writer_node] ──> [docx_node] ──> [END]
                                       │
                                (Tavily AI Tool)
🌟 Core Features
Autonomous Document Planning: Breaks user prompts into logical sections and formulates targeted search queries for sections requiring live data.

Real-Time Web Grounding: Parallel execution of web search queries using Tavily AI Search.

Automated Bibliographies: Generates professional citations with domains and timestamps directly in the final document.

Resilient Output Parsing: Recovers valid JSON data even when models produce trailing conversational filler.

Dynamic Failover: Automatically switches to secondary free models if an endpoint is deprecated or throttled.

Styled .docx Export: Uses python-docx to apply visual hierarchy, bold titles, callouts, and clean margins.

🏗️ Pipeline Execution Flow
Plaintext
       [User Input Topic]
                │
                ▼
    ┌───────────────────────┐
    │     planner_node      │  --> Creates outline & generates search queries
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │    researcher_node    │  --> Calls Tavily Search & collects source links
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │      writer_node      │  --> Synthesizes grounded content from research
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │       docx_node       │  --> Assembles formatted Word document
    └───────────────────────┘
                │
                ▼
     [.docx Download Stream]
📁 Project Directory Structure
Plaintext
document-agent/
│
├── agents/                     # LangGraph agents & state schema
│   ├── __init__.py
│   ├── planner.py              # Outline & search query planner
│   ├── worker.py               # Drafting & synthesis agent
│   └── state.py                # TypedDict AgentState definition
│
├── core/                       # Core application configurations
│   ├── __init__.py
│   └── config.py               # Environment variable loading
│
├── prompts/                    # System prompts & instructions
│   ├── __init__.py
│   ├── planner_prompt.py
│   └── worker_prompt.py
│
├── services/                   # Business logic & external clients
│   ├── __init__.py
│   ├── document_writer.py      # python-docx formatting & citation engine
│   ├── llm_service.py          # OpenRouter client & API caller
│   └── model_manager.py        # Model failover routing logic
│
├── tools/                      # External tool calling
│   ├── __init__.py
│   └── search_tool.py          # Tavily search API wrapper
│
├── utils/                      # Helper utilities
│   └── json_parser.py          # Resilient raw_decode JSON parser
│
├── static/                     # Web UI stylesheets & scripts
├── templates/                  # Frontend HTML templates
├── outputs/                    # Generated .docx files (git-ignored)
│
├── app.py                      # FastAPI application entrypoint
├── graph_orchestrator.py       # Compiled LangGraph workflow
├── orchestrator.py             # Legacy procedural script (retained for reference)
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # System documentation
🚀 Getting Started
1. Prerequisites
Python 3.10+

An OpenRouter API Key (https://openrouter.ai/)

A Tavily Search API Key (https://tavily.com/)

2. Installation
Bash
# Clone the repository
git clone [https://github.com/anvika6677/document-agent.git](https://github.com/anvika6677/document-agent.git)
cd document-agent

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# macOS / Linux:
# python3 -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
3. Environment Configuration
Create a .env file in the project root:

Code snippet
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
4. Running the Application
Bash
uvicorn app:app --reload
Open your browser at http://127.0.0.1:8000, enter a topic, and download the generated .docx document.

🛠️ Technology Stack
Workflow Orchestration: LangGraph, LangChain Core

Web Framework: FastAPI, Uvicorn, Pydantic

Search Tool: Tavily AI Search API

LLM Provider: OpenRouter API

Document Generation: python-docx

Frontend: HTML5, CSS3, Vanilla JavaScript