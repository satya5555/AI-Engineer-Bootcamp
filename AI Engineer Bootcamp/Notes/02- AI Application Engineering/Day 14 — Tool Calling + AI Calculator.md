

## 🎯 Day Objective

Learn how an LLM can decide when to use external tools and how an AI application can safely execute those tools and return the result back to the LLM.

### Today's Core Idea

> **The LLM decides what tool to use. The application decides whether and how to execute it.**

---

# 1. Why Tool Calling?

A basic LLM application looks like:

```text
User
 ↓
Prompt
 ↓
LLM
 ↓
Text Response
```

The LLM can generate text, but it cannot directly perform actions in our application.

For example, if the user asks:

```text
What is 25 multiplied by 8?
```

We could ask the LLM to calculate it, but in an AI application we may want the model to use a deterministic calculator instead.

Tool calling changes the architecture:

```text
User
 ↓
LLM
 ↓
Tool Selection
 ↓
Tool Arguments
 ↓
Application Executes Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final Response
```

---

# 2. What Is Tool Calling?

Tool calling allows an LLM to return a structured request asking the application to execute a particular function.

For example:

```python
{
    "name": "multiply",
    "args": {
        "a": 25,
        "b": 8
    }
}
```

The LLM is **not executing Python**.

It is only requesting:

```text
Please execute the multiply tool
with a = 25
and b = 8
```

The application then decides whether to execute that tool.

---

# 3. Function Calling vs Tool Calling

These terms are often used interchangeably.

### Function Calling

The model produces a structured function call.

Example:

```text
multiply(a=25, b=8)
```

### Tool Calling

A broader concept where the model can request application capabilities such as:

* Python functions
* APIs
* databases
* search
* calculators
* file operations
* MCP tools

For modern AI applications, **tool calling is the broader mental model**.

---

# 4. Tool Schema

For an LLM to use a tool correctly, it needs information about the tool.

A useful tool definition contains:

| Component    | Purpose                      |
| ------------ | ---------------------------- |
| Name         | Identifies the tool          |
| Description  | Explains what the tool does  |
| Arguments    | Defines required inputs      |
| Types        | Defines expected input types |
| Return value | Defines the expected result  |

For example:

```python
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
```

The type hints and description help LangChain construct a tool schema for the model.

---

# 5. Project — AI Calculator

Project location:

```text
Projects/ai-calculator/
```

Architecture:

```text
User
 ↓
Streamlit UI / main.py
 ↓
Calculator Service
 ↓
Gemini
 ↓
Tool Selection
 ↓
Tool Router
 ↓
Calculator Function
 ↓
Tool Result
 ↓
Gemini
 ↓
Final Answer
```

---

# 6. Project Structure

```text
ai-calculator/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   └── tools.py
├── main.py
├── test_tools.py
├── ui.py
├── requirements.txt
├── .env
└── .gitignore
```

---

# 7. Calculator Tools

`app/tools.py`

```python
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide the first number by the second."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")

    return a / b
```

These functions are deterministic.

The LLM decides which one should be used, but Python performs the actual calculation.

---

# 8. Binding Tools to Gemini

The calculator service creates the Gemini model:

```python
self.llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
```

The available tools are registered:

```python
self.tools = [
    add,
    subtract,
    multiply,
    divide,
]
```

Then they are bound to the model:

```python
self.llm_with_tools = self.llm.bind_tools(
    self.tools
)
```

This tells the model:

> These are the tools your application makes available.

---

# 9. Tool Selection

When we send:

```text
What is 25 multiplied by 8?
```

Gemini can return a tool call similar to:

```python
[
    {
        "name": "multiply",
        "args": {
            "a": 25,
            "b": 8
        },
        "id": "..."
    }
]
```

The important distinction is:

```text
LLM → selects tool
Application → executes tool
```

---

# 10. Tool Router

The application maintains an allowlist:

```python
self.tool_map = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}
```

The requested tool is looked up:

```python
tool = self.tool_map.get(tool_name)
```

Unknown tools are rejected:

```python
if tool is None:
    raise ValueError(
        f"Unknown tool: {tool_name}"
    )
```

This creates a controlled execution boundary.

---

# 11. Executing Tool Calls

The application extracts:

```python
tool_name = tool_call["name"]
tool_args = tool_call["args"]
```

Then executes the registered function:

```python
result = tool(**tool_args)
```

