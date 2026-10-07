# Autonomous Research Agent

An AI-powered autonomous research agent built with **Python, LangGraph, LangChain, Google Gemini, and Tavily**.

The system takes a research question, creates a structured research plan, performs web research, fact-checks the collected claims, and synthesizes the evidence into a final research report.

## Project Overview

The goal of this project is to demonstrate an end-to-end **Agentic AI research workflow** rather than a simple question-answering application.

### Workflow

```text
Research Question
       │
       ▼
┌─────────────────┐
│ Research Planner│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Web Researcher  │
│     Tavily      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Fact Checker   │
│  Gemini / LLM   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Report          │
│ Synthesizer     │
└────────┬────────┘
         │
         ▼
   Final Research
      Report
```

The workflow is orchestrated using **LangGraph**.

---

## Key Features

- Autonomous research planning
- Multi-step agent workflow
- Web research using Tavily
- LLM-powered fact checking
- Evidence-based research synthesis
- Structured research state using Python `TypedDict`
- LangGraph workflow orchestration
- LLM retry handling for temporary server errors
- Handling of API quota/rate-limit failures
- JSON and Markdown report generation
- Mock workflow testing without consuming LLM API quota
- Environment-variable based API configuration

---

## Technology Stack

| Technology    | Purpose                                      |
| ------------- | -------------------------------------------- |
| Python 3.11   | Application development                      |
| LangGraph     | Agent/workflow orchestration                 |
| LangChain     | LLM integration                              |
| Google Gemini | Planning, fact checking and report synthesis |
| Tavily        | Web research/search                          |
| Pydantic      | Structured data validation                   |
| python-dotenv | Environment variable management              |
| PowerShell    | Windows development environment              |

---

## Project Structure

```text
autonomous-research-agent/
│
├── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── web_researcher.py
│   │   ├── fact_checker.py
│   │   ├── report_synthesizer.py
│   │   └── mock_report_synthesizer.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── workflow.py
│   │
│   ├── utils/
│   │   └── llm_retry.py
│   │
│   ├── config.py
│   └── main.py
│
├── test_workflow_mock.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> `.env` should never be committed to GitHub because it contains API credentials.

---

## Research State

The LangGraph workflow uses a shared `ResearchState` containing:

- `question`
- `research_plan`
- `research_evidence`
- `fact_check_report`
- `final_report`

This allows each agent/node to consume the output of the previous stage and contribute to the overall research process.

---

## Agents

### 1. Research Planner

The Planner receives the research question and converts it into a structured research plan.

For example, a broad question can be divided into research areas such as:

- Current use cases
- Market/adoption trends
- Regulation
- Infrastructure
- Ethics and risks
- Investment/startups
- Future outlook

---

### 2. Web Researcher

The Web Researcher executes the research tasks and uses **Tavily** to retrieve relevant web information.

The collected evidence is passed to the next stage of the workflow.

---

### 3. Fact Checker

The Fact Checker evaluates collected claims and evidence using the LLM.

It helps identify:

- Supported claims
- Uncertain claims
- Contradictory information
- Claims requiring additional verification

---

### 4. Report Synthesizer

The Report Synthesizer combines the research evidence and fact-checking results into a structured final report.

The report model includes sections such as:

- Title
- Executive Summary
- Key Findings
- Verified Facts
- Uncertain/Partial Findings
- Contradicted Claims
- Opportunities
- Challenges
- Future Outlook
- Conclusion
- Sources

---

## Example Research Question

The project was developed and tested using:

> **What is the future of Generative AI in Indian healthcare?**

The research plan covered areas including:

- Generative AI healthcare use cases
- Adoption in India
- Regulation and the DPDP Act
- ABDM and digital health infrastructure
- Data localization and sovereignty
- Computing infrastructure
- Bias and security
- Indian startups and investment
- 5–10 year outlook

---

## Installation

### 1. Clone the repository

```powershell
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd autonomous-research-agent
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## API Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit the `.env` file.

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
reports/
```

---

## Running the Application

From the project root:

```powershell
python -m app.main
```

The application runs the LangGraph workflow:

```text
Planner
   ↓
Web Researcher
   ↓
Fact Checker
   ↓
Report Synthesizer
   ↓
Final Report
```

---

## Output

The completed workflow can generate research reports in:

```text
reports/
├── final_report.json
└── final_report.md
```

### JSON

The JSON output is useful for:

- APIs
- downstream applications
- structured processing
- databases
- future RAG pipelines

### Markdown

The Markdown output is useful for:

- Human reading
- GitHub documentation
- Research sharing
- Conversion to other document formats

---

## Testing

The project also includes a mock workflow test:

```powershell
python .\test_workflow_mock.py
```

The mock workflow allows the graph structure and report-synthesis path to be tested without repeatedly consuming external LLM API quota.

This is useful during development and debugging.

---

## Error Handling

The project includes an LLM retry utility:

```text
app/utils/llm_retry.py
```

Temporary server failures such as HTTP `503` can be retried using exponential backoff.

Rate-limit/quota errors such as HTTP `429` are handled separately so the application does not repeatedly make requests when the provider quota has been exhausted.

---

## Architecture

The project follows a modular architecture:

```text
User Question
     │
     ▼
┌───────────────┐
│ Configuration │
└───────┬───────┘
        │
        ▼
┌───────────────────────────────┐
│          LangGraph            │
│                               │
│ Planner → Research → Fact     │
│                    Check      │
│                       ↓       │
│                 Synthesizer   │
└───────────────────────┬───────┘
                        │
                        ▼
                 Research Report
```

This separation makes it possible to replace individual agents without redesigning the entire application.

---

## Why LangGraph?

LangGraph is used because the application requires a stateful, multi-step workflow.

Instead of making one LLM call:

```text
Question → LLM → Answer
```

the project implements:

```text
Question
   ↓
Plan
   ↓
Research
   ↓
Evidence
   ↓
Fact Check
   ↓
Synthesis
   ↓
Report
```

Each stage has a specific responsibility and shares state with the other stages.

---

## Why Tavily?

General-purpose LLMs have knowledge limitations and may not have access to current information.

Tavily provides web-search capabilities so the research agent can collect current external evidence before generating the final report.

---

## Security

API keys are loaded through environment variables.

Do not commit:

```text
.env
```

or expose:

```text
GOOGLE_API_KEY
TAVILY_API_KEY
```

If an API key is accidentally pushed to GitHub, revoke/rotate it immediately.

---

## Future Improvements

Possible future enhancements include:

- Parallel research tasks
- Source quality scoring
- Citation-level evidence tracking
- Persistent research memory
- Human approval checkpoints
- Additional search providers
- More sophisticated claim verification
- RAG-based research memory
- PostgreSQL/vector database integration
- FastAPI backend
- Streamlit/React frontend
- Docker containerization
- AWS deployment
- Observability and tracing
- Scheduled autonomous research
- Multi-agent debate/verification

---

## Learning Outcomes

This project demonstrates practical experience with:

- Python
- LLM application development
- LangChain
- LangGraph
- Agentic AI
- Prompt engineering
- Web research
- Fact checking
- Structured state management
- API integration
- Error handling
- Retry mechanisms
- Environment configuration
- Automated report generation
- Testing AI workflows

---

## Project Status

**Status: Completed**

The core autonomous research workflow has been implemented and tested.

The project is suitable as a portfolio project demonstrating an end-to-end **Agentic AI / Generative AI research system**.

---

## Author

**Ashok**


---

## License

This project is intended for educational and portfolio purposes.

Add a license appropriate to your intended use before publishing if required.
