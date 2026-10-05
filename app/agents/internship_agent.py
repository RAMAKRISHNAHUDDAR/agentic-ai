from app.tools.internship_tools import get_internship_status


class InternshipDataCollectionAgent:
    """
    Collects internship information for a student.
    """

    def collect(self, student_id: str):
        internship = get_internship_status(student_id)

        return {
            "student_id": student_id,
            "internship": internship
        }


if __name__ == "__main__":
    agent = InternshipDataCollectionAgent()

    result = agent.collect("STU003")

    print(result)