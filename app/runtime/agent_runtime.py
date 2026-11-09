
from app.runtime.skill_registry import skill_registry
from app.runtime.tool_registry import tool_registry
from app.runtime.audit_logger import log_action
from app.runtime.agent_registry import agent_registry


from app.memory.memory_manager import (
    add_memory,
    get_student_memory
)

from app.safety.governance import check_intervention_approval


class AgentRuntime:
    """Central runtime for executing skills, tools and memory operations."""

    def __init__(self):
        self.skills = skill_registry
        self.tools = tool_registry
        self.agents = agent_registry

    def execute_skill(self, name, **kwargs):
        student_id = kwargs.get("student_id")

        try:
            result = self.skills.execute_skill(name, **kwargs)

            log_action(
                student_id, "agent_runtime",
                f"execute_skill:{name}", {"status": "success"}
            )
            return result

        except Exception as error:
            log_action(
                student_id, "agent_runtime",
                f"execute_skill:{name}",
                {"status": "error", "error": str(error)}
            )
            return {"status": "error", "message": str(error)}

    def execute_tool(self, name, **kwargs):
        student_id = kwargs.get("student_id")

        try:
            result = self.tools.execute_tool(name, **kwargs)

            log_action(
                student_id, "agent_runtime",
                f"execute_tool:{name}", {"status": "success"}
            )
            return result

        except Exception as error:
            log_action(
                student_id, "agent_runtime",
                f"execute_tool:{name}",
                {"status": "error", "error": str(error)}
            )
            return {"status": "error", "message": str(error)}

    def store_memory(self, record):
        try:
            result = add_memory(record)

            log_action(
                record.get("student_id"),
                "agent_runtime",
                "store_memory",
                {"status": "success"}
            )
            return result

        except Exception as error:
            return {"status": "error", "message": str(error)}

    def retrieve_memory(self, student_id):
        try:
            return get_student_memory(student_id)

        except Exception as error:
            return {"status": "error", "message": str(error)}

    def check_governance(self, student_id, intervention):
        """Check whether an intervention has mentor approval."""

        try:
            result = check_intervention_approval(
                student_id,
                intervention
            )

            log_action(
                student_id,
                "agent_runtime",
                "check_governance",
                result
            )

            return result

        except Exception as error:
            log_action(
                student_id,
                "agent_runtime",
                "check_governance",
                {"status": "error", "error": str(error)}
            )

            return {
                "approved": False,
                "status": "error",
                "message": str(error)
            }

    def list_skills(self):
        return self.skills.list_skills()

    def list_tools(self):
        return self.tools.list_tools()


    def execute_agent(self, name, **kwargs):
        """Execute a registered agent and audit the result."""

        student_id = kwargs.get("student_id")

        try:
            agent = self.agents.get_agent(name)
            result = agent(**kwargs)

            log_action(
                student_id,
                "agent_runtime",
                f"execute_agent:{name}",
                {"status": "success"}
            )

            return result

        except Exception as error:
            log_action(
                student_id,
                "agent_runtime",
                f"execute_agent:{name}",
                {"status": "error", "error": str(error)}
            )

            return {"status": "error", "message": str(error)}


    def list_agents(self):
        return self.agents.list_agents()    


agent_runtime = AgentRuntime()
