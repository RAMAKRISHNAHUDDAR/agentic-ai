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
        "Collect complete student information for STU9999"
    )

    assert result["status"] == "error"
    
def test_coordinator_handles_missing_student_id():
    agent = CoordinatorAgent()

    result = agent.run(
        "Collect complete student information"
    )

    assert result["status"] == "error"
    assert "student ID" in result["message"]