# Student Success & Early Warning System

An agent-based application that analyzes student academic and
career-readiness data, identifies students who may need support, and
helps mentors manage recommended interventions.

## Features

-   **Student data:** Student records include attendance, marks,
    assignments, backlogs, internship status, and placement status.
-   **Risk prediction:** A Logistic Regression model classifies students
    as **At Risk** or **Not At Risk** and returns a risk probability.
-   **Risk explanations:** Shows indicators contributing to a student's
    risk assessment.
-   **Recommendations:** Generates suggestions based on academic
    performance and career-readiness indicators.
-   **Intervention tracking:** Stores interventions and tracks their
    status.
-   **Mentor approval:** Mentors can approve or reject pending
    interventions and add feedback.
-   **Memory and audit logging:** Uses local storage for intervention
    history and logs selected agent actions.
-   **Dashboard:** Provides the main application navigation and any
    system-level overview metrics implemented in the current UI.

## Technology Stack

-   Python
-   Streamlit
-   Pandas
-   Scikit-learn
-   SQLite
-   MCP Python SDK

## Project Structure

``` text
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

The repository may contain additional modules as development continues.

## Setup

### 1. Clone the repository

``` bash
git clone https://github.com/RAMAKRISHNAHUDDAR/agentic-ai.git
cd agentic-ai
```

### 2. Create and activate a virtual environment (recommended)

Windows PowerShell:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use a terminal with the appropriate
execution policy or run the project with the virtual environment's
Python interpreter directly.

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

If `requirements.txt` is not up to date, install the packages used by
the project:

``` bash
python -m pip install streamlit pandas scikit-learn mcp
```

### 4. Initialize the database

Run this from the repository root:

``` powershell
$env:PYTHONPATH="."
python -c "from app.database.database import create_tables; create_tables(); print('Database tables ready')"
```

If the database is empty, check `app/database/seed.py` for the current
data-seeding procedure.

### 5. Launch the application

From the repository root:

``` powershell
python -m streamlit run app/main.py
```

Open the local URL printed in the terminal.

## Using the Application

### Student View

1.  Open **Student View**.
2.  Enter a student ID, such as `STU378` or `STU007`, if those records
    exist in your dataset.
3.  Select **View Student**.
4.  Review the risk classification, probability, reasons,
    recommendations, and intervention history.

### Intervention View

1.  Open **Intervention View**.
2.  Find or select a student.
3.  For a pending intervention, enter mentor feedback if needed.
4.  Select **Approve** or **Reject**.
5.  Confirm that the status and feedback appear in the intervention
    history.

The application is designed to avoid creating duplicate intervention
records when the same student is viewed repeatedly.

## Risk Model

The current model uses these features:

-   Attendance
-   Marks
-   Assignment completion
-   Number of backlogs

The model predicts a risk class and probability. The application also
generates rule-based explanations and recommendations from student
indicators.

**Important:** The included dataset is synthetic/demo data. If risk
labels were generated from rules using the same features, high test
scores show that the model reproduces those rules; they do not establish
real-world predictive performance. Evaluate the model on representative,
appropriately governed data before any institutional use.

## Data and Local Files

-   CSV files in `data/` provide student and related records.
-   A local SQLite database stores structured records.
-   Intervention memory and audit logs may be stored in local JSON
    files, depending on the current configuration.

Do not commit real student personal data, local database files,
generated runtime logs, API keys, or other secrets to Git. Use
anonymized or synthetic data for development and demonstrations.

## Running the Risk Model Separately

From the repository root:

``` powershell
$env:PYTHONPATH="."
python -m app.ml.risk_model
```

This trains and evaluates the model using the configured CSV path.

## Development Workflow

The team's shared repository uses `main` as the integration branch and
`Ram` as a development branch.

To update local code after changes have been merged into `main`:

``` powershell
git checkout main
git pull origin main
git checkout Ram
git merge main
git push origin Ram
```

Resolve any merge conflicts deliberately before pushing.

## Limitations

-   Predictions and recommendations depend on the available data and
    implemented rules.
-   The demo dataset is not a substitute for validated institutional
    data.
-   Recommendations should support mentor review, not make automatic
    decisions about a student's academic future.
-   Integration with real Contineo, LMS, internship, or placement
    platforms depends on the systems' available APIs and credentials.

## Project Goal

The goal is to provide a unified student-risk view, explain potential
risk indicators, recommend supportive actions, and maintain a record of
mentor-reviewed interventions.
