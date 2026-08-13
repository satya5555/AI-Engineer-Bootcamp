````
# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 10 – AI Knowledge Assistant

---

# 🎯 Today's Goal

Today's objective was to transform our basic RAG pipeline into a complete AI Knowledge Assistant.

We combined:

- RAG
- ChromaDB
- Semantic Retrieval
- Gemini
- FastAPI
- Next.js
- Source Display
- Grounded Generation

to build a web-based AI application capable of answering questions using a private knowledge base.

---

# 🧠 From RAG Demo to AI Application

In Day 9, we built the core RAG pipeline:

```text
Question
   ↓
ChromaDB
   ↓
Relevant Context
   ↓
Gemini
   ↓
Answer
````

Today we added an application layer around it:

```
User
 ↓
Next.js UI
 ↓
FastAPI
 ↓
RAG Pipeline
 ↓
ChromaDB + Gemini
 ↓
Answer + Sources
 ↓
Next.js UI
```

---

# 🏗️ Complete Application Architecture

```
                     User
                       │
                       ▼
                 Next.js UI
                       │
                       ▼
                    FastAPI
                       │
                       ▼
                 RAG Pipeline
                  /        \
                 ▼          ▼
            ChromaDB      Gemini
                 ▲
                 │
           Knowledge Base
```

---

# 📚 Knowledge Base

Our knowledge base contains company-related information.

Location:

```
backend/data/knowledge_base.txt
```

It contains information such as:

- Company Working Hours
- Work From Home Policy
- Leave Policy
- IT Support
- Security Policy
- Employee Benefits
- Performance Reviews

The knowledge base is divided into meaningful chunks before being stored in ChromaDB.

---

# 🔎 RAG Pipeline

The RAG logic is separated into different components.

```
Question
   ↓
Retriever
   ↓
ChromaDB
   ↓
Relevant Chunks
   ↓
Context Construction
   ↓
Generator
   ↓
Gemini
   ↓
Answer
```

### Retriever

Responsible for finding relevant information from ChromaDB.

```
backend/app/retriever.py
```

### Generator

Responsible for sending the question and retrieved context to Gemini.

```
backend/app/generator.py
```

### RAG Pipeline

Connects retrieval and generation.

```
backend/app/rag.py
```

---

# 📏 Retrieval Quality

During testing, we observed that the top retrieved documents are not always guaranteed to contain the answer.

For example:

```
Question:
What is the company's maternity leave policy?

        ↓

ChromaDB

        ↓

Retrieved Documents
```

ChromaDB may return the closest available documents even if the required information is not actually present.

Therefore:

```
Top-K Results
      ≠
Guaranteed Relevant Answer
```

This shows why retrieval quality is an important part of a RAG system.

Future improvements can include:

- Relevance thresholds
- Reranking
- Hybrid search
- Better chunking
- Retrieval evaluation

---

# 🤖 Gemini

Gemini acts as the generation component of our RAG system.

We used:

```
gemini-2.5-flash
```

Gemini receives:

```
User Question
      +
Retrieved Context
```

and generates the final answer.

---

# 📝 Grounded Generation

Our prompt instructs Gemini to:

- Use only the provided context
- Avoid outside knowledge
- Avoid inventing information
- Clearly state when information is unavailable
- Keep answers concise

Fallback response:

```
I don't have enough information in the provided knowledge base.
```

This helps reduce unsupported answers and hallucination.

---

# 🚫 Hallucination Test

We tested:

```
What is the company's maternity leave policy?
```

The knowledge base did not contain enough information to answer the question.

The system returned:

```
I don't have enough information in the provided knowledge base.
```

This confirmed that the system can avoid generating an unsupported answer when the required information is not available.

---

# 🌐 FastAPI

We introduced FastAPI to expose the RAG system through an API.

Main endpoint:

```
POST /ask
```

Example request:

```
{
  "question": "What is the work from home policy?"
}
```

The processing flow is:

```
Frontend
   ↓
POST /ask
   ↓
FastAPI
   ↓
RAG Pipeline
   ↓
ChromaDB
   ↓
Retrieved Context
   ↓
Gemini
   ↓
Answer
   ↓
FastAPI Response
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# 🎨 Next.js UI

Previously our RAG project was mainly console-based.

Today we added a basic UI so that the project can be demonstrated as a proper mini-project.

The frontend provides:

- Question input
- Ask AI button
- Loading state
- AI answer
- Retrieved sources
- Retrieval distance
- Error handling

Frontend:

```
http://localhost:3000
```

---

# 📚 Source Display

The UI displays the retrieved sources along with the generated answer.

Example:

