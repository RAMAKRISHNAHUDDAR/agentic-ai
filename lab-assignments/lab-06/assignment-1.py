
"""
Lab 6 - Assignment 1
Add Per-User Rate Limiting

Each user may run at most 3 tasks per session.
The limit is enforced inside receive_task().
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


# ---- Per-user rate limit ----------------------------------------

MAX_TASKS_PER_SESSION = 3
TASK_COUNTS = {}


def receive_task(task, user, memory, audit):
    current_count = TASK_COUNTS.get(user, 0)

    if current_count >= MAX_TASKS_PER_SESSION:
        return (
            f"Rate limit exceeded: user '{user}' may run "
            f"only {MAX_TASKS_PER_SESSION} tasks per session."
        )

    TASK_COUNTS[user] = current_count + 1

    return run_task(task, user, memory, audit)


if __name__ == "__main__":

    memory, audit = Memory(), Audit()
    user = "uday"

    task = {
        "skill": "summarize_notes",
        "text": "Agentic AI systems combine goals tools skills memory"
    }

    print("=== Task 1 ===")
    print(receive_task(task, user, memory, audit))

    print("\n=== Task 2 ===")
    print(receive_task(task, user, memory, audit))

    print("\n=== Task 3 ===")
    print(receive_task(task, user, memory, audit))

    print("\n=== Task 4: should be rejected ===")
    print(receive_task(task, user, memory, audit))

    print("\n=== User task count ===")
    print(TASK_COUNTS)
