
"""
orchestrator.py
Builds the LangGraph StateGraph that wires all 4 agents together.
State flows: Triage → Research → Code → Report
Each agent reads from and writes to the shared state dict.
"""
from typing import TypedDict, Any
from langgraph.graph import StateGraph, END

# Import all our agents
from agents.triage_agent import run_triage_agent
from agents.research_agent import run_research_agent
from agents.code_agent import run_code_agent
from agents.report_agent import run_report_agent


# Define the shape of our shared state (all agents read/write to this)
class BugTriageState(TypedDict):
    bug_report: dict           # input: the raw bug
    triage_result: dict        # output of Triage Agent
    research_result: dict      # output of Research Agent
    code_result: dict          # output of Code Agent
    final_report: str          # output of Report Agent


def build_bug_triage_graph():
    """
    Creates and compiles the LangGraph graph.
    Think of this as defining the 'flowchart' of which agent runs when.
    """
    # Create the graph with our state type
    graph = StateGraph(BugTriageState)

    # Add each agent as a 'node' in the graph
    graph.add_node("triage", run_triage_agent)
    graph.add_node("research", run_research_agent)
    graph.add_node("code", run_code_agent)
    graph.add_node("report", run_report_agent)

    # Define the edges (flow): start → triage → research → code → report → end
    graph.set_entry_point("triage")          # First agent to run
    graph.add_edge("triage", "research")      # Triage → Research
    graph.add_edge("research", "code")        # Research → Code
    graph.add_edge("code", "report")          # Code → Report
    graph.add_edge("report", END)              # Report → Done

    # Compile = "lock in" the graph for execution
    return graph.compile()


# Make it importable or runnable directly
bug_triage_app = build_bug_triage_graph()