from app.agents.coordinator_agent import CoordinatorAgent


def test_coordinator_collects_student_data():
    agent = CoordinatorAgent()

    result = agent.run(
        "Collect complete student information for STU003"
    )

    assert result["status"] == "success"
    assert result["student"]["student_id"] == "STU003"
    assert result["academic"]["marks"] == 38.0
    assert result["attendance"]["attendance"] == 45.0
    assert result["internship"]["internship_status"] == "Not Started"
    assert result["placement"]["placement_status"] == "Not Ready"


def test_coordinator_handles_invalid_student():
    agent = CoordinatorAgent()

    result = agent.run(
        "Collect complete student information for STU999"
    )

    assert result["status"] == "error"