# Student Success & Early Warning System

An Agentic AI application that analyzes student academic and career-readiness data, identifies students who may need support, and helps mentors manage recommended interventions.

The system combines **AI agents, Machine Learning, tools, memory, and human approval** to support student risk analysis and intervention management.

## Features

- **Student Data Collection:** Uses student records containing attendance, marks, assignments, backlogs, internship status, and placement status.
- **Machine Learning Risk Prediction:** Uses a Logistic Regression model to classify students as **At Risk** or **Not At Risk** and estimate their risk probability.
- **Risk Analysis Agent:** Uses the ML prediction and student indicators to provide a risk classification with supporting reasons.
- **Recommendation Agent:** Generates recommendations based on academic performance, backlogs, attendance, internship status, and placement readiness.
- **Agent Workflow:** Connects risk analysis, recommendation generation, and intervention management into a workflow that supports the student review process.
- **Tool Usage:** Uses Python functions and database operations to retrieve student information and manage intervention records.
- **Memory Management:** Stores intervention history so existing records can be retrieved and duplicate interventions can be prevented.
- **Mentor Approval:** Allows mentors to approve or reject pending interventions and record feedback.
- **Audit Logging:** Records selected agent actions to support traceability.
- **Dashboard:** Provides access to the main application views and system overview information where implemented.

## How Agentic AI and Machine Learning Work Together

The project combines Machine Learning with an agent-based workflow. These components have different responsibilities.

### 1. Machine Learning Model

The Logistic Regression model analyzes selected student features:

- Attendance
- Marks
- Assignment completion
- Number of backlogs

It predicts whether a student is **At Risk** or **Not At Risk** and provides a risk probability.

### 2. Risk Analysis Agent

The Risk Analysis Agent retrieves student data, invokes the ML model, interprets the prediction alongside predefined risk indicators, and returns a structured risk assessment with reasons.

### 3. Recommendation Agent

The Recommendation Agent uses student information and the risk assessment to generate relevant academic and career-readiness recommendations.

### 4. Memory and Intervention Management

The intervention workflow stores recommendations as intervention records, maintains their statuses, and retrieves intervention history. Existing records are checked to avoid creating duplicates when a student is reviewed again.

### 5. Human-in-the-Loop Approval

The mentor reviews pending interventions and can approve or reject them with feedback. This keeps the intervention decision under human supervision rather than allowing the system to make it entirely autonomously.

### Overall Workflow

**Student Data → ML Risk Prediction → Risk Analysis Agent → Recommendation Agent → Intervention Memory → Mentor Approval/Rejection**

The ML model provides the prediction, while the agents coordinate the surrounding tasks, use application tools, prepare recommendations, and manage the intervention workflow.

## Technology Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- Logistic Regression
- SQLite
- MCP Python SDK
- JSON-based memory and audit logging

## Project Structure

```text
agentic-ai/
├── app/
│   ├── agents/
│   ├── database/
│   ├── memory/
│   ├── ml/
│   ├── mcp/
│   ├── runtime/
│   ├── safety/
│   ├── skills/
│   ├── tools/
│   └── ui/
│       ├── dashboard.py
│       ├── student_view.py
│       └── intervention_view.py
├── data/
│   ├── students.csv
│   ├── academic_data.csv
│   ├── attendance.csv
│   ├── internship_data.csv
│   └── placement_data.csv
├── requirements.txt
└── README.md
```


## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RAMAKRISHNAHUDDAR/agentic-ai.git
cd agentic-ai
```

### 2. Create and Activate a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an appropriate execution policy or run the project using the virtual environment's Python interpreter.

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If `requirements.txt` is not up to date, install the packages used by the project:

```bash
python -m pip install streamlit pandas scikit-learn mcp
```

### 4. Initialize the Database

Run this from the repository root:

```powershell
$env:PYTHONPATH="."
python -c "from app.database.database import create_tables; create_tables(); print('Database tables ready')"
```

If the database is empty, check `app/database/seed.py` for the current data-seeding procedure.

### 5. Launch the Application

From the repository root:

```powershell
python -m streamlit run app/main.py
```

Open the local URL printed in the terminal.

## Using the Application

### Student View

1. Open **Student View**.
2. Enter a student ID, such as `STU378` or `STU007`, if the record exists in the dataset.
3. Select **View Student**.
4. Review the risk classification, probability, reasons, recommendations, and intervention history.

### Intervention View

1. Open **Intervention View**.
2. Find or select a student.
3. Review the student's intervention records.
4. Enter mentor feedback for a pending intervention, if needed.
5. Select **Approve** or **Reject**.
6. Confirm that the status and feedback appear in the intervention history.

The application is designed to avoid creating duplicate intervention records when the same student is reviewed repeatedly.

## Machine Learning Model

The current risk model uses the following features:

- Attendance
- Marks
- Assignment completion
- Number of backlogs

The model predicts a risk class and probability. The Risk Analysis Agent uses this result alongside predefined indicators to provide explanations. The Recommendation Agent applies implemented rules to generate recommendations.

**Important:** The included dataset is synthetic/demo data. If risk labels were generated using rules based on the same features, high test scores show how well the model reproduces those rules; they do not establish real-world predictive performance. The model should be evaluated on representative, appropriately governed data before any institutional use.

## Data and Local Files

- CSV files in `data/` provide student and related records.
- SQLite stores structured student and intervention records.
- JSON memory may store intervention history.
- JSON audit logs record selected agent actions.

Do not commit real student personal data, local database files, generated runtime logs, API keys, or other secrets to Git. Use synthetic or appropriately anonymized data for development and demonstrations.

## Running the Risk Model Separately

From the repository root:

```powershell
$env:PYTHONPATH="."
python -m app.ml.risk_model
```

This trains and evaluates the model using the configured CSV path.

## Limitations

- Risk predictions depend on the available data and the implemented model.
- Recommendations depend on the rules implemented in the Recommendation Agent.
- The demo dataset is not a substitute for validated institutional data.
- Recommendations should support mentor review, not make automatic decisions about a student's academic future.
- Integration with real Contineo, LMS, internship, or placement systems depends on their available APIs and credentials.
- The project uses an agentic workflow, but not every component is an autonomous LLM agent. The ML model performs prediction, while application agents and tools handle the associated workflow.

## Project Goal

The goal is to build an Agentic AI-based student support system that combines Machine Learning risk prediction with agent-driven analysis, recommendations, memory, and human approval.

By connecting these components, the system aims to identify students who may need support, explain potential risk indicators, recommend suitable actions, and maintain a record of mentor-reviewed interventions.
