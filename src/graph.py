from typing import Literal
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send

from .state import ResearchQuery, AgentState
from .nodes.planner import plan_research
from .nodes.researcher import execute_search
from .nodes.writer import write_draft


# ---- Main Flow ----
def map_research_tasks(state: AgentState):
    """
    The 'Map' step.
    Determines how many parallel research worker to spawn
    based on the plan generated from the planner node.
    """
    # For every query in the plan, send a payload to the 'execute_search' node
    return [Send("execute_search", {"query_obj": q}) for q in state.research_plan]


def should_continue(state: AgentState) -> Literal["finalize", "revise"]:
    """
    Determines if we need another iteration based on human feedback.
    """
    if state.human_critique:
        print(f"--- Decision: Revision requested ({state.revision_count}) ---")
        return "revise"

    print("--- Decision: Content approved ---")
    return "finalize"


# --- Graph Consturction ---
def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("planner", plan_research)
    workflow.add_node("execute_search", execute_search)  # type: ignore
    workflow.add_node("writer", write_draft)

    # 2. Define Edges

    # Start -> Plan
    workflow.add_edge(START, "planner")

    # Plan -> Map step (Parallel Research)
    workflow.add_conditional_edges("planner", map_research_tasks, ["execute_search"])

    # After all parallel research tasks finish, they implicitly converge.
    # Route them to the writer (Reducer).
    workflow.add_edge("execute_search", "writer")

    # Writer -> Human Interaction Check
    # 3. Compilation
    checkpointer = MemorySaver()

    # Compile with interrupt_before specific nodes if needed,

    return workflow.compile(checkpointer=checkpointer)
