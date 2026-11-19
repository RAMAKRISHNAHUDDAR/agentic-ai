
"""
Lab 7 - Assignment 1
Add a Security-Scan Node between builder and tester.
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
    state["build_ok"] = True
    state["code"] = "app.py generated"
    return state


def security_scan_node(state):
    # Input: generated application code
    # Output: security_scan_passed and scan_report
    state["scan_report"] = {
        "checked": ["SQL injection", "hardcoded secrets", "unsafe input"],
        "vulnerabilities": (
            ["Hardcoded secret detected"]
            if state.get("force_security_fail")
            else []
        )
    }

    state["security_scan_passed"] = (
        len(state["scan_report"]["vulnerabilities"]) == 0
    )
    return state


def tester_node(state):
    state["tests_passed"] = (
        state.get("build_ok", False)
        and state.get("security_scan_passed", False)
    )
    return state


def reviewer_node(state):
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state):
    state["human_signoff"] = state.get("review_clean", False)
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
         builder_node, "retry_build_or_escalate"),

    Node("security_scan", "security_agent",
         lambda s: s.get("security_scan_passed", False),
         security_scan_node, "block_release_and_escalate"),

    Node("tester", "tester_agent",
         lambda s: s.get("tests_passed", False),
         tester_node, "route_back_to_builder"),

    Node("reviewer", "reviewer_agent",
         lambda s: s.get("review_clean", False),
         reviewer_node, "route_back_to_builder"),

    Node("human_gate", "human",
         lambda s: s.get("human_signoff", False),
         human_gate_node, "return_to_planner"),
]


def simulate(force_security_fail=False):
    state = {
        "force_security_fail": force_security_fail
    }
    trace = []

    for node in GRAPH:
        state = node.on_success(state)
        ok = node.success_fn(state)

        trace.append({
            "node": node.name,
            "owner": node.owner,
            "success": ok,
            "state_after": {
                k: v for k, v in state.items()
                if k != "force_security_fail"
            }
        })

        if not ok:
            trace.append({
                "node": node.name,
                "failure_behavior_triggered": node.on_fail
            })
            break

    return trace


if __name__ == "__main__":
    print("=== SECURITY SCAN SUCCESS PATH ===")
    for step in simulate(False):
        print(step)

    print("\n=== SECURITY SCAN FAILURE PATH ===")
    for step in simulate(True):
        print(step)
