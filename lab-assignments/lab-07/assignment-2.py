
"""
Lab 7 - Assignment 2
Add a retry limit to the Builder Node.

Scenario A: Builder fails once, retries, and succeeds.
Scenario B: Builder fails twice and escalates to a human.
"""

class Node:
    def __init__(self, name, owner, success_fn, on_success, on_fail):
        self.name = name
        self.owner = owner
        self.success_fn = success_fn
        self.on_success = on_success
        self.on_fail = on_fail


def requirement_node(state):
    state["requirements"] = ["user login", "event listing", "RSVP button"]
    return state


def planner_node(state):
    state["tasks"] = {
        req: f"task_for({req})"
        for req in state["requirements"]
    }
    return state


def builder_node(state):
    state["build_attempts"] += 1

    if state["build_attempts"] <= state["fail_attempts"]:
        state["build_ok"] = False
        state["build_error"] = (
            f"Build failed on attempt {state['build_attempts']}"
        )
    else:
        state["build_ok"] = True
        state["code"] = "app.py generated"
        state["build_error"] = None

    return state


def tester_node(state):
    state["tests_passed"] = state.get("build_ok", False)
    return state


def reviewer_node(state):
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state):
    state["human_escalation"] = True
    state["escalation_reason"] = state.get(
        "build_error",
        "Builder failed after maximum attempts"
    )
    return state


GRAPH = [
    Node("requirement", "requirement_agent",
         lambda s: len(s.get("requirements", [])) >= 3,
         requirement_node, "escalate_to_human"),

    Node("planner", "planner_agent",
         lambda s: bool(s.get("tasks")),
         planner_node, "return_to_requirement"),

    Node("builder", "builder_agent",
         lambda s: s.get("build_ok", False),
         builder_node, "retry_once_then_escalate"),

    Node("tester", "tester_agent",
         lambda s: s.get("tests_passed", False),
         tester_node, "route_back_to_builder"),

    Node("reviewer", "reviewer_agent",
         lambda s: s.get("review_clean", False),
         reviewer_node, "route_back_to_builder"),
]


def simulate(fail_attempts):
    state = {
        "fail_attempts": fail_attempts,
        "build_attempts": 0,
        "build_ok": False,
        "human_escalation": False
    }

    trace = []

    for node in GRAPH:
        if node.name != "builder":
            state = node.on_success(state)
            ok = node.success_fn(state)

            trace.append({
                "node": node.name,
                "owner": node.owner,
                "success": ok
            })

            if not ok:
                break
            continue

        # Builder gets a maximum of two attempts.
        while state["build_attempts"] < 2:
            state = node.on_success(state)
            ok = node.success_fn(state)

            trace.append({
                "node": "builder",
                "owner": node.owner,
                "attempt": state["build_attempts"],
                "success": ok,
                "error": state.get("build_error")
            })

            if ok:
                break

        if not state["build_ok"]:
            trace.append({
                "node": "human_escalation",
                "owner": "human",
                "success": False,
                "reason": "Builder failed twice; human intervention required"
            })
            human_gate_node(state)
            break

    return trace, state


if __name__ == "__main__":
    print("=== SCENARIO A: FAIL ONCE, RETRY, SUCCEED ===")
    trace, state = simulate(fail_attempts=1)

    for step in trace:
        print(step)

    print("Final status:", "SUCCESS" if state["build_ok"] else "FAILED")

    print("\n=== SCENARIO B: FAIL TWICE, ESCALATE ===")
    trace, state = simulate(fail_attempts=2)

    for step in trace:
        print(step)

    print("Human escalation:", state["human_escalation"])
    print("Escalation reason:", state.get("escalation_reason"))
