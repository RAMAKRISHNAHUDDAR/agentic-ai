from datetime import datetime

from app.memory.memory_manager import add_memory, get_student_memory


def log_intervention(
    student_id,
    intervention,
    status="pending",
    mentor_feedback=""
):
    """Create and store an intervention record."""

    record = {
        "student_id": student_id,
        "intervention": intervention,
        "status": status,
        "mentor_feedback": mentor_feedback,
        "timestamp": datetime.now().isoformat()
    }

    return add_memory(record)


def get_intervention_history(student_id):
    """Retrieve intervention history for a student."""
    return get_student_memory(student_id)