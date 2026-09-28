
## 🎯 Objective

Move from a basic RAG pipeline to a more reliable and production-oriented **Advanced RAG system**.

Focus areas:

- Better document chunking
    
- Embeddings
    
- ChromaDB vector storage
    
- Similarity search
    
- Retrieval configuration
    
- Distance thresholds
    
- Retrieval inspection
    
- Context construction
    
- Source attribution
    
- RAG evaluation
    
- Failure analysis
    
- Retrieval tuning
    
- Building a Streamlit document chatbot
    

---

# 1. Basic RAG vs Advanced RAG

A basic RAG pipeline looks like:

```text
Document
   ↓
Load
   ↓
Split
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
LLM
   ↓
Answer
```

The problem is that a RAG application can technically work while still producing poor answers.

For example:

```text
Question
   ↓
Retriever
   ↓
Irrelevant chunks
   ↓
LLM
   ↓
Incorrect answer
```

Advanced RAG focuses on improving the quality of the context provided to the LLM.

---

# 2. Advanced RAG Architecture

The final Day 17 architecture:

```text
                    ┌──────────────┐
                    │   Document   │
                    └──────┬───────┘
                           ↓
                    Document Loader
                           ↓
                     Text Splitter
                           ↓
                      Embeddings
                           ↓
                    Vector Database
                           ↓
                       Retriever
                           ↓
                  Retrieval Filtering
                           ↓
                    Relevant Context
                           ↓
                         LLM
                           ↓
                  Answer + Sources
```

Our implementation:

```text
PDF
 ↓
PyPDFLoader
 ↓
RecursiveCharacterTextSplitter
 ↓
Gemini Embeddings
 ↓
ChromaDB
 ↓
Similarity Search
 ↓
Distance Threshold
 ↓
Gemini
 ↓
Answer + Sources
```

---

# 3. Why Retrieval Quality Matters

Consider a technical manual with hundreds of pages.

User asks:

> How do I reset the device after a firmware failure?

A naive retriever may return chunks containing words such as:

- firmware
    
- device
    
- reset
    
- failure
    

But the retrieved chunks may not contain the actual reset procedure.

Therefore:

> Retrieval quality directly affects the quality of the final answer.

The LLM cannot reliably answer from information that was never retrieved.

---

# 4. Document Loading

We used `PyPDFLoader`.

```python
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:
    def load(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        return documents
```

The loader produces LangChain `Document` objects containing:

```text
page_content
metadata
```

Metadata can contain information such as:

```text
source
page
total_pages
```

This metadata becomes important for source attribution.

---

# 5. Text Splitting

We used:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

Implementation:

```python
class TextSplitter:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split(self, documents):
        return self.splitter.split_documents(documents)
```

Our starting configuration:

```text
chunk_size = 500
chunk_overlap = 100
```

### Important

`chunk_size` is a target rather than a guarantee that every chunk will contain exactly that number of characters.

`chunk_overlap` is also target behavior. The exact overlap depends on how the splitter respects separators.

---

# 6. Embeddings

Embeddings convert text into numerical vectors representing semantic information.

Example:

```text
"How do I reset my password?"
              ↓
        Embedding Model
              ↓
[0.021, -0.184, 0.731, ...]
```

A semantically similar sentence such as:

```text
"How can I change my password?"
```

should produce a relatively nearby vector.

This allows semantic search rather than relying only on exact keyword matching.

---

# 7. ChromaDB

We used ChromaDB as the local vector database.

The vector store stores:

```text
Chunk
 +
Embedding
 +
Metadata
```

Architecture:

```text
Document chunks
      ↓
Embedding model
      ↓
Vectors
      ↓
ChromaDB
```

Our project uses:

```python
Chroma(
    collection_name="advanced_rag",
    embedding_function=self.embeddings,
    persist_directory="./chroma_db"
)
```

The local `chroma_db/` directory is ignored by Git.

---

# 8. Ingestion vs Querying

