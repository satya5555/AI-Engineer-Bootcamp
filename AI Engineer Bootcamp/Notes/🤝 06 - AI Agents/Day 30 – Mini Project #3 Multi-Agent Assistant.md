## 1. Objective

Build a multi-agent assistant in Python that can dynamically plan tasks, delegate work to specialized agents, coordinate their execution and generate a final response.

The project brings together concepts from:

- Multi-agent systems
    
- Agent coordination
    
- Task delegation
    
- Supervisor architecture
    
- Tool integration
    
- Persistent memory
    
- Human-in-the-loop workflows
    

## 2. Multi-Agent System

A multi-agent system consists of multiple specialized agents working together to achieve a common goal.

Instead of one agent performing every task, responsibilities are distributed among agents.

### Benefits

- Specialization of tasks.
    
- Separation of responsibilities.
    
- Easier maintenance and testing.
    
- Flexible task execution.
    
- Reusable agents and tools.
    

## 3. Agents implemented

### Researcher Agent

Responsibilities:

- Understand the research request.
    
- Search the knowledge base.
    
- Retrieve relevant previous memories.
    
- Generate research findings.
    
- Hand off findings to the Analyst.
    

### Analyst Agent

Responsibilities:

- Process research findings.
    
- Use the text-analysis tool.
    
- Identify key themes.
    
- Analyze benefits and challenges.
    
- Produce structured analysis.
    

### Writer Agent

Responsibilities:

- Consume available research and analysis.
    
- Generate the final response.
    
- Support standalone writing when source material is available.
    

### Supervisor Agent

Responsibilities:

- Generate the execution plan.
    
- Delegate tasks to agents.
    
- Maintain shared state.
    
- Coordinate workflow execution.
    
- Handle human approval.
    
- Resume or reject workflows.
    
- Save completed workflow memory.
    

## 4. Supervisor Architecture

The Supervisor acts as the central coordinator.

```
User Request
     |
     v
Dynamic Planner
     |
     v
Supervisor
     |
     +----> Researcher
     |
     +----> Analyst
     |
     +----> Writer
     |
     v
Human Approval
     |
     v
Final Response
```

The Supervisor selects the agents required for the task rather than always executing every agent.

## 5. Dynamic Planning and Delegation

Implemented using `app/core/planner.py`.

|Request|Planned agents|
|---|---|
|Research AI in healthcare|Researcher → Analyst → Writer|
|Analyze findings|Analyst → Writer|
|Summarize findings|Writer|
|Compare technologies|Researcher → Analyst → Writer|

The planner currently uses keyword-based rules.

Important distinction: selecting an agent does not automatically provide it with valid source material. The workflow prepares standalone analysis and writing inputs from the user's supplied request when necessary.

## 6. Shared Workflow State

Implemented in `app/core/state.py`.

The shared state contains:

- `user_request`
    
- `plan`
    
- `research_findings`
    
- `retrieved_memories`
    
- `analysis`
    
- `final_response`
    
- `status`
    
- `current_agent`
    
- `agent_history`
    
- `agent_messages`
    
- `errors`
    
- `human_approved`
    
- `created_at`
    

The state allows agents and the Supervisor to share workflow information.

### Agent communication

Agent communication history records:

- Sender
    
- Receiver
    
- Message content
    
- Timestamp
    

This helps track how information moves between agents.

## 7. Local LLM Integration

Implemented using Ollama and Qwen 2.5 3B.

Python integration:

```
import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain multi-agent AI systems."
        }
    ]
)

print(response["message"]["content"])
```

The project uses a shared LLM client to avoid duplicating model integration code.

## 8. Tool Integration

Implemented using a central tool registry.

### Knowledge Search Tool

- Searches a local sample knowledge base.
    
- Matches query keywords against stored content.
    
- Returns relevant entries.
    

### Text Analysis Tool

- Character count.
    
- Word count.
    
- Sentence count.
    

### Tool Registry

The registry maps tool names to Python functions and provides a common execution interface.

Example:

```
execute_tool(
    "analyze_text",
    text="AI supports healthcare."
)
```

## 9. Persistent Memory

Implemented in `app/core/memory.py`.

The application saves completed workflow information in a JSON file.

### Memory operations

1. Load memories.
    
2. Save completed workflows.
    
3. Retrieve recent memories.
    
4. Retrieve relevant memories.
    

### Memory retrieval

The current implementation uses keyword overlap to identify relevant past workflows.

This is not semantic vector retrieval. An embedding model and vector database would be a future enhancement.

## 10. Human-in-the-Loop

The application pauses before the final writing stage.

Workflow:

1. Supervisor creates a plan.
    
2. Researcher and/or Analyst execute as selected.
    
3. Results are displayed.
    
4. User approves or rejects.
    
5. If approved, the remaining Writer executes.
    
6. Completed workflow is saved.
    

This introduces human oversight into agent execution.

## 11. Testing

Framework: `pytest`

Test coverage includes:

- Individual agent behavior.
    
- Dynamic planning.
    
- Supervisor execution.
    
- Approval and rejection.
    
- Workflow resumption.
    
- State management.
    
- Memory saving and retrieval.
    
- Tool execution.
    
- Error handling.
    

Run tests:

```
python -m pytest -v
```

Unit tests mock LLM responses so they can run without repeatedly calling the local model.

## 12. Project Structure

```
multi-agent-assistant/
├── app/
│   ├── agents/
│   │   ├── researcher.py
│   │   ├── analyst.py
│   │   └── writer.py
│   ├── core/
│   │   ├── llm_client.py
│   │   ├── memory.py
│   │   ├── planner.py
│   │   ├── state.py
│   │   └── supervisor.py
│   ├── tools/
│   │   ├── knowledge_search.py
│   │   ├── text_analysis.py
│   │   └── registry.py
│   └── main.py
├── tests/
├── memory/
├── logs/
├── reports/
├── requirements.txt
└── README.md
```

## 13. Important Learnings

- How multiple AI agents collaborate.
    
- How a Supervisor coordinates agents.
    
- How dynamic task planning works.
    
- How to manage shared state.
    
- How to integrate a local LLM.
    
- How to build and register reusable tools.
    
- How to implement persistent memory.
    
- How to pause and resume workflows with human approval.
    
- How to test agent workflows with mocked LLM responses.
    

## 14. Limitations and Future Scope

Current limitations:

- Sample local knowledge base.
    
- Keyword-based planner.
    
- Keyword-based memory retrieval.
    
- Predefined Python tools rather than MCP.
    
- No production-grade distributed agent execution.
    

Future improvements:

- Semantic memory using embeddings and vector databases.
    
- MCP server and client integration.
    
- External research tools.
    
- Agent observability and evaluation.
    
- Retry mechanisms and robust error recovery.
    
- Web interface.
    

## 15. Completion Checklist

- Researcher Agent
    
- Analyst Agent
    
- Writer Agent
    
- Supervisor
    
- Dynamic planning
    
- Agent delegation
    
- Shared workflow state
    
- Agent communication history
    
- Local Ollama integration
    
- Tool registry
    
- Persistent memory
    
- Memory retrieval
    
- Human approval and workflow resumption
    
- Automated test suite
    
- Final local test verification
    
- Git commit and push
    

---

**Day 30 status:** Implementation and test fixes completed; final verification and repository housekeeping remain.