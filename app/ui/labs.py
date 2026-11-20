import streamlit as st

from app.agents.cloud_operations_agent import run_cloud_operations
from app.runtime.agent_runtime import agent_runtime
from app.workflows.release_lab import acceptance_cases, evaluate, implementation, snapshot, stage, transition

from app.auth.permissions import require_role

require_role("mentor")
actor = st.session_state["user_id"]
st.title("Mentor lab workspace")
research, cloud, release = st.tabs(["Research briefing", "Cloud incident", "Release review"])

with research:
    question = st.text_input("Research question", "Which indicators contribute to student risk?")
    if st.button("Prepare briefing"):
        result = agent_runtime.execute_skill("research_summary", topic=question)
        if result.get("status") == "error":
            st.warning(result["message"])
        else:
            st.table(result["evidence_table"])
            st.write(result["executive_summary"])
            st.write(result["recommended_next_questions"])


with cloud:
    st.subheader("Deployment simulator")

    # Simulated deployment data (not a real cloud deployment).
    versions = {
        "v1": {
            "responses": [200] * 99 + [500],
            "previous_version": None
        },
        "v2": {
            "responses": [200] * 90 + [500] * 10,
            "previous_version": "v1"
        }
    }

    version = st.session_state.setdefault(
        "lab_service_version", "v2"
    )

    version_data = versions[version]

    rate = agent_runtime.execute_tool(
        "calculate_percentage",
        part=version_data["responses"].count(500),
        total=len(version_data["responses"])
    )

    deployment_history = [
        {
            "service": "portal",
            "version": version,
            "previous_version": version_data["previous_version"],
            "time": "09:00"
        }
    ]

    incident = run_cloud_operations(
        service="portal",
        logs=["ERROR processing request"],
        error_rate=rate,
        baseline_error_rate=1,
        deploy_history=deployment_history
    )

    if incident["status"] == "error":
        st.error(incident["message"])

    else:
        st.metric("Measured error rate", f"{rate:.0f}%")

        st.write(
            f"Running {version} · "
            f"{incident['severity']} · "
            f"{incident['proposed_action']}"
        )

        if incident.get("diagnosis"):
            st.write("**Incident diagnosis**")
            st.info(incident["diagnosis"])

        if incident.get("rollback_plan"):
            st.write("**Proposed remediation**")
            st.write(incident["rollback_plan"])

        approval = incident.get("approval_request")
        rollback_target = incident.get("previous_version")

        if approval:
            st.warning(approval["message"])

            if rollback_target:
                if st.button("Approve simulated rollback"):
                    from app.runtime.audit_logger import log_action

                    log_action(
                        None,
                        actor,
                        "approved_simulated_rollback",
                        {
                            "from": version,
                            "to": rollback_target
                        }
                    )

                    st.session_state.lab_service_version = rollback_target
                    st.rerun()

            else:
                st.warning(
                    "No previous stable version is recorded. "
                    "Rollback cannot be simulated safely."
                )

        elif st.button("Restart deployment exercise"):
            st.session_state.lab_service_version = "v2"
            st.rerun()


with release:
    st.subheader("Attendance policy release")
    requirement = st.text_input("Requirement", "Flag attendance below 65%")
    if st.button("Build and test policy"):
        try:
            stage(requirement, actor)
        except ValueError as error:
            st.warning(str(error))
    releases, events = snapshot()
    active = next((r for r in releases if r["state"] == "active"), None)
    attendance = st.slider("Monitor a sample attendance value", 0, 100, 62)
    cutoff = active["cutoff"] if active else 60
    st.write(f"Active cutoff {cutoff}% · Sample {'flagged' if evaluate(cutoff, attendance) else 'clear'}")
    for r in releases:
        st.write(f"Revision {r['id']} · Below {r['cutoff']}% · {r['state']}")
        if r["state"] == "tested":
            delta = r["cutoff"] - cutoff
            st.caption(f"Threshold change {delta:+} percentage points. A higher threshold flags more students. "
                       "Rollback restores the previous policy.")
            with st.expander(f"Acceptance checks for revision {r['id']}"):
                st.code(implementation(r["cutoff"]), language="python")
                st.download_button("Download policy module", implementation(r["cutoff"]),
                                   file_name=f"attendance_policy_{r['id']}.py", key=f"download_{r['id']}")
                st.table([{"Attendance": point, "Expected flag": expected,
                           "Passed": evaluate(r["cutoff"], point) == expected}
                          for point, expected in acceptance_cases(r["cutoff"])])
        action = {"active": "rollback", "tested": "approve"}.get(r["state"])
        if action and st.button(action.title(), key=f"{action}_{r['id']}"):
            try:
                transition(r["id"], action, actor, st.session_state.user_role)
                st.rerun()
            except ValueError as error:
                st.warning(str(error))
    with st.expander("Review history"):
        st.dataframe(events)
