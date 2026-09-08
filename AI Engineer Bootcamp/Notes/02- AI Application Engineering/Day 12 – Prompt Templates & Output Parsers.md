````markdown
# 🚀 AI Engineer Bootcamp

# Sprint 2 – LangChain & Advanced RAG

# 📅 Day 12 – Prompt Templates & Output Parsers

---

# 🎯 Today’s Goal

Today's goal was to understand how to build reusable and reliable AI application components using:

- Prompt Templates
- Dynamic Prompt Variables
- LangChain Expression Language (LCEL)
- Output Parsers
- `StrOutputParser`
- Structured Outputs
- Pydantic
- Gemini
- Separation of AI logic and UI
- Basic error handling

We built a small browser-based **AI Utility** using LangChain, Gemini, Pydantic, and Streamlit.

---

# 🧠 Why Prompt Templates?

A hardcoded prompt is difficult to reuse.

Example:

```python
prompt = "Explain vector databases"
````

This only works for one topic.

A Prompt Template allows us to create a reusable prompt:

```python
prompt = ChatPromptTemplate.from_template(
    """
    Explain the following topic in simple terms:

    Topic:
    {topic}
    """
)
```

The `{topic}` is a dynamic variable.

We can then provide different values:

```python
chain.invoke({
    "topic": "Vector databases"
})
```

or:

```python
chain.invoke({
    "topic": "RAG"
})
```

or:

```python
chain.invoke({
    "topic": "LangGraph"
})
```

The prompt itself does not need to change.

---

# 🔹 ChatPromptTemplate

`ChatPromptTemplate` allows us to define reusable prompts that can accept variables.

Example:

```python
from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template(
    """
    Explain the following topic in simple terms:

    Topic:
    {topic}
    """
)
```

The template contains:

```text
{topic}
```

which is replaced with the actual input when the chain is invoked.

---

# 🔄 Dynamic Prompt Flow

The basic flow is:

```text
Application Input
       ↓
Prompt Template
       ↓
Final Prompt
       ↓
LLM
```

For example:

```text
User Input:
"Vector databases"

        ↓

Prompt Template:
"Explain the following topic..."

        ↓

Gemini

        ↓

Generated Explanation
```

---

# 🔗 LangChain Expression Language (LCEL)

LCEL allows LangChain components to be connected using the pipe operator:

```python
|
```

Example:

```python
chain = prompt | llm
```

This means:

```text
Prompt
  ↓
LLM
```

We can extend the chain:

```python
chain = prompt | llm | parser
```

which means:

```text
Prompt
  ↓
LLM
  ↓
Output Parser
```

---

# 🧩 Output Parsers

An LLM response is not always returned in the exact format an application wants.

An output parser transforms the model response into an application-friendly format.

General architecture:

```text
Prompt
  ↓
LLM
  ↓
Output Parser
  ↓
Application Output
```

---

# 🔹 StrOutputParser

`StrOutputParser` is useful when we want the LLM response as text.

Example:

```python
from langchain_core.output_parsers import StrOutputParser


parser = StrOutputParser()

chain = prompt | llm | parser
```

The result can then be used as text:

```python
response = chain.invoke({
    "topic": "Vector databases"
})
```

The application can treat the result as a string.

We verified:

```python
isinstance(response, str)
```

which returned:

```text
True
```

---

# 🧠 Why Use StrOutputParser?

Without an output parser:

```text
Prompt
  ↓
LLM
  ↓
AI Message
```

With `StrOutputParser`:

```text
Prompt
  ↓
LLM
  ↓
StrOutputParser
  ↓
String
```

This is useful for:

* Summaries
* Rewriting
* Explanations
* General text generation

---

# 📦 Structured Output

Free-form text is not always suitable for an application.

For example, suppose an AI system analyzes a support ticket.

Instead of:

```text
"This seems like a high priority technical issue..."
```

we may want:

```json
{
    "category": "technical_issue",
    "priority": "high",
    "summary": "User cannot access their laptop.",
    "sentiment": "frustrated"
}
```

Now the application can directly use each field.

---

# 🔹 Pydantic

Pydantic allows us to define a structured response model.

Example:

```python
from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):

    category: str = Field(
        description="The category of the customer issue"
    )

    priority: str = Field(
        description="The priority: low, medium, or high"
    )

    summary: str = Field(
        description="A short summary of the issue"
    )

    sentiment: str = Field(
        description="The customer's sentiment"
    )
```

This defines the expected structure of the AI response.

---

# 🔹 Gemini Structured Output

We used:

```python
structured_llm = llm.with_structured_output(
    TicketAnalysis
)
```

This connects Gemini's response to our Pydantic model.

The chain becomes:

```text
Prompt
  ↓
Gemini
  ↓
Structured Output
  ↓
