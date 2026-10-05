import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "student_success.db"


def get_connection():
    """Create and return a SQLite database connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create the students table if it does not already exist."""
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            attendance REAL NOT NULL,
            marks REAL NOT NULL,
            assignments REAL NOT NULL,
            backlogs INTEGER NOT NULL,
            internship_status TEXT NOT NULL,
            placement_status TEXT NOT NULL,
            risk_label INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_student(student_id):
    """Return one student by student ID."""
    connection = get_connection()

    cursor = connection.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()
    connection.close()

    return dict(student) if student else None


def get_all_students():
    """Return all students."""
    connection = get_connection()

    cursor = connection.execute(
        "SELECT * FROM students ORDER BY student_id"
    )

    students = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return students