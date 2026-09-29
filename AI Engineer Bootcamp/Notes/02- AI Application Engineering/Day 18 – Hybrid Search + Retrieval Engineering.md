## Objective

Build a **Hybrid Search Engine** that combines:

- Keyword search using **BM25**
    
- Semantic search using **embeddings + ChromaDB**
    
- **Reciprocal Rank Fusion (RRF)** for combining retrieval rankings
    
- Gemini for grounded answer generation
    
- Source/page tracking
    
- Retrieval evaluation
    
- Streamlit UI
    

The main goal was to understand why combining keyword and semantic retrieval can provide better search coverage than relying on only one retrieval method.

---

# 1. What is Hybrid Search?

Hybrid search combines multiple retrieval strategies.

The two strategies used in this project were:

```text
Keyword Search
      +
Semantic Search
      ↓
Hybrid Retrieval
```

### Keyword Search

Keyword search looks for matching terms in documents.

It is particularly useful for:

- Names
    
- IDs
    
- Error codes
    
- Product codes
    
- Exact terminology
    
- Technical identifiers
    

Example:

```text
Query:
ERR-502
```

A keyword retriever can directly match:

```text
ERR-502 indicates a payment service failure.
```

---

### Semantic Search

Semantic search uses embeddings to represent text as vectors.

It focuses on meaning rather than exact wording.

For example:

```text
Query:
Why was the payment service failing?
```

can retrieve:

```text
ERR-502 indicates a payment service failure.
```

even though the query does not contain the exact phrase from the document.

---

# 2. Why Hybrid Search?

Neither retrieval method is perfect for every type of query.

```text
BM25
 ↓
Strong lexical/exact matching

Semantic Search
 ↓
Strong meaning-based matching
```

Hybrid search combines their strengths.

```text
                  Query
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
        BM25              Semantic
      Keyword              Vector
          │                   │
          └─────────┬─────────┘
                    ▼
                 Fusion
                    │
                    ▼
             Ranked Results
```

---

# 3. BM25

BM25 is a keyword-based document ranking algorithm.

In the project, LangChain's:

```python
BM25Retriever
```

was used.

Implementation:

```python
from langchain_community.retrievers import BM25Retriever


class KeywordSearch:

    def __init__(self, documents):
        self.retriever = BM25Retriever.from_documents(documents)

    def search(self, question, k=4):
        self.retriever.k = k
        return self.retriever.invoke(question)
```

BM25 depends on terms appearing in the document.

It is therefore useful for exact information such as:

```text
ERR-502
CUST-84721
Python
```

---

# 4. Semantic Search

Semantic search was implemented using:

- Gemini embeddings
    
- ChromaDB
    
- Vector retrieval
    

Implementation:

```python
class SemanticSearch:

    def __init__(self, vector_store):
        self.retriever = vector_store.as_retriever(
            search_kwargs={"k": 4}
        )

    def search(self, question):
        return self.retriever.invoke(question)
```

The pipeline is:

```text
Document
   ↓
Embedding
   ↓
Vector
   ↓
ChromaDB
```

Query:

```text
User question
   ↓
Query embedding
   ↓
Similarity search
   ↓
Relevant chunks
```

---

# 5. Comparing BM25 and Semantic Search

We tested both retrieval approaches independently.

### Exact query

```text
ERR-502
```

BM25 naturally performed well because the exact identifier existed in the document.

### Meaning-based query

```text
Why was the payment service failing?
```

Semantic search was useful because it could match the concept of a payment service failure.

This demonstrated the main reason for hybrid retrieval.

---

# 6. Reciprocal Rank Fusion (RRF)

RRF was used to combine the rankings produced by BM25 and semantic search.

Conceptually:

```text
BM25:

A → Rank 1
B → Rank 2
C → Rank 3
```

Semantic search:

```text
C → Rank 1
A → Rank 2
D → Rank 3
```

RRF gives each document a contribution based on its ranking.

The formula used was:

```text
RRF Score = 1 / (60 + rank)
```

For documents appearing in both retrieval systems, their contributions are added.

Therefore:

```text
Document appears high in BM25
        +
Document appears high in Semantic
        ↓
Higher combined RRF score
```

---

# 7. Why RRF?

BM25 and semantic retrieval do not necessarily produce scores on the same scale.

Therefore, directly adding their raw scores would not necessarily be meaningful.

RRF solves this by combining **rank positions** rather than directly combining raw retrieval scores.

Important:

> RRF score is a ranking signal, not a percentage relevance score.

For example:

```text
0.032
```

does NOT mean:

```text
32% relevant
```

It represents a contribution from the document's rankings.

---

# 8. Hybrid Search Implementation

The hybrid search combines:

```text
BM25 results
      +
Semantic results
      ↓
RRF
      ↓
Ranked documents
```

The implementation tracks:

- RRF score
    
- BM25 contribution
    
- Semantic contribution
    

Example result:

```text
Document A

RRF:      0.0320
BM25:     0.0161
Semantic: 0.0159
```