TicketAnalysis
```

We can then access individual fields:

```python
response.category
```

```python
response.priority
```

```python
response.summary
```

```python
response.sentiment
```

---

# 🆚 StrOutputParser vs Structured Output

| Feature         | StrOutputParser            | Structured Output |
| --------------- | -------------------------- | ----------------- |
| Output          | Text                       | Structured data   |
| Best for        | General text               | Application data  |
| Schema          | No                         | Yes               |
| Pydantic        | No                         | Yes               |
| Classification  | Possible but less reliable | Better suited     |
| Data extraction | Not ideal                  | Excellent         |
| API workflows   | Limited                    | Very useful       |
| Agent workflows | Sometimes                  | Very useful       |

---

# 🏗️ AI Application Architecture

A basic AI application can follow:

```text
User Input
    ↓
Prompt Template
    ↓
LLM
    ↓
Output Parser
    ↓
Application
```

With structured output:

```text
User Input
    ↓
Prompt Template
    ↓
LLM
    ↓
Structured Output
    ↓
Pydantic Model
    ↓
Application
```

---

# 🛠️ Day 12 Project – AI Utility

We built a reusable AI Utility with four operations:

1. Summarize
2. Rewrite
3. Classify
4. Analyze Support Ticket

---

# 📁 Project Structure

```text
ai-utility/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── prompts.py
│   └── utility.py
│
├── main.py
├── ui.py
├── requirements.txt
├── .env
└── .gitignore
```

---

# 📄 models.py

The Pydantic model is stored separately:

```python
class TicketAnalysis(BaseModel):

    category: str
    priority: str
    summary: str
    sentiment: str
```

This represents the expected AI response structure.

---

# 📄 prompts.py

Reusable prompt templates were created for different operations.

Example:

```python
summarize_prompt = ChatPromptTemplate.from_template(
    """
    Summarize the following text clearly and concisely.

    Text:
    {text}
    """
)
```

Similarly, we created:

```python
rewrite_prompt
```

and:

```python
classify_prompt
```

This keeps prompt definitions separate from the application logic.

---

# 📄 utility.py

The `AIUtility` class contains the actual AI functionality.

Conceptually:

```text
AIUtility
    │
    ├── summarize()
    │
    ├── rewrite()
    │
    ├── classify()
    │
    └── analyze_ticket()
```

This creates a reusable AI service layer.

---

# 🔹 Summarization

The summarization chain uses:

```text
Summarize Prompt
      ↓
Gemini
      ↓
StrOutputParser
      ↓
String
```

---

# 🔹 Rewrite

The rewrite operation uses:

```text
Rewrite Prompt
      ↓
Gemini
      ↓
StrOutputParser
      ↓
String
```

It can transform informal text into professional text while preserving the original meaning.

---

# 🔹 Classification

The classification operation asks Gemini to select from predefined categories:

```text
technical_issue
billing
account
general
other
```

Architecture:

```text
Input
 ↓
Classification Prompt
 ↓
Gemini
 ↓
StrOutputParser
 ↓
Category
```

---

# 🔹 Support Ticket Analysis

This operation uses structured output.

Architecture:

```text
Customer Message
       ↓
Prompt
       ↓
Gemini
       ↓
Pydantic Structured Output
       ↓
TicketAnalysis
```

The resulting fields are:

```text
category
priority
summary
sentiment
```

---

# 🌐 Streamlit UI

We added a basic browser UI using Streamlit.

The application allows the user to choose:

```text
Summarize
Rewrite
Classify
Analyze Support Ticket
```

The user enters text and clicks:

```text
Run AI
```

The UI then displays the result.

---

# 🖥️ UI Architecture

```text
                Streamlit UI
                     │
                     ↓
                 AIUtility
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      Summarize   Rewrite    Classify
          │          │          │
          └──────────┼──────────┘
                     ↓
                   Gemini
                     │
                     ↓
               AI Response
```

For structured ticket analysis:

```text
Streamlit
   ↓
AIUtility
   ↓
Prompt
   ↓
Gemini
   ↓
Pydantic
   ↓
TicketAnalysis
   ↓
UI
```

---

# 🛡️ Basic Error Handling

We added error handling around the AI execution:

```python
try:
    ...
except Exception as error:
    st.error(
        "Something went wrong while processing your request."
    )
    st.exception(error)
```

This prevents the UI from simply crashing when an unexpected error occurs.

We also validate empty input:

```python
if not text.strip():
    st.warning("Please enter some text first.")
```

---

# 🧠 Separation of Concerns

One of the most important engineering lessons from this project is separating the UI from AI logic.

The UI should not directly contain:

```python
ChatGoogleGenerativeAI(...)
```

or:

```python
ChatPromptTemplate(...)
```

Instead:

```text
UI
 ↓
AIUtility
 ↓
LangChain
 ↓
Gemini
```

This makes the application easier to:

* Test
* Maintain
* Extend
* Debug
* Deploy

---

# 🔥 AI Demo vs AI Application

A simple AI demo might look like:

```python
question = input("Ask something: ")

response = llm.invoke(question)

print(response)
```

This proves that the model works.

Our Day 12 project goes further:

```text
User
 ↓
UI
 ↓
Application Logic
 ↓
Prompt Template
 ↓
LLM
 ↓
Parser / Structured Output
 ↓
Application Result
 ↓
UI
```

This is closer to actual AI application engineering.

---

# 🌎 Real-World Applications

The concepts learned today are used in:

### Customer Support

```text
Message
 ↓
