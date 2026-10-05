import csv
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

STUDENTS_FILE = DATA_DIR / "students.csv"
ACADEMIC_FILE = DATA_DIR / "academic_data.csv"
ATTENDANCE_FILE = DATA_DIR / "attendance.csv"
INTERNSHIP_FILE = DATA_DIR / "internship_data.csv"
PLACEMENT_FILE = DATA_DIR / "placement_data.csv"

random.seed(42)


FIRST_NAMES = [
    "Aarav", "Aditya", "Akash", "Aman", "Ananya",
    "Arjun", "Aryan", "Diya", "Isha", "Kavya",
    "Kiran", "Krishna", "Meera", "Neha", "Nikhil",
    "Pooja", "Priya", "Rahul", "Riya", "Rohan",
    "Sahil", "Sneha", "Tanvi", "Varun", "Vivek",
]

LAST_NAMES = [
    "Sharma", "Patil", "Rao", "Kumar", "Joshi",
    "Desai", "Shah", "Kulkarni", "Reddy", "Nair",
    "Pawar", "Shetty", "Naik", "Jadhav", "More",
]


def calculate_risk_label(attendance, marks, assignments, backlogs):
    """
    Risk label:
    1 = At Risk
    0 = Not At Risk

    A student is At Risk when at least two of these
    conditions are true:
      - attendance < 60
      - marks < 50
      - assignments < 50
      - backlogs >= 2
    """

    risk_indicators = 0

    if attendance < 60:
        risk_indicators += 1

    if marks < 50:
        risk_indicators += 1

    if assignments < 50:
        risk_indicators += 1

    if backlogs >= 2:
        risk_indicators += 1

    return 1 if risk_indicators >= 2 else 0


def generate_student(student_number):
    """
    Generate one synthetic student.

    The academic values are correlated so that
    weaker students generally have lower attendance,
    marks and assignments.
    """

    attendance = random.randint(40, 98)

    # Academic performance loosely follows attendance.
    marks = int(
        max(
            25,
            min(
                98,
                attendance + random.randint(-18, 10)
            )
        )
    )

    assignments = int(
        max(
            25,
            min(
                100,
                marks + random.randint(-12, 12)
            )
        )
    )

    # More likely to have backlogs when marks are low.
    if marks < 45:
        backlogs = random.randint(2, 4)
    elif marks < 60:
        backlogs = random.randint(0, 2)
    else:
        backlogs = random.choices(
            [0, 1],
            weights=[85, 15]
        )[0]

    # Internship status.
    if attendance >= 75 and marks >= 65:
        internship_status = random.choices(
            ["Completed", "In Progress"],
            weights=[60, 40]
        )[0]
    elif marks >= 50:
        internship_status = random.choices(
            ["In Progress", "Not Started"],
            weights=[70, 30]
        )[0]
    else:
        internship_status = random.choice(
            ["Not Started", "In Progress"]
        )

    # Placement status.
    if (
        attendance >= 75
        and marks >= 65
        and backlogs == 0
    ):
        placement_status = random.choices(
            ["Ready", "Preparing"],
            weights=[70, 30]
        )[0]
    elif marks >= 50 and backlogs <= 1:
        placement_status = random.choice(
            ["Preparing", "Not Ready"]
        )
    else:
        placement_status = "Not Ready"

    risk_label = calculate_risk_label(
        attendance,
        marks,
        assignments,
        backlogs,
    )

    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    return {
        "student_id": f"STU{student_number:03d}",
        "name": f"{first_name} {last_name}",
        "attendance": attendance,
        "marks": marks,
        "assignments": assignments,
        "backlogs": backlogs,
        "internship_status": internship_status,
        "placement_status": placement_status,
        "risk_label": risk_label,
    }


def load_existing_students():
    """Load the original 10 students."""
    with open(
        STUDENTS_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def write_students(students):
    """Write the complete students.csv file."""

    fieldnames = [
        "student_id",
        "name",
        "attendance",
        "marks",
        "assignments",
        "backlogs",
        "internship_status",
        "placement_status",
        "risk_label",
    ]

    with open(
        STUDENTS_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(students)


def write_related_files(students):
    """Create the four supporting CSV files."""

    with open(
        ACADEMIC_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "student_id",
                "marks",
                "assignments",
                "backlogs",
            ],
        )

        writer.writeheader()

        for student in students:
            writer.writerow({
                "student_id": student["student_id"],
                "marks": student["marks"],
                "assignments": student["assignments"],
                "backlogs": student["backlogs"],
            })

    with open(
        ATTENDANCE_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "student_id",
                "attendance",
            ],
        )

        writer.writeheader()

        for student in students:
            writer.writerow({
                "student_id": student["student_id"],
                "attendance": student["attendance"],
            })

    with open(
        INTERNSHIP_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "student_id",
                "internship_status",
            ],
        )

        writer.writeheader()

        for student in students:
            writer.writerow({
                "student_id": student["student_id"],
                "internship_status": student[
                    "internship_status"
                ],
            })

    with open(
        PLACEMENT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "student_id",
                "placement_status",
            ],
        )

        writer.writeheader()

        for student in students:
            writer.writerow({
                "student_id": student["student_id"],
                "placement_status": student[
                    "placement_status"
                ],
            })


def main():
    existing_students = load_existing_students()

    print(
        f"Existing students found: "
        f"{len(existing_students)}"
    )

    # Generate STU011 through STU1000.
    new_students = [
        generate_student(number)
        for number in range(11, 1001)
    ]

    all_students = existing_students + new_students

    write_students(all_students)
    write_related_files(all_students)

    print(
        f"Generated {len(new_students)} new students."
    )

    print(
        f"Total students: {len(all_students)}"
    )

    risk_count = sum(
        int(student["risk_label"])
        for student in all_students
    )

    print(f"At-risk students: {risk_count}")
    print(
        f"Not-at-risk students: "
        f"{len(all_students) - risk_count}"
    )


if __name__ == "__main__":
    main()