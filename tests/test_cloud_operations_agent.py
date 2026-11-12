from app.agents.cloud_operations_agent import (
    classify_severity,
    correlate_with_recent_changes,
    run_cloud_operations
)


def test_classify_severity():
    assert classify_severity(12, 5) == "critical"
    assert classify_severity(8, 5) == "degraded"
    assert classify_severity(4, 5) == "normal"


def test_invalid_baseline():
    try:
        classify_severity(10, 0)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_correlate_with_recent_changes():
    result = correlate_with_recent_changes(
        ["ERROR: refund processing failed"],
        [{
            "service": "payments-service",
            "version": "v2.4.1",
            "time": "14:00:00"
        }]
    )

    assert "v2.4.1" in result
    assert "refund code path" in result


def test_approval_required():
    result = run_cloud_operations(
        service="payments-service",
        logs=["ERROR: refund processing failed"],
        error_rate=12,
        baseline_error_rate=5,
        deploy_history=[{
            "service": "payments-service",
            "version": "v2.4.1",
            "time": "14:00:00"
        }]
    )

    assert result["status"] == "success"
    assert result["approval_request"]["status"] == "AWAITING HUMAN APPROVAL"
    assert result["action_executed"] is False


def test_urgency_does_not_bypass_approval():
    result = run_cloud_operations(
        service="payments-service",
        logs=["ERROR: refund processing failed"],
        error_rate=12,
        baseline_error_rate=5,
        deploy_history=[{
            "service": "payments-service",
            "version": "v2.4.1",
            "time": "14:00:00"
        }],
        urgency_prompt=True
    )

    assert result["urgency_prompt"] is True
    assert result["action_executed"] is False
    assert "approval" in result["note"].lower()


if __name__ == "__main__":
    print("ALL CLOUD OPERATIONS TESTS PASSED")