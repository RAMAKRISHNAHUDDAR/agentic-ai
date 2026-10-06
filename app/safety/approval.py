from app.database.database import update_intervention
from app.memory.memory_manager import load_memory, save_memory
from app.runtime.audit_logger import log_action


def approve_intervention(
    student_id,
    intervention,
    mentor_feedback=""
):
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

            update_intervention(
                student_id=student_id,
                intervention=intervention,
                status="approved",
                mentor_feedback=mentor_feedback,
            )

            log_action(
                student_id,
                "Mentor Approval",
                "approve_intervention",
                "Approved"
            )

            return record

    return {"error": "Pending intervention not found"}


def reject_intervention(
    student_id,
    intervention,
    mentor_feedback=""
):
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

            update_intervention(
                student_id=student_id,
                intervention=intervention,
                status="rejected",
                mentor_feedback=mentor_feedback,
            )

            log_action(
                student_id,
                "Mentor Approval",
                "reject_intervention",
                "Rejected"
            )

            return record

    return {"error": "Pending intervention not found"}
