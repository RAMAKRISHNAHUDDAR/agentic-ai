from app.tools.placement_tools import get_placement_status


class PlacementDataCollectionAgent:
    """
    Collects placement information for a student.
    """

    def collect(self, student_id: str):
        placement = get_placement_status(student_id)

        return {
            "student_id": student_id,
            "placement": placement
        }


if __name__ == "__main__":
    agent = PlacementDataCollectionAgent()

    result = agent.collect("STU003")

    print(result)