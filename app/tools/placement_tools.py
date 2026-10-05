from app.database.database import get_student


def get_placement_status(student_id: str):
    """Get placement status for a student."""
    student = get_student(student_id)

    if not student:
        return None

    return {
        "student_id": student["student_id"],
        "placement_status": student["placement_status"],
    }