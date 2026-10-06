from datetime import datetime

from app.database.database import add_intervention
from app.memory.memory_manager import add_memory, get_student_memory


def log_intervention(
    student_id,
    intervention,
    status="pending",
    mentor_feedback=""
):
    """Create and store an intervention record."""

    timestamp = datetime.now().isoformat()

    record = {
        "student_id": student_id,
        "intervention": intervention,
        "status": status,
        "mentor_feedback": mentor_feedback,
        "timestamp": timestamp
    }

    # Store in the existing JSON memory system.
    add_memory(record)

    # Store in the SQLite database.
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
