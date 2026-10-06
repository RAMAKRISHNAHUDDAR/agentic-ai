from app.tools.student_tools import get_student_data


class ContineoDataCollectionAgent:
    """
    Collects basic student information from the
    Contineo-related student data source.
    """

    def collect(self, student_id: str):
        student_data = get_student_data(student_id)

        if student_data is None:
            return {
                "status": "error",
                "message": f"Student {student_id} not found."
            }

        return {
            "status": "success",
            "student": student_data
        }


if __name__ == "__main__":
    agent = ContineoDataCollectionAgent()

    student_id = input("Enter student ID: ")
    result = agent.collect(student_id)

    print(result)