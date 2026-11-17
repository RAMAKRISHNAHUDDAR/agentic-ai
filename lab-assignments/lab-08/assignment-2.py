
"""
Lab 8 - Assignment 2
Distributed Critique

Each of the five roles independently critiques the merged draft
against its own constraints.
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


def research_critique(draft):
    objections = []

    if "24-hour" not in draft["format_notes"]:
        objections.append("Event format differs from research recommendation.")

    return objections


def logistics_critique(draft):
    objections = []

    if draft["venue_cost"] > draft["budget_cap"]:
        objections.append(
            f"Venue cost {draft['venue_cost']} exceeds budget "
            f"{draft['budget_cap']}."
        )

    return objections


def budget_critique(draft):
    objections = []

    total_cost = draft["venue_cost"] + draft["marketing_cost"]

    if total_cost > draft["budget_cap"]:
        objections.append(
            f"Combined cost {total_cost} exceeds budget "
            f"{draft['budget_cap']}."
        )

    return objections


def judging_critique(draft):
    objections = []

    if not draft["judging_criteria"]:
        objections.append("Judging criteria are missing.")

    return objections


def marketing_critique(draft):
    objections = []

    if draft["marketing_cost"] > draft["budget_cap"]:
        objections.append("Marketing cost alone exceeds the total budget.")

    return objections


CRITICS = {
    "research": research_critique,
    "logistics": logistics_critique,
    "budget": budget_critique,
    "judging": judging_critique,
    "marketing": marketing_critique,
}


def distributed_critique(draft):
    conflict_log = []

    with ThreadPoolExecutor(max_workers=len(CRITICS)) as pool:
        futures = {
            role: pool.submit(critic, draft)
            for role, critic in CRITICS.items()
        }

        for role, future in futures.items():
            objections = future.result()

            for objection in objections:
                conflict_log.append({
                    "raised_by": role,
                    "objection": objection
                })

    return conflict_log


if __name__ == "__main__":
    outputs = run_swarm("Plan a college AI hackathon")

    print("=== Parallel role outputs ===")
    for name, out in outputs.items():
        print(name, ":", out["output"])

    draft = merge(outputs)

    print("\n=== Merged draft plan ===")
    print(draft)

    conflict_log = distributed_critique(draft)

    print("\n=== Distributed critique ===")

    for entry in conflict_log:
        print(entry)

    print("\n=== Final conflict log ===")
    print("Total objections:", len(conflict_log))

    for entry in conflict_log:
        print(entry)
