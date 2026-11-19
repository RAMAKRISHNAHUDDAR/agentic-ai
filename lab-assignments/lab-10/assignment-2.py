# Assignment 2: Safe Auto-Remediation Path

def execute_low_risk_action(action):
    if risk_level(action) == "low":
        return {
            "action": action,
            "status": "EXECUTED",
            "message": "Low-risk action executed automatically."
        }

    return {
        "action": action,
        "status": "BLOCKED",
        "message": "Action is not permitted for automatic execution."
    }


def safe_diagnose_and_propose(
    logs,
    deploys,
    metrics,
    proposed_action
):
    severity = classify_severity(metrics)

    incident_start = find_incident_start(logs)

    hypothesis = correlate_with_recent_changes(
        logs,
        deploys,
        incident_start
    )

    risk = risk_level(proposed_action)

    if risk == "high":
        request = draft_approval_request(
            hypothesis,
            proposed_action,
            "Rollback requires human approval before execution."
        )

        return {
            "severity": severity,
            "risk": risk,
            **request,
            "action_executed": False
        }

    if risk == "low":
        execution = execute_low_risk_action(proposed_action)

        return {
            "severity": severity,
            "risk": risk,
            "diagnosis": hypothesis["hypothesis"],
            **execution
        }

    return {
        "severity": severity,
        "risk": risk,
        "status": "BLOCKED",
        "message": "Unknown action risk; manual review required."
    }


if __name__ == "__main__":

    # Scenario A: Low-risk restart
    print("=== Scenario A: Safe Auto-Remediation ===")

    warning_metrics = {
        "baseline_error_rate": 1.0,
        "current_error_rate": 1.2
    }

    safe_result = safe_diagnose_and_propose(
        LOGS,
        DEPLOY_HISTORY,
        warning_metrics,
        "restart_single_pod"
    )

    for key, value in safe_result.items():
        print(f"{key}: {value}")

    assert safe_result["status"] == "EXECUTED"

    # Scenario B: High-risk rollback
    print("\n=== Scenario B: High-Risk Rollback ===")

    rollback_result = safe_diagnose_and_propose(
        LOGS,
        DEPLOY_HISTORY,
        METRICS,
        "rollback"
    )

    for key, value in rollback_result.items():
        print(f"{key}: {value}")

    assert rollback_result["status"] == "AWAITING HUMAN APPROVAL -- NOT EXECUTED"
    assert rollback_result["action_executed"] is False

    print("\nConfirmed:")
    print("- Low-risk restart executed automatically.")
    print("- High-risk rollback requires human approval.")