One important engineering improvement was separating ingestion from querying.

### Ingestion

```text
PDF
 ↓
Load
 ↓
Split
 ↓
Embed
 ↓
ChromaDB
```

Implemented in:

```text
ingest.py
```

### Query

```text
Question
 ↓
ChromaDB
 ↓
Retrieve
 ↓
Filter
 ↓
LLM
 ↓
Answer
```

Implemented in:

```text
main.py
```

This prevents repeatedly adding the same chunks to ChromaDB every time a question is asked.

---

# 9. Retriever

Our retriever:

```python
class DocumentRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def search(
        self,
        question: str,
        k: int = 4,
        max_distance: float = 0.70
    ):
        results = self.vector_store.similarity_search_with_score(
            question,
            k=k
        )

        filtered_results = []

        for document, score in results:
            if score <= max_distance:
                filtered_results.append(
                    (document, score)
                )

        return filtered_results
```

The retriever performs two tasks:

1. Retrieve candidate chunks.
    
2. Filter weak matches.
    

---

# 10. `k` — Number of Retrieved Chunks

`k` controls how many candidate chunks are retrieved.

Example:

```python
search(
    question,
    k=4
)
```

means:

```text
Question
   ↓
Vector Search
   ↓
Top 4 chunks
```

Different values have different trade-offs.

|k|Possible behavior|
|---|---|
|2|Focused but may miss information|
|4|Moderate context|
|6|More coverage but potentially more noise|
|10|High coverage but potentially lots of irrelevant context|

There is no universal best value.

It should be evaluated against the application and data.

---

# 11. Similarity Search Scores

We used:

```python
similarity_search_with_score()
```

The returned score from Chroma in this setup represents a **distance**, rather than a percentage of relevance.

Therefore:

```text
Lower distance
      ↓
Closer / more similar
```

Do NOT interpret:

```text
0.56 = 56% relevant
```

That interpretation is incorrect.

The meaning and scale of scores depend on the vector store and search configuration.

---

# 12. Similarity / Distance Threshold

Retrieving the top `k` documents alone isn't enough.

We added a filtering mechanism:

```python
if score <= max_distance:
    filtered_results.append(
        (document, score)
    )
```

Example:

```text
max_distance = 0.70
```

Then:

```text
0.31 → Keep
0.44 → Keep
0.62 → Keep
0.91 → Reject
```

The threshold is not universal.

It must be experimentally evaluated.

---

# 13. Why Thresholds Matter

Without filtering:

```text
Question
   ↓
Top 4 chunks
   ↓
LLM
```

Even weakly related chunks may reach the LLM.

With filtering:

```text
Question
   ↓
Top 4 candidates
   ↓
Distance Filter
   ↓
Relevant chunks
   ↓
LLM
```

This can reduce:

- irrelevant context
    
- token usage
    
- noisy answers
    
- hallucination opportunities
    

But an overly strict threshold can also remove useful information.

---

# 14. Precision vs Recall

Retrieval tuning involves a trade-off.

### Higher recall

Retrieve more potentially useful information.

```text
k ↑
threshold ↑
```

Potential benefit:

> Lower chance of missing required information.

Potential downside:

> More irrelevant context.

### Higher precision

Retrieve fewer, more relevant chunks.

```text
k ↓
threshold ↓
```

Potential benefit:

> Cleaner context.

Potential downside:

> Potentially missing useful information.

Therefore:

```text
Precision  ←────────────→  Recall
```

must be balanced based on the application.

---

# 15. Retrieval Inspection

One of the most important AI engineering practices is to inspect retrieval before blaming the LLM.

We can inspect:

```python
results = retriever.search(
    question,
    k=4
)

for document, score in results:
    print(document.page_content)
    print(document.metadata)
    print(score)
```

This helps distinguish:

### Retrieval failure

```text
Question
 ↓
Retriever
 ↓
❌ Wrong chunks
 ↓
LLM
 ↓
❌ Wrong answer
```

