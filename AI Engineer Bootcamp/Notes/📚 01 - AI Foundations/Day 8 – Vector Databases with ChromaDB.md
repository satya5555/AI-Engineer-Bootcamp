# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 8 – Vector Databases with ChromaDB

---

# 🎯 Today's Goal

Today's objective was to understand why vector databases are required for modern AI applications and how they improve upon the basic in-memory semantic search engine we built on Day 7.

We used **ChromaDB** to store documents, embeddings, metadata, and perform semantic similarity searches.

---

# 🧠 Why Do We Need Vector Databases?

On Day 7, our embeddings were stored in Python memory.

```text
Documents
    ↓
Embeddings
    ↓
Python Memory
    ↓
Cosine Similarity
    ↓
Results
```

This approach works for a small number of documents.

However, imagine an enterprise with:

```text
10 documents
       ↓
10,000 documents
       ↓
1,000,000 documents
       ↓
10,000,000 documents
```

Keeping all vectors in application memory and comparing every vector manually becomes inefficient.

This is where vector databases are useful.

---

# 🗄️ What is a Vector Database?

A vector database is a database designed to store and retrieve vector representations efficiently.

A stored item can contain:

```text
Document
    +
Embedding
    +
Metadata
    +
Unique ID
```

Example:

```text
Document:
Python is a programming language.

Embedding:
[0.12, -0.45, 0.78, ...]

Metadata:
{
    "category": "programming"
}
```

---

# 🔄 Day 7 vs Day 8

## Day 7

```text
Documents
    ↓
Sentence Transformer
    ↓
Embeddings
    ↓
Python Memory
    ↓
Cosine Similarity
```

## Day 8

```text
Documents
    ↓
ChromaDB
    ↓
Vector Storage
    ↓
Vector Search
    ↓
Relevant Documents
```

---

# 🧩 ChromaDB

ChromaDB is an open-source vector database designed for AI and machine learning applications.

We used it to:

- Store documents
- Store embeddings
- Perform similarity search
- Store metadata
- Persist vector data

---

# 💾 Persistent Storage

We created a persistent ChromaDB client:

```python
client = chromadb.PersistentClient(
    path="./chroma_db"
)
```

This creates a local database directory:

```text
chroma_db/
```

Unlike normal Python variables, the database persists after the program exits.

---

# 📦 Collections

A ChromaDB collection is a logical group of documents and their associated vector information.

We created:

```python
collection = client.get_or_create_collection(
    name="semantic_documents"
)
```

Conceptually:

```text
ChromaDB
    ↓
Collection
    ↓
Documents + Embeddings + Metadata
```

---

# 📄 Adding Documents

Documents were added using:

```python
collection.add(
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))]
)
```

Each document receives a unique ID.

Example:

```text
doc_0
doc_1
doc_2
...
```

---

# 🔎 Querying ChromaDB

We performed semantic search using:

```python
results = collection.query(
    query_texts=[query],
    n_results=3
)
```

The system then retrieves the most relevant documents.

---

# 🧠 Search Architecture

```text
User Query
     ↓
Embedding
     ↓
Vector Similarity
     ↓
ChromaDB
     ↓
Top 3 Documents
```

---

# 🏷️ Metadata

Metadata provides additional information about a document.

Example:

```python
{
    "category": "programming"
}
```

Other examples could include:

```text
department
author
date
document_type
language
access_level
```

---

# 🔍 Metadata Filtering

We tested filtering using:

```python
results = collection.query(
    query_texts=["How do I develop software?"],
    n_results=3,
    where={"category": "programming"}
)
```

This means the semantic search is performed within a specific metadata category.

Architecture:

```text
User Query
     +
Metadata Filter
     ↓
Semantic Search
     ↓
Relevant Documents
```

---

# 🏭 Enterprise Example

Imagine an enterprise has millions of documents:

```text
Documents
│
├── HR
├── Finance
├── Manufacturing
├── Quality
├── Safety
├── IT
└── Engineering
```

A query such as:

```text
machine maintenance procedure
```

could first filter:

```text
department = Manufacturing
```

and then perform semantic search.

This reduces the search space and can improve retrieval relevance.

---

# 🧱 Code Structure

We refactored the application into functions:

```python
def load_documents():
    ...

def create_collection():
    ...

def add_documents():
    ...

def search_documents():
    ...

def main():
    ...
```

This improves:

- Readability
- Maintainability
- Debugging
- Reusability
- Extensibility

---

# 📁 Project Structure