Classification
 ↓
Priority
 ↓
Ticket Routing
```

### Document Processing

```text
Document
 ↓
LLM
 ↓
Structured Data
 ↓
Database
```

### Email Automation

```text
Email
 ↓
Classification
 ↓
Summarization
 ↓
Action
```

### AI Agents

```text
User Request
 ↓
LLM
 ↓
Structured Decision
 ↓
Tool
```

### Enterprise AI

```text
User
 ↓
AI Application
 ↓
Structured Output
 ↓
Business System
```

---

# 📌 Key Components

| Component          | Purpose                                   |
| ------------------ | ----------------------------------------- |
| ChatPromptTemplate | Creates reusable prompts                  |
| Dynamic Variables  | Allows prompts to accept different inputs |
| LCEL               | Connects LangChain components             |
| StrOutputParser    | Converts model output into text           |
| Pydantic           | Defines structured response schemas       |
| Structured Output  | Produces predictable application data     |
| Gemini             | LLM used for generation                   |
| Streamlit          | Provides the basic web UI                 |
| AIUtility          | Encapsulates AI functionality             |

---

# 🎯 Key Takeaways

1. Prompt templates make prompts reusable.
2. Dynamic variables allow applications to handle different inputs.
3. LCEL allows components to be composed using `|`.
4. Output parsers convert model output into application-friendly formats.
5. `StrOutputParser` is useful for text responses.
6. Structured output is better when applications need predictable fields.
7. Pydantic provides a clear schema for structured AI responses.
8. AI logic should be separated from the UI.
9. Error handling is important in AI applications.
10. Structured outputs are particularly useful for automation, APIs, and agents.

---

# 🎤 Interview Corner

### Q1. What is a PromptTemplate?

A PromptTemplate is a reusable prompt containing variables that can be dynamically populated at runtime.

---

### Q2. What is LCEL?

LCEL stands for LangChain Expression Language.

It provides a way to compose LangChain components into pipelines.

Example:

```python
chain = prompt | llm | parser
```

---

### Q3. What does the `|` operator mean in LangChain?

It connects components so that the output of one component becomes the input of the next component.

Example:

```text
Prompt
 ↓
LLM
 ↓
Parser
```

---

### Q4. Why use an Output Parser?

An output parser converts the LLM response into a format that is easier for the application to consume.

---

### Q5. What is the difference between StrOutputParser and Structured Output?

`StrOutputParser` is mainly used when the application needs a text response.

Structured Output is used when the application needs predictable fields and a defined schema.

---

### Q6. Why use Pydantic?

Pydantic allows us to define the expected structure and fields of application data.

Example:

```python
class TicketAnalysis(BaseModel):
    category: str
    priority: str
    summary: str
    sentiment: str
```

---

### Q7. Why separate UI and AI logic?

Separation of concerns makes the system easier to test, maintain, debug, extend, and deploy.

---

### Q8. When should you use structured output?

Use it when the AI response needs to be consumed programmatically.

Examples:

* Classification
* Data extraction
* API responses
* Database records
* Agent decisions
* Workflow automation

---

# 💡 Practical Interview Scenario

### Interviewer:

You are building a customer support application. A user submits:

```text
"My account has been locked and I can't access my data.
I've already tried resetting my password."
```

How would you design the AI component?

### Answer:

I would create a reusable prompt template and ask the LLM to return structured output.

For example:

```text
Input
 ↓
Prompt Template
 ↓
LLM
 ↓
Structured Output
 ↓
Pydantic Model
```

The Pydantic model could contain:

```text
category
priority
summary
sentiment
```

The application can then use those fields to route the ticket or display it in a dashboard.

---

# 🚀 Project Completed

## AI Utility

The Day 12 project demonstrates:

* Prompt Templates
* Dynamic prompts
* LCEL
* Gemini
* StrOutputParser
* Structured Outputs
* Pydantic
* Modular AI architecture
* Streamlit
* Basic validation
* Error handling

The application supports:

```text
📝 Summarize
✍️ Rewrite
🏷️ Classify
🎫 Analyze Support Ticket
```

---

# 📊 Day 12 Summary

Today we moved from:

```text
Simple LLM Calls
```

to:

```text
Reusable AI Components
```

The core pattern learned was:

```text
Prompt Template
       ↓
      LLM
       ↓
Output Parser
       ↓
Application
```

And for structured applications:

```text
Prompt Template
       ↓
      LLM
       ↓
Structured Output
       ↓
Pydantic Model
       ↓
Application
```

This is an important step toward building production-oriented AI applications.

---

# 🔮 Next Step

## Day 13 – Memory in AI Applications

Next we will learn how AI applications maintain conversational context.

We will build:

```text
User
 ↓
Message 1
 ↓
AI
 ↓
Message 2
 ↓
AI + Previous Context
 ↓
Message 3
 ↓
AI + Conversation History
```

Project:

**💬 Chat Memory Demo**

Topics will include:

* Conversation history
* Short-term memory
* Message storage
* Context management
* Memory patterns in LangChain
* Building a conversational AI application

```
```
