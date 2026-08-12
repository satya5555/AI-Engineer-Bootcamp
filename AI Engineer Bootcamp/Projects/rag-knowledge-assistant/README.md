# RAG Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application built using ChromaDB and Google Gemini as part of the AI Engineer Bootcamp.

## Features

- Document-based knowledge retrieval
- Document chunking
- Semantic search
- ChromaDB vector database
- Gemini-powered answer generation
- Grounded responses
- Hallucination fallback
- Interactive question answering

## Architecture

```text
User Question
      ↓
Query Embedding
      ↓
ChromaDB
      ↓
Relevant Chunks
      ↓
Context Construction
      ↓
Gemini
      ↓
Grounded Answer
```

## Technologies

- Python
- ChromaDB
- Sentence Transformers
- Google Gemini
- Google GenAI SDK
- python-dotenv

## Project Structure

```text
rag-knowledge-assistant/
│
├── knowledge_base.txt
├── ingest.py
├── retrieve.py
├── generate.py
├── main.py
├── requirements.txt
└── .gitignore
```

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env.local`:

```text
GEMINI_API_KEY=your_api_key_here
```

Never commit the API key to GitHub.

## Run

First ingest the knowledge base:

```bash
python ingest.py
```

Then run the assistant:

```bash
python main.py
```

## Example

```text
Question: How many days can I work from home?

Answer:
Employees can work from home up to two days per week
with prior approval from their manager.
```

## RAG Pipeline

```text
Knowledge Base
      ↓
Chunking
      ↓
Embeddings
      ↓
ChromaDB
      ↓
Semantic Retrieval
      ↓
Context
      ↓
Gemini
      ↓
Answer
```

## Learning Objectives

- Understand RAG architecture
- Implement document chunking
- Use vector databases for retrieval
- Connect retrieval with an LLM
- Ground LLM responses using external knowledge
