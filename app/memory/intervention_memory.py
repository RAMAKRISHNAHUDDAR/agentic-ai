
from uuid import uuid4

from app.database.repositories import (
    create_intervention,
    get_interventions,
)


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


def log_intervention(
    student_id,
    intervention,
    status="pending",
    mentor_feedback=""
):
    """Create and store an intervention in MongoDB if it does not already exist."""

    # Check existing MongoDB intervention records first.
    existing_records = get_interventions(student_id)

    for record in existing_records:
        description = record.get(
            "description",
            record.get("intervention", "")
        )

        if description == intervention:
            return _format_intervention(record)

    # New interventions must always start as pending.
    if status != "pending":
        raise ValueError(
            "New interventions must have pending status."
        )

    document = {
        "intervention_id": str(uuid4()),
        "student_id": student_id,
        "description": intervention,
        "mentor_feedback": mentor_feedback,
    }

    # Store the intervention in MongoDB.
    created_record = create_intervention(document)

    return _format_intervention(created_record)


def get_intervention_history(student_id):
    """Retrieve intervention history from MongoDB."""

    records = get_interventions(student_id)

    return [
        _format_intervention(record)
        for record in records
    ]
