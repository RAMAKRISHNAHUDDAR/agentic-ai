from app.runtime.agent_runtime import agent_runtime


class CoordinatorAgent:
    """
    Coordinates the student data collection agents.
    """

    def run(self, task: str):
        student_id = self._extract_student_id(task)

        if not student_id:
            return {
                "status": "error",
                "message": "No valid student ID found in the task."
            }

        # Collect data through Agent Runtime
        contineo = agent_runtime.execute_agent(
            "contineo_agent", student_id=student_id
        )

        if contineo.get("status") == "error":
            return contineo

        if not contineo.get("student"):
            return {
                "status": "error",
                "message": f"Student {student_id} not found."
            }

        lms = agent_runtime.execute_agent(
            "lms_agent", student_id=student_id
        )

        internship = agent_runtime.execute_agent(
            "internship_agent", student_id=student_id
        )

        placement = agent_runtime.execute_agent(
            "placement_agent", student_id=student_id
        )

        return {
            "status": "success",
            "student": contineo["student"],
            "academic": lms["academic"],
            "attendance": lms["attendance"],
            "internship": internship["internship"],
            "placement": placement["placement"]
        }

    @staticmethod
    def _extract_student_id(task: str):
        """Find a student ID from the task."""
        words = task.upper().replace(",", " ").split()

        for word in words:
            if word.startswith("STU") and word[3:].isdigit():
                return word

        return None


if __name__ == "__main__":
    agent = CoordinatorAgent()

    task = input("Enter task: ")
    result = agent.run(task)

    print(result)