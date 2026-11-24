from app.tools.knowledge_search import search_knowledge
from app.tools.text_analysis import analyze_text


TOOLS = {
    "search_knowledge": search_knowledge,
    "analyze_text": analyze_text
}


def execute_tool(tool_name, **kwargs):
    """Execute an approved tool by name."""

    tool = TOOLS.get(tool_name)

    if tool is None:
        raise ValueError(f"Tool not allowed: {tool_name}")

    return tool(**kwargs)


def list_tools():
    """Return the available tool names."""

    return list(TOOLS.keys())