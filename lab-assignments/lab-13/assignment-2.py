"""
Lab 13 - Assignment 2
Escalate on a Trend, Not Just a Threshold
"""

SENSOR_LOG = [
    {"t": 0, "vibration_mm_s": 1.8, "temp_c": 61},
    {"t": 1, "vibration_mm_s": 2.9, "temp_c": 65},
    {"t": 2, "vibration_mm_s": 3.1, "temp_c": 67},
    {"t": 3, "vibration_mm_s": 3.8, "temp_c": 69},
    {"t": 4, "vibration_mm_s": 3.9, "temp_c": 69},
    {"t": 5, "vibration_mm_s": 4.0, "temp_c": 69},
]

THRESHOLDS = {
    "vibration_warn": 2.8,
    "vibration_alarm": 4.5,
    "temp_warn": 70,
    "temp_alarm": 80
}


def classify_condition(reading):
    if (
        reading["vibration_mm_s"] >= THRESHOLDS["vibration_alarm"]
        or reading["temp_c"] >= THRESHOLDS["temp_alarm"]
    ):
        return "ALARM"

    if (
        reading["vibration_mm_s"] >= THRESHOLDS["vibration_warn"]
        or reading["temp_c"] >= THRESHOLDS["temp_warn"]
    ):
        return "WARNING"

    return "NORMAL"


def safety_check(condition, warning_count):
    # ALARM always requires human review.
    if condition == "ALARM":
        return {
            "action_allowed": "recommend_shutdown_for_human_review",
            "auto_execute": False
        }

    # Three consecutive WARNING readings trigger escalation.
    if warning_count >= 3:
        return {
            "action_allowed": "schedule_inspection",
            "auto_execute": False
        }

    if condition == "WARNING":
        return {
            "action_allowed": "continue_monitoring",
            "auto_execute": False
        }

    return {
        "action_allowed": "continue_monitoring",
        "auto_execute": True
    }


def predictive_maintenance_agent():
    warning_count = 0
    latest_condition = "NORMAL"

    for reading in SENSOR_LOG:
        condition = classify_condition(reading)

        if condition == "WARNING":
            warning_count += 1
        else:
            warning_count = 0

        latest_condition = condition

    latest = SENSOR_LOG[-1]

    safety = safety_check(latest_condition, warning_count)

    return {
        "domain": "Mechanical Engineering -- Predictive Maintenance",
        "latest_reading": latest,
        "condition": latest_condition,
        "consecutive_warning_readings": warning_count,
        "recommended_action": safety["action_allowed"],
        "auto_executed": safety["auto_execute"]
    }


if __name__ == "__main__":
    result = predictive_maintenance_agent()

    print("=== Trend-Based Predictive Maintenance Agent ===")

    for key, value in result.items():
        print(f"{key}: {value}")

    assert result["consecutive_warning_readings"] == 5
    assert result["recommended_action"] == "schedule_inspection"
    assert result["auto_executed"] is False

    print(
        "\nConfirmed: consecutive WARNING readings trigger "
        "inspection without reaching ALARM."
    )