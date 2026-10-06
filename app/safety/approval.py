from app.memory.memory_manager import load_memory, save_memory


def approve_intervention(student_id, intervention, mentor_feedback=""):
    """Approve a pending intervention for a student."""

    records = load_memory()

    for record in records:
        if (
            record.get("student_id") == student_id
            and record.get("intervention") == intervention
            and record.get("status") == "pending"
        ):
            record["status"] = "approved"
            record["mentor_feedback"] = mentor_feedback
            save_memory(records)

            return record

    return {
        "error": "Pending intervention not found"
    }


def reject_intervention(student_id, intervention, mentor_feedback=""):
    """Reject a pending intervention for a student."""

    records = load_memory()

    for record in records:
        if (
            record.get("student_id") == student_id
            and record.get("intervention") == intervention
            and record.get("status") == "pending"
        ):
            record["status"] = "rejected"
            record["mentor_feedback"] = mentor_feedback
            save_memory(records)

            return record

    return {
        "error": "Pending intervention not found"
    }