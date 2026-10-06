from app.database.database import get_student
from app.ml.risk_model import train_model, predict_risk
from app.runtime.audit_logger import log_action


def generate_reasons(student):
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
    student = get_student(student_id)

    if not student:
        log_action(
            student_id,
            "Risk Analysis Agent",
            "analyze_risk",
            "Student not found"
        )

        return {"error": "Student not found"}

    model, _, _ = train_model()
    prediction = predict_risk(model, student)
    reasons = generate_reasons(student)

    risk = "At Risk" if prediction["prediction"] == 1 else "Not At Risk"

    log_action(
        student["student_id"],
        "Risk Analysis Agent",
        "analyze_risk",
        risk
    )

    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "risk": risk,
        "risk_probability": prediction["risk_probability"],
        "reasons": reasons,
    }


if __name__ == "__main__":
    student_id = input("Enter student ID: ")

    result = analyze_student_risk(student_id)

    if "error" in result:
        print(result["error"])
    else:
        print("Student Risk Analysis")
        print("---------------------")
        print(f"Student ID: {result['student_id']}")
        print(f"Name: {result['name']}")
        print(f"Risk: {result['risk']}")
        print(f"Risk Probability: {result['risk_probability']:.2%}")

        print("\nReasons:")
        for reason in result["reasons"]:
            print(f"- {reason}")