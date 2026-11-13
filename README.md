
# Student Success & Early Warning System

An Agentic AI-powered system designed to monitor student performance, identify academic risks, and support timely interventions through intelligent agents and mentor involvement.

## Project Overview

The Student Success & Early Warning System uses multiple AI agents to collect and analyze student information, identify students who may be at academic risk, and recommend suitable interventions.

The system integrates student data, academic performance, attendance, internship and placement information. It also includes mentor approval workflows to ensure human oversight before interventions are approved.

The project demonstrates how Agentic AI concepts can be applied to a real-world student support system.

## Key Features

- **Student and Mentor Authentication:** Provides authentication and role-based access.
- **Student Data Integration:** Retrieves student, academic, attendance, internship, and placement information.
- **Risk Analysis:** Identifies students who may be academically at risk.
- **Recommendation Agent:** Generates suitable recommendations and interventions.
- **Human-in-the-Loop Approval:** Allows mentors to approve or reject proposed interventions.
- **Notification System:** Supports notifications following intervention approval.
- **Agent Runtime:** Provides a centralized runtime for executing registered agents.
- **Skill Registry:** Manages reusable agent skills.
- **Tool Registry:** Manages tools that agents can execute.
- **Agent Registry:** Maintains registered agents.
- **Memory and Retrieval:** Supports storing and retrieving agent memory.
- **Governance Checks:** Checks whether actions have the required approval.
- **Audit Logging:** Records agent executions and governance activities.
- **LangGraph Workflow:** Implements a node-based workflow for student data collection, retrieval, and risk analysis.
- **Parallel Swarm:** Executes multiple agent tasks concurrently and collects their results.
- **Deep Research Agent:** Analyzes supplied research sources, compares claims, identifies evidence gaps, and generates summaries.
- **Cloud Operations Agent:** Analyzes deployment logs and error metrics, classifies severity, and requests human approval for proposed rollback actions.

## Technology Stack

- Python
- MongoDB Atlas
- PyMongo
- LangGraph
- Python Concurrent Futures
- Pytest

Refer to `requirements.txt` for project dependencies.

## Project Structure

```text
agentic-ai/
│
├── app/
│   ├── agents/
│   │   ├── coordinator_agent.py
│   │   ├── deep_research_agent.py
│   │   └── cloud_operations_agent.py
│   │
│   ├── auth/
│   │
│   ├── database/
│   │
│   ├── runtime/
│   │   ├── agent_registry.py
│   │   ├── agent_runtime.py
│   │   ├── audit_logger.py
│   │   ├── skill_registry.py
│   │   └── tool_registry.py
│   │
│   ├── workflows/
│   │   ├── node_graph.py
│   │   └── parallel_swarm.py
│   │
│   └── ui/
│
├── tests/
│
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RAMAKRISHNAHUDDAR/agentic-ai.git
cd agentic-ai
```

### 2. Create a Virtual Environment

For Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure MongoDB Atlas

Configure the MongoDB Atlas connection using the database configuration expected by the project.

Ensure that:
- MongoDB Atlas is accessible.
- The connection string is correctly configured.
- Required credentials are available.
- Sensitive credentials are not committed to GitHub.

## Running the Project

Run commands from the project root directory.

### LangGraph Student Workflow

```bash
python -m app.workflows.node_graph
```

This workflow demonstrates:

- Student data collection.
- MCP-style retrieval.
- Risk analysis.
- Conditional routing.
- Retry handling.
- Failure handling.

### Parallel Swarm Workflow

The parallel swarm workflow executes multiple registered agent tasks concurrently.

Refer to:

```text
app/workflows/parallel_swarm.py
```

### Deep Research Agent

The Deep Research Agent accepts research sources as input and:

- Validates research sources.
- Compares agreements and contradictions.
- Identifies evidence gaps.
- Generates an executive summary.
- Suggests follow-up research questions.

Note: Research sources are supplied by the caller; the agent does not independently search the web.

### Cloud Operations Agent

The Cloud Operations Agent:

- Analyzes deployment logs.
- Examines error rates and baseline metrics.
- Classifies incident severity.
- Identifies possible deployment-related causes.
- Proposes rollback actions.
- Requests human approval before high-risk remediation.

The agent does not automatically execute rollback operations.

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run individual test modules:

```bash
python -m pytest tests/test_agent_graph.py -v
```

```bash
python -m pytest tests/test_parallel_swarm.py -v
```

```bash
python -m pytest tests/test_deep_research_agent.py -v
```

```bash
python -m pytest tests/test_cloud_operations_agent.py -v
```

## Safety and Governance

The project incorporates safety and governance mechanisms to ensure that agent actions are controlled.

Implemented capabilities include:

- Risk classification.
- Permission and access control.
- Human approval and rejection.
- Agent execution evaluation through tests.
- Audit logging.
- Governance checks.
- Human approval before proposed high-risk cloud rollback actions.

These mechanisms help maintain transparency, accountability, and human oversight during agent execution.

## Agentic AI Lab Coverage

The project has been developed alongside the Agentic AI laboratory curriculum.

| Lab | Topic | Status |
|---|---|---|
| Lab 1 | Agent vs Chatbot | Completed |
| Lab 2 | Tool-Using Agent | Completed |
| Lab 3 | Skill Creation | Completed |
| Lab 4 | Memory & Retrieval | Completed |
| Lab 5 | MCP-Style Connector | Completed |
| Lab 6 | Agent Runtime / Registries | Implemented |
| Lab 7 | Agentic Node Graph | Implemented |
| Lab 8 | Parallel Swarm | Implemented |
| Lab 9 | Deep Research Agent | Implemented |
| Lab 10 | Cloud Operations Agent | Implemented |
| Lab 11 | Agentic SDLC Factory | Planned |
| Lab 12 | Safety & Governance | Considered Implemented |
| Lab 13 | Discipline-Specific Agents | Planned |
| Lab 14 | Capstone Project Studio | Planned |

## Team Collaboration

The project is developed collaboratively using Git and GitHub.

Before starting new work, synchronize your branch:

```bash
git fetch origin
git merge origin/main
```

Run the relevant tests before committing changes.

Use feature branches and pull requests to integrate changes into the main branch.

## Important Notes

- The Deep Research Agent analyzes research sources supplied to it.
- The Cloud Operations Agent requests approval before proposed high-risk rollback actions.
- Mentor approval and governance checks support human oversight.
- Database credentials and API keys must never be committed to the repository.
- Test results should be verified before claiming successful execution.

## License

Add the license and usage terms selected by the project team before distributing the repository.
