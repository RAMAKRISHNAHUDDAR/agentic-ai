from app.agents.contineo_agent import ContineoDataCollectionAgent
from app.agents.lms_agent import LMSDataCollectionAgent
from app.agents.internship_agent import InternshipDataCollectionAgent
from app.agents.placement_agent import PlacementDataCollectionAgent


class CoordinatorAgent:
    """
    Coordinates the student data collection agents.
    """

    def __init__(self):
        self.contineo_agent = ContineoDataCollectionAgent()
        self.lms_agent = LMSDataCollectionAgent()
        self.internship_agent = InternshipDataCollectionAgent()
        self.placement_agent = PlacementDataCollectionAgent()

    def run(self, task: str):
        student_id = self._extract_student_id(task)

        if not student_id:
            return {
                "status": "error",
                "message": "No valid student ID found in the task."
            }

        # Collect data through specialized agents
        contineo = self.contineo_agent.collect(student_id)

        if contineo.get("status") == "error":
            return contineo

        if not contineo.get("student"):
            return {
        "status": "error",
        "message": f"Student {student_id} not found."
        }   

        lms = self.lms_agent.collect(student_id)
        internship = self.internship_agent.collect(student_id)
        placement = self.placement_agent.collect(student_id)

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