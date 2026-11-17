
import json


SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"],
}

FEEDBACK_ROUNDS = [
    "Move Tuesday's session to the evening.",
    "Also make Friday's session shorter, only one hour.",
]


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

    def satisfied(self):
        return self.goal["schedule_generated"] is True

    def next_step(self):
        for field in ["subjects", "hours_per_day", "unavailable_days"]:
            if self.goal[field] is None:
                return ("ask", field)

        return ("generate_plan", None)

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
                    "planned": "read existing schedule before generating plan",
                    "action": "tool call: read_existing_schedule()",
                    "observed": busy,
                    "stopped": False,
                })

                self.plan = self._build_plan(busy)
                self.goal["schedule_generated"] = True

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "generate schedule from gathered requirements",
                    "action": "built weekly plan",
                    "observed": self.plan,
                    "stopped": True,
                    "stop_reason": "goal.schedule_generated is now True",
                })

        return self.plan

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

    # Apply feedback directly to the existing plan object
    def revise(self, feedback, round_number):
        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": f"apply feedback round {round_number}",
            "action": f"feedback received: '{feedback}'",
            "observed": None,
            "stopped": False,
        })

        if "tuesday" in feedback.lower() and "evening" in feedback.lower():
            if "Tuesday" in self.plan:
                self.plan["Tuesday"]["time"] = "20:00-22:00"

        elif "friday" in feedback.lower() and "one hour" in feedback.lower():
            if "Friday" in self.plan:
                self.plan["Friday"]["time"] = "17:00-18:00"

        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": f"confirm feedback round {round_number}",
            "action": f"mutated existing plan in round {round_number}",
            "observed": self.plan,
            "stopped": True,
            "stop_reason": "existing plan modified without regeneration",
        })

        return self.plan


if __name__ == "__main__":
    existing_schedule = {"busy_days": ["Wednesday"]}

    agent = StudyPlannerAgent(existing_schedule)

    print("=== Generating Initial Plan ===")
    initial_plan = agent.run()
    print(json.dumps(initial_plan, indent=2))

    # Keep reference to the original plan object
    original_plan_id = id(agent.plan)

    print("\n=== Feedback Round 1 ===")
    revised_plan = agent.revise(FEEDBACK_ROUNDS[0], 1)
    print(json.dumps(revised_plan, indent=2))

    print("\n=== Feedback Round 2 ===")
    revised_plan = agent.revise(FEEDBACK_ROUNDS[1], 2)
    print(json.dumps(revised_plan, indent=2))

    print("\n=== Same Plan Object Verification ===")
    print("Original plan object ID:", original_plan_id)
    print("Current plan object ID:", id(agent.plan))
    print("Same object:", original_plan_id == id(agent.plan))

    print("\n=== Full Iteration Log ===")
    for entry in agent.log:
        print(json.dumps(entry, indent=2))
