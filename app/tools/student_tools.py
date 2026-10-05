from app.database.database import get_student, get_all_students


def get_student_data(student_id: str):
    """Get complete student information."""
    return get_student(student_id)


def get_all_student_data():
    """Get information for all students."""
    return get_all_students()