```
🤖 AI Answer

Employees can work from home up to two days per week
with prior approval from their manager.

📚 Retrieved Sources

Source 1
Work From Home Policy

Distance: 0.1837
```

Displaying sources helps with:

- Transparency
- Debugging
- Retrieval evaluation
- Understanding the generated answer

---

# 🧪 Testing

## Test 1 – Known Information

Question:

```
What is the work from home policy?
```

Result:

```
Employees can work from home up to two days per week with
prior approval from their manager. Employees working remotely
must remain available during standard working hours and attend
scheduled meetings.
```

Result:

- ✅ Retrieval working
- ✅ Gemini generation working
- ✅ Grounded answer
- ✅ Source displayed

---

## Test 2 – Unknown Information

Question:

```
What is the company's maternity leave policy?
```

Result:

```
I don't have enough information in the provided knowledge base.
```

Result:

- ✅ No unsupported answer
- ✅ Knowledge-base grounding maintained

---

## Test 3 – Frontend

Complete UI flow:

```
Enter Question
      ↓
Click Ask AI
      ↓
Loading
      ↓
AI Answer
      ↓
Retrieved Sources
```

Result:

- ✅ Frontend working
- ✅ Backend working
- ✅ RAG working
- ✅ Gemini working

---

# 📁 Final Project Structure

```
rag-knowledge-assistant/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── generator.py
│   │   ├── rag.py
│   │   └── retriever.py
│   │
│   ├── data/
│   │   └── knowledge_base.txt
│   │
│   ├── api.py
│   ├── ingest.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── README.md
└── .gitignore
```

---

# 🛠️ Technologies Used

- Python
- ChromaDB
- Gemini
- FastAPI
- Next.js
- React
- TypeScript
- Tailwind CSS
- Git
- GitHub

---

# 🧠 Key Takeaways

- A RAG pipeline can be converted into a complete AI application.
- ChromaDB handles semantic retrieval.
- Gemini generates answers using retrieved context.
- Retrieval quality directly affects answer quality.
- Top-K retrieval does not guarantee that the answer exists in the retrieved documents.
- Grounded prompts help reduce hallucination.
- FastAPI provides a backend API for the RAG system.
- Next.js provides a user-friendly interface.
- Source display improves transparency.
- Separating retrieval, generation, API, and frontend creates a cleaner application architecture.
- RAG allows external knowledge to be updated without retraining the LLM.

---

# 🎯 Interview Corner

## Q1. What is the role of FastAPI in this project?

FastAPI exposes the RAG functionality through an API and allows the frontend to communicate with the backend.

---

## Q2. Why did we add a frontend?

The frontend converts the console-based RAG prototype into a user-friendly and demonstrable AI application.

---

## Q3. Why display retrieved sources?

Sources provide transparency and help users understand which knowledge was retrieved for generating the answer.

---

## Q4. Does retrieving the top K documents guarantee the correct answer?

No. Top-K retrieval returns the closest available documents, but they may still be irrelevant to the actual question.

---

## Q5. How does grounding help?

Grounding instructs the LLM to use the retrieved context instead of relying on unsupported outside information.

---

# 🧪 Practical Interview Scenario

### Interviewer:

You have a company knowledge base and want employees to ask questions through a web application. How would you build it?

### Expected Answer:

I would build a RAG-based application. I would chunk the company documents and store them in a vector database such as ChromaDB. When a user asks a question, the backend retrieves the most relevant chunks and provides them as context to an LLM such as Gemini. I would expose this RAG pipeline through FastAPI and build a frontend using Next.js. The UI would display both the generated answer and the retrieved sources.

---

# 🏆 Project Completed

## AI Knowledge Assistant

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
- ✅ FastAPI Backend
- ✅ Next.js Frontend
- ✅ Retrieved Source Display
- ✅ Interactive Questions

---

# 🚀 Day 10 Summary

Day 7 introduced embeddings.

Day 8 introduced vector databases.

Day 9 connected retrieval with generation.

Day 10 converted the RAG pipeline into a complete AI application.

The progression is:

```
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

Day 10
Next.js UI
     ↓
FastAPI
     ↓
RAG Pipeline
     ↓
ChromaDB + Gemini
     ↓
Answer + Sources
```

The final project is a working:

**AI Knowledge Assistant**

---

# 🚀 Next Step

## Day 11 – LangChain Fundamentals

Topics:

- Why LangChain exists
- LLM abstractions
- Prompt Templates
- Output Parsers
- Chains
- Runnables
- LCEL
- Model integration
- LangChain vs direct API calls
- When to use LangChain
- When not to use LangChain

The goal is to understand what problem LangChain solves and what happens underneath its abstractions before using it in larger AI applications.