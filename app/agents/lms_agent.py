from app.tools.academic_tools import get_academic_data
from app.tools.attendance_tools import get_attendance


class LMSDataCollectionAgent:
    """
    Collects academic and attendance information
    from the LMS-related tools.
    """

    def collect(self, student_id: str):
        academic = get_academic_data(student_id)
        attendance = get_attendance(student_id)

        return {
            "student_id": student_id,
            "academic": academic,
            "attendance": attendance
        }


if __name__ == "__main__":
    agent = LMSDataCollectionAgent()

    result = agent.collect("STU003")

    print(result)