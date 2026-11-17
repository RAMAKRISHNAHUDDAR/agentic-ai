
import json


SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"],
}


class StudyPlannerAgent:
    def __init__(self, existing_schedule):
        self.goal = {
            "subjects": None,
            "hours_per_day": None,
            "unavailable_days": None,
            "schedule_generated": False,
        }

        self.existing_schedule = existing_schedule
        self.plan = None
        self.log = []
        self.conflicts = []

    def satisfied(self):
        return self.goal["schedule_generated"] is True

    def next_step(self):
        for field in ["subjects", "hours_per_day", "unavailable_days"]:
            if self.goal[field] is None:
                return ("ask", field)

        return ("generate_plan", None)

    # Read existing schedule with two busy days
    def read_existing_schedule(self):
        result = self.existing_schedule

        if "error" in result:
            raise RuntimeError(f"tool error: {result['error']}")

        return result

    def run(self):
        while not self.satisfied():
            step, arg = self.next_step()

            if step == "ask":
                answer = SIMULATED_ANSWERS[arg]
                self.goal[arg] = answer

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": f"ask for {arg}",
                    "action": f"asked user for {arg}",
                    "observed": answer,
                    "stopped": False,
                })

            elif step == "generate_plan":
                busy = self.read_existing_schedule()

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "read existing schedule",
                    "action": "tool call: read_existing_schedule()",
                    "observed": busy,
                    "stopped": False,
                })

                # Check whether all busy days are avoided
                busy_days = set(busy.get("busy_days", []))
                unavailable_days = set(
                    self.goal["unavailable_days"]
                )

                conflicting_days = busy_days - unavailable_days

                if conflicting_days:
                    self.conflicts = sorted(conflicting_days)

                    conflict_message = (
                        "Scheduling conflict detected! "
                        "The following busy days are not included "
                        "in the student's unavailable days: "
                        + ", ".join(self.conflicts)
                    )

                    print("\n" + conflict_message)

                    self.log.append({
                        "iteration": len(self.log) + 1,
                        "planned": "check scheduling conflicts",
                        "action": "reported scheduling conflict",
                        "observed": conflict_message,
                        "stopped": False,
                    })

                    # Do not silently finalize a conflicting plan
                    return None

                self.plan = self._build_plan(busy)
                self.goal["schedule_generated"] = True

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "generate schedule",
                    "action": "built weekly plan",
                    "observed": self.plan,
                    "stopped": True,
                    "stop_reason": "goal.schedule_generated is now True",
                })

        return self.plan

    # Build the plan only after conflict validation
    def _build_plan(self, busy_slots):
        days = [
            day for day in
            ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]
            if day not in self.goal["unavailable_days"]
        ]

        subjects = self.goal["subjects"]
        plan = {}

        for i, day in enumerate(days):
            subject = subjects[i % len(subjects)]
            slot = "17:00-19:00"

            if day in busy_slots.get("busy_days", []):
                slot = "20:00-22:00"

            plan[day] = {
                "subject": subject,
                "time": slot,
            }

        return plan


if __name__ == "__main__":

    # Tool returns two busy days
    existing_schedule = {
        "busy_days": ["Wednesday", "Friday"]
    }

    agent = StudyPlannerAgent(existing_schedule)

    print("=== Starting Study Planner Agent ===")

    plan = agent.run()

    print("\n=== Scheduling Result ===")

    if plan is None:
        print("Plan was not finalized because of a conflict.")
    else:
        print(json.dumps(plan, indent=2))

    print("\n=== Detected Conflicts ===")
    print(json.dumps(agent.conflicts, indent=2))

    print("\n=== Full Iteration Log ===")

    for entry in agent.log:
        print(json.dumps(entry, indent=2))
