
import sys
from pathlib import Path

import pytest
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Allow tests to import server.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from server import add, greet, get_research_notes, research_summary


# Test 1: Addition
def test_add():
    assert add(10, 20) == 30
    assert add(-5, 5) == 0


# Test 2: Invalid addition
def test_add_invalid():
    with pytest.raises(ValueError):
        add(True, 10)


# Test 3: Greeting
def test_greet():
    assert greet("Developer") == "Hello, Developer! Welcome to MCP."


# Test 4: Invalid greeting
def test_greet_invalid():
    with pytest.raises(ValueError):
        greet("   ")

    with pytest.raises(ValueError):
        greet("A" * 51)


# Test 5: Research resource
def test_research_resource():
    result = get_research_notes()

    assert "Artificial Intelligence Research Notes" in result
    assert "Machine Learning" in result


# Test 6: Research prompt
def test_research_prompt():
    result = research_summary("Machine Learning")

    assert "Machine Learning" in result
    assert "Introduction" in result
    assert "Conclusion" in result


def test_mcp_client_server():
    async def run_test():

        server_params = StdioServerParameters(
            command=sys.executable,
            args=["server.py"],
            env=None
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:

                await session.initialize()

                # Discover tools
                tools = await session.list_tools()
                tool_names = [tool.name for tool in tools.tools]

                assert "add" in tool_names
                assert "greet" in tool_names

                # Call addition tool
                result = await session.call_tool(
                    "add",
                    arguments={"a": 15, "b": 25}
                )

                assert not result.isError
                assert result.content[0].text == "40"

                # Discover resources
                resources = await session.list_resources()
                resource_uris = [
                    str(resource.uri)
                    for resource in resources.resources
                ]

                assert "research://notes" in resource_uris

                # Discover prompts
                prompts = await session.list_prompts()
                prompt_names = [
                    prompt.name for prompt in prompts.prompts
                ]

                assert "research_summary" in prompt_names

    asyncio.run(run_test())
