# 🚀 AI Engineer Bootcamp

# Sprint 2 – AI Application Engineering

# 📅 Day 13 – Memory in AI Applications

---

## 🎯 Today’s Goal

Understand how conversational AI applications maintain context across multiple interactions.

Today we learned:

- Conversation history
    
- LLM statelessness
    
- HumanMessage and AIMessage
    
- Application-managed memory
    
- Short-term memory
    
- Session-based memory
    
- Memory size management
    
- Context-window limitations
    
- Memory vs persistent memory
    
- Memory vs RAG
    
- Streamlit session state
    
- Building a conversational AI application
    

---

# 🧠 What is Memory in an AI Application?

An LLM does not automatically remember previous requests.

For example:

```text
User:
My name is Sai.

AI:
Nice to meet you!

User:
What is my name?
```

The application needs to provide the previous conversation as context.

Conceptually:

```text
User Message
     ↓
Conversation History
     ↓
Prompt / Context
     ↓
LLM
     ↓
Response
     ↓
Conversation History Updated
```

> **LLM memory is usually application-managed context.**

---

# 1️⃣ Stateless LLM

A normal LLM invocation is independent:

```python
response = llm.invoke(
    "My name is Sai"
)
```

A later request:

```python
response = llm.invoke(
    "What is my name?"
)
```

doesn't inherently know about the previous request.

Conceptually:

```text
Request 1
   ↓
LLM
   ↓
Response 1

Request 2
   ↓
LLM
   ↓
Response 2
```

The application needs to maintain the state.

---

# 2️⃣ Conversation Memory

Conversation memory provides the model with previous messages.

Example:

```text
System:
You are a helpful AI assistant.

User:
My name is Sai.

Assistant:
Nice to meet you, Sai!

User:
What is my name?
```

The model can answer the final question because the relevant conversation history is included in the request.

Architecture:

```text
Conversation
     ↓
Memory
     ↓
Prompt / Context
     ↓
LLM
     ↓
Response
```

---

# 3️⃣ LangChain Message Types

LangChain provides different message types for conversations.

## HumanMessage

Represents the user's message.

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(
    content="My name is Sai."
)
```

## AIMessage

Represents the assistant's response.

```python
from langchain_core.messages import AIMessage

message = AIMessage(
    content="Nice to meet you, Sai!"
)
```

## SystemMessage

Defines system-level behavior or instructions.

```python
from langchain_core.messages import SystemMessage

message = SystemMessage(
    content="You are a helpful AI assistant."
)
```

A conversation can therefore look like:

```text
SystemMessage
      ↓
HumanMessage
      ↓
AIMessage
      ↓
HumanMessage
      ↓
AIMessage
```

---

# 4️⃣ Basic Conversation History

The simplest implementation is a Python list:

```python
history = []
```

Add messages:

```python
history.append(
    HumanMessage(
        content="My name is Sai."
    )
)

history.append(
    AIMessage(
        content="Nice to meet you, Sai!"
    )
)
```

Then pass the history to the LLM:

```python
response = llm.invoke(history)
```

The model now receives the previous conversation.

---

# 5️⃣ Building a ChatMemory Class

Instead of manually managing the history everywhere, we created a reusable abstraction.

```python
class ChatMemory:
    def __init__(self, max_messages: int = 10):
        self.history = []
        self.max_messages = max_messages
```

The class provides methods for:

```text
add_user_message()
add_ai_message()
get_history()
clear()
```

This gives us separation of concerns.

```text
main.py
   ↓
ChatMemory
   ↓
Conversation History
```

The application doesn't need to know how the history is internally stored.

---

# 6️⃣ Short-Term Memory

Our implementation provides **short-term conversational memory**.

Example:

```text
User:
I'm building a Python application.

AI:
Great!

User:
It uses FastAPI.

AI:
Nice.

User:
What framework did I say I was using?

AI:
You said FastAPI.
```

The application remembers information from the current conversation.

Useful for:

- Chatbots
    
- Customer-support assistants
    
- Coding assistants
    
- Research assistants
    
- AI copilots
    
- Personal assistants
    

---

# 7️⃣ Memory Size Management

Keeping every message forever is inefficient.

For example:

```text
Message 1
Message 2
Message 3
...
Message 500
Message 501
```

Sending the entire history every time can cause:

```text
More messages
     ↓
