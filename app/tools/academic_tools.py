
from app.database.repositories import get_student


def get_academic_data(student_id: str):
    """Get academic information for a student from MongoDB."""
    student = get_student(student_id)

    if not student:
        return None

    return {
        "student_id": student["student_id"],
        "marks": student["marks"],
        "assignments": student["assignments"],
        "backlogs": student["backlogs"],
    }
