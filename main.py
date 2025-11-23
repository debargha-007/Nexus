# ------ // Entry Point for main logic // ----- #
import asyncio
import uuid
from termcolor import colored

from src.graph import build_graph
from src.state import AgentState
from src.memory_store import MemoryStore


async def run_interactive_session():
    # 1. Setup Long Term Memory
    user_id = "user_123"  # In production, this comes from auth
    profile = MemoryStore.load_profile()

    print(colored(f"--- Welcome back, {profile.name} ---", "cyan"))
    print(colored(f"Current Style Preferences: {profile.preferences}", "cyan"))

    # 2. Get User Input
    task = input(colored("\nWhat would you like me to research today? > ", "green"))

    # Optional: Allow user to update preferences on the fly
    if "concise" in task.lower():
        MemoryStore.update_profile("Use concise, bulleted format")

    # 3. Initialize Graph State
    initial_state = AgentState(task=task, user_profile=profile)

    graph = build_graph()
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print(colored("\n--- Nexus Agent Started ---", "yellow"))

    # 4. Run Phase 1: Planning -> Research -> Initial Draft
    # We stream events to show progress
    async for event in graph.astream(initial_state, config, stream_mode="updates"):
        for node_name, node_content in event.items():
            print(colored(f"Completed: {node_name}", "grey"))
            if node_name == "planner":
                plan = node_content["research_plan"]
                print(f"  Planned {len(plan)} tasks.")

    # 5. Human-in-the-Loop Phase
    while True:
        # Retrieve current state after the run pauses/finishes
        snapshot = await graph.aget_state(config)
        current_draft = snapshot.values["draft_content"]

        print(colored("\n--- Draft Generated ---", "white", attrs=["bold"]))
        print(current_draft)
        print(colored("\n-----------------------", "white", attrs=["bold"]))

        feedback = input(
            colored("\n[Hit Enter to Approve] or [Type feedback to Revise]: ", "yellow")
        )

        if not feedback:
            print(colored("Content Approved. Saving to history...", "green"))
            break
        else:
            print(colored("Updating draft with feedback...", "magenta"))

            # Update state with critique
            graph.update_state(config, {"human_critique": feedback})

            # Continue execution from the writer node
            # We assume the writer node is smart enough to see the critique in the state
            async for event in graph.astream(None, config, stream_mode="updates"):
                for node_name, _ in event.items():
                    print(colored(f"Refined: {node_name}", "grey"))

    print(colored("\n--- Agent Finished ---", "cyan"))


if __name__ == "__main__":
    asyncio.run(run_interactive_session())
