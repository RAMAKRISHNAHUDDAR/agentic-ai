from app.database.database import get_student
from app.agents.risk_agent import analyze_student_risk
from app.memory.intervention_memory import log_intervention
from app.runtime.audit_logger import log_action


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
    student = get_student(student_id)

    if not student:
        log_action(
            student_id,
            "Recommendation Agent",
            "create_action_plan",
            "Student not found"
        )
        return {"error": "Student not found"}

    risk_analysis = analyze_student_risk(student_id)
    recommendations = generate_recommendations(student)

    interventions = []

    for recommendation in recommendations:
        interventions.append(
            log_intervention(
                student_id=student_id,
                intervention=recommendation
            )
        )

    log_action(
        student["student_id"],
        "Recommendation Agent",
        "create_action_plan",
        f"{len(recommendations)} recommendations generated"
    )

    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "risk": risk_analysis["risk"],
        "risk_probability": risk_analysis["risk_probability"],
        "recommendations": recommendations,
        "interventions": interventions,
        "mentor_approval_required": True,
    }