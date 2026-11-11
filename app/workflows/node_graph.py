
from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.agents.coordinator_agent import CoordinatorAgent
from app.mcp.client import get_student
from app.runtime.agent_runtime import agent_runtime


# --------------------------------------------------
# Shared State
# --------------------------------------------------

class AgentState(TypedDict):
    student_id: str
    student_data: dict
    mcp_student: dict
    risk: dict
    status: str
    message: str
    attempts: int
    simulate_failure: bool
    simulate_permanent_failure: bool



# --------------------------------------------------
# Node Specifications (Lab 7)
# --------------------------------------------------

NODE_SPECS = {
    "collect_student_data": {
        "owner": "CoordinatorAgent",
        "input": "student_id",
        "output": "student_data",
        "success_criteria": "Student information collected successfully",
        "retry_behavior": "No automatic retry; stop on failure",
        "human_approval": "Not required"
    },

    "retrieve_mcp_data": {
        "owner": "MCP Client",
        "input": "student_id",
        "output": "mcp_student",
        "success_criteria": "Student record retrieved through MCP",
        "retry_behavior": "No automatic retry; stop on failure",
        "human_approval": "Not required"
    },

    "analyze_risk": {
        "owner": "Risk Agent",
        "input": "student_id",
        "output": "risk",
        "success_criteria": "Risk result generated successfully",
        "retry_behavior": "Retry once, then stop",
        "human_approval": "Not required"
    },

    "handle_failure": {
        "owner": "Workflow Controller",
        "input": "error message",
        "output": "failure status",
        "success_criteria": "Failure recorded and execution stopped",
        "retry_behavior": "No retry",
        "human_approval": "Not required"
    }
}



# --------------------------------------------------
# Student Success Node Graph
# --------------------------------------------------

class StudentSuccessNodeGraph:

    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.graph = self.build_graph()

    # Node 1: Collect student data
    def collect_student_data(self, state: AgentState):

        print("\n[Node 1] Collecting student data...")

        data = self.coordinator.run(
            f"Collect complete student information for {state['student_id']}"
        )

        if data.get("status") == "error":
            return {
                "status": "error",
                "message": data.get("message", "Data collection failed.")
            }

        return {
            "student_data": data,
            "status": "success"
        }

    # Node 2: Retrieve student data through MCP
    def retrieve_mcp_data(self, state: AgentState):

        print("\n[Node 2] Retrieving student data through MCP...")

        mcp_student = get_student(state["student_id"])

        if not mcp_student or "error" in mcp_student:
            return {
                "status": "error",
                "message": "MCP student data retrieval failed."
            }

        return {
            "mcp_student": mcp_student,
            "status": "success"
        }

    # Node 3: Analyze student risk
    def analyze_risk(self, state: AgentState):

        print("\n[Node 3] Analyzing student risk...")

        attempts = state.get("attempts", 0) + 1

        # Simulate failure for Lab 7 demonstration
        if state.get("simulate_failure") and (state.get("simulate_permanent_failure") or attempts == 1):
            print("Simulated risk analysis failure.")

            return {
                "attempts": attempts,
                "status": "error",
                "message": "Simulated risk analysis failure."
            }

        risk = agent_runtime.execute_agent(
            "risk_agent",
            student_id=state["student_id"]
        )

        if not risk or risk.get("error"):
            return {
                "attempts": attempts,
                "status": "error",
                "message": risk.get("error", "Risk analysis failed.")
            }

        print("Risk analysis completed:", risk["risk"])

        return {
            "risk": risk,
            "attempts": attempts,
            "status": "success",
            "message": ""
        }

    # Failure handler
    def handle_failure(self, state: AgentState):

        print("\n[Failure Handler]")
        print("Execution failed:", state.get("message"))

        return {}

    # Conditional routing
    @staticmethod
    def check_status(state: AgentState):

        if state.get("status") == "error":
            return "failure"

        return "next"

    @staticmethod
    def check_risk_status(state: AgentState):

        if state.get("status") == "success":
            return "success"

        if state.get("attempts", 0) < 2:
            print("Retrying risk analysis...")
            return "retry"

        return "failure"

    # Build LangGraph
    def build_graph(self):

        workflow = StateGraph(AgentState)

        workflow.add_node(
            "collect_student_data",
            self.collect_student_data
        )

        workflow.add_node(
            "retrieve_mcp_data",
            self.retrieve_mcp_data
        )

        workflow.add_node(
            "analyze_risk",
            self.analyze_risk
        )

        workflow.add_node(
            "handle_failure",
            self.handle_failure
        )

        workflow.set_entry_point("collect_student_data")

        workflow.add_conditional_edges(
            "collect_student_data",
            self.check_status,
            {
                "next": "retrieve_mcp_data",
                "failure": "handle_failure"
            }
        )

        workflow.add_conditional_edges(
            "retrieve_mcp_data",
            self.check_status,
            {
                "next": "analyze_risk",
                "failure": "handle_failure"
            }
        )

        workflow.add_conditional_edges(
            "analyze_risk",
            self.check_risk_status,
            {
                "success": END,
                "retry": "analyze_risk",
                "failure": "handle_failure"
            }
        )

        workflow.add_edge("handle_failure", END)

        return workflow.compile()

    # Execute graph
    def run(self, student_id: str, simulate_failure=False, simulate_permanent_failure=False):

        initial_state = {
            "student_id": student_id,
            "student_data": {},
            "mcp_student": {},
            "risk": {},
            "status": "success",
            "message": "",
            "attempts": 0,
            "simulate_failure": simulate_failure,
            "simulate_permanent_failure": simulate_permanent_failure
        }

        result = self.graph.invoke(initial_state)

        if result.get("status") == "error":
            return {
                "status": "error",
                "message": result.get("message")
            }

        data = result["student_data"]

        return {
            "status": "success",
            "student_id": student_id,
            "student": data["student"],
            "academic": data["academic"],
            "attendance": data["attendance"],
            "internship": data["internship"],
            "placement": data["placement"],
            "mcp_student": result["mcp_student"],
            "risk": result["risk"]
        }


# --------------------------------------------------
# Main Program
# --------------------------------------------------

if __name__ == "__main__":

    workflow = StudentSuccessNodeGraph()

    student_id = input("Enter student ID: ")

    print("\n========== SUCCESS PATH ==========")

    result = workflow.run(student_id)

    print("\nFinal Result:")
    print(result)

    choice = input("\nSimulate failure? (y/n): ")

    if choice.lower() == "y":

        print("\n========== FAILURE PATH ==========")

        result = workflow.run(
            student_id,
            simulate_failure=True
        )

        print("\nFailure Test Result:")
        print(result)


        print("\n========== PERMANENT FAILURE PATH ==========")

        result = workflow.run(
            student_id,
            simulate_failure=True,
            simulate_permanent_failure=True
        )

        print("\nPermanent Failure Result:")
        print(result)