This allows retrieval inspection.

We can understand whether a document was supported by:

```text
BM25 only
Semantic only
Both
```

---

# 9. PDF Ingestion Pipeline

The final project uses a PDF as the document source.

Pipeline:

```text
PDF
 ↓
PyPDFLoader
 ↓
Pages
 ↓
RecursiveCharacterTextSplitter
 ↓
Chunks
```

The test document contained:

```text
3 pages
```

and produced:

```text
10 chunks
```

The chunk configuration was:

```python
chunk_size=500
chunk_overlap=100
```

---

# 10. Two Retrieval Indexes

An important architectural concept from Day 18 is that the same document chunks are used by two retrieval systems.

```text
                 PDF
                  │
              Chunking
                  │
           ┌──────┴──────┐
           ▼             ▼
         BM25          Chroma
       Keyword        Semantic
           │             │
           └──────┬──────┘
                  ▼
                 RRF
```

BM25 works with the document text.

Chroma works with embeddings.

---

# 11. Hybrid RAG Pipeline

After retrieval, the top-ranked chunks are passed to Gemini.

Final pipeline:

```text
User Query
     │
     ▼
┌───────────────┐
│ Hybrid Search │
└───────┬───────┘
        │
   ┌────┴────┐
   ▼         ▼
 BM25     Semantic
   │         │
   └────┬────┘
        ▼
    RRF Fusion
        │
        ▼
      Top-K
        │
        ▼
      Gemini
        │
        ▼
 Grounded Answer
        │
        ▼
     Sources
```

The LLM is instructed to answer using only the retrieved context.

---

# 12. Grounded Answer Generation

The prompt used rules such as:

```text
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not supported by the context,
   say that you could not find the information.
4. Give a concise and direct answer.
```

This helps reduce hallucination by constraining the model to retrieved context.

---

# 13. Source Tracking

The application tracks the page associated with retrieved chunks.

Example:

```text
SOURCES

Page 1 | RRF: 0.031xxx
Page 2 | RRF: 0.016xxx
```

This gives the user traceability from:

```text
Answer
  ↓
Retrieved context
  ↓
Original document page
```

Source tracking is important for document-based AI applications.

---

# 14. Retrieval Evaluation

We tested different types of queries.

### Exact-term query

Example:

```text
ERR-502
```

Purpose:

Test keyword retrieval.

### Semantic query

Example:

```text
Why was the payment service failing?
```

Purpose:

Test meaning-based retrieval.

### Combined query

Contains both terminology and conceptual intent.

Purpose:

Test hybrid retrieval.

### Unsupported query

Example:

```text
What is the recipe for pasta?
```

Purpose:

Test whether the system recognizes that the document does not contain relevant information.

---

# 15. Important Failure Case

The unsupported query produced an important observation.

For:

```text
What is the recipe for pasta?
```

the system still retrieved medical-document chunks.

For example:

```text
ATarax 10MG
APPETITE : NORMAL
Medicover Hospitals
```

These chunks were clearly unrelated to pasta.

This revealed:

```text
Unsupported Query
       ↓
Top-K Retrieval
       ↓
Unrelated Documents
```

This is an important RAG engineering problem.

---

# 16. Key Retrieval Lesson

Retrievers normally return the best available candidates.

That does not automatically mean:

```text
Best available candidate
=
Actually relevant document
```

For an unsupported query, the system can still produce ranked results.

Therefore:

> Retrieval ranking and relevance are not exactly the same thing.

This is why production RAG systems need mechanisms for detecting insufficient relevance.

---

# 17. Retrieval Thresholds

We experimented with filtering hybrid results using an RRF threshold.

Conceptually:

```text
RRF score
    ↓
Threshold
    ↓
Keep sufficiently strong candidates
```

However, an important limitation was identified:

> RRF scores are based on rank contributions and should not be treated as universal relevance scores.

Therefore, a fixed RRF threshold is only a simple experiment, not a complete production relevance solution.

---

# 18. Future Improvement — Reranking

A stronger production architecture can introduce a reranking stage.

```text
                 Query
                   │
            ┌──────┴──────┐
            ▼             ▼
          BM25         Semantic
            │             │
            └──────┬──────┘
                   ▼
              Candidates
                   │
                   ▼
                Reranker
                   │
                   ▼
          Relevance Filtering
                   │
                   ▼
                 LLM
```

The initial retrievers provide candidates.

A reranker can then evaluate those candidates more carefully before sending them to the LLM.

---

# 19. Streamlit UI

A Streamlit interface was added.

The UI supports:

- PDF upload
    
- Question input
    
- Hybrid retrieval
    
- Gemini answer generation
    
- Source display
    
- Retrieval details
    

The retrieval details expose:

```text
RRF score
BM25 contribution
Semantic contribution
Page number
Retrieved content
```

This makes the application easier to inspect and debug.

---

# 20. Project Structure

Final project structure:

