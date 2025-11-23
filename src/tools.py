from langchain_core.tools import tool
from langchain_tavily import TavilySearch


@tool
def web_search(query: str) -> str:
    """Performs a web search to gather information."""
    try:
        tavily_search = TavilySearch(max_results=3)  # Web-search tool
        data = tavily_search.invoke({"query": query})
        results = data.get("results", data)

        formatted_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
                for doc in results
            ]
        )

        return formatted_docs

    except Exception as e:
        return f"Error prompting search: {str(e)}"
