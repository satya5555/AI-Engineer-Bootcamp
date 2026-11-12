
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # Configure the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize connection
            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()

            print("Available MCP tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call the addition tool
            result = await session.call_tool(
                "add",
                arguments={"a": 10, "b": 20}
            )

            print("\nAddition result:")
            print(result.content)

            # Call the greeting tool
            # Call the greeting tool
            result = await session.call_tool(
                "greet",
                arguments={"name": "Developer"}
            )

            print("\nGreeting result:")
            print(result.content)

            # Test invalid greeting input
            print("\nTesting invalid input:")

            try:
                result = await session.call_tool(
                    "greet",
                    arguments={"name": "   "}
                )

                if result.isError:
                    print("Expected error:", result.content)
                else:
                    print("Unexpected success")

            except Exception as e:
                print("Caught exception:", e)


            # Discover available resources
            resources = await session.list_resources()

            print("\nAvailable MCP resources:")

            for resource in resources.resources:
                print(f"- {resource.name}: {resource.uri}")

            # Read the research resource
           # Read the research resource
            result = await session.read_resource(
                "research://notes"
            )

            print("\nResearch notes:")

            for item in result.contents:
                print(item.text)


            print("\nResearch resource result:")
            print(result.contents)

            # Discover available prompts
            prompts = await session.list_prompts()

            print("\nAvailable MCP prompts:")

            for prompt in prompts.prompts:
                print(f"- {prompt.name}: {prompt.description}")

            # Get a research summary prompt
            prompt_result = await session.get_prompt(
                "research_summary",
                arguments={"topic": "Artificial Intelligence"}
            )

            print("\nGenerated prompt:")

            for message in prompt_result.messages:
                print(message.content)


if __name__ == "__main__":
    asyncio.run(main())
