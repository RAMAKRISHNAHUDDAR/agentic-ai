from app.database.database import get_student
from app.agents.risk_agent import analyze_student_risk


def generate_recommendations(student):
    """Generate an action plan based on student risk indicators."""
    recommendations = []

    if student["attendance"] < 60:
        recommendations.append(
            "Improve attendance and maintain at least 75% attendance."
        )

    if student["marks"] < 50:
        recommendations.append(
            "Attend academic support sessions and improve subject marks."
        )

    if student["assignments"] < 50:
        recommendations.append(
            "Complete pending assignments and maintain regular submission."
        )

    if student["backlogs"] >= 2:
        recommendations.append(
            "Create a backlog clearance plan with mentor guidance."
        )

    if student["internship_status"] == "Not Started":
        recommendations.append(
            "Start the internship preparation process."
        )

    if student["placement_status"] == "Not Ready":
        recommendations.append(
            "Begin placement preparation and career guidance activities."
        )

    if not recommendations:
        recommendations.append(
            "Continue current academic and career preparation."
        )

    return recommendations


def create_action_plan(student_id):
    """Create an intervention action plan for a student."""
    student = get_student(student_id)

    if not student:
        return {
            "error": "Student not found"
        }

    risk_analysis = analyze_student_risk(student_id)

    recommendations = generate_recommendations(student)

    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "risk": risk_analysis["risk"],
        "risk_probability": risk_analysis["risk_probability"],
        "recommendations": recommendations,
        "mentor_approval_required": True,
    }