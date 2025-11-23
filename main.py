# ------ // Entry Point for main logic // ----- #
import asyncio
import uuid
from termcolor import colored

from src.graph import build_graph
from src.state import AgentState
from src.memory_store import MemoryStore


async def run_interactive_session():
    # 1. Setup Long-Term Memory
    user_id = "user_123"  # use authentication
    profile = MemoryStore.load_profile()

    print(colored(f"--- Welcome back, {profile.name} ---", "cyan"))
    print(colored(f"Current Style Preferences: {profile.preferences}", "cyan"))

    # 2. Get user Input
    task = input(colored("\nWhat would you like me to research today? > ", "green"))

    # 3. Initialize Graph State
    initial_state = AgentState(task=task, user_profile=profile)

    graph = build_graph()
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print(colored("\n--- Nexus Agent Started ---", "yellow"))

    # 4. Run Phase 1: Planning -> Research -> Initial Draft
    # We stream events to show progress
    async for event in graph.astream(initial_state, config, stream_mode="updates"):  # type: ignore
        for node_name, node_content in event.items():
            print(colored(f"Completed: {node_name}", "grey"))
            if node_name == "planner":
                plan = node_content["research_plan"]
                print(f"  Planned {len(plan)} tasks.")