For example:

```text
multiply
a = 25
b = 8

↓

200
```

---

# 12. Returning the Tool Result

The tool result is wrapped in a `ToolMessage`:

```python
ToolMessage(
    content=str(result),
    tool_call_id=tool_call_id,
)
```

The `tool_call_id` connects the result to the original tool request.

The conversation becomes:

```text
Human:
What is 25 multiplied by 8?

Assistant:
Call multiply(a=25, b=8)

Tool:
200

Assistant:
25 multiplied by 8 is 200.
```

---

# 13. Complete Tool Calling Loop

The final architecture is:

```text
                 User Question
                       │
                       ▼
                ┌─────────────┐
                │   Gemini    │
                └──────┬──────┘
                       │
                  Tool Call
                       │
                       ▼
                ┌─────────────┐
                │ Tool Router │
                └──────┬──────┘
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           add     multiply    divide
             │         │         │
             └─────────┼─────────┘
                       ▼
                  Tool Result
                       │
                       ▼
                ┌─────────────┐
                │   Gemini    │
                └──────┬──────┘
                       │
                       ▼
                  Final Answer
```

---

# 14. Why Tool Calling Matters

Tool calling is the foundation for modern AI agents.

Without tools:

```text
User → LLM → Answer
```

With tools:

```text
User
 ↓
LLM
 ↓
Choose Action
 ↓
Execute Action
 ↓
Observe Result
 ↓
LLM
 ↓
Answer
```

This is the foundation we will build upon when we study **AI Agents**.

---

# 15. Error Handling

AI applications interact with external systems, so errors are expected.

Our calculator protects against division by zero:

```python
if b == 0:
    raise ValueError("Cannot divide by zero.")
```

We also handle API failures.

For example, Gemini returned:

```text
429 RESOURCE_EXHAUSTED
```

when the API quota was exhausted.

Instead of exposing a huge traceback to the user, the application returns:

```text
Gemini API quota has been exceeded.
Please try again later.
```

### Production Principle

> **Never expose raw provider errors directly to end users.**

Convert infrastructure errors into meaningful application-level messages.

---

# 16. Model Configuration

Instead of hard-coding the model, the project uses an environment variable:

```text
GEMINI_MODEL=gemini-3.6-flash
```

The application reads it with:

```python
model=os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)
```

This makes model selection configurable without changing application code.

---

# 17. Security — Never Blindly Trust Tool Calls

This is one of the most important lessons from Day 14.

An LLM-generated tool call is **untrusted input**.

Never do:

```python
eval(user_input)
```

or:

```python
exec(user_input)
```

A dangerous architecture would be:

```text
User
 ↓
LLM
 ↓
Generated Python code
 ↓
eval()
 ↓
Execution
```

Instead:

```text
User
 ↓
LLM
 ↓
Registered Tool
 ↓
Validate Tool
 ↓
Validate Arguments
 ↓
Check Permissions
 ↓
Execute
```

---

# 18. Allowlist Approach

Our calculator only allows:

```text
add
subtract
multiply
divide
```

The application doesn't allow arbitrary functions.

This is an **allowlist**.

> Only explicitly registered tools can be executed.

This becomes extremely important when tools eventually have access to:

* databases
* files
* APIs
* emails
* customer data
* cloud resources
* financial operations

---

# 19. Deterministic Tool Testing

We created:

```text
test_tools.py
```

to test the calculator functions independently of Gemini.

Example:

```python
from app.tools import add, subtract, multiply, divide


print("Add:", add(10, 5))
print("Subtract:", subtract(10, 5))
print("Multiply:", multiply(10, 5))
print("Divide:", divide(10, 5))


try:
    divide(10, 0)
except ValueError as error:
    print("Division Error:", error)
```

Expected:

```text
Add: 15
Subtract: 5
Multiply: 50
Divide: 2.0
Division Error: Cannot divide by zero.
```

This is useful because these tests consume **zero LLM API calls**.

---

# 20. Streamlit UI

The project also contains a Streamlit interface.

Architecture:

```text
Streamlit UI
     ↓
Calculator.calculate()
     ↓
Gemini + Tools
     ↓
Result
     ↓
Streamlit
```

The UI should not contain the tool-calling implementation.

Instead:

```python
answer = calculator.calculate(question)
```

This keeps the application modular.

---

# 21. UI Design Principle

We separate:

