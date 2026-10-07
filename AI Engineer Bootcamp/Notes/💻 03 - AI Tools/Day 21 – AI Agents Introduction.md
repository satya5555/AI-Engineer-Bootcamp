## 🎯 Objective

Understand the fundamentals of AI Agents and build a simple tool-using AI Agent from scratch.

The goal is to understand the agent concept before using agent frameworks such as CrewAI, LangGraph, Google ADK, and OpenAI Agents SDK.

---

# 1. What is an AI Agent?

An AI Agent is an AI system that can understand a user's goal, decide what action is required, use tools when necessary, observe the result, and produce a final response.

A simple agent follows:

```
User Goal
    ↓
Think / Decide
    ↓
Choose Action
    ↓
Execute Tool
    ↓
Observe Result
    ↓
Final Answer
```

Unlike a normal LLM application, an agent can take actions instead of only generating text.

---

# 2. LLM vs AI Agent

### Traditional LLM

```
User
 ↓
LLM
 ↓
Response
```

The LLM primarily generates a response based on the input.

### AI Agent

```
User
 ↓
LLM
 ↓
Decision
 ↓
Tool
 ↓
Observation
 ↓
LLM
 ↓
Final Response
```

The agent can decide when an external tool is required.

---

# 3. Project – Simple AI Agent

For Day 21, a simple AI Agent was built using:

- Python
    
- LangChain
    
- Gemini
    
- Custom Python tools
    
- Streamlit
    

The agent supports three tools:

```
add()
multiply()
get_word_count()
```

---

# 4. Project Structure

```
ai-simple-agent/
│
├── app/
│   ├── __init__.py
│   ├── tools.py
│   └── agent.py
│
├── main.py
├── ui.py
├── requirements.txt
└── .gitignore
```

### Responsibility of each file

**tools.py**

Contains the functions that the agent can use.

**agent.py**

Contains the agent's decision-making and tool execution logic.

**main.py**

Provides a simple terminal interface for testing the agent.

**ui.py**

Provides a Streamlit interface.

---

# 5. Tool Layer

The agent was given three tools.

## add()

```
def add(a, b):
    return a + b
```

Example:

```
add(10, 20)
→ 30
```

## multiply()

```
def multiply(a, b):
    return a * b
```

Example:

```
multiply(25, 4)
→ 100
```

## get_word_count()

```
def get_word_count(text):
    return len(text.split())
```

Example:

```
get_word_count("AI agents can use tools")
→ 5
```

---

# 6. Agent Decision Layer

The LLM is instructed to decide whether a tool is required.

For example:

```
User:
What is 25 multiplied by 4?
```

The LLM produces:

```
TOOL: multiply
ARGS: 25, 4
```

For a question that does not require a tool:

```
User:
What is an AI agent?
```

The LLM can produce:

```
DIRECT: An AI agent is an AI system that can make decisions and use tools to accomplish a task.
```

---

# 7. Tool Selection

The agent maintains a tool registry:

```
self.tools = {
    "add": add,
    "multiply": multiply,
    "get_word_count": get_word_count
}
```

This allows the agent to map the LLM's decision to an actual Python function.

---

# 8. Tool Execution

The agent parses the LLM decision.

Example:

```
TOOL: multiply
ARGS: 25, 4
```

The agent extracts:

```
tool_name = multiply
arguments = 25, 4
```

Then executes:

```
multiply(25, 4)
```

Result:

```
100
```

---

# 9. Observation → Final Answer

The tool result is then provided back to the LLM.

```
User Question:
What is 25 multiplied by 4?

Tool:
multiply

Tool Result:
100
```

The LLM generates the final response:

```
25 multiplied by 4 is 100.
```

This creates the important agent pattern:

```
Question
   ↓
Decision
   ↓
Action
   ↓
Observation
   ↓
Final Answer
```

---

# 10. Agent Execution Flow

The complete flow implemented in Day 21 is:

```
                    User
                      │
                      ↓
                  Question
                      │
                      ↓
                ┌───────────┐
                │    LLM    │
                │  Decide   │
                └─────┬─────┘
                      │
              ┌───────┴────────┐
              │                │
         No tool needed    Tool required
              │                │
              ↓                ↓
        Direct Answer      Select Tool
                               │
                               ↓
                         Execute Tool
                               │
                               ↓
                          Tool Result
                               │
                               ↓
                              LLM
                               │
                               ↓
                         Final Answer
```

---

# 11. Example

### User

```
What is 25 multiplied by 4?
```

### Agent decision

```
TOOL: multiply
ARGS: 25, 4
```

### Tool execution

```
multiply(25, 4)
```

### Result

```
100
```

### Final response

