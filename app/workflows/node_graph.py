from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.risk_agent import analyze_student_risk
from app.mcp.client import get_student


class StudentSuccessNodeGraph:
    """
    Simple node-based workflow for the Student Success
    and Early Warning System.
    """

    def __init__(self):
        self.coordinator = CoordinatorAgent()

    def run(self, student_id: str):
        # Node 1: Collect student data
        data = self.coordinator.run(
            f"Collect complete student information for {student_id}"
        )

        if data["status"] == "error":
            return data

        # Node 2: Get student data through MCP
        mcp_student = get_student(student_id)

        if "error" in mcp_student:
            return {
                "status": "error",
                "message": "MCP student data retrieval failed."
            }

        # Node 3: Analyze student risk
        risk = analyze_student_risk(student_id)

        if "error" in risk:
            return {
                "status": "error",
                "message": "Student risk analysis failed."
            }

        # Node 4: Prepare final result
        result = {
            "status": "success",
            "student_id": student_id,
            "student": data["student"],
            "academic": data["academic"],
            "attendance": data["attendance"],
            "internship": data["internship"],
            "placement": data["placement"],
            "mcp_student": mcp_student,
            "risk": risk
        }

        return result


if __name__ == "__main__":
    workflow = StudentSuccessNodeGraph()

    student_id = input("Enter student ID: ")
    result = workflow.run(student_id)

    print(result)