# ChromaDB Semantic Search Engine

A semantic search application built using Sentence Transformers and ChromaDB as part of the AI Engineer Bootcamp.

## Features

- Semantic document search
- Persistent vector storage
- ChromaDB vector database
- Sentence Transformer embeddings
- Top 3 search results
- Interactive search
- Metadata-based filtering
- Persistent collections

## Technologies

- Python
- ChromaDB
- Sentence Transformers
- Hugging Face
- NumPy
- Scikit-learn

## Project Architecture

```text
documents.txt
      ↓
Sentence Transformer
      ↓
Embeddings
      ↓
ChromaDB
      ↓
Vector Search
      ↓
Top Relevant Documents
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Example

```text
Search: automobile

Top Results:

1. Electric vehicles are becoming increasingly popular around the world.
2. ...
```

## Key Concepts

- Embeddings
- Vector Databases
- Semantic Search
- Cosine Similarity
- Metadata
- Vector Retrieval
- Persistent Storage

## Learning Objective

This project demonstrates how a vector database can store and retrieve semantically similar documents and serves as the foundation for Retrieval-Augmented Generation (RAG).
