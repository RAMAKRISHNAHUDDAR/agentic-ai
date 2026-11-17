"""
Lab 10: Cloud Operations Agent -- Failed Deployment Diagnosis

Observe -> Reason -> Act, ending in a drafted human-approval request.
The agent NEVER auto-executes high-risk remediation, even
under a simulated urgency prompt.
"""

LOGS = [
    {"ts": "14:00:00", "level": "INFO", "msg": "deploy started: payments-service v2.4.1"},
    {"ts": "14:00:45", "level": "INFO", "msg": "deploy completed: payments-service v2.4.1"},
    {"ts": "14:03:10", "level": "WARN", "msg": "refund endpoint latency elevated"},
    {"ts": "14:03:40", "level": "ERROR", "msg": "refund endpoint: NullPointerException in RefundHandler"},
    {"ts": "14:04:05", "level": "ERROR", "msg": "refund endpoint: NullPointerException in RefundHandler"},
    {"ts": "14:04:30", "level": "ERROR", "msg": "refund endpoint: NullPointerException in RefundHandler"},
]

DEPLOY_HISTORY = [
    {
        "ts": "14:00:00",
        "service": "payments-service",
        "version": "v2.4.1",
        "prev_version": "v2.4.0"
    }
]

METRICS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 1.6
}


def classify_severity(metrics):
    ratio = metrics["current_error_rate"] / metrics["baseline_error_rate"]

    if metrics["current_error_rate"] > 50:
        return "critical"

    if ratio >= 2:
        return "degraded"

    return "early_warning"


def find_incident_start(logs):
    for entry in logs:
        if entry["level"] == "ERROR":
            return entry["ts"]

    return None


def correlate_with_recent_changes(logs, deploys, incident_start):
    error_msgs = [
        log["msg"]
        for log in logs
        if log["level"] == "ERROR"
    ]

    affected_path = (
        ["refund"]
        if any("refund" in msg.lower() for msg in error_msgs)
        else ["unknown"]
    )

    for deploy in deploys:
        if deploy["ts"] < incident_start:
            if deploy["service"].lower().startswith("payments"):
                return {
                    "hypothesis": (
                        f"Error rate rose starting {incident_start}, shortly "
                        f"after the {deploy['ts']} deploy of "
                        f"{deploy['service']} {deploy['version']}. "
                        f"Errors are concentrated in the "
                        f"{affected_path[0]} code path, consistent with a "
                        f"regression introduced in that release."
                    ),
                    "suspect_deploy": deploy,
                    "affected_path": affected_path
                }

    return {
        "hypothesis": "No recent deploy correlates with the incident window.",
        "suspect_deploy": None,
        "affected_path": affected_path
    }


def risk_level(action):
    HIGH_RISK = {
        "rollback",
        "scale",
        "config_change",
        "delete"
    }

    LOW_RISK = {
        "open_ticket",
        "notify",
        "restart_single_pod"
    }

    if action in HIGH_RISK:
        return "high"

    if action in LOW_RISK:
        return "low"

    return "unknown"


def draft_approval_request(hypothesis, action, rollback_plan):
    return {
        "diagnosis": hypothesis["hypothesis"],
        "proposed_action": action,
        "risk_if_wrong": (
            "Brief service interruption (~30s) during rollback "
            "if hypothesis is incorrect."
        ),
        "rollback_plan": rollback_plan,
        "status": "AWAITING HUMAN APPROVAL -- NOT EXECUTED"
    }


def diagnose_and_propose(logs, deploys, metrics, urgency_prompt=False):
    severity = classify_severity(metrics)
    incident_start = find_incident_start(logs)

    hypothesis = correlate_with_recent_changes(
        logs,
        deploys,
        incident_start
    )

    proposed_action = "rollback"
    risk = risk_level(proposed_action)

    if risk == "high":
        request = draft_approval_request(
            hypothesis,
            proposed_action,
            (
                f"Revert to {hypothesis['suspect_deploy']['prev_version']}; "
                f"if that also errors, re-deploy "
                f"{hypothesis['suspect_deploy']['version']}."
            )
        )

        if urgency_prompt:
            request["note"] = (
                "Urgency noted, but high-risk action still requires "
                "human approval -- not bypassing the gate."
            )

        return {
            "severity": severity,
            "incident_start": incident_start,
            **request
        }

    return {
        "severity": severity,
        "incident_start": incident_start,
        "action_executed": proposed_action
    }


if __name__ == "__main__":
    result = diagnose_and_propose(
        LOGS,
        DEPLOY_HISTORY,
        METRICS,
        urgency_prompt=True
    )

    print("=== Diagnostic + Approval Request ===")

    for key, value in result.items():
        print(f"{key}: {value}")

    assert "action_executed" not in result, (
        "High-risk action must never auto-execute!"
    )

    print("\nConfirmed: no destructive action was executed automatically.")