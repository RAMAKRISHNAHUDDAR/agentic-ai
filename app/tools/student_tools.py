
from app.database.repositories import (
    get_student,
    get_all_students,
)


def get_student_data(student_id: str):
    """Get complete student information from MongoDB."""
    return get_student(student_id)


def get_all_student_data():
    """Get information for all students from MongoDB."""
    return get_all_students()
