
from app.database.repositories import get_student


def get_attendance(student_id: str):
    """Get attendance information for a student from MongoDB."""
    student = get_student(student_id)

    if not student:
        return None

    return {
        "student_id": student["student_id"],
        "attendance": student["attendance"],
    }