from:

### Generation failure

```text
Question
 ↓
Retriever
 ↓
✅ Correct chunks
 ↓
LLM
 ↓
❌ Wrong answer
```

These are different engineering problems.

---

# 16. Source-Aware RAG

Our RAG system preserves page metadata.

Context is constructed as:

```text
[Source: Page 2]
chunk content

[Source: Page 1]
chunk content

[Source: Page 3]
chunk content
```

This gives the model structured context.

It also allows the application to return sources:

```text
Page 2
Page 1
Page 3
```

---

# 17. Duplicate Source Handling

Multiple retrieved chunks may come from the same page.

For example:

```text
Page 2
Page 2
Page 1
Page 1
```

We deduplicated the displayed source list using a set:

```python
seen_sources = set()
```

Then:

```python
if source_key not in seen_sources:
    sources.append({
        "page": page_number,
        "score": score
    })

    seen_sources.add(source_key)
```

The context can still contain multiple useful chunks from the same page, while the displayed source list remains clean.

---

# 18. Grounded RAG Prompt

Our prompt tells the model:

```text
Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer is not supported by the context,
   say that you could not find the information
   in the document.
4. Give a concise and direct answer.
```

This establishes a grounding boundary.

The model should not answer from its general knowledge when the document doesn't contain the requested information.

---

# 19. Handling Retrieval Failure

A critical RAG behavior is:

```text
No relevant chunks
       ↓
Don't blindly call the LLM
       ↓
Tell the user information wasn't found
```

Our system returns:

```text
I couldn't find sufficiently relevant information
in the document.
```

This is safer than:

```text
No context
   ↓
LLM
   ↓
Potential hallucination
```

---

# 20. Answer Normalization

The Gemini integration can return content in different formats.

For example:

```python
response.content
```

may be a string or a list of content blocks.

We normalize it:

```python
if isinstance(response.content, str):
    answer = response.content

elif isinstance(response.content, list):

    text_parts = []

    for item in response.content:

        if isinstance(item, dict):

            text = item.get("text")

            if text:
                text_parts.append(text)

    answer = "\n".join(text_parts)

else:
    answer = str(response.content)
```

This ensures the UI receives clean text.

---

# 21. RAG Evaluation

A RAG application should not be considered successful simply because it generates an answer.

We need to evaluate:

```text
Retrieval
   ↓
Context
   ↓
Generation
```

### Retrieval relevance

Did we retrieve useful chunks?

### Context relevance

Does the retrieved context contain the information required to answer?

### Faithfulness

Is the generated answer supported by the retrieved context?

### Correctness

Is the final answer actually correct?

---

# 22. Faithfulness vs Correctness

These are different concepts.

Suppose the context says:

```text
Doctor: Dr. Vinay Kumar
```

The model answers:

```text
Dr. Vinay Kumar is a cardiologist.
```

Even if that statement happens to be factually correct elsewhere, it isn't supported by the provided context.

Therefore:

```text
Correctness ≠ Faithfulness
```

A strong RAG system needs both.

---

# 23. Failure Analysis

Four useful scenarios:

### A. Good retrieval + good answer

```text
Retriever ✅
Answer    ✅
```

### B. Bad retrieval + bad answer

```text
Retriever ❌
Answer    ❌
```

Likely retrieval problem.

### C. Good retrieval + bad answer

```text
Retriever ✅
Answer    ❌
```

Likely generation or grounding problem.

### D. No retrieval + model still answers

```text
Retriever ❌
Answer    ❌
```

Potential hallucination/fallback problem.

---

# 24. Retrieval Evaluation

We created:

```text
evaluation_questions.txt
```

Questions should contain both:

### Answerable questions

Information exists in the document.

### Unanswerable questions

Information does not exist in the document.

Example:

```text
Doctor details?
What department does the doctor belong to?
What information is provided about the patient?
What is the main purpose of the document?
What is the patient's favorite programming language?
What is the recipe for pasta?
```

