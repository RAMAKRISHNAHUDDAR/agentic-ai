
import time

from app.workflows.parallel_swarm import run_parallel_swarm


def test_parallel_execution(monkeypatch):
    from app.workflows import parallel_swarm

    def mock_execute_agent(name, **kwargs):
        time.sleep(0.1)
        return {"agent_output": name}

    monkeypatch.setattr(
        parallel_swarm.agent_runtime,
        "execute_agent",
        mock_execute_agent
    )

    tasks = [
        {"agent": "agent_one", "kwargs": {}},
        {"agent": "agent_two", "kwargs": {}},
        {"agent": "agent_three", "kwargs": {}}
    ]

    start = time.time()
    result = run_parallel_swarm(tasks)
    elapsed = time.time() - start

    assert result["status"] == "success"
    assert result["successful_agents"] == 3
    assert result["failed_agents"] == 0
    assert len(result["merged_result"]) == 3
    assert elapsed < 0.28


def test_result_merging(monkeypatch):
    from app.workflows import parallel_swarm

    def mock_execute_agent(name, **kwargs):
        return {"output": name}

    monkeypatch.setattr(
        parallel_swarm.agent_runtime,
        "execute_agent",
        mock_execute_agent
    )

    tasks = [
        {"agent": "agent_one", "kwargs": {}},
        {"agent": "agent_two", "kwargs": {}}
    ]

    result = run_parallel_swarm(tasks)

    assert result["merged_result"] == [
        {"output": "agent_one"},
        {"output": "agent_two"}
    ]


def test_individual_agent_failure(monkeypatch):
    from app.workflows import parallel_swarm

    def mock_execute_agent(name, **kwargs):
        if name == "failing_agent":
            return {"status": "error", "message": "Simulated failure"}

        return {"output": name}

    monkeypatch.setattr(
        parallel_swarm.agent_runtime,
        "execute_agent",
        mock_execute_agent
    )

    tasks = [
        {"agent": "working_agent", "kwargs": {}},
        {"agent": "failing_agent", "kwargs": {}}
    ]

    result = run_parallel_swarm(tasks)

    assert result["status"] == "partial_success"
    assert result["successful_agents"] == 1
    assert result["failed_agents"] == 1
    assert result["merged_result"] == [{"output": "working_agent"}]


def test_all_agents_fail(monkeypatch):
    from app.workflows import parallel_swarm

    def mock_execute_agent(name, **kwargs):
        return {"status": "error", "message": "Agent failed"}

    monkeypatch.setattr(
        parallel_swarm.agent_runtime,
        "execute_agent",
        mock_execute_agent
    )

    tasks = [
        {"agent": "agent_one", "kwargs": {}},
        {"agent": "agent_two", "kwargs": {}}
    ]

    result = run_parallel_swarm(tasks)

    assert result["status"] == "error"
    assert result["successful_agents"] == 0
    assert result["failed_agents"] == 2


def test_invalid_input():
    result = run_parallel_swarm([])

    assert result["status"] == "error"


def test_invalid_task():
    result = run_parallel_swarm([
        {"agent": "", "kwargs": {}}
    ])

    assert result["status"] == "error"
