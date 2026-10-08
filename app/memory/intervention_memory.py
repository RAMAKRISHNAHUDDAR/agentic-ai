from datetime import datetime

from app.database.database import (
    add_intervention,
    get_student_interventions,
)
from app.memory.memory_manager import (
    add_memory,
    get_student_memory,
)


def log_intervention(
    student_id,
    intervention,
    status="pending",
    mentor_feedback=""
):
    """Create and store an intervention if it does not already exist."""

    # Check existing memory records first.
    existing_records = get_student_memory(student_id)

    for record in existing_records:
        if record.get("intervention") == intervention:
            return record

    timestamp = datetime.now().isoformat()

    record = {
        "student_id": student_id,
        "intervention": intervention,
        "status": status,
        "mentor_feedback": mentor_feedback,
        "timestamp": timestamp,
    }

    # Store in JSON memory.
    add_memory(record)

    # Store in SQLite.
    add_intervention(
        student_id=student_id,
        intervention=intervention,
        status=status,
        mentor_feedback=mentor_feedback,
        timestamp=timestamp,
    )

    return record


def get_intervention_history(student_id):
    """Retrieve intervention history for a student."""
    return get_student_memory(student_id)