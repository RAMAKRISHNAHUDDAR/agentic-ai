# Assignment 1: Second Incident Type
# Database connection-pool exhaustion

DB_LOGS = [
    {
        "ts": "15:00:00",
        "level": "INFO",
        "msg": "deploy started: database-service v3.2.0"
    },
    {
        "ts": "15:00:30",
        "level": "INFO",
        "msg": "deploy completed: database-service v3.2.0"
    },
    {
        "ts": "15:02:00",
        "level": "WARN",
        "msg": "database connection pool usage above 90%"
    },
    {
        "ts": "15:03:00",
        "level": "ERROR",
        "msg": "database connection pool exhausted"
    },
    {
        "ts": "15:03:30",
        "level": "ERROR",
        "msg": "database connection timeout"
    },
    {
        "ts": "15:04:00",
        "level": "ERROR",
        "msg": "database connection pool exhausted"
    }
]

DB_DEPLOY_HISTORY = [
    {
        "ts": "15:00:00",
        "service": "database-service",
        "version": "v3.2.0",
        "prev_version": "v3.1.9"
    }
]

DB_METRICS = {
    "baseline_error_rate": 1.0,
    "current_error_rate": 4.5
}


def classify_db_severity(metrics):
    ratio = (
        metrics["current_error_rate"]
        / metrics["baseline_error_rate"]
    )

    if metrics["current_error_rate"] > 50:
        return "critical"

    if ratio >= 2:
        return "degraded"

    return "early_warning"


def diagnose_db_incident(logs, deploys):
    incident_start = find_incident_start(logs)

    error_messages = [
        entry["msg"].lower()
        for entry in logs
        if entry["level"] == "ERROR"
    ]

    if any("connection pool" in msg for msg in error_messages):
        affected_path = "database connection pool"
        diagnosis = (
            "Database connection pool exhaustion detected. "
            "The service is unable to obtain available database connections."
        )
    else:
        affected_path = "unknown"
        diagnosis = "Database incident detected, but the cause is unclear."

    suspect_deploy = None

    for deploy in deploys:
        if deploy["ts"] < incident_start:
            suspect_deploy = deploy

    if suspect_deploy:
        diagnosis += (
            f" The incident started after deployment of "
            f"{suspect_deploy['service']} "
            f"{suspect_deploy['version']}."
        )

    return {
        "incident_start": incident_start,
        "affected_path": affected_path,
        "diagnosis": diagnosis,
        "suspect_deploy": suspect_deploy
    }


if __name__ == "__main__":
    db_severity = classify_db_severity(DB_METRICS)

    db_diagnosis = diagnose_db_incident(
        DB_LOGS,
        DB_DEPLOY_HISTORY
    )

    print("=== Database Incident Diagnosis ===")
    print("Severity:", db_severity)

    for key, value in db_diagnosis.items():
        print(f"{key}: {value}")

    assert db_diagnosis["affected_path"] == "database connection pool"
    assert db_severity != classify_severity(METRICS)

    print("\nConfirmed: database incident has a different diagnosis and severity.")