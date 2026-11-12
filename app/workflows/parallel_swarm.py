
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.runtime.agent_runtime import agent_runtime


def run_parallel_swarm(agent_tasks, max_workers=None):
    """
    Execute multiple registered agents concurrently,
    collect their results and handle individual failures.
    
    Each task must contain:
        {
            "agent": "agent_name",
            "kwargs": {"key": "value"}
        }
    """

    if not isinstance(agent_tasks, list) or not agent_tasks:
        return {
            "status": "error",
            "message": "At least one agent task is required."
        }

    for task in agent_tasks:
        if (
            not isinstance(task, dict)
            or not isinstance(task.get("agent"), str)
            or not task["agent"].strip()
            or not isinstance(task.get("kwargs", {}), dict)
        ):
            return {
                "status": "error",
                "message": "Each task must contain a valid agent name and kwargs dictionary."
            }

    if max_workers is not None and (
        not isinstance(max_workers, int)
        or isinstance(max_workers, bool)
        or max_workers < 1
    ):
        return {
            "status": "error",
            "message": "max_workers must be a positive integer."
        }

    results = [None] * len(agent_tasks)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        future_to_index = {
            executor.submit(
                agent_runtime.execute_agent,
                task["agent"],
                **task.get("kwargs", {})
            ): index
            for index, task in enumerate(agent_tasks)
        }

        for future in as_completed(future_to_index):
            index = future_to_index[future]
            agent_name = agent_tasks[index]["agent"]

            try:
                result = future.result()

                if isinstance(result, dict) and result.get("status") == "error":
                    results[index] = {
                        "agent": agent_name,
                        "status": "error",
                        "message": result.get("message", "Agent execution failed.")
                    }
                else:
                    results[index] = {
                        "agent": agent_name,
                        "status": "success",
                        "result": result
                    }

            except Exception as error:
                results[index] = {
                    "agent": agent_name,
                    "status": "error",
                    "message": str(error)
                }

    successful_results = [
        item for item in results
        if item["status"] == "success"
    ]

    failed_results = [
        item for item in results
        if item["status"] == "error"
    ]

    if not failed_results:
        status = "success"
    elif successful_results:
        status = "partial_success"
    else:
        status = "error"

    return {
        "status": status,
        "total_agents": len(agent_tasks),
        "successful_agents": len(successful_results),
        "failed_agents": len(failed_results),
        "results": results,
        "merged_result": [
            item["result"] for item in successful_results
        ],
        "errors": failed_results
    }
