from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from ddgs import DDGS


class WebSearchInput(BaseModel):
    query: str = Field(description="The topic or question to search for")


class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = (
        "Search the internet for relevant information "
        "about a given research topic."
    )
    args_schema: type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=5)

            for index, item in enumerate(search_results, start=1):
                results.append(
                    f"""
                    Source {index}
                    Title: {item.get('title', '')}
                    URL: {item.get('href', '')}
                    Content: {item.get('body', '')}
                    """
                )

        if not results:
            return "No relevant search results found."

        return "\n".join(results)


web_search_tool = WebSearchTool()