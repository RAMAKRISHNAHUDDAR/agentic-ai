
"""
Lab 8 - Assignment 1
Add a fifth role: Marketing.
"""

from concurrent.futures import ThreadPoolExecutor


def research_agent(goal):
    return {
        "role": "research",
        "output": "Past events favored a 24-hour format with themed tracks."
    }


def logistics_agent(goal):
    return {
        "role": "logistics",
        "output": {
            "venue": "Grand Hall",
            "venue_cost": 45000,
            "date": "Saturday"
        }
    }


def budget_agent(goal):
    return {
        "role": "budget",
        "output": {"total_cap": 30000}
    }


def judging_agent(goal):
    return {
        "role": "judging",
        "output": "Judge on innovation, technical depth, and demo quality."
    }


def marketing_agent(goal):
    return {
        "role": "marketing",
        "output": {
            "publicity_plan": "Social media campaign, posters and email promotions",
            "marketing_cost": 12000
        }
    }


ROLES = {
    "research": research_agent,
    "logistics": logistics_agent,
    "budget": budget_agent,
    "judging": judging_agent,
    "marketing": marketing_agent,
}


def run_swarm(goal):
    with ThreadPoolExecutor(max_workers=len(ROLES)) as pool:
        futures = {
            name: pool.submit(fn, goal)
            for name, fn in ROLES.items()
        }

        return {
            name: future.result()
            for name, future in futures.items()
        }


def merge(outputs):
    return {
        "format_notes": outputs["research"]["output"],
        "venue": outputs["logistics"]["output"]["venue"],
        "venue_cost": outputs["logistics"]["output"]["venue_cost"],
        "date": outputs["logistics"]["output"]["date"],
        "budget_cap": outputs["budget"]["output"]["total_cap"],
        "judging_criteria": outputs["judging"]["output"],
        "publicity_plan": outputs["marketing"]["output"]["publicity_plan"],
        "marketing_cost": outputs["marketing"]["output"]["marketing_cost"],
    }


def critique(draft):
    conflicts = []

    if draft["venue_cost"] > draft["budget_cap"]:
        conflicts.append({
            "conflict": "venue_cost exceeds budget_cap",
            "roles_involved": ["logistics", "budget"],
            "value": draft["venue_cost"],
            "budget_value": draft["budget_cap"],
        })

    if draft["marketing_cost"] > draft["budget_cap"]:
        conflicts.append({
            "conflict": "marketing_cost exceeds budget_cap",
            "roles_involved": ["marketing", "budget"],
            "value": draft["marketing_cost"],
            "budget_value": draft["budget_cap"],
        })

    return conflicts


def resolve(conflict, priority_rule="budget_over_preference"):
    if conflict["conflict"] in [
        "venue_cost exceeds budget_cap",
        "marketing_cost exceeds budget_cap"
    ]:
        return {
            "rule_applied": priority_rule,
            "resolution": (
                f"Reject proposed cost {conflict['value']}; "
                f"request a revised proposal within "
                f"{conflict['budget_value']}."
            )
        }

    return {
        "rule_applied": priority_rule,
        "resolution": "no rule matched"
    }


if __name__ == "__main__":
    outputs = run_swarm("Plan a college AI hackathon")

    print("=== Parallel role outputs ===")
    for name, out in outputs.items():
        print(name, ":", out["output"])

    draft = merge(outputs)
    print("\n=== Merged draft plan ===")
    print(draft)

    conflicts = critique(draft)
    print("\n=== Conflicts ===")

    conflict_log = []

    for conflict in conflicts:
        result = resolve(conflict)
        entry = {**conflict, **result}
        conflict_log.append(entry)
        print(entry)

    if not conflicts:
        print("No conflicts found.")

    print("\n=== Extended conflict log ===")
    for entry in conflict_log:
        print(entry)
