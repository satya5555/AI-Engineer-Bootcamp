# 🧠 AI Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based knowledge assistant that answers questions using a custom company knowledge base.

The application combines semantic search, ChromaDB, Gemini, FastAPI, and a Next.js interface to provide grounded answers with retrieved sources.

---

## 🚀 Features

- Ask questions in a simple web interface
- Semantic retrieval using ChromaDB
- Gemini-powered answer generation
- Grounded responses based only on the knowledge base
- Source documents displayed with similarity distance
- Handles questions that are not available in the knowledge base
- FastAPI backend
- Next.js frontend

---

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
                Next.js UI
                     │
                     │ POST /ask
                     ▼
                 FastAPI
                     │
                     ▼
                RAG Pipeline
                 /       \
                ▼         ▼
           ChromaDB     Gemini
                ▲
                │
          Knowledge Base
```