This allows us to test both retrieval and refusal behavior.

---

# 25. Retrieval Tuning Experiments

We experimented with:

```text
k = 2
k = 4
k = 6
```

and considered different thresholds:

```text
0.50
0.60
0.70
0.80
```

The goal is to observe:

```text
Threshold
    ↓
Retrieved Context
    ↓
Answer Quality
```

There is no universal optimal configuration.

---

# 26. Project Structure

Final project:

```text
ai-advanced-rag/
│
├── app/
│   ├── __init__.py
│   ├── chat.py
│   ├── loader.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vectorstore.py
│
├── documents/
│   └── sample.pdf
│
├── chroma_db/
│   └── local vector database
│
├── ingest.py
├── main.py
├── evaluate.py
├── ui.py
├── evaluation_questions.txt
├── requirements.txt
└── .gitignore
```

Sensitive/local files:

```text
documents/*.pdf
chroma_db/
.env
```

should not be committed.

---

# 27. Streamlit Application

The final application provides:

```text
┌──────────────────────────────────────┐
│       📚 Advanced Document Chat      │
├──────────────────────────────────────┤
│                                      │
│ Upload a PDF                         │
│                                      │
│ [ PDF Upload ]                       │
│                                      │
│ Loaded X pages                       │
│ Created X chunks                     │
│                                      │
│ Ask a question                       │
│ ┌──────────────────────────────────┐ │
│ │ Doctor details?                  │ │
│ └──────────────────────────────────┘ │
│                                      │
│ Answer                               │
│ ──────────────────────────────────── │
│ ...                                  │
│                                      │
│ Sources                              │
│ 📄 Page 2                            │
│ 📄 Page 1                            │
└──────────────────────────────────────┘
```

---

# 28. Enterprise Scenario

Imagine an enterprise has:

```text
500-page technical manual
```

A user asks:

> How do I reset the device after a firmware failure?

A production RAG system should:

1. Load the manual.
    
2. Split it intelligently.
    
3. Generate embeddings.
    
4. Store vectors.
    
5. Convert the question into a vector.
    
6. Retrieve candidate chunks.
    
7. Filter weak results.
    
8. Construct relevant context.
    
9. Generate a grounded answer.
    
10. Provide source information.
    
11. Refuse when the information cannot be found.
    
12. Evaluate retrieval and answer quality.
    

---

# 29. Production Considerations

A production RAG system would additionally consider:

### Retrieval

- Hybrid search
    
- Metadata filtering
    
- Reranking
    
- Query rewriting
    
- Multi-query retrieval
    
- Parent-child retrieval
    

### Data

- Document versioning
    
- Incremental ingestion
    
- Duplicate detection
    
- Access control
    
- Data freshness
    

### Model

- Model selection
    
- Latency
    
- Token usage
    
- Cost
    
- Context window
    
- Fallback models
    

### Security

- Prompt injection
    
- Malicious documents
    
- Data leakage
    
- Access control
    
- Tenant isolation
    

### Monitoring

- Retrieval latency
    
- LLM latency
    
- Token usage
    
- Retrieval quality
    
- Answer quality
    
- Failure rates
    

---

# 30. Interview Corner 🎯

### Q1. What is Advanced RAG?

Advanced RAG improves the basic retrieval pipeline using techniques such as better chunking, retrieval filtering, metadata handling, reranking, query transformation, evaluation, and better context construction.

---

### Q2. What does `k` mean in retrieval?

`k` is the number of top candidate documents or chunks returned by the retriever.

---

### Q3. Why shouldn't we always increase `k`?

More chunks can increase context coverage but also introduce irrelevant information, increase token usage, latency, and potentially reduce answer quality.

---

### Q4. What is a similarity threshold?

A threshold filters retrieved results based on their similarity or distance score so weak matches aren't passed to the generation layer.

---

### Q5. Why inspect retrieved documents?

