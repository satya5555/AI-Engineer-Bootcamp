# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 9 – Retrieval-Augmented Generation (RAG)

---

# 🎯 Today's Goal

Today's objective was to understand and build a complete Retrieval-Augmented Generation (RAG) pipeline.

We combined:

- Embeddings
- ChromaDB
- Semantic Retrieval
- Context Construction
- Gemini
- Prompt Engineering

to create an AI Knowledge Assistant capable of answering questions using a private knowledge base.

---

# 🧠 What is RAG?

RAG stands for:

**Retrieval-Augmented Generation**

It combines three concepts:

```text
Retrieval
+
Augmentation
+
Generation
=
RAG
```

---

# 🔎 Retrieval

Retrieval means finding relevant information from an external knowledge source.

In our application:

```text
User Question
      ↓
ChromaDB
      ↓
Relevant Documents
```

---

# ➕ Augmentation

The retrieved information is added to the LLM's prompt as context.

```text
User Question
      +
Retrieved Context
      ↓
LLM Prompt
```

---

# ✍️ Generation

The LLM uses the provided context to generate a natural-language answer.

```text
Context + Question
       ↓
Gemini
       ↓
Answer
```

---

# 🏗️ Complete RAG Architecture

```text
                 User Question
                       │
                       ▼
                Query Embedding
                       │
                       ▼
                   ChromaDB
                       │
                       ▼
                Relevant Chunks
                       │
                       ▼
               Context Construction
                       │
                       ▼
                 Prompt + Context
                       │
                       ▼
                    Gemini
                       │
                       ▼
                  Final Answer
```

---

# ❓ Why Do We Need RAG?

LLMs may not know:

- Private company information
- Internal policies
- Recently created documents
- Organization-specific procedures
- Proprietary knowledge

Instead of retraining the model, we can retrieve relevant information and provide it as context.

---

# 🧠 RAG vs Normal LLM

## Normal LLM

```text
Question
   ↓
LLM
   ↓
Answer
```

## RAG

```text
Question
   ↓
Retrieve Knowledge
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

---

# 📚 Our Knowledge Base

We created:

```text
knowledge_base.txt
```

It contained:

- Company Working Hours
- Work From Home Policy
- Leave Policy
- IT Support
- Security Policy
- Employee Benefits
- Performance Reviews

---

# ✂️ Chunking

Initially we stored the entire knowledge base as one document.

```text
7 Policies
    ↓
1 Document
```

This was not ideal.

We then split the knowledge base into individual sections.

```text
Knowledge Base
      ↓
Chunking
      ↓
Working Hours
WFH Policy
Leave Policy
IT Support
Security
Benefits
Performance Reviews
```

---

# 🔥 Why Chunking Matters

Large documents are difficult to retrieve efficiently.

Instead of retrieving:

```text
Entire Company Knowledge Base
```

we retrieve:

```text
Relevant Section
```

For example:

Question:

```text
How many days can I work from home?
```

Retrieved chunk:

```text
Work From Home Policy
```

This reduces unnecessary context sent to the LLM.

---

# 🗄️ ChromaDB

ChromaDB acts as our vector database.

It stores:

```text
Documents
+
Embeddings
+
IDs
+
Metadata
```

and allows semantic retrieval.

---

# 🔎 Retrieval

We queried ChromaDB using:

```python
results = collection.query(
    query_texts=[question],
    n_results=2
)
```

The retrieved chunks become the context for the LLM.

---

# 📐 Retrieval Distance

ChromaDB can return distances between the query and retrieved vectors.

Conceptually:

```text
Smaller Distance
       ↓
More Similar
       ↓
More Relevant
```

---

# 🧩 Context Construction

Multiple retrieved chunks can be combined:

```python
context_text = "\n\n".join(context)
```

The resulting context is then added to the prompt.

---

# 🤖 Gemini

Gemini acts as the **generation component** of our RAG system.

We used:

```text
gemini-2.5-flash
```

The LLM receives:

```text
Question
+
Retrieved Context
```

and generates the answer.

---

# 📝 RAG Prompt

Our prompt instructed Gemini to:

- Use only the provided context
- Avoid outside knowledge
- Avoid inventing information
- Clearly state when information is unavailable
- Keep answers concise

This helps reduce hallucination.

---

# 🚫 Hallucination Test

We asked:

```text
What is the company's maternity leave policy?
```

The knowledge base did not contain this information.

The expected behavior was:

```text
I don't have enough information in the provided knowledge base.
```

The system should not invent an answer.

---

# 🧱 Project Structure

```text
rag-knowledge-assistant/
│
├── .venv/
├── .env.local
├── .gitignore
├── chroma_db/
├── knowledge_base.txt
├── ingest.py
├── retrieve.py
├── generate.py
└── main.py
```

---

# 🔄 Complete Data Flow

```text
knowledge_base.txt
        ↓
