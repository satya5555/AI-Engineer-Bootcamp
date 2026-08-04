# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 7 – Embeddings & Semantic Search

---

# 🎯 Today's Goal

Today's objective was to understand one of the most important concepts in modern Artificial Intelligence:

**Embeddings**

Instead of searching using exact keywords, we learned how AI searches based on **meaning**.

We built our first Semantic Search Engine capable of retrieving documents using vector similarity.

---

# 🧠 Why Keyword Search Fails

Traditional search engines compare words.

Example

Search

```
automobile
```

Document

```
I bought a new car yesterday.
```

Keyword Search

```
No Match
```

Although humans know that

```
car == automobile
```

the computer only compares words.

It does not understand meaning.

---

# 🌍 Semantic Search

Semantic Search compares **meaning** instead of words.

```
Search Query

↓

Embedding

↓

Vector

↓

Similarity Search

↓

Best Matching Document
```

Instead of searching text,

AI searches vectors.

---

# 🔥 What are Embeddings?

An embedding is a numerical representation of meaning.

Example

Sentence

```
I bought a car.
```

↓

Embedding

```
[-0.28,
 0.42,
...
384 numbers]
```

Another sentence

```
I purchased an automobile.
```

↓

Another embedding

Different numbers

Similar meaning

The vectors become close together.

---

# 🗺️ Vector Space

Imagine every sentence becoming a point on a map.

```
Programming

Python

Java


Vehicles

Car

Automobile

Truck


Animals

Dog

Cat
```

Similar ideas are close together.

Different ideas are far apart.

This mathematical space is called **Vector Space**.

---

# 📦 Sentence Transformers

We used the library

```python
from sentence_transformers import SentenceTransformer
```

Model

```
all-MiniLM-L6-v2
```

Why this model?

- Small
- Fast
- High quality
- Widely used
- Excellent for Semantic Search

---

# 🧩 Generating Embeddings

Example

```python
embedding = model.encode(sentence)
```

Output

```
384-dimensional vector
```

Every sentence produces

```
384 numbers
```

representing its semantic meaning.

---

# 📏 Embedding Dimensions

Our model produces

```
384
```

dimensions.

This means every sentence becomes a point inside a 384-dimensional mathematical space.

---

# 📄 Documents

Instead of hardcoding text,

we created

```
documents.txt
```

Advantages

- Cleaner code
- Easier updates
- Real-world approach
- Similar to enterprise document storage

---

# 🔎 Semantic Search Pipeline

```
documents.txt

↓

SentenceTransformer

↓

Embeddings

↓

User Query

↓

Embedding

↓

Cosine Similarity

↓

Top Matching Documents
```

---

# 📐 Cosine Similarity

Cosine Similarity measures how similar two vectors are.

Range

```
1

↓

Very Similar

0

↓

Unrelated

-1

↓

Opposite
```

Higher score

↓

More similar meaning.

---

# 🧮 Calculating Similarity

We used

```python
cosine_similarity()
```

instead of comparing raw text.

Example

```
Query

↓

Embedding

↓

Compare with

↓

Document Embeddings

↓

Similarity Scores
```

---

# 🏆 Top Results

Instead of returning only one document,

our search engine returns

Top 3 Results.

Example

```
1.

Python is a programming language.

Score

0.91

----------------

2.

Machine Learning is a subset of AI.

Score

0.84

----------------

3.

Docker helps package applications.

Score

0.32
```

---

# 🚫 Similarity Threshold

We added

```
0.30
```

as a minimum similarity score.

Purpose

Prevent unrelated documents from appearing.

Without threshold

```
banana

↓

Git tutorial
```

With threshold

```
banana

↓

No Relevant Documents
```

---

# 🧠 AI Engineering Insight

A RAG system is simply

```
User Question

↓

Embedding

↓

Vector Search

↓

Relevant Documents

↓

LLM

↓

Final Answer
```

Today we built everything **except the LLM step**.

---

# 🛠️ Technologies Used

- Python
- Sentence Transformers
- Hugging Face
- NumPy
- Scikit-learn
- Cosine Similarity

---

# 📖 New Terms

### Embedding

A numerical representation of semantic meaning.

---

### Vector

An array of numbers representing information.

---

### Vector Space

A mathematical space where embeddings are stored.

---

### Semantic Search

Searching using meaning instead of exact keywords.

---

### Cosine Similarity

A metric used to compare vector similarity.

---

### Embedding Model

A model that converts text into vectors.

---

### Retrieval

Finding relevant information before generating an answer.

---

# 🌍 Real-World Applications

- ChatGPT Memory
- RAG
- Enterprise Search
- FAQ Bots
- AI Assistants
- GitHub Copilot
- Netflix Recommendations
- Spotify Recommendations
- Amazon Product Search

---

# 📝 Key Takeaways

- Embeddings represent semantic meaning.
- Similar sentences produce similar vectors.
- Semantic search is more powerful than keyword search.
- Cosine similarity measures closeness between embeddings.
- Documents should be stored separately from application code.
- Returning multiple relevant documents improves retrieval quality.
- Similarity thresholds help avoid irrelevant search results.
- Embeddings are the foundation of modern RAG systems.

---

# ❓ Questions I Still Have

- How are embeddings trained?
- Why did we use 384 dimensions?
- What happens if we have millions of documents?
- Why do we need vector databases?
- How does ChromaDB store vectors?
- What is ANN (Approximate Nearest Neighbor)?
- How does RAG retrieve documents?

---

# 🏆 Project Completed

## Semantic Search Engine

Features

- ✅ Sentence Transformers
- ✅ Embedding Generation
- ✅ Cosine Similarity
- ✅ Semantic Search
- ✅ Top 3 Results
- ✅ Similarity Threshold
- ✅ External Document File
- ✅ Interactive Search

---

# 🚀 Day 7 Summary

Today we learned one of the most important concepts in AI Engineering.

Instead of searching using exact words, our application searches using semantic meaning.

This forms the foundation of Retrieval-Augmented Generation (RAG), enterprise AI search, recommendation systems, and AI assistants.

---

# 🚀 Next Step

Tomorrow we will replace our in-memory embeddings with a real Vector Database:

**ChromaDB**

This will allow our application to scale beyond a handful of documents and prepare us for building a complete RAG system.