
"""
Lab 12: Safety, Evaluation, and Governance
Guardrails for a Production-Change Agent.

Implements six controls and rejects actions when required
evidence is missing.
"""

REGRESSION_SUITE_RESULT = {"passed": 9, "total": 10}


class ProdChangeAgent:

    def __init__(self):
        self.permissions = {"can_write": "staging_only"}
        self.audit_log = []
        self.evaluated = False

    def evaluate(self):
        # Control 2: Evaluation gate
        pass_rate = (
            REGRESSION_SUITE_RESULT["passed"]
            / REGRESSION_SUITE_RESULT["total"]
        )

        self.evaluated = pass_rate >= 0.8

        self._log(
            "evaluation",
            {
                "pass_rate": pass_rate,
                "passed_gate": self.evaluated
            }
        )

        return self.evaluated

    def _log(self, step, data):
        # Control 4: Audit every decision point
        self.audit_log.append({
            "step": step,
            "data": data
        })

    def propose_change(
        self,
        diagnosis,
        action,
        rollback_plan,
        privacy_scrubbed
    ):

        if not self.evaluated:
            self._log(
                "propose_change",
                {"rejected": True, "reason": "Agent not evaluated"}
            )
            return {
                "rejected": True,
                "reason": "Evaluation gate not passed; cannot propose changes."
            }

        # Control 1: Least-privilege permissions
        if self.permissions["can_write"] != "staging_only":
            raise PermissionError(
                "Agent must not hold direct production write access."
            )

        # Control 5: Privacy protection
        if not privacy_scrubbed:
            self._log(
                "propose_change",
                {
                    "rejected": True,
                    "reason": "Un-scrubbed customer data in input"
                }
            )
            return {
                "rejected": True,
                "reason": (
                    "Diagnostic input was not privacy-scrubbed; rejecting."
                )
            }

        # Control 6: Rollback plan required
        if not rollback_plan:
            self._log(
                "propose_change",
                {
                    "rejected": True,
                    "reason": "No rollback plan supplied"
                }
            )
            return {
                "rejected": True,
                "reason": "No rollback plan defined; rejecting proposal."
            }

        # Control 3: Human approval required
        request = {
            "diagnosis": diagnosis,
            "proposed_action": action,
            "rollback_plan": rollback_plan,
            "category": "production",
            "requires_approval": True
        }

        self._log("approval_requested", request)

        return request

    def apply_after_approval(self, request, human_decision):
        # A separate privileged process performs the actual change.
        self._log(
            "human_decision",
            {"decision": human_decision}
        )

        if human_decision == "approved":
            return {
                "applied": False,
                "handed_off_to": "privileged_deploy_process",
                "note": (
                    "This agent never holds production write access; "
                    "a separate privileged process performs the actual apply step."
                )
            }

        return {
            "applied": False,
            "reason": "Human approval was not granted."
        }


if __name__ == "__main__":

    agent = ProdChangeAgent()

    print("=== Control 2: Evaluation gate ===")
    print(f"Evaluated and passed: {agent.evaluate()}")

    print("\n=== Attempt 1: Missing rollback plan ===")

    result = agent.propose_change(
        diagnosis="Config X causes memory leak under load.",
        action="revert config X to previous value",
        rollback_plan=None,
        privacy_scrubbed=True
    )
    print(result)

    print("\n=== Attempt 2: Un-scrubbed customer data ===")

    result = agent.propose_change(
        diagnosis="Config X causes memory leak under load.",
        action="revert config X to previous value",
        rollback_plan="Revert config X to v3 if v4 also leaks.",
        privacy_scrubbed=False
    )
    print(result)

    print("\n=== Attempt 3: Complete, valid proposal ===")

    request = agent.propose_change(
        diagnosis="Config X causes memory leak under load.",
        action="revert config X to previous value",
        rollback_plan="Revert config X to v3 if v4 also leaks.",
        privacy_scrubbed=True
    )
    print(request)

    print("\n=== Human approves; separate process applies it ===")

    outcome = agent.apply_after_approval(
        request,
        human_decision="approved"
    )
    print(outcome)

    print("\n=== Adversarial test: Direct production write ===")

    try:
        agent.permissions["can_write"] = "production"
        agent.propose_change(
            "Test diagnosis",
            "Test action",
            "Test rollback",
            True
        )
    except PermissionError as error:
        print(f"Blocked as expected: {error}")

    print("\n=== Full audit log ===")

    for entry in agent.audit_log:
        print(entry)
