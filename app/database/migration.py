
import sqlite3
from pathlib import Path

import pandas as pd

from app.database.mongodb import get_database
from app.database.indexes import create_indexes
from app.database import validators


# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

STUDENTS_CSV = DATA_DIR / "students.csv"

SUPPLEMENTAL_CSVS = [
    DATA_DIR / "academic_data.csv",
    DATA_DIR / "attendance.csv",
    DATA_DIR / "internship_data.csv",
    DATA_DIR / "placement_data.csv",
]

SQLITE_DB = DATA_DIR / "student_success.db"

SPECIAL_PARENT_EMAILS = {
    "STU378": "neilrego3@gmail.com",
    "STU007": "ramakrishnahuddar@gmail.com"
}


INDIAN_PARENT_FIRST_NAMES = [
    "Rajesh", "Sunita", "Amit", "Kavita", "Suresh",
    "Meena", "Vijay", "Anita", "Ramesh", "Pooja",
    "Sanjay", "Neha", "Mahesh", "Priya", "Ashok",
    "Rekha", "Prakash", "Seema", "Anil", "Swati",
    "Manoj", "Deepa", "Nitin", "Shilpa", "Ravi"
]

INDIAN_PARENT_LAST_NAMES = [
    "Sharma", "Patil", "Desai", "Kulkarni", "Joshi",
    "Verma", "Shah", "Reddy", "Iyer", "Nair",
    "Gupta", "Kadam", "Jadhav", "Pawar", "Mehta",
    "Mishra", "Chavan", "More", "Singh", "Kulkarni"
]



def load_and_merge_student_csvs():
    """Load and merge all five CSV files using student_id."""

    students = pd.read_csv(STUDENTS_CSV)

    if students["student_id"].duplicated().any():
        raise ValueError("Duplicate student IDs found in students.csv")

    merged = students.copy()

    for file_path in SUPPLEMENTAL_CSVS:
        supplemental = pd.read_csv(file_path)

        if supplemental["student_id"].duplicated().any():
            raise ValueError(
                f"Duplicate student IDs found in {file_path.name}"
            )

        if set(merged["student_id"]) != set(supplemental["student_id"]):
            raise ValueError(
                f"Student IDs do not match in {file_path.name}"
            )

        # Check overlapping columns for inconsistent values.
        overlapping = [
            column
            for column in supplemental.columns
            if column in merged.columns and column != "student_id"
        ]

        comparison = merged.merge(
            supplemental,
            on="student_id",
            how="inner",
            suffixes=("_main", "_source"),
            validate="one_to_one"
        )

        for column in overlapping:
            if not comparison[f"{column}_main"].equals(
                comparison[f"{column}_source"]
            ):
                raise ValueError(
                    f"Inconsistent {column} values in {file_path.name}"
                )

        # Use the supplemental file as the source for its fields.
        merged = merged.drop(columns=overlapping)

        merged = merged.merge(
            supplemental,
            on="student_id",
            how="inner",
            validate="one_to_one"
        )

    if len(merged) != len(students):
        raise ValueError("Student count changed during CSV merging")

    return merged



def generate_parent(student):
    """Generate deterministic synthetic Indian parent data."""

    student_id = str(student["student_id"])

    # Generate a consistent name for each student.
    numeric_part = int(
        "".join(
            character for character in student_id
            if character.isdigit()
        ) or 0
    )

    first_name = INDIAN_PARENT_FIRST_NAMES[
        numeric_part % len(INDIAN_PARENT_FIRST_NAMES)
    ]

    last_name = INDIAN_PARENT_LAST_NAMES[
        numeric_part % len(INDIAN_PARENT_LAST_NAMES)
    ]

    phone_number = str(9000000000 + numeric_part)

    email = SPECIAL_PARENT_EMAILS.get(
        student_id,
        f"parent_{student_id.lower()}@example.com"
    )

    return {
        "parent_id": f"PAR_{student_id}",
        "name": f"{first_name} {last_name}",
        "phone": phone_number,
        "email": email,
        "email_opt_in": True,
    }


def migrate_students_and_parents(db):
    """Migrate merged student data and generate parent records."""

    merged_students = load_and_merge_student_csvs()

    student_count = 0
    parent_count = 0

    for record in merged_students.to_dict(orient="records"):

        student_id = str(record["student_id"])

        student = {
            "student_id": student_id,
            "name": str(record["name"]),
            "attendance": float(record["attendance"]),
            "marks": float(record["marks"]),
            "assignments": float(record["assignments"]),
            "backlogs": int(record["backlogs"]),
            "internship_status": str(record["internship_status"]),
            "placement_status": str(record["placement_status"]),
            "risk_label": str(record["risk_label"]),
        }

        parent = generate_parent(student)
        validators.validate_parent(parent)

        # Save or update the parent.
        db.parents.update_one(
            {"parent_id": parent["parent_id"]},
            {"$set": parent},
            upsert=True
        )

        parent_count += 1

        # Link the parent to the student.
        student["parent_id"] = parent["parent_id"]

        validators.validate_student(student)

        db.students.update_one(
            {"student_id": student_id},
            {"$set": student},
            upsert=True
        )

        student_count += 1

    return student_count, parent_count


def migrate_interventions(db):
    """Migrate existing SQLite interventions without changing their status."""

    if not SQLITE_DB.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {SQLITE_DB}"
        )

    connection = sqlite3.connect(SQLITE_DB)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute(
            "SELECT * FROM interventions"
        ).fetchall()
    finally:
        connection.close()

    intervention_count = 0

    for row in rows:

        intervention = {
            "intervention_id": f"SQLITE_INT_{row['id']}",
            "student_id": str(row["student_id"]),
            "description": str(row["intervention"]),
            "status": str(row["status"]),
            "mentor_feedback": row["mentor_feedback"] or "",
            "timestamp": str(row["timestamp"]),
            "legacy_sqlite_id": row["id"],
        }

        validators.validate_intervention(intervention)

        # Confirm that the referenced student exists.
        if not db.students.find_one(
            {"student_id": intervention["student_id"]}
        ):
            raise ValueError(
                "Student not found for intervention: "
                f"{intervention['intervention_id']}"
            )

        # Direct upsert preserves the original intervention status.
        db.interventions.update_one(
            {"intervention_id": intervention["intervention_id"]},
            {"$set": intervention},
            upsert=True
        )

        intervention_count += 1

    return intervention_count


def migrate_all():
    """Run the complete student, parent and intervention migration."""

    db = get_database()

    # Ensure all required unique indexes exist.
    create_indexes(db)

    print("\nStarting CSV migration...")

    student_count, parent_count = migrate_students_and_parents(db)

    print(f"Students migrated: {student_count}")
    print(f"Parents migrated: {parent_count}")

    print("\nStarting SQLite intervention migration...")

    intervention_count = migrate_interventions(db)

    print(f"Interventions migrated: {intervention_count}")

    print("\nMigration completed successfully!")

    print("\nMongoDB collection counts:")
    print("Students:", db.students.count_documents({}))
    print("Parents:", db.parents.count_documents({}))
    print("Interventions:", db.interventions.count_documents({}))


if __name__ == "__main__":
    migrate_all()