More tokens
     ↓
Higher cost
     ↓
Higher latency
     ↓
Context-window limitations
```

Therefore, we implemented a maximum history size.

Example:

```python
memory = ChatMemory(
    max_messages=10
)
```

When the history exceeds the limit, older messages are removed.

Conceptually:

```text
Old Messages
     ↓
Removed

Recent Messages
     ↓
Retained
```

---

# 8️⃣ Recent-Message Memory

Our trimming logic keeps the most recent messages:

```python
def _trim_history(self):
    if len(self.history) > self.max_messages:
        self.history = self.history[-self.max_messages:]
```

For example, if the maximum is 4:

```text
Message 1
Message 2
Message 3
Message 4
Message 5
Message 6
```

the retained history becomes:

```text
Message 3
Message 4
Message 5
Message 6
```

This reduces context size.

---

# ⚠️ 9️⃣ The Problem With Simple Trimming

Recent-message memory can lose important information.

Example:

```text
User:
My project is called Atlas.

...

40 messages later...

User:
What is my project called?
```

If the original message has already been removed, the model cannot answer from the conversation history.

Therefore, production systems often need more sophisticated memory strategies.

---

# 🧠 1️⃣0️⃣ Summarization Memory

Instead of simply deleting old messages, we can summarize older conversation content.

For example:

```text
Conversation Summary:

The user is building a project called Atlas.
The user is learning AI Engineering.
The user is using Python and LangChain.
```

Then combine:

```text
Conversation Summary
        +
Recent Messages
        ↓
Context
        ↓
LLM
```

Conceptually:

```text
┌─────────────────────────┐
│ Conversation Summary    │
└────────────┬────────────┘
             │
             +
             │
┌────────────▼────────────┐
│ Recent Messages         │
└────────────┬────────────┘
             │
             ▼
            LLM
```

We did not implement summarization in today's project. We focused on understanding the concept and implementing recent-message memory.

---

# 🧩 1️⃣1️⃣ Memory Hierarchy

AI applications can use different forms of memory:

```text
                    AI Memory
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Recent       Summary      Persistent
       Messages     Memory        Memory
          │            │            │
          ▼            ▼            ▼
       Current      Compressed    Database /
       Context      Context       Vector DB
```

### Recent Messages

Useful for:

> "What did I just say?"

### Summary Memory

Useful for:

> "What have we discussed during this conversation?"

### Persistent Memory

Useful for:

> "What do you know about this user from previous sessions?"

---

# 🗄️ 1️⃣2️⃣ Persistent Memory

Our current memory exists only during the application session.

If the application restarts, the conversation is lost.

Persistent memory stores information outside the running application.

Conceptually:

```text
User
 ↓
Application
 ↓
Database
 ↓
Persistent Memory
```

Potential technologies include:

- PostgreSQL
    
- Redis
    
- Other databases
    

Example:

```text
User Profile
-------------------------
Name: Sai
Role: AI Engineer
Project: AI Research Assistant
```

We will revisit persistent storage later when we work with PostgreSQL.

---

# 📚 1️⃣3️⃣ Memory vs RAG

Memory and RAG solve different problems.

### Conversation Memory

Maintains conversational state.

```text
Conversation
     ↓
Memory
     ↓
LLM
```

Example:

> "What did I just tell you?"

---

### RAG

Retrieves relevant external knowledge.

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retriever
    ↓
Relevant Context
    ↓
LLM
```

Example:

> "What is our company's WFH policy?"

---

# 🔥 1️⃣4️⃣ Memory vs Persistent Memory vs RAG

|Feature|Conversation Memory|Persistent Memory|RAG|
|---|---|---|---|
|Purpose|Current conversation|Long-term information|External knowledge retrieval|
|Example|"What did I just say?"|"What is my project?"|"What is our leave policy?"|
|Lifetime|Session|Long-term|Long-term|
|Storage|Application/session state|Database|Vector DB / Search|
|Main Data|Messages|User/application information|Documents|
|Retrieval|Conversation history|Database lookup|Semantic / keyword retrieval|

