from app.memory.memory_manager import load_memory


def check_intervention_approval(student_id, intervention):
    """Check whether an intervention has mentor approval."""

    records = load_memory()

    for record in records:
        if (
            record.get("student_id") == student_id
            and record.get("intervention") == intervention
        ):
            if record.get("status") == "approved":
                return {
                    "approved": True,
                    "status": "approved",
                    "mentor_feedback": record.get("mentor_feedback", "")
                }

            return {
                "approved": False,
                "status": record.get("status", "pending"),
                "mentor_feedback": record.get("mentor_feedback", "")
            }

    return {
        "approved": False,
        "status": "not_found",
        "mentor_feedback": ""
    }