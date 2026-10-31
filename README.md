# Agentic AI – Student Success & Early Warning System

An AI-powered Student Success and Early Warning System designed to monitor student performance, identify students who may be at academic risk, and support timely interventions through a coordinated multi-agent architecture.

The system brings together student information, academic performance, risk assessment, recommendations, and mentor-led intervention workflows in a unified application.

## Project Overview

The Student Success & Early Warning System aims to help educational institutions identify students who may need academic support at an early stage.

The platform uses seven specialized agents coordinated to support student monitoring, risk identification, recommendations, internships, and placement-related activities. It also provides role-based access for students and mentors, intervention management, and email notifications for approved interventions.

## Key Features

- **Student Dashboard:** Displays student academic performance, career status, risk assessment, and recommendations.
- **Mentor Dashboard:** Supports mentor access to student information and intervention management.
- **Multi-Agent Architecture:** Uses seven specialized agents coordinated through a central coordinator.
- **Risk Assessment:** Identifies students who may require academic intervention.
- **Recommendations:** Provides relevant recommendations based on student requirements and available information.
- **Intervention Workflow:** Supports mentor review, approval, and rejection of interventions.
- **Email Notifications:** Sends parent email notifications when an intervention is approved, subject to notification preferences.
- **Authentication:** Supports student and mentor login with password hashing and role-based permissions.
- **MongoDB Atlas:** Stores application data through a MongoDB-based repository layer.

## Seven Specialized Agents

| Agent | Responsibility |
|---|---|
| Contineo Agent | Supports the Contineo-related project workflow. |
| Coordinator Agent | Coordinates communication and task flow between specialized agents. |
| Internship Agent | Handles internship-related information and support. |
| LMS Agent | Supports learning management and academic learning information. |
| Risk Agent | Identifies and assesses potential student academic risks. |
| Recommendation Agent | Provides relevant recommendations for student improvement. |
| Placement Agent | Supports placement and career-related activities. |

## System Architecture

The application follows a modular, multi-agent architecture.

1. **User Interface:** Students and mentors interact with the application through the Streamlit interface.
2. **Authentication Layer:** Handles login, password verification, and user roles.
3. **Coordinator Agent:** Coordinates the specialized agents.
4. **Specialized Agents:** Perform their respective academic, risk, recommendation, internship, and placement tasks.
5. **Database Layer:** Stores and retrieves application information using MongoDB Atlas.
6. **Intervention Workflow:** Allows mentors to review and respond to interventions.
7. **Notification Layer:** Handles parent email notifications associated with approved interventions.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend / User Interface | Streamlit |
| Database | MongoDB Atlas |
| Database Integration | PyMongo |
| Authentication | Werkzeug password hashing |
| Testing | Pytest |
| Version Control | Git and GitHub |

## Project Structure

The project is organized into modular components:

```text
agentic-ai/
│
├── app/
│   ├── agents/          # Specialized AI agents
│   ├── auth/            # Authentication and permissions
│   ├── database/        # MongoDB connection and repositories
│   ├── mcp/             # MCP integration
│   ├── memory/          # Agent memory components
│   ├── ml/              # Machine learning components
│   ├── research/        # Research-related components
│   ├── runtime/         # Agent runtime
│   ├── safety/          # Safety and governance
│   ├── skills/          # Agent skills
│   ├── tools/           # Agent tools
│   ├── ui/              # Streamlit user interface
│   └── workflows/       # Application workflows
│
├── data/                # Project data
├── docs/                # Documentation
├── scripts/             # Utility scripts
├── tests/               # Test modules
│
├── .env.example         # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/RAMAKRISHNAHUDDAR/agentic-ai.git
cd agentic-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using the provided template:

```powershell
Copy-Item .env.example .env
```

Configure the required database and service settings in `.env`. Do not commit credentials or secret keys to GitHub.

### 5. Run the application

In Windows PowerShell, from the project root:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m streamlit run app/main.py
```

The Streamlit application will provide a local URL in the terminal. Open that URL in your browser.

## Testing

Run the following commands from the project root.

### Check Python compilation

```bash
python -m compileall -q app
```

### Run email and intervention approval tests

```bash
python -m pytest tests/test_email_service.py tests/test_approval.py -v
```

### Run repository tests

```bash
python -m tests.test_repositories_manual
```

The repository manual test uses the configured test database. Verify the database configuration before running it.

## Verified Test Coverage

The following components have been tested during project development:

- Password hashing and password verification.
- Student and mentor authentication functions.
- Duplicate user and email validation.
- Inactive account login rejection.
- Role permission functions.
- MongoDB Atlas connectivity.
- Repository CRUD operations and validation.
- Intervention approval and rejection workflows.
- Parent email notification behavior.
- Prevention of duplicate notifications.
- Student login and logout through the browser.
- Mentor login and Intervention View access through the browser.

These checks represent verified development tests, not a claim that every application feature has completed end-to-end testing.

## Authentication and Access

The application supports two primary user roles:

**Student**
- Logs in using registered credentials.
- Views personal academic and career information.
- Accesses risk assessment and recommendations.

**Mentor**
- Logs in using registered credentials.
- Accesses the Intervention View.
- Reviews student-related intervention information.
- Can approve or reject interventions where the workflow permits.

Passwords are stored using password hashing rather than plain-text storage.

## Database

The project uses MongoDB Atlas as its database service.

The database layer provides repository operations for application entities such as:

- Users
- Students
- Parents
- Mentors
- Interventions
- Notifications

The repository layer separates database operations from the user interface and application workflows.

## Intervention and Notification Workflow

1. Student-related information is processed through the application.
2. Potential academic concerns can lead to intervention records.
3. Mentors review the intervention through the Intervention View.
4. The mentor approves or rejects the intervention.
5. Parent email notification is sent for approved interventions when applicable.
6. Notification status is tracked to prevent duplicate emails.

## Version Control and Contribution

The project uses Git and GitHub for version control and team collaboration.

Recommended workflow:

1. Create or switch to your assigned feature branch.
2. Make and test your changes.
3. Commit the changes.
4. Push the branch to GitHub.
5. Create a Pull Request targeting `main`.
6. Review and merge after approval.

Avoid committing `.env` files, database credentials, passwords, or other sensitive information.

## Future Improvements

- Expand end-to-end testing across all seven agents.
- Strengthen page-level access control for protected views.
- Improve agent coordination and workflow observability.
- Expand student risk analytics and reporting.
- Improve recommendation evaluation.
- Add further monitoring and audit capabilities.

## Project Repository

GitHub: https://github.com/RAMAKRISHNAHUDDAR/agentic-ai