---

# 🧠 1️⃣5️⃣ Production AI Applications Can Use All Three

A production AI assistant may combine:

```text
                         User
                          │
                          ▼
                    AI Application
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        Conversation   Persistent     RAG
           Memory        Memory     Retrieval
              │           │           │
              ▼           ▼           ▼
          Current      User Data   Documents
          Context      Database    Vector DB
              │           │           │
              └───────────┼───────────┘
                          ▼
                    Context Builder
                          │
                          ▼
                         LLM
                          │
                          ▼
                       Response
```

This is an important AI application architecture pattern.

---

# 🌐 1️⃣6️⃣ Streamlit Session State

For the UI, we used Streamlit.

Streamlit reruns the Python script when the user interacts with the application.

Therefore, simply creating:

```python
memory = ChatMemory()
```

inside the script isn't sufficient for maintaining UI session state.

We used:

```python
st.session_state
```

to maintain state for the current Streamlit session.

Conceptually:

```text
Streamlit UI
      ↓
st.session_state
      ↓
ChatService
      ↓
ChatMemory
      ↓
Gemini
```

---

# 🏗️ 1️⃣7️⃣ Project Architecture

Our Day 13 application follows a modular structure:

```text
ai-chat-memory/
│
├── app/
│   ├── __init__.py
│   ├── memory.py
│   └── chat.py
│
├── main.py
├── ui.py
├── requirements.txt
├── .env
└── .gitignore
```

### `memory.py`

Responsible for:

- Conversation history
    
- Adding messages
    
- Retrieving history
    
- Clearing memory
    
- Limiting history size
    

### `chat.py`

Responsible for:

- Gemini initialization
    
- Chat execution
    
- Connecting memory to the LLM
    

### `ui.py`

Responsible for:

- Streamlit interface
    
- Displaying messages
    
- User input
    
- Session state
    
- Clearing the conversation
    

### `main.py`

Used for testing the conversational memory independently from the UI.

---

# 🔄 1️⃣8️⃣ Complete Data Flow

```text
                    User
                     │
                     ▼
                Streamlit UI
                     │
                     ▼
                ChatService
                     │
                     ▼
                 ChatMemory
                     │
                     ▼
            Conversation History
                     │
                     ▼
                  Gemini
                     │
                     ▼
                AI Response
                     │
                     ▼
                 ChatMemory
                     │
                     ▼
                Streamlit UI
```

---

# 🧪 1️⃣9️⃣ Testing Memory

We tested multi-turn conversations such as:

```text
User:
My name is Sai.

User:
I'm learning AI Engineering.

User:
What is my name?

AI:
Your name is Sai.

User:
What am I learning?

AI:
You are learning AI Engineering.
```

We also tested:

### Clear Conversation

After clearing memory:

```text
User:
What is my name?
```

The assistant should no longer know the answer from the previous conversation.

This confirms that the session memory was successfully cleared.

---

# ⚠️ 2️⃣0️⃣ Current Project Limitations

Our implementation is intentionally simple.

Current limitations:

- Memory exists only during the session
    
- No database persistence
    
- No long-term user memory
    
- No conversation summarization
    
- No semantic retrieval of old conversations
    
- Recent-message trimming can lose older information
    

These are concepts we'll revisit later as the bootcamp moves toward production AI systems.

---

# 🧠 AI Engineering Insight

The important question isn't:

> "Does the AI have memory?"

A better AI Engineering question is:

> **"What information should the model see, how much should it see, where should that information come from, and how long should it be retained?"**

This leads to four important concerns:

```text
Information
    ↓
Context
    ↓
Memory Management
    ↓
LLM
```

---

# 🏢 Real-World Applications

Conversation memory is commonly useful in:

- Customer support
    
- AI copilots
    
- Coding assistants
    
- Research assistants
    
- Personal assistants
    
- Enterprise chat applications
    
- Workflow assistants
    
- Agentic AI systems
    

---

# 📊 Key Components

