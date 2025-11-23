from langchain_core.prompts import ChatPromptTemplate
from ..config import llm
from ..state import AgentState


async def write_draft(state: AgentState):
    """
    Synthsizes all research results into a cohesize draft.
    """
    print("--- Node: Writing Draft ---")

    # Format inputs
    research_text = "\n\n".join(
        [f"### Data on {r.query_id}:\n{r.content}" for r in state.research_results]
    )

    user_prefs = ", ".join(state.user_profile.preferences)
    tone = state.user_profile.tone_preference

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an Expert Technical Writer. "
                    f"Write a comprehensive response based on the provided research. "
                    f"Style Guide: Tone={tone}, Preferences=[{user_prefs}]. "
                    "If specific feedback is provided, address it directly."
                ),
            ),
            (
                "user",
                (
                    f"Original Task: {state.task}\n\n"
                    f"Research Materials:\n{research_text}\n\n"
                    f"Previous Feedback (if any): {state.human_critique}\n\n"
                    "Write the final document:"
                ),
            ),
        ]
    )

    response = await (prompt | llm).ainvoke({})

    return {
        "draft_content": response.content,
        "revision_count": state.revision_count + 1,
        "human_critique": None,  # Clear critique after addressing it
    }
