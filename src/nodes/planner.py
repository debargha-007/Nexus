from langchain_core.prompts import ChatPromptTemplate
from ..config import llm
from ..state import AgentState, ResearchQuery
from typing import List
from pydantic import BaseModel


class PlanOutput(BaseModel):
    queries: List[ResearchQuery]


async def plan_research(state: AgentState):
    """
    Analyzes the user request and User Profile (Long-term memory)
    to generate a targeted research plan.
    """
    print(f"--- Node: Planning Research for '{state.task}' ---")

    # Incorporate long-term memory into the planning prompt
    user_prefs = ", ".join(state.user_profile.preferences)
    tone = state.user_profile.tone_preference

    system_msg = (
        "You are a Senior Research Architect. Break down the user's task into "
        "distinct, search-optimized queries. "
        f"Keep in mind the user's preferences: [{user_prefs}] and preferred tone: {tone}. "
        "Generate 3-4 specific search queries that cover different aspects of the topic."
    )

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_msg), ("user", "{task}")]
    )

    # Structured output extraction
    planner = prompt | llm.with_structured_output(PlanOutput)

    result = await planner.ainvoke({"task": state.task})

    return {"research_plan": result.queries}  # type: ignore
