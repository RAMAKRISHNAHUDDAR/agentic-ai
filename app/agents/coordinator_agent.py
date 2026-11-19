from app.workflows.parallel_swarm import run_parallel_swarm


class CoordinatorAgent:
    """
    Coordinates the student data collection agents.
    """

    def run(self, task: str):
        student_id = self._extract_student_id(task)

        if not student_id:
            return {
                "status": "error",
                "message": "Which student should I review? Enter an ID such as STU003."
            }

        roles = ("contineo_agent", "lms_agent", "internship_agent", "placement_agent")
        batch = run_parallel_swarm([
            {"agent": role, "kwargs": {"student_id": student_id}} for role in roles
        ])
        if batch["errors"]:
            return {"status": "error", "message": batch["errors"][0]["message"]}
        fields = {}
        for result in batch["merged_result"]:
            fields.update(result)
        student = fields["student"]
        for field in ("academic", "attendance", "internship", "placement"):
            evidence = fields.get(field)
            if not evidence or any(v is None or student.get(k) != v for k, v in evidence.items()):
                return {"status": "error", "message": f"Please verify the {field} record for {student_id}."}
        return {**fields, "status": "success"}

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
    if not agent._extract_student_id(task):
        task += " " + input("Which student should I review? ")
    result = agent.run(task)

    print(result)