## 🎯 Objective

Learn how to divide large documents into smaller, meaningful pieces called **chunks**, while understanding how chunk size and overlap affect retrieval quality, context, cost, and latency.

Today's project:

> **Build a Smart Document Chunker and experiment with chunk size and chunk overlap.**

---

# 🧠 1. Why Do We Need Chunking?

Sending an entire large document to an LLM is inefficient.

For example:

```text
500-page document
       ↓
Extract everything
       ↓
Send entire document to LLM
```

This can lead to:

- Large prompts
    
- High token usage
    
- Higher cost
    
- Increased latency
    
- Irrelevant context
    
- Context-window limitations
    

Instead, we divide the document into smaller pieces.

```text
Document
   ↓
Chunking
   ↓
Chunk 1
Chunk 2
Chunk 3
...
Chunk N
```

These chunks can later be embedded, stored, and retrieved.

---

# 📦 2. What Is a Chunk?

A **chunk** is a smaller piece of document content.

For example:

```text
Original document
────────────────────────────────

Paragraph 1
Paragraph 2
Paragraph 3
Paragraph 4
```

After chunking:

```text
Chunk 1
Paragraph 1

Chunk 2
Paragraph 2

Chunk 3
Paragraph 3
```

The goal is not simply to make text smaller.

The goal is:

> **Create chunks that preserve enough meaning to be useful for retrieval.**

---

# 📏 3. Chunk Size

One important parameter is:

```python
chunk_size
```

Example:

```python
chunk_size=500
```

For `RecursiveCharacterTextSplitter`, chunk size is based on characters.

However:

> `chunk_size` is a target rather than a guarantee that every chunk will contain exactly that number of characters.

The splitter attempts to respect useful text boundaries.

---

# 🔄 4. Chunk Overlap

Chunk overlap is the amount of content shared between neighboring chunks.

Conceptually:

```text
Chunk 1
A B C D E F G

Chunk 2
        E F G H I J K
```

The overlapping content is:

```text
E F G
```

In LangChain:

```python
chunk_overlap=50
```

requests approximately 50 characters of overlap where appropriate.

---

# 🧠 5. Why Is Overlap Important?

Important information can cross a chunk boundary.

For example:

```text
Chunk 1:
The company introduced an AI system that
improved customer support

Chunk 2:
improved customer support response time by 40%.
```

The repeated context helps preserve meaning.

Therefore:

> **Overlap reduces the risk of losing context at chunk boundaries.**

---

# 🔧 6. RecursiveCharacterTextSplitter

We used:

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
```

This splitter attempts to split text using a hierarchy of separators rather than blindly cutting at arbitrary positions.

Conceptually:

```text
Larger text boundary
       ↓
Paragraph
       ↓
Line
       ↓
Smaller boundary
       ↓
Character
```

The exact behavior depends on the configured separators and document structure.

---

# 🏗️ 7. Project Architecture

Today's pipeline:

```text
Document
   ↓
TextChunker
   ↓
RecursiveCharacterTextSplitter
   ↓
Chunks
   ↓
Metadata preserved
```

Future RAG pipeline:

```text
Document
   ↓
Loader
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
LLM
```

---

# 📁 8. Project Structure

```text
ai-text-chunker/
│
├── app/
│   ├── __init__.py
│   └── chunker.py
│
├── documents/
│   └── sample.txt
│
├── main.py
├── requirements.txt
└── .gitignore
```

---

# 💻 9. Installing the Splitter

We installed:

```powershell
pip install langchain-text-splitters
```

Requirements include:

```text
langchain-text-splitters
```

---

# 🔨 10. TextChunker

`app/chunker.py`

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split(self, documents):
        return self.splitter.split_documents(
            documents
        )
```

---

# 📄 11. Creating a Document

We used LangChain's `Document`:

```python
from langchain_core.documents import Document
```

Then:

```python
document = Document(
    page_content=text,
    metadata={
        "source": "documents/sample.txt"
    }
)
```

This gives us:

```text
Document
├── page_content
└── metadata
```

---

# 🔗 12. Using `split_documents()`

We used:

```python
chunks = chunker.split(
    [document]
)
```

Internally this uses:

```python
self.splitter.split_documents(
    documents
)
```