### Presentation

```text
ui.py
```

Responsible for:

* input
* buttons
* output
* user experience

### Business / AI Logic

```text
calculator.py
```

Responsible for:

* Gemini
* tool selection
* tool execution
* error handling

### Tools

```text
tools.py
```

Responsible for:

* actual deterministic calculations

This separation makes the project easier to test and extend.

---

# 22. Real-World Scenario

Imagine building an AI customer-support assistant.

Instead of only answering:

```text
Your order is probably arriving tomorrow.
```

the assistant could use tools:

```text
User
 ↓
AI Support Agent
 ↓
get_order_status()
 ↓
Database / API
 ↓
Order information
 ↓
LLM
 ↓
Your order shipped today and is expected tomorrow.
```

The LLM provides the reasoning and interaction layer.

The tools provide access to real systems.

---

# 23. Interview Corner 💼

### Q1. What is tool calling?

Tool calling allows an LLM to produce a structured request for an application to execute a specific registered tool.

---

### Q2. Does the LLM execute the tool?

No.

The LLM generates the tool call. The application executes the actual function.

---

### Q3. Why is this distinction important?

Because the application controls permissions, validation, execution, and security.

---

### Q4. What is an allowlist?

An allowlist explicitly defines which tools are permitted to execute.

Example:

```python
{
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}
```

---

### Q5. Why shouldn't we use `eval()` for an AI calculator?

Because it can turn untrusted input into arbitrary code execution.

---

### Q6. Why does the tool result need to go back to the LLM?

The LLM needs the actual tool output so it can generate the final natural-language response.

---

### Q7. What is the difference between a tool and an LLM?

A tool performs a specific deterministic action.

An LLM interprets language and decides how to respond or which tool may be useful.

---

# 24. Production AI Engineering Considerations

Tool calling introduces additional production concerns:

### Security

* tool permissions
* argument validation
* authentication
* authorization
* prompt injection
* malicious tool requests
* data leakage

### Reliability

* retries
* timeouts
* tool failures
* API failures
* fallback behavior

### Observability

Track:

```text
tool selected
tool arguments
tool execution time
tool success/failure
LLM latency
token usage
```

### Cost

One user request may require:

```text
LLM call
+
Tool execution
+
LLM call
```

Therefore tool-using systems can consume more tokens and API requests than simple LLM applications.

---

# 25. Key Mental Model

Remember this:

> **LLM = Decision / Reasoning Layer**

> **Tool = Action Layer**

> **Application = Control + Security Layer**

Together:

```text
LLM
 ↓
Decision
 ↓
Application
 ↓
Validation / Permissions
 ↓
Tool
 ↓
Result
 ↓
LLM
```

---

# 26. Day 14 Project Completed 🎉

## 🧮 AI Calculator

The project demonstrates:

* Gemini tool calling
* LangChain tool binding
* tool selection
* structured tool arguments
* application-side tool execution
* `ToolMessage`
* final LLM response
* error handling
* API quota handling
* configurable model selection
* deterministic tool testing
* Streamlit UI
* tool security fundamentals

### Final architecture

```text
             ┌──────────────────┐
             │   Streamlit UI   │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │    Calculator    │
             │     Service      │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │     Gemini       │
             └────────┬─────────┘
                      │
                 Tool Call
                      │
                      ▼
             ┌──────────────────┐
             │   Tool Router    │
             └────────┬─────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        add       multiply      divide
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Tool Result
                      │
                      ▼
                   Gemini
                      │
                      ▼
                Final Answer
```

---

# 27. Day 14 Summary

Today we moved from:

```text
LLM → Text
```

to:

```text
LLM → Tool → Result → LLM → Answer
```

The most important lesson is:

> **The model can request an action, but the application remains responsible for executing and securing that action.**

This concept will become the foundation for:

* AI Agents
* MCP
* Multi-Agent Systems
* External APIs
* Database agents
* Enterprise AI systems

---

# 🚀 Next Step

## Day 15 — Document Loaders

We will learn how AI applications ingest real-world documents such as PDFs.

The progression will be:

```text
PDF
 ↓
Document Loader
 ↓
Documents
 ↓
Text Processing
 ↓
Chunks
 ↓
Embeddings
 ↓
Vector Database
 ↓
RAG
```

This will connect directly with the RAG systems we built earlier and prepare us for **Advanced RAG**.
