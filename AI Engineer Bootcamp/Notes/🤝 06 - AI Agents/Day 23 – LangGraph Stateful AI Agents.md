## 1. Overview

**Objective:** Build a stateful AI assistant using LangGraph, Gemini, native tool calling, conversation memory, and SQLite persistence.

LangGraph is a framework for building stateful, multi-step AI applications using graph-based workflows.

Unlike a basic LLM chain, LangGraph allows us to define:

- Nodes – individual processing steps.
    
- Edges – connections between processing steps.
    
- Conditional edges – dynamic routing based on the current state.
    
- State – information shared between nodes.
    
- Checkpointing – saving workflow state for later continuation.
    

## 2. Technologies Used

- Python
    
- LangGraph
    
- LangChain
    
- Gemini 2.5 Flash
    
- Streamlit
    
- SQLite
    
- Python dotenv
    

## 3. LangGraph Architecture

The application follows this workflow:

User Input → Assistant Node → Tool Decision

- If a tool is required: Execute Tool → Assistant Node.
    
- If no tool is required: Return the final response.
    

The graph can cycle between the assistant and tool nodes until the assistant produces a final answer.

## 4. Core LangGraph Concepts

### StateGraph

`StateGraph` defines the graph workflow and the state shared across its nodes.

### Nodes

Nodes are Python functions that perform specific tasks.

Example:

- Assistant node: Processes user messages and invokes Gemini.
    
- Tools node: Executes the selected tool.
    

### Edges

Edges determine the execution order of nodes.

### Conditional Edges

Conditional edges dynamically determine the next node based on the current state.

### MessagesState

`MessagesState` provides a predefined state structure containing a messages list.

It supports conversation history through messages such as:

- HumanMessage
    
- AIMessage
    
- ToolMessage
    

## 5. Native Tool Calling

The project uses LangChain's native tool-calling functionality.

### Tool Definition

The calculator is defined using the `@tool` decorator.

It supports:

- Addition
    
- Subtraction
    
- Multiplication
    
- Division
    
- Modulo
    
- Exponentiation
    

An AST-based expression evaluator is used instead of Python's `eval()` to restrict supported operations.

### Binding Tools

`llm.bind_tools([calculator])` makes the calculator available to the Gemini model.

### ToolNode

`ToolNode` executes tool calls requested by the LLM.

### tools_condition

`tools_condition` checks whether the assistant response contains tool calls and routes execution accordingly.

## 6. Conversation Memory

The assistant maintains conversation history using LangGraph state.

This allows it to:

- Remember previous messages.
    
- Refer to previous calculations.
    
- Answer follow-up questions.
    
- Maintain separate conversations.
    

## 7. Checkpointing and Persistence

Checkpointing saves graph state so that a conversation can continue later.

### InMemorySaver

Stores conversation checkpoints in memory. Data is lost when the application process ends.

### SqliteSaver

Stores checkpoints in an SQLite database.

Benefits:

- Conversation persistence.
    
- State recovery.
    
- Local database storage.
    
- Conversation continuation after application restarts.
    

### Thread ID

Each conversation is associated with a unique `thread_id`.

The same thread ID retrieves the corresponding conversation state. A different thread ID creates an independent conversation.

## 8. Streamlit User Interface

The project includes a Streamlit interface with:

- Chat input and responses.
    
- Conversation history.
    
- New Conversation option.
    
- Clear Chat option.
    
- Thread ID display.
    
- Loading indicator.
    

The UI communicates with the LangGraph agent using `agent.invoke()`.

## 9. Project Architecture

```
langgraph-stateful-agent/
│
├── app/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   ├── tools.py
│   └── graph.py
│
├── main.py
├── ui.py
├── requirements.txt
├── .env
├── .gitignore
└── checkpoints.sqlite
```

**File responsibilities:**

|File|Responsibility|
|---|---|
|state.py|Defines agent state|
|nodes.py|Defines assistant node and LLM|
|tools.py|Defines calculator tool|
|graph.py|Builds and compiles the graph|
|main.py|Runs the agent from terminal|
|ui.py|Provides Streamlit interface|
|checkpoints.sqlite|Stores conversation checkpoints|

`.env` and the SQLite database are local files and should not be committed to GitHub.

## 10. Testing Performed

|Test|Expected Result|
|---|---|
|General knowledge question|Direct LLM response|
|Calculator: 25 × 40|1000|
|Follow-up question|Uses previous conversation context|
|New conversation|Starts an independent thread|
|Application restart|Restores saved conversation using the same thread ID|

## 11. Key Learnings

1. Understood graph-based AI workflows.
    
2. Implemented nodes, edges, and conditional routing.
    
3. Integrated Gemini with LangGraph.
    
4. Implemented native tool calling.
    
5. Used ToolNode and tools_condition.
    
6. Implemented conversation history using MessagesState.
    
7. Understood checkpointing and SQLite persistence.
    
8. Used thread IDs to manage independent conversations.
    
9. Built a chat interface using Streamlit.
    

## 12. Limitations and Production Considerations

- SQLite is suitable for local learning and lightweight applications.
    
- Production applications need appropriate database and connection lifecycle management.
    
- API rate limits and failures need retry and error-handling strategies.
    
- Tool inputs must be validated.
    
- Persistent conversation state needs suitable access controls and retention policies.
    
- Conversation memory should be scoped to the correct user and thread.
    

## 13. Interview Questions

**Q1. What is LangGraph?**

LangGraph is a framework for building stateful, multi-step AI workflows using nodes, edges, and shared state.

**Q2. What is the difference between LangChain and LangGraph?**

LangChain provides components for building LLM applications, while LangGraph provides graph-based orchestration for stateful and cyclic workflows.

**Q3. What is StateGraph?**

StateGraph is used to define a workflow where nodes operate on a shared state.

**Q4. What is the difference between an edge and a conditional edge?**

An edge defines a fixed transition, whereas a conditional edge selects the next node based on a routing condition.

**Q5. What is MessagesState?**

MessagesState is a predefined LangGraph state that maintains a list of conversation messages.

**Q6. What is ToolNode?**

ToolNode executes tools requested by the LLM.

**Q7. What is tools_condition?**

It routes execution based on whether the assistant generated tool calls.

**Q8. What is checkpointing?**

Checkpointing saves graph state so that execution can resume from a previously saved state.

**Q9. What is the purpose of thread_id?**

It identifies a conversation and allows LangGraph to retrieve its corresponding checkpointed state.

**Q10. What is the difference between InMemorySaver and SqliteSaver?**

InMemorySaver stores checkpoints in memory, whereas SqliteSaver persists them in an SQLite database.

**Q11. Why should we avoid eval() for calculator tools?**

`eval()` can execute arbitrary Python expressions. An AST-based evaluator can restrict execution to explicitly supported operations.

**Q12. How does a tool-calling cycle work?**

The assistant requests a tool, ToolNode executes it, and the result is passed back to the assistant. This continues until the assistant returns a final response.

## 14. Day 23 Outcome

**Project:** LangGraph Stateful AI Assistant

Built a conversational AI assistant with Gemini, native calculator tool calling, conversation memory, SQLite checkpointing, and a Streamlit interface.

**Next:** Day 24 – Google ADK Workflow Agent.