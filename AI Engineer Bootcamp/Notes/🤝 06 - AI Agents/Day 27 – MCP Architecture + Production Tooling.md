## 1. What is MCP?

Model Context Protocol (MCP) is a standardised protocol that allows AI applications to communicate with external tools, resources and services.

It provides a common interface for AI applications to discover and use external capabilities.

## 2. MCP Architecture

### Core components

- **MCP Host:** The AI application that manages the interaction.
    
- **MCP Client:** Establishes and manages a connection to an MCP server.
    
- **MCP Server:** Exposes tools, resources and prompts.
    

### Communication flow

1. The host manages the AI application.
    
2. The MCP client connects to an MCP server.
    
3. The client discovers available capabilities.
    
4. The client invokes tools or reads resources.
    
5. The server returns the results.
    

## 3. Three Core MCP Capabilities

### Tools

Tools are executable functions that an AI application can invoke.

Examples:

- Calculator
    
- Weather lookup
    
- Database query
    
- File processing
    

Implementation:

`@mcp.tool()`

### Resources

Resources expose data that an AI application can read.

Examples:

- Local text files
    
- Database records
    
- Application information
    

Implementation:

`@mcp.resource("research://notes")`

### Prompts

Prompts are reusable prompt templates exposed by an MCP server.

Examples:

- Research summarisation
    
- Code review
    
- Report generation
    

Implementation:

`@mcp.prompt()`

**Important distinction:** Retrieving a prompt does not automatically execute an LLM. The AI application can send the returned prompt to its chosen model.

## 4. MCP Transports

### stdio

- Uses standard input and standard output.
    
- The client launches the server as a subprocess.
    
- Suitable for local integrations.
    
- Implemented in this project.
    

### Streamable HTTP

- Allows clients to communicate with remote MCP servers over HTTP.
    
- Suitable for network-accessible integrations.
    
- Supports streaming and session management.
    

Streamable HTTP was studied conceptually but not implemented in this project.

## 5. Python MCP SDK

Used the Python MCP SDK and `FastMCP`.

Important components:

- `FastMCP`: Creates an MCP server.
    
- `ClientSession`: Manages the client session.
    
- `stdio_client`: Establishes stdio communication.
    
- `session.initialize()`: Initialises the session.
    
- `session.list_tools()`: Discovers tools.
    
- `session.call_tool()`: Invokes tools.
    
- `session.list_resources()`: Discovers resources.
    
- `session.read_resource()`: Reads resources.
    
- `session.list_prompts()`: Discovers prompts.
    
- `session.get_prompt()`: Retrieves prompts.
    

## 6. Logging and Error Handling

### Logging

Used Python's logging module to record tool execution.

- INFO: General execution information.
    
- WARNING: Unexpected or potentially problematic conditions.
    
- ERROR: Failures.
    

For stdio servers, diagnostics should go to stderr rather than stdout, because stdout carries MCP protocol messages.

### Input validation

Implemented checks for:

- Invalid integer inputs.
    
- Empty or whitespace-only names.
    
- Names exceeding the allowed length.
    

### Error handling

MCP tool execution errors can be represented by a result with `isError=True`. Clients should inspect the result rather than assuming every failure raises a Python exception.

## 7. Security Fundamentals

Important production security practices:

1. Validate incoming arguments.
    
2. Restrict file access to permitted directories.
    
3. Avoid exposing environment variables and sensitive files.
    
4. Never execute arbitrary user-provided shell commands.
    
5. Use authentication and authorisation for remote servers.
    
6. Apply least-privilege access.
    
7. Avoid logging passwords, tokens and personal data.
    

Implemented a resolved-path check to ensure the research resource stays within the permitted data directory.

Authentication and authorisation were studied conceptually, not implemented.

## 8. Testing

### Unit testing

Used pytest to test:

- Addition.
    
- Invalid addition.
    
- Greeting.
    
- Invalid greeting.
    
- Research resource.
    
- Research prompt.
    

### Integration testing

Created an MCP client-server integration test that verifies:

- Server connection.
    
- Tool discovery.
    
- Tool execution.
    
- Resource discovery.
    
- Prompt discovery.
    

**Result: 7/7 tests passed.**

## 9. Project Structure

```
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

## 10. Key Learnings

- Understand MCP architecture and communication.
    
- Build an MCP server using Python.
    
- Expose tools, resources and prompts.
    
- Connect an MCP client through stdio.
    
- Discover and invoke MCP capabilities.
    
- Add logging and input validation.
    
- Apply basic file-access security.
    
- Write unit and integration tests.
    

## 11. Limitations and Future Improvements

- Implement Streamable HTTP transport.
    
- Add authentication and authorisation.
    
- Connect the MCP server to a real external service.
    
- Add more practical tools and resources.
    
- Improve automated security testing.
    
- Integrate the MCP server with an AI application.
    

## 12. Day 27 Completion

Built a working local MCP server and client using Python.

Implemented all three core MCP capabilities, stdio communication, validation, logging, file-access protection and automated tests.

**Test result: 7/7 passed.**