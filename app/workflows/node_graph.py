
import argparse
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import UUID, uuid4
from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.agents.coordinator_agent import CoordinatorAgent
from app.mcp.client import get_student
from app.runtime.agent_runtime import agent_runtime


# --------------------------------------------------
# Shared State
# --------------------------------------------------

class AgentState(TypedDict):
    resume_from: str
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

    def __init__(self, checkpoint_dir=None):
        self.checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir else None
        self.checkpoint = None
        self.run_id = None
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

        student = state["student_data"]["student"]
        if any(mcp_student.get(key) != student.get(key) for key in ("student_id", "attendance", "marks", "assignments", "backlogs")):
            return {"status": "error", "resume_from": "collect_student_data", "message": "Student evidence changed. Fresh collection is required."}
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
            student_id=state["student_id"], student=state["student_data"]["student"]
        )

        if not isinstance(risk, dict) or "risk" not in risk or risk.get("status") == "error":
            return {
                "attempts": attempts,
                "status": "error",
                "message": (risk.get("message") or risk.get("error") if isinstance(risk, dict) else None) or "Risk analysis failed."
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

        workflow.set_conditional_entry_point(
            lambda state: state["resume_from"],
            {name: name for name in ("collect_student_data", "retrieve_mcp_data", "analyze_risk")}
        )

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

    def save_progress(self, state, next_node):
        self.checkpoint = {
            "student_id": state["student_id"], "resume_from": next_node,
            "student_data": state["student_data"] if next_node != "collect_student_data" else {},
            "mcp_student": state["mcp_student"] if next_node == "analyze_risk" else {},
        }
        if self.checkpoint_dir:
            self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
            path = self.checkpoint_dir / f"{self.run_id}.json"
            with NamedTemporaryFile(mode="w", dir=self.checkpoint_dir, delete=False, encoding="utf-8") as file:
                json.dump(self.checkpoint, file, default=str)
            os.replace(file.name, path)

    def resume(self, run_id=None):
        if run_id:
            self.run_id = str(UUID(run_id))
            path = self.checkpoint_dir / f"{self.run_id}.json"
            self.checkpoint = json.loads(path.read_text(encoding="utf-8"))
        if not self.checkpoint:
            raise ValueError("No paused assessment to resume.")
        node = self.checkpoint["resume_from"]
        print(f"Resuming run {self.run_id} at {node}.")
        if node == "analyze_risk":
            print("Reusing completed data collection and MCP verification.")
        elif node == "retrieve_mcp_data":
            print("Reusing completed data collection.")
        return self.execute(self.checkpoint.copy())

    def run(self, student_id: str, simulate_failure=False, simulate_permanent_failure=False):
        self.run_id = str(uuid4())
        state = {"student_id": student_id, "student_data": {}, "mcp_student": {},
                 "resume_from": "collect_student_data"}
        self.save_progress(state, "collect_student_data")
        return self.execute(state, simulate_failure, simulate_permanent_failure)

    def execute(self, state, simulate_failure=False, simulate_permanent_failure=False):
        result = {**state, "risk": {}, "status": "success", "message": "", "attempts": 0,
                  "simulate_failure": simulate_failure, "simulate_permanent_failure": simulate_permanent_failure}
        next_nodes = {"collect_student_data": "retrieve_mcp_data", "retrieve_mcp_data": "analyze_risk"}
        for update in self.graph.stream(result.copy(), stream_mode="updates"):
            for node, changes in update.items():
                result.update(changes or {})
                if node in next_nodes and result["status"] == "success":
                    self.save_progress(result, next_nodes[node])
                elif changes and changes.get("resume_from") == "collect_student_data":
                    self.save_progress(result, "collect_student_data")
        student_id = result["student_id"]
        if result.get("status") == "error":
            return {
                "status": "error",
                "message": result.get("message")
            }

        if self.checkpoint_dir:
            (self.checkpoint_dir / f"{self.run_id}.json").unlink(missing_ok=True)
        self.checkpoint = None
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

    parser = argparse.ArgumentParser(description="Run or resume a student assessment.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--resume", metavar="RUN_ID")
    group.add_argument("--demo-recovery", metavar="STUDENT_ID")
    args = parser.parse_args()
    workflow = StudentSuccessNodeGraph(Path(__file__).resolve().parents[2] / "data" / "assessment_checkpoints")

    def report(result):
        print("Assessment:", result.get("message") or result["risk"]["risk"])
        if result["status"] == "error":
            print("After resolving the failure, run:")
            print(f"python -m app.workflows.node_graph --resume {workflow.run_id}")

    if args.resume:
        try:
            report(workflow.resume(args.resume))
        except (ValueError, FileNotFoundError) as error:
            parser.exit(1, f"Checkpoint unavailable: {error}\n")
    elif args.demo_recovery:
        report(workflow.run(args.demo_recovery, simulate_failure=True, simulate_permanent_failure=True))
    else:
        student_id = input("Enter student ID: ").strip().upper()
        result = workflow.run(student_id)
        report(result)
        if result["status"] == "success" and input("Simulate failure? (y/n): ").lower() == "y":
            print("Temporary risk failure")
            report(workflow.run(student_id, simulate_failure=True))
            print("Persistent risk failure")
            report(workflow.run(student_id, simulate_failure=True, simulate_permanent_failure=True))
