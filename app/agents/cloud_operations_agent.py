def classify_severity(error_rate, baseline_error_rate):
    """Classify incident severity using the error-rate ratio."""

    if baseline_error_rate <= 0:
        raise ValueError("Baseline error rate must be greater than zero.")

    ratio = error_rate / baseline_error_rate

    if ratio >= 2:
        return "critical"
    elif ratio >= 1.5:
        return "degraded"

    return "normal"


def correlate_with_recent_changes(logs, deploy_history):
    """Identify a likely cause by correlating errors with recent deployments."""

    if not deploy_history:
        return "No recent deployment found to correlate with the incident."

    error_text = " ".join(logs).lower()

    latest_deploy = deploy_history[-1]

    service = latest_deploy["service"]
    version = latest_deploy["version"]
    deploy_time = latest_deploy["time"]

    if "refund" in error_text:
        code_path = "refund code path"
    else:
        code_path = "deployment-related code path"

    return (
        f"Errors appeared after the {deploy_time} deployment of "
        f"{service} {version}. Errors indicate an issue in the "
        f"{code_path}, suggesting a possible regression."
    )


def draft_approval_request(action, service, risk_reason):
    """Draft a human approval request for a high-risk action."""

    return {
        "status": "AWAITING HUMAN APPROVAL",
        "action": action,
        "service": service,
        "risk_if_wrong": risk_reason,
        "message": (
            f"Approval required to perform {action} on {service}. "
            f"Reason: {risk_reason}"
        )
    }


def run_cloud_operations(
    service,
    logs,
    error_rate,
    baseline_error_rate,
    deploy_history,
    urgency_prompt=False
):
    """Diagnose a deployment incident and prepare safe remediation."""

    try:
        severity = classify_severity(
            error_rate,
            baseline_error_rate
        )

        diagnosis = correlate_with_recent_changes(
            logs,
            deploy_history
        )

        action = "rollback"
        risk_level = "high"

        approval = draft_approval_request(
            action,
            service,
            "Brief service interruption if the rollback hypothesis is incorrect."
        )

        return {
            "status": "success",
            "affected_service": service,
            "severity": severity,
            "diagnosis": diagnosis,
            "proposed_action": action,
            "risk_level": risk_level,
            "rollback_plan": "Revert to the previous stable deployment version.",
            "approval_request": approval,
            "action_executed": False,
            "urgency_prompt": urgency_prompt,
            "note": (
                "Urgency does not bypass human approval. "
                "No deployment action was executed."
            )
        }

    except (ValueError, TypeError, KeyError) as error:
        return {
            "status": "error",
            "message": str(error)
        }