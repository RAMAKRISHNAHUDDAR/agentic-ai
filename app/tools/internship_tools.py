
from app.database.repositories import get_student


def get_internship_status(student_id: str):
    """Get internship status for a student from MongoDB."""
    student = get_student(student_id)

    if not student:
        return None

    return {
        "student_id": student["student_id"],
        "internship_status": student["internship_status"],
    }
