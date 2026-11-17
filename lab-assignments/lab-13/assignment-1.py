"""
Lab 13 - Assignment 1
Electrical Engineering: Load Forecasting Agent
"""

# Simulated electrical load readings
ELECTRICAL_LOG = [
    {"t": 0, "load_kw": 45, "voltage_v": 230},
    {"t": 1, "load_kw": 48, "voltage_v": 229},
    {"t": 2, "load_kw": 55, "voltage_v": 228},
    {"t": 3, "load_kw": 65, "voltage_v": 227},
    {"t": 4, "load_kw": 78, "voltage_v": 226},
    {"t": 5, "load_kw": 92, "voltage_v": 225},
]

THRESHOLDS = {
    "load_warn": 70,
    "load_alarm": 90,
    "voltage_warn": 215,
    "voltage_alarm": 205
}


def tool_read_electrical_log():
    return ELECTRICAL_LOG


def classify_electrical_condition(reading):
    if (
        reading["load_kw"] >= THRESHOLDS["load_alarm"]
        or reading["voltage_v"] <= THRESHOLDS["voltage_alarm"]
    ):
        return "ALARM"

    if (
        reading["load_kw"] >= THRESHOLDS["load_warn"]
        or reading["voltage_v"] <= THRESHOLDS["voltage_warn"]
    ):
        return "WARNING"

    return "NORMAL"


def load_trend_direction(log):
    deltas = [
        log[i + 1]["load_kw"] - log[i]["load_kw"]
        for i in range(len(log) - 1)
    ]

    return "increasing" if all(d >= 0 for d in deltas) else "mixed"


def electrical_safety_check(condition):
    # Human review is mandatory for ALARM-level recommendations.
    if condition == "ALARM":
        return {
            "action_allowed": "recommend_load_reduction_for_human_review",
            "auto_execute": False
        }

    if condition == "WARNING":
        return {
            "action_allowed": "schedule_electrical_inspection",
            "auto_execute": False
        }

    return {
        "action_allowed": "continue_load_monitoring",
        "auto_execute": True
    }


def electrical_load_agent():
    log = tool_read_electrical_log()
    latest = log[-1]

    condition = classify_electrical_condition(latest)
    trend = load_trend_direction(log)
    safety = electrical_safety_check(condition)

    return {
        "domain": "Electrical Engineering -- Load Forecasting",
        "latest_reading": latest,
        "condition": condition,
        "load_trend": trend,
        "recommended_action": safety["action_allowed"],
        "auto_executed": safety["auto_execute"]
    }


if __name__ == "__main__":
    result = electrical_load_agent()

    print("=== Electrical Load Forecasting Agent ===")

    for key, value in result.items():
        print(f"{key}: {value}")

    assert (
        result["condition"] != "ALARM"
        or result["auto_executed"] is False
    )

    print("\nConfirmed: ALARM-level recommendations require human review.")