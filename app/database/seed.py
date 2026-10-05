import csv
from pathlib import Path

from app.database.database import get_connection, create_tables


BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "students.csv"


def seed_students():
    create_tables()

    connection = get_connection()

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            connection.execute(
                """
                INSERT OR REPLACE INTO students (
                    student_id,
                    name,
                    attendance,
                    marks,
                    assignments,
                    backlogs,
                    internship_status,
                    placement_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["student_id"],
                    row["name"],
                    float(row["attendance"]),
                    float(row["marks"]),
                    float(row["assignments"]),
                    int(row["backlogs"]),
                    row["internship_status"],
                    row["placement_status"],
                ),
            )

    connection.commit()
    connection.close()

    print("Student data seeded successfully.")


if __name__ == "__main__":
    seed_students()