```text
semantic-search-engine/
│
├── .venv/
├── chroma_db/
├── documents.txt
├── main.py
├── chroma_test.py
├── requirements.txt
├── README.md
└── .gitignore
```

The `chroma_db/` directory is generated locally and should not be committed to GitHub.

---

# 🛠️ Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- Hugging Face
- NumPy
- Scikit-learn

---

# 📖 New Terms

## Vector Database

A database optimized for storing and searching vector representations.

## Collection

A logical group of documents and their vector information.

## Metadata

Additional information stored alongside documents.

## Persistence

The ability to retain data after an application exits.

## Vector Search

Searching for documents based on similarity between vector representations.

## Similarity Search

Finding vectors that are mathematically close to a query vector.

---

# 🔥 Why Vector Databases Matter for RAG

RAG requires two major stages:

```text
1. Retrieval

2. Generation
```

Retrieval:

```text
User Question
     ↓
Embedding
     ↓
Vector Database
     ↓
Relevant Documents
```

Generation:

```text
Relevant Documents
     +
User Question
     ↓
LLM
     ↓
Answer
```

Therefore:

```text
Vector Database
       ↓
Retrieval
       ↓
RAG
```

---

# 🌍 Real-World Applications

Vector databases are commonly used for:

- Enterprise Search
- RAG
- Recommendation Systems
- Document Search
- AI Assistants
- Knowledge Bases
- Semantic Search
- Similarity Matching

---

# 📝 Key Takeaways

- In-memory vectors are not suitable for large-scale applications.
- Vector databases provide persistent vector storage.
- ChromaDB can store and retrieve vector-based information.
- Collections organize documents and vector data.
- Metadata enables filtering.
- Persistent storage allows data to survive application restarts.
- Vector search is a core component of modern RAG systems.
- Good code structure is important as AI projects become more complex.

---

# 🏆 Project Completed

## ChromaDB Semantic Search Engine

Features:

- ✅ ChromaDB
- ✅ Persistent Vector Storage
- ✅ Semantic Search
- ✅ Document Retrieval
- ✅ Metadata
- ✅ Metadata Filtering
- ✅ Interactive Search
- ✅ Modular Python Code

---

# 🎯 Interview Corner

## Q1. What is a vector database?

A vector database is a database optimized for storing and searching numerical vector representations of data, allowing applications to retrieve semantically similar information efficiently.

---

## Q2. Why do we need a vector database?

For large collections of embeddings, manually storing vectors in application memory and comparing them individually is inefficient. Vector databases provide specialized storage and retrieval mechanisms for vector similarity search.

---

## Q3. What is metadata in a vector database?

Metadata is additional information associated with a document or vector, such as category, author, department, date, or document type. It can be used to filter search results.

---

## Q4. What is the difference between a normal database and a vector database?

Traditional databases primarily perform exact or structured queries, while vector databases are optimized for similarity searches between high-dimensional vectors.

---

## Q5. Why is ChromaDB useful for RAG?

ChromaDB can store document embeddings and retrieve semantically relevant documents for a user's query. These retrieved documents can then be provided as context to an LLM to generate a grounded response.

---

# 🎯 Practical Interview Scenario

### Interviewer:

Your company has 500,000 internal documents. Employees should be able to ask questions using natural language.

How would you design the retrieval system?

### Expected Answer:

I would convert the documents into embeddings and store them in a vector database such as ChromaDB or another production-grade vector store. When a user submits a question, I would generate an embedding for the query, perform vector similarity search, optionally apply metadata filters, retrieve the most relevant documents, and pass those documents as context to an LLM.

This creates the retrieval component of a RAG architecture.

---

# 🚀 Day 8 Summary

Day 7 introduced embeddings and semantic search.

Day 8 introduced the storage and retrieval layer required to scale that approach.

The progression is:

```text
Day 7

Embeddings
    ↓
Semantic Search


Day 8

Embeddings
    ↓
Vector Database
    ↓
Semantic Search


Day 9

Embeddings
    ↓
Vector Database
    ↓
Retrieved Context
    ↓
LLM
    ↓
RAG
```

---

# 🚀 Next Step

## Day 9 – Retrieval-Augmented Generation (RAG)

Tomorrow we will connect:

```text
User Question
      ↓
Embedding
      ↓
ChromaDB
      ↓
Relevant Documents
      ↓
Gemini
      ↓
Grounded Answer
```

We will finally turn our semantic search engine into an actual **AI Knowledge Assistant**.