
from app.database.repositories import (
    get_interventions,
    update_intervention_status,
)
from app.runtime.audit_logger import log_action


def _format_intervention(record):
    """Convert a MongoDB intervention into the existing application format."""

    return {
        "intervention_id": record["intervention_id"],
        "student_id": record["student_id"],
        "intervention": record.get(
            "description",
            record.get("intervention", "")
        ),
        "status": record.get("status", "pending"),
        "mentor_feedback": record.get("mentor_feedback", ""),
        "timestamp": record.get(
            "created_at",
            record.get("timestamp", "")
        ),
    }


def _review_intervention(
    student_id,
    intervention,
    status,
    mentor_feedback=""
):
    """Find and review a pending intervention in MongoDB."""

    records = get_interventions(student_id)

    for record in records:
        description = record.get(
            "description",
            record.get("intervention", "")
        )

        if (
            description == intervention
            and record.get("status") == "pending"
        ):

            updated_record = update_intervention_status(
                intervention_id=record["intervention_id"],
                status=status,
                reviewed_by="Mentor",
                mentor_feedback=mentor_feedback,
            )

            if updated_record is None:
                return {
                    "error": "Intervention could not be updated."
                }

            action = (
                "approve_intervention"
                if status == "approved"
                else "reject_intervention"
            )

            result = (
                "Approved"
                if status == "approved"
                else "Rejected"
            )

            log_action(
                student_id,
                "Mentor Approval",
                action,
                result
            )

            return _format_intervention(updated_record)

    return {
        "error": "Pending intervention not found"
    }


def approve_intervention(
    student_id,
    intervention,
    mentor_feedback=""
):
    """Approve a pending intervention for a student."""

    return _review_intervention(
        student_id,
        intervention,
        "approved",
        mentor_feedback,
    )


def reject_intervention(
    student_id,
    intervention,
    mentor_feedback=""
):
    """Reject a pending intervention for a student."""

    return _review_intervention(
        student_id,
        intervention,
        "rejected",
        mentor_feedback,
    )
