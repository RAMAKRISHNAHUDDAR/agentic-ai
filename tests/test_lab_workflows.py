import pytest
from app.agents.cloud_operations_agent import run_cloud_operations
from app.agents.deep_research_agent import run_deep_research
from app.agents.recommendation_agent import create_action_plan
from app.workflows import release_lab
from app.workflows.node_graph import StudentSuccessNodeGraph
from app.workflows.parallel_swarm import run_parallel_swarm


def test_release_lifecycle(tmp_path, monkeypatch):
    monkeypatch.setattr(release_lab, "DATABASE", tmp_path / "lab.db")
    one = release_lab.stage("Flag attendance below 65%", "A")
    stale = release_lab.stage("Flag attendance below 75%", "A")
    with pytest.raises(PermissionError):
        release_lab.transition(one, "approve", "S", "student")
    release_lab.transition(one, "approve", "B", "mentor")
    with pytest.raises(ValueError):
        release_lab.transition(stale, "approve", "B", "mentor")
    two = release_lab.stage("Flag attendance below 70%", "A")
    release_lab.transition(two, "approve", "B", "mentor")
    release_lab.transition(two, "rollback", "B", "mentor")
    rows, audit = release_lab.snapshot()
    assert [r["cutoff"] for r in rows if r["state"] == "active"] == [65]
    assert audit[0]["actor"] == "B"
    assert audit[0]["action"] == "rollback"


def test_real_risk_exception_retries(monkeypatch):
    graph = StudentSuccessNodeGraph()
    row = {"student_id": "STU001"}
    monkeypatch.setattr(graph.coordinator, "run", lambda _: {"status": "success", "student": row})
    monkeypatch.setattr("app.workflows.node_graph.get_student", lambda _: row)
    calls = []
    def fail(**kwargs):
        calls.append(1)
        raise RuntimeError("Model unavailable")
    monkeypatch.setattr("app.runtime.agent_runtime.log_action", lambda *args: None)
    from app.runtime.agent_registry import agent_registry
    monkeypatch.setitem(agent_registry.agents, "risk_agent", fail)
    assert graph.run("STU001") == {"status": "error", "message": "Model unavailable"}
    assert len(calls) == 2


def test_swarm_and_audit_report_domain_failure(monkeypatch):
    from app.runtime.agent_registry import agent_registry
    audit = []
    monkeypatch.setattr("app.runtime.agent_runtime.log_action", lambda *args: audit.append(args))
    monkeypatch.setitem(agent_registry.agents, "sample", lambda: {"error": "Missing"})
    assert run_parallel_swarm([{"agent": "sample"}])["status"] == "error"
    assert audit[-1][-1]["status"] == "error"


def test_mentor_rejection_changes_proposal(monkeypatch):
    from app.agents import recommendation_agent as agent
    old = "Improve attendance and maintain at least 75% attendance."
    monkeypatch.setattr(agent, "get_intervention_history", lambda _: [
        {"status": "rejected", "intervention": old, "mentor_feedback": "Timetable clash"}])
    monkeypatch.setattr(agent, "log_intervention", lambda **kw: {**kw, "status": "pending"})
    monkeypatch.setattr(agent, "log_action", lambda *args: None)
    row = dict(student_id="S", name="Fixture", attendance=40, marks=80, assignments=80,
               backlogs=0, internship_status="Completed", placement_status="Ready")
    result = create_action_plan("S", {"risk": "At Risk", "risk_probability": .9}, row)
    assert old not in result["recommendations"]
    assert "asynchronous" in result["recommendations"][0]


def test_catalog_and_cloud_decisions():
    result = run_deep_research("student risk")
    assert result["comparison"]["agreements"]
    assert result["recommended_next_questions"]
    assert run_cloud_operations("portal", [], 1, 1, [])["proposed_action"] == "monitor"
    assert run_cloud_operations("portal", [], 8, 1, [])["proposed_action"] == "gather_evidence"

def test_resume_from_disk_skips_completed_nodes(tmp_path, monkeypatch):
    row = {"student_id": "STU001"}
    snapshot = {k: {} for k in ("academic", "attendance", "internship", "placement")}
    first = StudentSuccessNodeGraph(tmp_path)
    monkeypatch.setattr(first.coordinator, "run", lambda _: {"student": row, **snapshot})
    monkeypatch.setattr("app.workflows.node_graph.get_student", lambda _: row)
    assert first.run("STU001", True, True)["status"] == "error"

    resumed = StudentSuccessNodeGraph(tmp_path)
    monkeypatch.setattr(resumed.coordinator, "run", lambda _: pytest.fail("Repeated collection"))
    monkeypatch.setattr("app.workflows.node_graph.get_student", lambda _: pytest.fail("Repeated MCP"))
    monkeypatch.setattr("app.workflows.node_graph.agent_runtime.execute_agent",
                        lambda *args, **kwargs: {"risk": "At Risk"})
    assert resumed.resume(first.run_id)["status"] == "success"
    assert list(tmp_path.iterdir()) == []
