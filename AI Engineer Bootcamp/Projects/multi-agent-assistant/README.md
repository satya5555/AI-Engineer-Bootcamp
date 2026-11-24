# Multi-Agent Assistant

A locally running multi-agent AI assistant built with Python and Ollama. The system uses specialized agents coordinated by a Supervisor to research, analyze and write responses to user requests.

## Project objectives

- Understand multi-agent architecture and agent collaboration.
- Implement dynamic task planning and delegation.
- Coordinate multiple specialized agents through a Supervisor.
- Integrate a locally hosted LLM.
- Implement human-in-the-loop approval.
- Maintain persistent workflow memory.
- Integrate reusable tools.
- Test agent behavior and workflow execution.

## Architecture

```text
                    User Request
                         |
                         v
                   Dynamic Planner
                         |
                         v
                     Supervisor
                         |
              Selects execution plan
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Researcher       Analyst        Writer
          |              |              |
          v              v              v
     Knowledge       Text Analysis   Final Response
       Search            Tool
          |              |
          +--------------+
                 |
                 v
          Shared Workflow State
                 |
                 v
          Human Approval Gate
                 |
           Approve / Reject
                 |
                 v
          Workflow Completion
                 |
                 v
          Persistent Memory
```

## Technology stack

| Technology  | Purpose                    |
| ----------- | -------------------------- |
| Python      | Application development    |
| Ollama      | Local LLM runtime          |
| Qwen 2.5 3B | Language model             |
| pytest      | Automated testing          |
| JSON        | Persistent workflow memory |

## Agents

### 1. Researcher

- Receives the user's research request.
- Searches the local knowledge base using the knowledge-search tool.
- Retrieves relevant previous workflow memories.
- Uses the LLM to prepare research findings.
- Passes findings to the Analyst.

### 2. Analyst

- Processes research findings.
- Uses the text-analysis tool.
- Identifies themes, benefits and challenges.
- Produces an analysis for the Writer.

### 3. Writer

- Produces the final response.
- Uses research findings and analysis when available.
- Supports standalone writing workflows when only source material is available.
- Avoids introducing unsupported facts.

### 4. Supervisor

- Creates a dynamic execution plan.
- Selects and invokes agents.
- Maintains shared workflow state.
- Pauses for human approval.
- Resumes or rejects workflows.
- Saves completed workflow memory.

## Dynamic task planning

The planner selects agents based on the user's request.

| Request type            | Execution plan                |
| ----------------------- | ----------------------------- |
| Research or investigate | Researcher → Analyst → Writer |
| Analyze or evaluate     | Analyst → Writer              |
| Summarize or rewrite    | Writer                        |
| Compare                 | Researcher → Analyst → Writer |

The workflow pauses at the human approval stage before final writing is executed.

## Tool integration

The project includes a simple tool registry.

**Knowledge search**

- Searches a local sample knowledge base.
- Returns relevant entries based on keyword matching.

**Text analysis**

- Calculates character count.
- Calculates word count.
- Calculates sentence count.

Tools are registered centrally and invoked by agents through the tool registry.

## Persistent memory

The application stores completed workflows in:

`memory/agent_memory.json`

Each memory record can contain:

- Original user request
- Research findings
- Analysis
- Final response
- Timestamp

The memory module supports:

- Saving completed workflows.
- Loading stored memories.
- Retrieving recent memories.
- Retrieving relevant memories using keyword matching.

Memory JSON files are runtime data and should not be committed to Git.

## Human-in-the-loop workflow

The workflow supports explicit human approval.

1. The Supervisor creates an execution plan.
2. The selected pre-approval agents execute.
3. The application displays the research and analysis.
4. The user approves or rejects the workflow.
5. If approved, the remaining Writer agent executes.
6. The completed workflow is saved to persistent memory.

## Installation and execution

### Prerequisites

- Python installed.
- Ollama installed and running.
- Git installed.

Pull the model:

```powershell
ollama pull qwen2.5:3b
```

Navigate to the project:

```powershell
cd "D:\AI Bootcamp\AI Engineer Bootcamp\Projects\multi-agent-assistant"
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the application:

```powershell
python -m app.main
```

Run automated tests:

```powershell
python -m pytest -v
```

## Project structure

```text
multi-agent-assistant/
│
├── app/
│   ├── agents/
│   │   ├── researcher.py
│   │   ├── analyst.py
│   │   └── writer.py
│   │
│   ├── core/
│   │   ├── llm_client.py
│   │   ├── memory.py
│   │   ├── planner.py
│   │   ├── state.py
│   │   └── supervisor.py
│   │
│   ├── tools/
│   │   ├── knowledge_search.py
│   │   ├── text_analysis.py
│   │   └── registry.py
│   │
│   └── main.py
│
├── tests/
├── memory/
├── logs/
├── reports/
├── requirements.txt
├── README.md
└── .gitignore
```

## Testing

The test suite covers:

- Agent execution.
- Dynamic planning.
- Workflow orchestration.
- Human approval and rejection.
- Workflow resumption.
- Persistent memory.
- Memory retrieval.
- Tool registration and execution.
- State updates and error handling.

Run the complete suite:

```powershell
python -m pytest -v
```

## Current limitations

- The knowledge base contains sample local data rather than live web research.
- Memory retrieval uses keyword matching, not embeddings or vector search.
- The tool registry uses predefined Python functions; it is not an MCP server.
- Unit tests mock LLM responses to keep tests deterministic and avoid depending on a running model.
- Real LLM execution requires Ollama and the configured model to be available.
- The application is a learning prototype, not a production-hardened multi-agent platform.

## Key learnings

- Multi-agent architecture and role specialization.
- Supervisor-based orchestration.
- Dynamic planning and task delegation.
- Shared state management.
- Human-in-the-loop workflows.
- Local LLM integration with Ollama.
- Tool registry design.
- Persistent memory and retrieval.
- Automated testing of agent workflows.

## Future improvements

- Replace keyword-based memory retrieval with embeddings and a vector database.
- Add external knowledge sources.
- Explore MCP server integration.
- Add stronger agent observability and evaluation.
- Add retry strategies and more robust failure recovery.
- Build a web-based interface.

---

**Project:** Day 30 – Mini Project #3  
**Track:** AI Engineer Bootcamp  
**Focus:** Multi-Agent Systems, Coordination, Delegation and Supervisors
