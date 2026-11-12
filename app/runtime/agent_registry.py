from app.agents.risk_agent import analyze_student_risk
from app.agents.recommendation_agent import create_action_plan

from app.agents.contineo_agent import ContineoDataCollectionAgent
from app.agents.lms_agent import LMSDataCollectionAgent
from app.agents.internship_agent import InternshipDataCollectionAgent
from app.agents.placement_agent import PlacementDataCollectionAgent
from app.agents.cloud_operations_agent import run_cloud_operations

class AgentRegistry:
    """Register and manage existing project agents."""

    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent_function):
        if not name:
            raise ValueError("Agent name is required")

        if not callable(agent_function):
            raise TypeError("Agent must be callable")

        if name in self.agents:
            raise ValueError(f"Agent '{name}' is already registered")

        self.agents[name] = agent_function

        return f"Agent '{name}' registered successfully"

    def get_agent(self, name):
        if name not in self.agents:
            raise KeyError(f"Agent '{name}' not found")

        return self.agents[name]

    def list_agents(self):
        return list(self.agents.keys())


agent_registry = AgentRegistry()

# Existing agents
agent_registry.register_agent("risk_agent", analyze_student_risk)
agent_registry.register_agent("recommendation_agent", create_action_plan)

# Data collection agents
contineo_agent = ContineoDataCollectionAgent()
lms_agent = LMSDataCollectionAgent()
internship_agent = InternshipDataCollectionAgent()
placement_agent = PlacementDataCollectionAgent()

agent_registry.register_agent("contineo_agent", contineo_agent.collect)
agent_registry.register_agent("lms_agent", lms_agent.collect)
agent_registry.register_agent("internship_agent", internship_agent.collect)
agent_registry.register_agent("placement_agent", placement_agent.collect)
from app.agents.deep_research_agent import run_deep_research
agent_registry.register_agent('deep_research_agent', run_deep_research)
agent_registry.register_agent("cloud_operations_agent", run_cloud_operations)