To determine whether a bad answer is caused by poor retrieval or poor generation.

---

### Q6. What is RAG faithfulness?

Faithfulness measures whether the generated answer is supported by the retrieved context.

---

### Q7. Correctness vs faithfulness?

Correctness asks whether the answer is factually correct.

Faithfulness asks whether the answer is supported by the retrieved context.

---

### Q8. Why preserve metadata?

Metadata allows us to trace retrieved content back to its source, such as a document, page, section, or record.

---

### Q9. What happens if retrieval returns nothing?

The system should explicitly handle the failure rather than blindly asking the LLM to answer without evidence.

---

### Q10. Why separate ingestion and querying?

Ingestion creates the vector index. Querying searches the existing index. Separating them prevents unnecessary repeated embedding and duplicate storage.

---

# 31. Practical Scenario

### Problem

A company has a large technical knowledge base.

Users complain:

> "The chatbot sometimes gives answers that are technically plausible but not actually present in our documentation."

### Investigation

Check:

```text
Question
 ↓
Retrieved chunks
```

If chunks are irrelevant:

> Retrieval problem.

If chunks are correct but answer contains unsupported information:

> Generation/faithfulness problem.

Possible improvements:

```text
Better chunking
       ↓
Better retrieval
       ↓
Threshold filtering
       ↓
Reranking
       ↓
Grounded prompt
       ↓
Faithfulness evaluation
```

This is the mindset of an AI engineer:

> **Don't just fix the answer. Identify which layer of the system failed.**

---

# 32. Mental Model

Remember:

```text
RAG ≠ Just Vector Search
```

A production RAG system is:

```text
Ingestion
    +
Chunking
    +
Embeddings
    +
Vector Search
    +
Retrieval Filtering
    +
Context Construction
    +
Generation
    +
Evaluation
    +
Observability
```

And the most important mental model:

> **The LLM can only reason reliably over the context we provide to it.**

---

# 33. Project Completed ✅

## Advanced Document Chatbot

Built using:

- Python
    
- LangChain
    
- Gemini
    
- Gemini Embeddings
    
- ChromaDB
    
- PyPDF
    
- Streamlit
    

Features:

- PDF ingestion
    
- Recursive chunking
    
- Semantic embeddings
    
- Vector storage
    
- Similarity search
    
- Retrieval filtering
    
- Source-aware context
    
- Grounded answers
    
- Source pages
    
- Retrieval evaluation
    
- Failure handling
    
- Streamlit UI
    

Architecture:

```text
User
 ↓
Streamlit
 ↓
PDF / Question
 ↓
Fast RAG Pipeline
 ↓
ChromaDB
 ↓
Retriever
 ↓
Filtering
 ↓
Gemini
 ↓
Answer + Sources
```

---

# 34. Key Takeaways

1. **Retrieval quality matters as much as model quality.**
    
2. `k` controls retrieval breadth.
    
3. Distance thresholds can filter weak results.
    
4. Similarity scores should not automatically be treated as percentages.
    
5. Retrieved context should be inspected during debugging.
    
6. Source metadata should be preserved throughout the pipeline.
    
7. Retrieval and generation are separate failure points.
    
8. Faithfulness and correctness are different metrics.
    
9. Ingestion and querying should be separated.
    
10. RAG needs evaluation rather than just a working demo.
    
11. More context isn't automatically better.
    
12. A good RAG system should know when the document doesn't contain the answer.
    

---

# 35. Day 17 Complete 🚀

### What we built

**Advanced RAG Document Chatbot**

### What we learned

**Retrieval Engineering + RAG Evaluation**

### Next

**Day 18 — Hybrid Search**

We will move beyond pure vector similarity and combine:

```text
Keyword Search
      +
Semantic Search
      ↓
Hybrid Retrieval
      ↓
Better Search Results
```

This will introduce another important production RAG concept: **combining lexical and semantic retrieval instead of depending on only one search strategy.**