|Component|Purpose|
|---|---|
|`HumanMessage`|Represents user input|
|`AIMessage`|Represents AI response|
|`SystemMessage`|Defines system behavior|
|`ChatMemory`|Manages conversation history|
|`st.session_state`|Maintains Streamlit session state|
|Gemini|Generates AI responses|
|Recent-message memory|Controls context size|
|Persistent memory|Stores information across sessions|
|RAG|Retrieves external knowledge|

---

# 🔑 Key Takeaways

1. LLMs are generally stateless between requests.
    
2. AI applications can implement memory by managing conversation context.
    
3. LangChain provides message abstractions such as `HumanMessage` and `AIMessage`.
    
4. Conversation history can be passed back to the LLM.
    
5. Memory increases context size and therefore affects cost and latency.
    
6. Recent-message memory can control context size.
    
7. Simple trimming can cause important information to be lost.
    
8. Summarization can preserve important information while reducing context.
    
9. Persistent memory is different from conversation memory.
    
10. RAG retrieves external knowledge and is different from conversational memory.
    
11. Streamlit `session_state` helps maintain state during a user session.
    
12. Production AI systems may combine conversation memory, persistent memory, and RAG.
    

---

# 🎤 Interview Corner

### Q1. Are LLMs stateful?

Generally, an LLM does not automatically maintain state between independent requests.

The application usually manages the required conversation context and sends it with subsequent requests.

---

### Q2. How would you implement memory in a chatbot?

I would maintain conversation history and provide the relevant messages to the LLM for each new request.

For longer conversations, I would consider message limits, summarization, or retrieval-based memory to control context size.

---

### Q3. Why can't we keep the entire conversation forever?

Because the conversation consumes tokens.

As history grows:

```text
More History
     ↓
More Tokens
     ↓
Higher Cost
     ↓
Higher Latency
     ↓
Context Limit
```

---

### Q4. What's the difference between memory and RAG?

Memory maintains conversational or user-specific context, while RAG retrieves relevant information from an external knowledge source.

---

### Q5. How would you design memory for a production chatbot?

A possible architecture would be:

```text
Recent Messages
       +
Conversation Summary
       +
Relevant Persistent Memory
       ↓
Context Builder
       ↓
LLM
```

The exact design depends on the application's requirements, cost constraints, and data-retention needs.

---

# 💼 Practical Interview Scenario

### Question

> A customer-support chatbot has a 200-message conversation. Sending the entire conversation to the LLM on every request is becoming expensive. What would you do?

### Strong Answer

I would avoid blindly sending the entire conversation on every request.

I could combine:

```text
Recent Messages
       +
Conversation Summary
       +
Relevant Persistent Information
       ↓
Context Construction
       ↓
LLM
```

I would also monitor:

- Token usage
    
- Latency
    
- Cost
    
- Answer quality
    
- Context relevance
    

The goal is to preserve the information necessary for a good response while minimizing unnecessary context.

---

# 🚀 Project Completed

## 💬 AI Chat Memory

We built a conversational AI application using:

```text
Streamlit
     +
LangChain
     +
Gemini
     +
Custom ChatMemory
     +
Session State
```

### Features

```text
✅ Multi-turn conversation
✅ Conversation history
✅ Short-term memory
✅ Memory size control
✅ Session-based memory
✅ Clear conversation
✅ Streamlit chat interface
✅ Modular architecture
```

---

# 📅 Day 13 Summary

Today we moved from:

```text
Question
   ↓
LLM
   ↓
Answer
```

to:

```text
Conversation
      ↓
Memory
      ↓
Context
      ↓
LLM
      ↓
Response
      ↓
Memory
```

The biggest concept to remember:

> **Memory isn't magic. It's context management.**

An AI Engineer needs to decide:

- What information should the model see?
    
- How much information should it see?
    
- Where should that information come from?
    
- How long should it be retained?
    
- How can context be managed efficiently?
    

---

# ➡️ Next Step

## Day 14 — Tool Calling

We'll move from:

```text
LLM
 ↓
Generate Response
```

to:

```text
User
 ↓
LLM
 ↓
Choose Tool
 ↓
Execute Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final Response
```

### Project

🧮 **AI Calculator**

We'll learn how AI systems can move beyond generating text and start interacting with external capabilities.

---