```
25 multiplied by 4 is 100.
```

---

# 12. Direct Answer Example

### User

```
What is an AI agent?
```

No external tool is required.

The agent directly generates an answer.

```
User
 ↓
LLM
 ↓
No tool required
 ↓
Direct answer
```

This demonstrates that an agent does not necessarily call a tool for every request.

---

# 13. Agent Loop

The fundamental concept learned today is the Agent Loop:

```
Think
 ↓
Act
 ↓
Observe
 ↓
Think Again
 ↓
Final Answer
```

In a more advanced agent, this loop can continue multiple times.

Example:

```
User Goal
   ↓
Think
   ↓
Tool A
   ↓
Observe
   ↓
Think
   ↓
Tool B
   ↓
Observe
   ↓
Think
   ↓
Final Answer
```

This is the foundation for more advanced agent frameworks.

---

# 14. Streamlit UI

A simple Streamlit interface was created to interact with the agent.

The UI allows the user to:

1. Enter a question
    
2. Run the agent
    
3. View the final answer
    

Example:

```
┌────────────────────────────────────┐
│        🤖 Simple AI Agent          │
│                                    │
│ Ask the agent                      │
│ ┌────────────────────────────────┐ │
│ │ What is 25 multiplied by 4?   │ │
│ └────────────────────────────────┘ │
│                                    │
│          [ Run Agent ]              │
│                                    │
│ Final Answer                       │
│ 25 multiplied by 4 is 100.         │
└────────────────────────────────────┘
```

---

# 15. Testing

The agent was tested with:

### Addition

```
What is 35 plus 17?
```

Expected:

```
52
```

### Multiplication

```
What is 12 multiplied by 8?
```

Expected:

```
96
```

### Word Count

```
How many words are in "AI agents can use tools"?
```

Expected:

```
5
```

### Direct Question

```
What is an AI agent?
```

Expected behavior:

```
No tool call
→ Direct answer
```

---

# 16. Important Learning

The important distinction is:

### LLM

```
Input → Generate Output
```

### Agent

```
Goal
 ↓
Reason / Decide
 ↓
Action
 ↓
Observation
 ↓
Reason Again
 ↓
Final Output
```

An agent combines:

- LLM
    
- Tools
    
- Decision making
    
- Execution
    
- Observation
    
- Iteration
    

---

# 17. Limitations of Today's Agent

This is intentionally a simple educational agent.

It currently has limitations:

- Tool selection is based on structured text generated by the LLM.
    
- Argument parsing is basic.
    
- Only a small number of tools are available.
    
- The execution loop is limited.
    
- There is no persistent memory.
    
- There is no advanced error recovery.
    
- There is no agent tracing or observability.
    
- There is no multi-agent coordination.
    

These limitations will be addressed in later days of the roadmap.

---

# 18. What Comes Next

Day 21 focused on understanding the agent concept without depending heavily on an agent framework.

The upcoming topics introduce production-oriented agent frameworks:

```
Day 21
Simple AI Agent
      ↓
Day 22
CrewAI
      ↓
Day 23
LangGraph
      ↓
Day 24
Google ADK
      ↓
Day 25
OpenAI Agents SDK
      ↓
Day 26
Multi-Agent Systems
      ↓
Day 27
MCP
      ↓
Day 28
Observability + Security
      ↓
Day 29
Agent Evaluation
      ↓
Day 30
Multi-Agent Assistant
```

---

# 19. Interview Questions

### What is an AI agent?

An AI agent is an AI system that can understand a goal, decide what action to take, use tools, observe results, and produce a final response.

### What is the difference between an LLM and an AI agent?

An LLM primarily generates responses, while an AI agent combines an LLM with tools, decision-making, execution, and observation.

### What is tool calling?

Tool calling allows an LLM to request the execution of an external function or tool when it needs capabilities beyond text generation.

### What is an agent loop?

An agent loop is the repeated process of:

```
Think → Act → Observe → Think Again → Final Answer
```

### Why do agents need tools?

Tools allow agents to perform actions that an LLM cannot reliably perform by text generation alone, such as calculations, database queries, API calls, searches, or file operations.

### Does an agent always use a tool?

No. An agent can decide that a question can be answered directly without using a tool.

---

# 20. Day 21 Outcome

Built a working **Simple AI Agent** that can:

- Understand a user request
    
- Decide whether a tool is required
    
- Select an appropriate tool
    
- Execute the tool
    
- Observe the tool result
    
- Send the result back to the LLM
    
- Generate a final response
    
- Provide a Streamlit interface
    

The key concept learned:

> **An AI agent is an LLM-driven system that can decide and act using tools to accomplish a goal.**