Chunking
        ↓
Embeddings
        ↓
ChromaDB
        ↓
        User Question
              ↓
         Query Embedding
              ↓
           ChromaDB
              ↓
       Relevant Chunks
              ↓
      Prompt + Context
              ↓
            Gemini
              ↓
           Answer
```

---

# 🛠️ Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- Google Gemini API
- Google GenAI SDK
- python-dotenv

---

# 🌍 Real-World Applications

RAG is useful for:

- Enterprise Knowledge Assistants
- Internal Company Search
- Customer Support
- Documentation Assistants
- HR Assistants
- Legal Document Search
- Technical Support
- Healthcare Knowledge Systems
- Product Documentation

---

# 🧠 Key RAG Components

| Component | Role |
|---|---|
| Knowledge Base | Source of information |
| Chunking | Breaks large documents into smaller pieces |
| Embeddings | Represents semantic meaning |
| Vector Database | Stores and retrieves vectors |
| Retriever | Finds relevant chunks |
| Context | Information provided to LLM |
| Prompt | Controls LLM behavior |
| LLM | Generates final answer |

---

# 🎯 Key Takeaways

- RAG allows LLMs to use external knowledge.
- Retrieval happens before generation.
- Vector databases are commonly used for retrieval.
- Chunking improves retrieval quality.
- Retrieved context is added to the LLM prompt.
- Good prompts can constrain the model to retrieved information.
- RAG can reduce hallucination by grounding responses in external context.
- RAG does not require retraining the LLM for every new document.

---

# 🎯 Interview Corner

## Q1. What is RAG?

RAG stands for Retrieval-Augmented Generation. It retrieves relevant external information and provides it to an LLM as context before generating an answer.

---

## Q2. Why use RAG instead of fine-tuning?

RAG allows external or frequently changing information to be updated without retraining the model. Documents can be updated in the knowledge base independently of the LLM.

---

## Q3. What is the role of a vector database in RAG?

The vector database stores embeddings and retrieves documents that are semantically similar to the user's query.

---

## Q4. What is chunking?

Chunking is the process of splitting large documents into smaller pieces so that relevant sections can be retrieved and provided as context to the LLM.

---

## Q5. What is grounding?

Grounding means generating an answer based on retrieved external information rather than relying only on the model's internal knowledge.

---

## Q6. What happens if retrieval returns irrelevant documents?

The generated answer may become inaccurate. Retrieval quality is therefore a critical part of a RAG system.

---

# 🧪 Practical Interview Scenario

### Interviewer:

Your company has thousands of internal documents. Employees want to ask questions about company policies.

How would you build the system?

### Expected Answer:

I would create a RAG pipeline. First, I would process and chunk the company documents. Then I would generate embeddings and store them in a vector database such as ChromaDB. When a user asks a question, I would generate an embedding for the query, retrieve the most relevant chunks, construct a prompt containing the retrieved context and the question, and send it to an LLM such as Gemini to generate a grounded answer.

---

# 🏆 Project Completed

## RAG Knowledge Assistant

Features:

- ✅ Knowledge Base
- ✅ Document Chunking
- ✅ Embeddings
- ✅ ChromaDB
- ✅ Semantic Retrieval
- ✅ Context Construction
- ✅ Gemini Integration
- ✅ Grounded Generation
- ✅ Hallucination Fallback
- ✅ Interactive Questions

---

# 🚀 Day 9 Summary

Day 7 introduced embeddings.

Day 8 introduced vector databases.

Day 9 connected retrieval with generation.

The progression is:

```text
Day 7
Embeddings
     ↓
Semantic Search

Day 8
Embeddings
     ↓
ChromaDB
     ↓
Vector Search

Day 9
Question
     ↓
ChromaDB
     ↓
Relevant Context
     ↓
Gemini
     ↓
Grounded Answer
```

This is the fundamental architecture behind many modern AI knowledge assistants.

---

# 🚀 Next Step

## Day 10 – AI Knowledge Assistant

The next step is to turn our basic RAG pipeline into a more polished AI application.

We'll focus on:

- Conversation experience
- Better document handling
- Source/reference display
- Retrieval quality
- Better error handling
- Application structure

The goal is to move from:

```text
RAG Demo
```

to:

```text
AI Knowledge Assistant
```