This is useful because we're splitting existing `Document` objects rather than raw strings.

The resulting chunks remain `Document` objects.

Therefore metadata can be preserved:

```text
Original Document
       │
       ├── Chunk 1 + metadata
       ├── Chunk 2 + metadata
       ├── Chunk 3 + metadata
       └── Chunk 4 + metadata
```

---

# 🧪 13. Chunking Experiment

Our original document contained approximately:

```text
940 characters
```

With a smaller chunk configuration, we observed:

```text
9 chunks
```

With a larger chunk configuration, we observed:

```text
4 chunks
```

This demonstrated:

```text
Smaller chunk size
      ↓
More chunks
      ↓
More granular information
```

while:

```text
Larger chunk size
      ↓
Fewer chunks
      ↓
More context per chunk
```

---

# 🔬 14. Demonstrating Overlap

We then used:

```python
chunk_size=150
chunk_overlap=50
```

The resulting chunks showed repeated content.

For example:

```text
Chunk 1:
data and make predictions without being explicitly
programmed for every possible situation.

Chunk 2:
data and make predictions without being explicitly
programmed for every possible situation.
Large language models...
```

The repeated content demonstrates chunk overlap.

---

# ⚠️ 15. Important Chunking Observation

We initially expected:

```text
chunk_size=300
chunk_overlap=100
```

to always produce exactly 100 repeated characters.

That isn't necessarily what happens.

`RecursiveCharacterTextSplitter` tries to respect useful separators and boundaries.

Therefore:

> **Chunk size and overlap are configuration targets, not necessarily exact boundaries for every chunk.**

---

# ⚖️ 16. Chunk Size Tradeoff

### Too Small

```text
Small chunks
    ↓
Less context
    ↓
Potentially incomplete meaning
```

### Too Large

```text
Large chunks
    ↓
More irrelevant information
    ↓
Less precise retrieval
    ↓
Higher token usage
```

The goal is an appropriate balance.

---

# 🔄 17. Chunk Overlap Tradeoff

### Low overlap

Advantages:

- Less duplication
    
- Lower storage
    
- Lower token usage
    

Risk:

- Context can be lost at boundaries
    

### High overlap

Advantages:

- Better continuity
    
- More repeated context
    

Risks:

- More storage
    
- More duplicated text
    
- More tokens
    

Therefore:

> **More overlap isn't automatically better.**

---

# 🔎 18. Chunking and Retrieval

Chunking becomes particularly important when retrieval is introduced.

Suppose:

```text
Chunk 42:
The company introduced a new support system.
The system reduced response time by 40%.
```

A user asks:

> How much did response time improve?

A good chunk contains the complete relevant context.

But poor chunking might separate related information.

Therefore:

> **Chunking quality directly affects retrieval quality.**

---

# 🧩 19. Chunking vs Retrieval

These are different concepts.

### Chunking

```text
Document
   ↓
Smaller pieces
```

### Retrieval

```text
Question
   ↓
Find relevant pieces
```

Together:

```text
Document
   ↓
Chunking
   ↓
Chunks
   ↓
Embeddings
   ↓
Vector Database
       ↑
       │
    Question
```

---

# 💼 20. Enterprise Scenario

Imagine a:

```text
500-page technical equipment manual
```

containing:

- Installation procedures
    
- Troubleshooting instructions
    
- Safety warnings
    
- Configuration steps
    
- Maintenance procedures
    
- Tables
    
- Technical explanations
    

A user asks:

> What should I do if the cooling unit shows error E42?

We don't want:

```text
500 pages
    ↓
LLM
```

Instead:

```text
500-page manual
       ↓
Chunking
       ↓
Chunks
       ↓
Embeddings
       ↓
Vector Database
       ↓
Relevant troubleshooting chunks
       ↓
LLM
       ↓
Answer + Source
```

---

# 🎯 21. Choosing Chunk Parameters

There is no universal perfect configuration.

For example:

```text
Option A
chunk_size = 100
chunk_overlap = 10

Option B
chunk_size = 500
chunk_overlap = 50

Option C
chunk_size = 1000
chunk_overlap = 200
```

