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
    connection.execute("""
        CREATE TABLE IF NOT EXISTS interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            intervention TEXT NOT NULL,
            status TEXT NOT NULL,
            mentor_feedback TEXT DEFAULT '',
            timestamp TEXT NOT NULL
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

def add_intervention(
    student_id,
    intervention,
    status,
    mentor_feedback,
    timestamp
):
    """Store an intervention in the SQLite database."""
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO interventions (
            student_id,
            intervention,
            status,
            mentor_feedback,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student_id,
            intervention,
            status,
            mentor_feedback,
            timestamp,
        ),
    )

    connection.commit()
    connection.close()


def get_student_interventions(student_id):
    """Return all interventions for a student from SQLite."""
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT
            id,
            student_id,
            intervention,
            status,
            mentor_feedback,
            timestamp
        FROM interventions
        WHERE student_id = ?
        ORDER BY id
        """,
        (student_id,),
    )

    interventions = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return interventions


def update_intervention(
    student_id,
    intervention,
    status,
    mentor_feedback
):
    """Update an intervention's status and mentor feedback."""
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE interventions
        SET
            status = ?,
            mentor_feedback = ?
        WHERE student_id = ?
          AND intervention = ?
        """,
        (
            status,
            mentor_feedback,
            student_id,
            intervention,
        ),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0