import json
from app.runtime.agent_runtime import agent_runtime


if __name__ == "__main__":
    print(json.dumps(agent_runtime.execute_skill("research_summary", topic="Student risk and attendance"), indent=2))