For a technical manual, a larger chunk such as Option C can be a reasonable **starting hypothesis** because troubleshooting procedures may require surrounding context.

However, it must be evaluated.

Possible problems include:

- too much irrelevant content
    
- less precise retrieval
    
- increased token usage
    
- increased storage requirements
    

Therefore:

> **Chunking parameters should be experimentally evaluated rather than chosen permanently by intuition.**

---

# 📊 22. What Should We Evaluate?

When tuning chunking for a RAG system, useful measurements include:

### Retrieval relevance

Did we retrieve the correct section?

### Context completeness

Did the retrieved chunk contain enough information?

### Context precision

How much of the retrieved content was actually useful?

### Answer correctness

Did the LLM produce the correct answer?

### Latency

How quickly did the system respond?

### Token usage

How much context did we send to the model?

### Cost

How expensive is the pipeline at scale?

---

# 🎤 23. Interview Corner

### Q1. Why do we chunk documents?

To divide large documents into manageable pieces that can be efficiently embedded, indexed, retrieved, and supplied to an LLM.

### Q2. What is chunk overlap?

The shared content between neighboring chunks.

### Q3. Why use overlap?

To preserve context when related information crosses a chunk boundary.

### Q4. What happens if chunks are too small?

They may not contain enough context to represent the meaning of the information.

### Q5. What happens if chunks are too large?

They may contain unnecessary information and increase retrieval noise and token usage.

### Q6. Is there a universal best chunk size?

No. It depends on the document, application, retrieval strategy, model, and workload.

### Q7. Difference between `split_text()` and `split_documents()`?

`split_text()` works with raw text.

`split_documents()` works with LangChain `Document` objects and allows metadata to be preserved.

---

# 🔐 24. Production Considerations

Production chunking may need more than simple character splitting.

Depending on the document, we may need:

- Semantic chunking
    
- Heading-aware chunking
    
- Page-aware chunking
    
- Table-aware processing
    
- Layout-aware parsing
    
- OCR
    
- Domain-specific chunking
    

For example, a technical manual may have:

```text
Section
   ↓
Subsection
   ↓
Procedure
   ↓
Steps
   ↓
Warnings
```

Blindly splitting characters may destroy this structure.

---

# 🧠 25. Day 16 Mental Model

Remember:

> **Chunking is not just splitting text. It is designing the units that your retrieval system will search over.**

Think:

```text
Document
   ↓
What should one retrievable unit contain?
   ↓
Chunk design
   ↓
Retrieval quality
```

Therefore:

> **Good chunking creates better retrieval candidates.**

---

# 🏆 26. Project Completed

## Smart Document Chunker

### Features

- LangChain document processing
    
- Recursive character splitting
    
- Configurable chunk size
    
- Configurable chunk overlap
    
- Metadata preservation
    
- Chunk inspection
    
- Chunk-size experimentation
    
- Overlap experimentation
    
- Retrieval trade-off analysis
    

---

# 📌 27. Key Takeaways

- Large documents should not always be passed entirely to an LLM.
    
- Chunking divides documents into retrievable units.
    
- `chunk_size` controls the approximate chunk size.
    
- `chunk_overlap` preserves context across boundaries.
    
- `RecursiveCharacterTextSplitter` attempts to respect useful text boundaries.
    
- Chunk size is a target, not necessarily an exact character count.
    
- Overlap is useful but introduces duplication.
    
- Small chunks can lose context.
    
- Large chunks can introduce irrelevant context.
    
- Chunking directly affects retrieval quality.
    
- Chunking parameters should be evaluated rather than blindly fixed.
    
- Metadata should be preserved for source traceability.
    
- Production systems may require semantic or structure-aware chunking.
    

---

# 🚀 Next Step

## Day 17 — Advanced RAG

We will finally connect:

```text
Document
   ↓
Loader
   ↓
Chunks
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
LLM
   ↓
Answer + Sources
```

We'll improve our previous RAG architecture using techniques such as:

- Better chunking
    
- Retrieval configuration
    
- Similarity thresholds
    
- Source handling
    
- Retrieval inspection
    
- Context quality
    
- Failure analysis
    

The goal is to move from:

> **"I built a RAG application."**

to:

> **"I understand how to engineer and evaluate a RAG pipeline."**