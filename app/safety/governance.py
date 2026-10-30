
from app.database.repositories import get_interventions


def check_intervention_approval(student_id, intervention):
    """Check whether an intervention has mentor approval using MongoDB."""

    records = get_interventions(student_id)

    for record in records:
        description = record.get(
            "description",
            record.get("intervention", "")
        )

        if description == intervention:
            status = record.get("status", "pending")

            if status == "approved":
                return {
                    "approved": True,
                    "status": "approved",
                    "mentor_feedback": record.get("mentor_feedback", "")
                }

            return {
                "approved": False,
                "status": status,
                "mentor_feedback": record.get("mentor_feedback", "")
            }

    return {
        "approved": False,
        "status": "not_found",
        "mentor_feedback": ""
    }
