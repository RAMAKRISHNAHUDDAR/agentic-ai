
from math import isfinite


DEFAULT_ERROR_INDICATORS = {
    "refund": "refund code path",
    "payment": "payment processing",
    "timeout": "service timeout",
    "database": "database operation",
    "connection": "service connection",
    "authentication": "authentication",
    "memory": "memory usage",
    "cpu": "CPU usage",
}


def classify_severity(
    error_rate,
    baseline_error_rate,
    critical_ratio=2.0,
    degraded_ratio=1.5
):
    """Classify incident severity using configurable error-rate thresholds."""

    values = (error_rate, baseline_error_rate, critical_ratio, degraded_ratio)

    if not all(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and isfinite(value)
        for value in values
    ):
        raise ValueError("Error rates and thresholds must be valid numbers.")

    if not 0 <= error_rate <= 100 or not 0 < baseline_error_rate <= 100:
        raise ValueError(
            "Error rates must be percentages between 0 and 100, "
            "and baseline must be greater than zero."
        )

    if critical_ratio <= degraded_ratio or degraded_ratio <= 1:
        raise ValueError(
            "Critical threshold must be greater than degraded threshold, "
            "and degraded threshold must be greater than 1."
        )

    ratio = error_rate / baseline_error_rate

    if ratio >= critical_ratio:
        return "critical"
    elif ratio >= degraded_ratio:
        return "degraded"

    return "normal"


def correlate_with_recent_changes(
    logs,
    deploy_history,
    error_indicators=None
):
    """Identify a possible deployment-related cause from logs and history."""

    if not deploy_history:
        return "No recent deployment found to correlate with the incident."

    if not isinstance(logs, list) or not all(
        isinstance(line, str) for line in logs
    ):
        raise ValueError("Logs must be a list of text entries.")

    latest_deploy = deploy_history[-1]

    service = latest_deploy["service"]
    version = latest_deploy["version"]
    deploy_time = latest_deploy["time"]

    error_text = " ".join(logs).lower()

    indicators = (
        DEFAULT_ERROR_INDICATORS
        if error_indicators is None
        else error_indicators
    )

    matched_paths = [
        description
        for keyword, description in indicators.items()
        if keyword.lower() in error_text
    ]

    if matched_paths:
        code_path = ", ".join(matched_paths)
    else:
        code_path = "an unidentified application code path"

    previous_version = latest_deploy.get("previous_version")

    if previous_version:
        version_context = (
            f" Previous recorded version: {previous_version}."
        )
    else:
        version_context = ""

    return (
        f"Incident logs contain indicators related to {code_path}. "
        f"The latest recorded deployment was {service} {version} "
        f"at {deploy_time}.{version_context} "
        "This deployment is a possible cause of the incident, "
        "but the available data does not establish causation."
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
    urgency_prompt=False,
    critical_ratio=2.0,
    degraded_ratio=1.5
):
    """Diagnose a deployment incident and prepare safe remediation."""

    try:
        if not isinstance(service, str) or not service.strip():
            raise ValueError("Service name is required.")

        if not isinstance(logs, list) or not all(
            isinstance(line, str) for line in logs
        ):
            raise ValueError("Logs must be a list of text entries.")

        if not isinstance(deploy_history, list):
            raise ValueError("Deployment history must be a list.")

        severity = classify_severity(
            error_rate,
            baseline_error_rate,
            critical_ratio,
            degraded_ratio
        )

        service_history = [
            entry for entry in deploy_history
            if isinstance(entry, dict)
            and entry.get("service") == service
        ]

        if severity == "normal":
            return {
                "status": "success",
                "severity": severity,
                "affected_service": service,
                "proposed_action": "monitor",
                "action_executed": False,
                "approval_request": None,
            }

        has_error_logs = any(
            word in line.lower()
            for line in logs
            for word in ("error", "fail", "exception")
        )

        if not service_history or not has_error_logs:
            return {
                "status": "success",
                "severity": severity,
                "affected_service": service,
                "proposed_action": "gather_evidence",
                "action_executed": False,
                "approval_request": None,
                "note": (
                    "More incident evidence or matching deployment "
                    "history is required before proposing rollback."
                )
            }

        latest_deploy = service_history[-1]

        required_fields = ("version", "time")
        if not all(latest_deploy.get(field) for field in required_fields):
            raise ValueError(
                "Deployment history requires version and time."
            )

        diagnosis = correlate_with_recent_changes(
            logs,
            service_history
        )

        action = "rollback"
        risk_level = "high"

        previous_version = latest_deploy.get("previous_version")

        if previous_version:
            rollback_plan = (
                f"Revert {service} from {latest_deploy['version']} "
                f"to the previous recorded version {previous_version}."
            )
        else:
            rollback_plan = (
                "Revert to the previous stable deployment version. "
                "The target version must be confirmed before execution."
            )

        approval = draft_approval_request(
            action,
            service,
            "A rollback may cause a brief service interruption "
            "if the rollback hypothesis is incorrect."
        )

        return {
            "status": "success",
            "affected_service": service,
            "severity": severity,
            "diagnosis": diagnosis,
            "proposed_action": action,
            "risk_level": risk_level,
            "previous_version": previous_version,
            "rollback_plan": rollback_plan,
            "approval_request": approval,
            "action_executed": False,
            "urgency_prompt": urgency_prompt,
            "note": (
                "Urgency does not bypass human approval. "
                "No deployment action was executed."
            )
        }

    except (ValueError, TypeError, KeyError, AttributeError) as error:
        return {
            "status": "error",
            "message": str(error)
        }
