
from unittest.mock import patch

from app.workflows.node_graph import StudentSuccessNodeGraph


def test_success_path():

    workflow = StudentSuccessNodeGraph()

    result = workflow.run("STU003")

    assert result["status"] == "success"
    assert result["student_id"] == "STU003"
    assert "risk" in result

    print("SUCCESS PATH PASSED")


def test_temporary_failure_retry():

    workflow = StudentSuccessNodeGraph()

    result = workflow.run(
        "STU003",
        simulate_failure=True
    )

    assert result["status"] == "success"
    assert result["risk"]["risk"] == "At Risk"

    print("RETRY PATH PASSED")


def test_permanent_failure():

    workflow = StudentSuccessNodeGraph()

    result = workflow.run(
        "STU003",
        simulate_failure=True,
        simulate_permanent_failure=True
    )

    assert result["status"] == "error"
    assert "Simulated risk analysis failure" in result["message"]

    print("PERMANENT FAILURE PATH PASSED")


if __name__ == "__main__":

    test_success_path()
    test_temporary_failure_retry()
    test_permanent_failure()

    print("\nALL LAB 7 TESTS PASSED")
