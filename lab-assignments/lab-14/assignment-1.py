"""
Lab 14 - Assignment 1
Add a Second Reusable Skill
"""

from datetime import datetime

# ---- Tools ----

FAQ_DB = {
    "wifi": "Connect to 'Campus-Secure' and log in with your student ID."
}

TICKET_DB = []


def tool_search_faq(query):
    for k, v in FAQ_DB.items():
        if k in query.lower():
            return {"found": True, "answer": v}

    return {"found": False}


def tool_create_ticket(issue):
    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"

    TICKET_DB.append({
        "id": ticket_id,
        "issue": issue,
        "status": "open"
    })

    return {"ticket_id": ticket_id}


def tool_check_ticket_status(ticket_id):
    for t in TICKET_DB:
        if t["id"] == ticket_id:
            return t

    return {"error": "not found"}


# ---- Skill 1: General issue triage ----

def triage_skill(issue_text):
    faq_result = tool_search_faq(issue_text)

    if faq_result["found"]:
        return {
            "resolution": "faq",
            "answer": faq_result["answer"]
        }

    ticket = tool_create_ticket(issue_text)

    return {
        "resolution": "escalated",
        "ticket_id": ticket["ticket_id"]
    }


# ---- Skill 2: Password reset guidance ----

def password_reset_skill(issue_text):
    """
    Password reset instructions.
    Never request or store a user's password.
    """

    return {
        "resolution": "password_guidance",
        "instructions": [
            "Open the official campus login page.",
            "Select Forgot Password.",
            "Enter your registered student email.",
            "Follow the password reset link sent to your email.",
            "Contact IT support if you cannot access your registered email."
        ],
        "security_note": "Never share your password or OTP."
    }


# ---- Memory ----

class CapstoneMemory:

    def __init__(self):
        self.session = {}
        self.history = []

    def record(self, user, issue, outcome):
        entry = {
            "user": user,
            "issue": issue,
            "outcome": outcome,
            "date": datetime.now().isoformat(timespec="seconds")
        }

        self.history.append(entry)
        self.session["last_issue"] = issue


# ---- Node graph with skill routing ----

def node_graph_run(user, issue, memory, audit_log, prompt_log):

    prompt_log.append({
        "stage": "intake",
        "input": issue
    })

    if not issue.strip():
        audit_log.append({
            "stage": "intake",
            "result": "rejected",
            "reason": "empty issue text"
        })

        return {
            "rejected": True,
            "reason": "empty issue text"
        }

    # Route to password skill or general triage skill.
    if "password" in issue.lower() or "reset" in issue.lower():
        skill_name = "password_reset_skill"
        outcome = password_reset_skill(issue)

    else:
        skill_name = "triage_skill"
        outcome = triage_skill(issue)

    prompt_log.append({
        "stage": "triage",
        "skill": skill_name,
        "output": outcome
    })

    if outcome["resolution"] == "faq":
        response = outcome["answer"]

    elif outcome["resolution"] == "password_guidance":
        response = "\n".join(outcome["instructions"])

    else:
        response = (
            f"Ticket {outcome['ticket_id']} created; "
            "support will follow up."
        )

    memory.record(user, issue, outcome)

    audit_log.append({
        "stage": "complete",
        "user": user,
        "issue": issue,
        "skill": skill_name,
        "outcome": outcome
    })

    return {
        "rejected": False,
        "skill": skill_name,
        "response": response,
        "outcome": outcome
    }


if __name__ == "__main__":

    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    print("=== Run 1: General FAQ skill ===")

    r1 = node_graph_run(
        "alice",
        "How do I connect to wifi?",
        memory,
        audit_log,
        prompt_log
    )

    print(r1)

    print("\n=== Run 2: Password reset skill ===")

    r2 = node_graph_run(
        "bob",
        "I need help with password reset",
        memory,
        audit_log,
        prompt_log
    )

    print(r2)

    print("\n=== Run 3: General issue escalation ===")

    r3 = node_graph_run(
        "carol",
        "My laptop charger is broken",
        memory,
        audit_log,
        prompt_log
    )

    print(r3)

    print("\n=== Prompt log ===")

    for p in prompt_log:
        print(p)

    print("\n=== Audit log ===")

    for a in audit_log:
        print(a)

    print("\n=== Memory history ===")

    for h in memory.history:
        print(h)