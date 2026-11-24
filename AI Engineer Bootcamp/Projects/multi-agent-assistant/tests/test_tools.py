import pytest

from app.tools.registry import (
    execute_tool,
    list_tools
)


def test_list_tools():
    tools = list_tools()

    assert "search_knowledge" in tools
    assert "analyze_text" in tools


def test_knowledge_search():
    results = execute_tool(
        "search_knowledge",
        query="AI healthcare"
    )

    assert len(results) > 0
    assert all("content" in item for item in results)


def test_text_analysis():
    result = execute_tool(
        "analyze_text",
        text="AI improves healthcare. AI supports doctors."
    )

    assert result["word_count"] == 6
    assert result["sentence_count"] == 2
    assert result["character_count"] > 0


def test_unknown_tool():
    with pytest.raises(ValueError):
        execute_tool("delete_files")


def test_empty_search():
    with pytest.raises(ValueError):
        execute_tool(
            "search_knowledge",
            query=""
        )


def test_empty_text():
    with pytest.raises(ValueError):
        execute_tool(
            "analyze_text",
            text=""
        )