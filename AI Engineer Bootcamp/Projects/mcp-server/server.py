
from mcp.server.fastmcp import FastMCP
import logging

# Create MCP server
mcp = FastMCP("My First MCP Server")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Tool 1: Addition

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers after validating inputs."""

    logger.info("Addition tool called")

    if not isinstance(a, int) or isinstance(a, bool):
        raise ValueError("First input must be an integer")

    if not isinstance(b, int) or isinstance(b, bool):
        raise ValueError("Second input must be an integer")

    return a + b

    


# Tool 2: Greeting

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user after validating the name."""

    logger.info("Greeting tool called")

    name = name.strip()

    if not name:
        raise ValueError("Name cannot be empty")

    if len(name) > 50:
        raise ValueError("Name cannot exceed 50 characters")

    return f"Hello, {name}! Welcome to MCP."



from pathlib import Path

@mcp.resource("research://notes")
def get_research_notes() -> str:
    """Read research notes from the permitted data directory."""

    base_dir = Path(__file__).parent.resolve()
    file_path = (base_dir / "data" / "research.txt").resolve()

    # Ensure the file stays inside the data directory
    data_dir = (base_dir / "data").resolve()

    if not file_path.is_relative_to(data_dir):
        raise ValueError("Access to this file is not permitted")

    if not file_path.is_file():
        raise FileNotFoundError("Research notes file not found")

    logger.info("Research notes resource accessed")

    return file_path.read_text(encoding="utf-8")



@mcp.prompt()
def research_summary(topic: str) -> str:
    """Generate instructions for summarising a research topic."""
    return f"""
    You are an AI research assistant.

    Summarise the following topic: {topic}

    Structure your response into:
    1. Introduction
    2. Key Concepts
    3. Applications
    4. Challenges
    5. Conclusion

    Use clear and simple language.
    """

# Start the server
if __name__ == "__main__":
    mcp.run()
