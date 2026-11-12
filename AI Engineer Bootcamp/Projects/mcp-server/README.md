# MCP Server – Python Implementation

A hands-on implementation of the Model Context Protocol (MCP) using Python and the official MCP SDK.

This project demonstrates how to build an MCP server, expose tools, resources and prompts, and connect to it through an MCP client using stdio transport.

## Features

- MCP server using FastMCP.
- Addition and greeting tools.
- Research notes resource.
- Research summary prompt.
- MCP client with capability discovery and invocation.
- stdio transport.
- Logging and input validation.
- Restricted local resource file access.
- Unit and integration tests using pytest.

## Tech Stack

- Python
- Model Context Protocol (MCP) Python SDK
- FastMCP
- asyncio
- pytest

## Project Structure

```text
mcp-server/
├── data/
│   └── research.txt
├── tests/
│   └── test_server.py
├── server.py
├── client.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

### 1. Clone the repository

```powershell
git clone <your-repository-url>
```

### 2. Navigate to the project

```powershell
cd Projects/mcp-server
```

### 3. Create a virtual environment

```powershell
python -m venv .venv
```

### 4. Activate it

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

## Run the MCP Server

```powershell
python server.py
```

The server uses stdio transport and waits for a compatible MCP client.

Stop it using `Ctrl + C`.

## Run the MCP Client

```powershell
python client.py
```

The client launches the server as a subprocess and performs the following operations:

1. Initialises the MCP session.
2. Discovers available tools.
3. Invokes the addition and greeting tools.
4. Discovers and reads the research resource.
5. Discovers and retrieves the research summary prompt.

## Available Capabilities

### Tools

| Tool          | Description                                  |
| ------------- | -------------------------------------------- |
| `add(a, b)`   | Adds two integers                            |
| `greet(name)` | Returns a greeting after validating the name |

### Resources

| Resource URI       | Description                      |
| ------------------ | -------------------------------- |
| `research://notes` | Provides local AI research notes |

### Prompts

| Prompt                    | Description                                          |
| ------------------------- | ---------------------------------------------------- |
| `research_summary(topic)` | Returns reusable research summarisation instructions |

## Testing

Run the complete test suite:

```powershell
python -m pytest -v
```

Tests cover:

- Addition and invalid inputs.
- Greeting and invalid inputs.
- Research resource access.
- Research prompt generation.
- MCP client-server integration.

**Verified result: 7/7 tests passed.**

## Security Considerations

- Validate tool arguments.
- Restrict resource file access to the permitted directory.
- Avoid exposing sensitive files and environment variables.
- Keep diagnostic logging separate from protocol output.
- Use authentication and authorisation when deploying remote servers.

## Learning Outcomes

- Understand MCP Host, Client and Server architecture.
- Implement MCP Tools, Resources and Prompts.
- Communicate through stdio transport.
- Discover and invoke MCP capabilities.
- Add logging and validation.
- Implement basic file-access protection.
- Test MCP functionality using pytest.

## Future Improvements

- Implement Streamable HTTP transport.
- Add authentication and authorisation.
- Integrate with external APIs.
- Connect the server to an LLM-powered application.
- Expand security and integration testing.

---

**Bootcamp:** AI Engineer Bootcamp  
**Sprint:** 3 – AI Agents  
**Day:** 27 – MCP Architecture + Production Tooling
