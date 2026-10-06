from app.agents.coordinator_agent import CoordinatorAgent


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

        # Node 2: Prepare collected data
        result = {
            "status": "success",
            "student_id": student_id,
            "student": data["student"],
            "academic": data["academic"],
            "attendance": data["attendance"],
            "internship": data["internship"],
            "placement": data["placement"]
        }

        return result


if __name__ == "__main__":
    workflow = StudentSuccessNodeGraph()

    student_id = input("Enter student ID: ")
    result = workflow.run(student_id)

    print(result)