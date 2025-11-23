from ..tools import web_search
from ..state import ResearchResult
import asyncio

# this node will be used inside a "Map" (Send) operation. It receives a discrete payload, not the whole state.


async def execute_search(request: dict):
    """
    Worker node that executes a single search query.
    """
    query_obj = request["query_obj"]  # Passed via Send API
    print(f"--- Node: Research Worker executing '{query_obj.query}' ---")

    # Execute the tool
    content = await web_search.ainvoke(query_obj.query)

    # Return a ResearchResult object.
    # Because the State defines `research_results` with `operator.add`,
    # returning a list here will append to the main state list.
    result = ResearchResult(
        query_id=query_obj.id, content=content, source="web_search_tool"
    )

    return {
        "research_results": [result]
    }  # Append to the "research_results" key in the main state
