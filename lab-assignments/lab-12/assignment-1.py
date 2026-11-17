
"""
Lab 12 - Assignment 1
Cost-Category Control
"""

BUDGET_THRESHOLD = 5000


class ProdChangeAgent:

    def __init__(self):
        self.audit_log = []
        self.evaluated = False
        self.permissions = {"can_write": "staging_only"}

    def log(self, step, data):
        self.audit_log.append({
            "step": step,
            "data": data
        })

    def evaluate(self):
        pass_rate = 9 / 10
        self.evaluated = pass_rate >= 0.8

        self.log("evaluation", {
            "pass_rate": pass_rate,
            "passed_gate": self.evaluated
        })

        return self.evaluated

    def propose_change(
        self,
        diagnosis,
        action,
        rollback_plan,
        privacy_scrubbed,
        cost_estimate=None,
        finance_approved=False
    ):

        if not self.evaluated:
            return {
                "rejected": True,
                "reason": "Evaluation gate not passed."
            }

        if self.permissions["can_write"] != "staging_only":
            raise PermissionError("Production write access is prohibited.")

        if not privacy_scrubbed:
            return {
                "rejected": True,
                "reason": "Privacy scrubbing is required."
            }

        if not rollback_plan:
            return {
                "rejected": True,
                "reason": "Rollback plan is required."
            }

        # Assignment 1: Cost must be explicitly provided.
        if cost_estimate is None:
            self.log("cost_check", {
                "rejected": True,
                "reason": "Missing cost estimate"
            })

            return {
                "rejected": True,
                "reason": "Cost estimate is mandatory; proposal rejected."
            }

        if not isinstance(cost_estimate, (int, float)) or cost_estimate < 0:
            return {
                "rejected": True,
                "reason": "Cost estimate must be a non-negative number."
            }

        # Reject costs exceeding the budget without finance approval.
        if cost_estimate > BUDGET_THRESHOLD and not finance_approved:
            self.log("cost_check", {
                "rejected": True,
                "cost_estimate": cost_estimate,
                "budget_threshold": BUDGET_THRESHOLD
            })

            return {
                "rejected": True,
                "reason": "Cost exceeds budget; finance approval required."
            }

        request = {
            "diagnosis": diagnosis,
            "proposed_action": action,
            "rollback_plan": rollback_plan,
            "cost_estimate": cost_estimate,
            "finance_approved": finance_approved,
            "requires_approval": True
        }

        self.log("approval_requested", request)

        return request


if __name__ == "__main__":

    agent = ProdChangeAgent()

    print("=== Evaluation ===")
    print(agent.evaluate())

    print("\n=== Test 1: Cost within budget ===")

    print(agent.propose_change(
        diagnosis="Memory leak detected.",
        action="Restart service",
        rollback_plan="Restore previous configuration.",
        privacy_scrubbed=True,
        cost_estimate=3000
    ))

    print("\n=== Test 2: Cost exceeds budget ===")

    print(agent.propose_change(
        diagnosis="Memory leak detected.",
        action="Upgrade infrastructure",
        rollback_plan="Restore previous infrastructure.",
        privacy_scrubbed=True,
        cost_estimate=8000
    ))

    print("\n=== Test 3: High cost with finance approval ===")

    print(agent.propose_change(
        diagnosis="Memory leak detected.",
        action="Upgrade infrastructure",
        rollback_plan="Restore previous infrastructure.",
        privacy_scrubbed=True,
        cost_estimate=8000,
        finance_approved=True
    ))

    print("\n=== Test 4: Adversarial test - missing cost ===")

    result = agent.propose_change(
        diagnosis="Memory leak detected.",
        action="Upgrade infrastructure",
        rollback_plan="Restore previous infrastructure.",
        privacy_scrubbed=True
        # Intentionally omitting cost_estimate
    )

    print(result)

    assert result["rejected"] is True
    assert "Cost estimate is mandatory" in result["reason"]

    print("\nPASS: Missing cost estimate was rejected.")
