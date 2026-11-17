
"""
Lab 6 - Assignment 2
Escalate After Two Failures

If the same skill fails twice for the same user,
the third attempt is escalated to a human.
"""

from datetime import datetime


# ---- Tools ------------------------------------------------------

def tool_word_count(text):
    return {"count": len(text.split())}


def tool_lookup_contact(name, contacts_db):
    return contacts_db.get(
        name,
        {"error": f"no contact found for {name}"}
    )


TOOLS = {
    "word_count": tool_word_count,
    "lookup_contact": tool_lookup_contact,
}


# ---- Memory -----------------------------------------------------

class Memory:
    def __init__(self):
        self._store = {}

    def scope(self, user):
        return self._store.setdefault(user, {})


# ---- Audit ------------------------------------------------------

class Audit:
    def __init__(self):
        self.entries = []

    def log(
        self,
        task,
        skill_name,
        tool_calls,
        result=None,
        error=None
    ):
        self.entries.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "task": task,
            "skill": skill_name,
            "tool_calls": tool_calls,
            "result": result,
            "error": error,
        })


# ---- Skills -----------------------------------------------------

class SummarizeNotesSkill:
    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        text = task.get("text", "")
        wc = TOOLS["word_count"](text)

        self.tool_calls.append({
            "tool": "word_count",
            "output": wc
        })

        self.memory_scope["last_note_length"] = wc["count"]

        return f"Summary stub: note has {wc['count']} words."


class DraftEmailSkill:
    CONTACTS = {
        "Dr. Meena": {
            "email": "meena@example.edu"
        }
    }

    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        contact = TOOLS["lookup_contact"](
            task["to"],
            self.CONTACTS
        )

        self.tool_calls.append({
            "tool": "lookup_contact",
            "output": contact
        })

        if "error" in contact:
            raise RuntimeError(contact["error"])

        return (
            f"Draft email to {contact['email']}: "
            f"'{task['subject']}'"
        )


class TranslateTextSkill:
    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        return (
            f"[translated to {task['target_lang']}] "
            f"{task['text']}"
        )


SKILL_REGISTRY = {
    "summarize_notes": SummarizeNotesSkill,
    "draft_email": DraftEmailSkill,
    "translate_text": TranslateTextSkill,
}


# ---- Runtime core loop: unchanged -------------------------------

def select_skill(task):
    return task["skill"]


def run_task(task, user, memory, audit):
    skill_name = select_skill(task)
    skill_cls = SKILL_REGISTRY[skill_name]
    skill = skill_cls(memory.scope(user))

    try:
        result = skill.execute(task)

        audit.log(
            task,
            skill_name,
            skill.tool_calls,
            result=result
        )

        return result

    except Exception as e:
        audit.log(
            task,
            skill_name,
            skill.tool_calls,
            error=str(e)
        )

        raise


# ---- Escalation control -----------------------------------------

def receive_task(task, user, memory, audit):
    skill_name = task["skill"]

    # Count previous failures for this user and skill.
    previous_failures = sum(
        1
        for entry in audit.entries
        if entry["skill"] == skill_name
        and entry["task"].get("_user") == user
        and entry["error"] is not None
    )

    # Escalate instead of executing the third attempt.
    if previous_failures >= 2:
        message = (
            f"HUMAN ESCALATION: skill '{skill_name}' "
            f"failed twice for user '{user}'. "
            "A human must review the issue."
        )

        audit.log(
            {**task, "_user": user},
            skill_name,
            [],
            error="Escalated to human after two failures"
        )

        return message

    # Attach user identity to the task so the audit log
    # can identify failures belonging to each user.
    tracked_task = {
        **task,
        "_user": user
    }

    return run_task(tracked_task, user, memory, audit)


if __name__ == "__main__":

    memory, audit = Memory(), Audit()
    user = "uday"

    failing_task = {
        "skill": "draft_email",
        "to": "Unknown Person",
        "subject": "Hello"
    }

    print("=== First attempt ===")

    try:
        print(receive_task(failing_task, user, memory, audit))
    except RuntimeError as e:
        print(f"Failure recorded: {e}")

    print("\n=== Second attempt ===")

    try:
        print(receive_task(failing_task, user, memory, audit))
    except RuntimeError as e:
        print(f"Failure recorded: {e}")

    print("\n=== Third attempt ===")
    print(receive_task(failing_task, user, memory, audit))

    print("\n=== Full audit log ===")

    for entry in audit.entries:
        print(entry)

    print("\n=== Failure and escalation summary ===")

    failures = [
        entry for entry in audit.entries
        if entry["skill"] == "draft_email"
        and entry["task"].get("_user") == user
        and entry["error"] is not None
    ]

    print("Recorded failures/escalations:", len(failures))
    print("Human escalation recorded:", any(
        "Escalated to human" in str(entry["error"])
        for entry in failures
    ))
