from app.database.database import get_student
from app.ml.risk_model import train_model, predict_risk


def generate_reasons(student):
    """Generate simple reasons for the student's risk."""
    reasons = []

    if student["attendance"] < 60:
        reasons.append("Attendance is below 60%.")

    if student["marks"] < 50:
        reasons.append("Marks are below 50%.")

    if student["assignments"] < 50:
        reasons.append("Assignments are below 50%.")

    if student["backlogs"] >= 2:
        reasons.append(f"Student has {student['backlogs']} backlogs.")

    if not reasons:
        reasons.append("No major risk indicators found.")

    return reasons


def analyze_student_risk(student_id):
    """Analyze the risk of one student."""
    student = get_student(student_id)

    if not student:
        return {
            "error": "Student not found"
        }

    model, _, _ = train_model()

    prediction = predict_risk(model, student)

    reasons = generate_reasons(student)

    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "risk": (
            "At Risk"
            if prediction["prediction"] == 1
            else "Not At Risk"
        ),
        "risk_probability": prediction["risk_probability"],
        "reasons": reasons,
    }


if __name__ == "__main__":
    student_id = input("Enter student ID: ")
    result = analyze_student_risk(student_id)

    print("Student Risk Analysis")
    print("---------------------")
    print(f"Student ID: {result['student_id']}")
    print(f"Name: {result['name']}")
    print(f"Risk: {result['risk']}")
    print(f"Risk Probability: {result['risk_probability']:.2%}")

    print()
    print("Reasons:")
    for reason in result["reasons"]:
        print(f"- {reason}")