```text
ai-hybrid-search/
│
├── app/
│   ├── __init__.py
│   ├── loader.py
│   ├── splitter.py
│   ├── keyword_search.py
│   ├── semantic_search.py
│   ├── hybrid_search.py
│   ├── vectorstore.py
│   └── chat.py
│
├── documents/
│   └── sample.pdf
│
├── ingest.py
├── evaluate.py
├── test_keyword.py
├── test_semantic.py
├── test_comparison.py
├── test_hybrid.py
├── main.py
├── ui.py
├── requirements.txt
└── .gitignore
```

The PDF and local Chroma database should not be committed if they contain private or generated data.

---

# 21. Dependency Issue Learned

During the Streamlit stage, the application produced:

```text
ImportError:
Could not import rank_bm25
```

The package was installed inside the project's virtual environment.

The actual issue was that:

```text
python
```

was using the project `.venv`, while:

```text
streamlit
```

was being launched from the global Python installation.

The project Python was:

```text
...\ai-hybrid-search\.venv\Scripts\python.exe
```

while Streamlit was initially:

```text
C:\Users\...\Python312\Scripts\streamlit.exe
```

The solution was to launch Streamlit through the active Python environment:

```powershell
python -m streamlit run ui.py
```

General lesson:

> Always make sure application commands use the same virtual environment where the project's dependencies are installed.

---

# 22. Day 18 Architecture

```text
                     USER
                       │
                       ▼
                Streamlit UI
                       │
                       ▼
                  User Query
                       │
              ┌────────┴────────┐
              ▼                 ▼
            BM25             Chroma
          Keyword           Semantic
              │                 │
              └────────┬────────┘
                       ▼
                  RRF Fusion
                       │
                       ▼
                    Top-K
                       │
                       ▼
                    Gemini
                       │
                       ▼
               Grounded Answer
                       │
                       ▼
                    Sources
```

---

# 23. Day 18 Key Concepts

### Hybrid Search

Combines keyword and semantic retrieval.

### BM25

Useful for lexical/exact matching.

### Semantic Search

Useful for meaning-based retrieval.

### RRF

Combines rankings from different retrieval systems.

### Top-K

Controls how many retrieved documents/chunks are passed forward.

### Grounded Generation

The LLM generates an answer using retrieved context.

### Retrieval Inspection

Examining retrieved documents and scores to understand system behavior.

### Retrieval Failure

A retriever can return candidates that are not actually relevant.

### Reranking

A future technique for improving the precision of retrieved context.

---

# 24. Interview Questions

### What is hybrid search?

Hybrid search combines keyword-based and semantic retrieval to handle both exact-term and meaning-based queries.

### Why use BM25 with vector search?

BM25 is useful for exact identifiers, names, error codes and terminology, while vector search is better at semantic similarity.

### What is RRF?

Reciprocal Rank Fusion is a ranking-fusion technique that combines results from multiple retrieval systems using their rank positions.

### Why not directly add BM25 and vector scores?

Their score scales and meanings can differ. RRF avoids this by combining rank positions instead.

### Can the top retrieved document always be trusted?

No. A retriever can return the best available candidate even when none of the candidates are actually relevant.

### How can retrieval quality be improved?

Possible approaches include:

- Better chunking
    
- Metadata filtering
    
- Hybrid search
    
- Query rewriting
    
- Multi-query retrieval
    
- Reranking
    
- Relevance thresholds
    
- Retrieval evaluation
    

### What happens if the user asks something outside the document?

A robust RAG system should detect insufficient evidence and avoid generating an unsupported answer.

---

# 25. Day 18 Mental Model

Remember:

```text
BM25
=
Exact words

Semantic Search
=
Meaning

RRF
=
Combine rankings

Reranking
=
Improve candidate ordering

LLM
=
Generate grounded answer
```

Or simply:

> **Find with multiple strategies → rank → verify relevance → generate with evidence.**

---

# 26. Day 18 Completed

### Technical Skills

- BM25
    
- Keyword retrieval
    
- Semantic retrieval
    
- ChromaDB
    
- RRF
    
- Hybrid retrieval
    
- Retrieval inspection
    
- Source tracking
    
- Grounded generation
    
- Retrieval evaluation
    
- Streamlit
    

### Engineering Skills

- Separating ingestion from querying
    
- Comparing retrieval strategies
    
- Investigating retrieval failures
    
- Understanding ranking vs relevance
    
- Managing Python virtual environments
    
- Building observable retrieval pipelines
    

---

# 27. Next — Day 19

**Day 19: Evaluation of AI Applications**

We move from:

```text
"Does my RAG application work?"
```

to:

```text
"How do I measure whether my RAG application works well?"
```

Topics:

- Evaluation datasets
    
- Ground-truth answers
    
- Retrieval evaluation
    
- Context relevance
    
- Answer relevance
    
- Faithfulness
    
- Correctness
    
- Hallucination detection
    
- Automated evaluation
    
- LLM-as-a-judge
    
- Failure analysis
    
- Evaluation pipelines
    
- Improving an AI application based on evaluation results