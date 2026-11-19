
"""
Lab 12 - Assignment 2
Mandatory Re-Evaluation After 5 Proposals
"""


class ProdChangeAgent:

    def __init__(self):
        self.audit_log = []
        self.evaluated = False
        self.proposal_count = 0
        self.proposals_since_evaluation = 0
        self.permissions = {"can_write": "staging_only"}

    def log(self, step, data):
        self.audit_log.append({
            "step": step,
            "data": data
        })

    def evaluate(self):
        pass_rate = 9 / 10
        self.evaluated = pass_rate >= 0.8

        # Reset the proposal counter after evaluation.
        self.proposals_since_evaluation = 0

        self.log("evaluation", {
            "pass_rate": pass_rate,
            "passed_gate": self.evaluated,
            "total_proposals": self.proposal_count
        })

        print("Agent evaluated successfully.")

        return self.evaluated

    def propose_change(
        self,
        diagnosis,
        action,
        rollback_plan,
        privacy_scrubbed
    ):

        if not self.evaluated:
            return {
                "rejected": True,
                "reason": "Agent must pass evaluation first."
            }

        # Assignment 2: Maximum five proposals per evaluation.
        if self.proposals_since_evaluation >= 5:
            self.log("proposal_blocked", {
                "reason": "Mandatory re-evaluation required",
                "proposals_since_evaluation": self.proposals_since_evaluation
            })

            return {
                "rejected": True,
                "reason": (
                    "Five proposals reached. "
                    "Call evaluate() before making another proposal."
                )
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

        # Count only valid proposals.
        self.proposal_count += 1
        self.proposals_since_evaluation += 1

        request = {
            "diagnosis": diagnosis,
            "proposed_action": action,
            "rollback_plan": rollback_plan,
            "requires_approval": True,
            "proposal_number": self.proposal_count
        }

        self.log("proposal_created", request)

        return request


if __name__ == "__main__":

    agent = ProdChangeAgent()

    print("=== Initial evaluation ===")
    agent.evaluate()

    print("\n=== First five proposals ===")

    for i in range(1, 6):
        result = agent.propose_change(
            diagnosis=f"Test diagnosis {i}",
            action=f"Test action {i}",
            rollback_plan=f"Rollback action {i}",
            privacy_scrubbed=True
        )

        print(f"Proposal {i}: {result}")

    print("\n=== Sixth proposal: Must be blocked ===")

    result = agent.propose_change(
        diagnosis="Sixth test diagnosis",
        action="Sixth test action",
        rollback_plan="Rollback sixth action",
        privacy_scrubbed=True
    )

    print(result)

    assert result["rejected"] is True

    print("\nPASS: Sixth proposal was blocked.")

    print("\n=== Re-evaluation ===")

    agent.evaluate()

    print("\n=== Seventh proposal after re-evaluation ===")

    result = agent.propose_change(
        diagnosis="New test diagnosis",
        action="New test action",
        rollback_plan="Rollback new action",
        privacy_scrubbed=True
    )

    print(result)

    assert "rejected" not in result

    print("\nPASS: Proposal allowed after re-evaluation.")

    print("\n=== Audit Log ===")

    for entry in agent.audit_log:
        print(entry)
