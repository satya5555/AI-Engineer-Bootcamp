## 🎯 Objective

Learn how AI applications ingest external documents and convert them into data that an LLM can understand.

Today's project:

> **Build a PDF Chat application that loads a PDF, extracts its contents, preserves page metadata, and answers questions using Gemini.**

---

# 🧠 1. Why Document Loaders?

LLMs cannot automatically understand every file format used by users.

For example:

```text
PDF
Word
CSV
Markdown
Web page
Text file
```

A document loader acts as an adapter between the external document and the AI application.

```text
External Document
       ↓
Document Loader
       ↓
AI-readable Documents
```

LangChain provides loaders for many document formats.

|Format|Example Loader|
|---|---|
|PDF|`PyPDFLoader`|
|Text|`TextLoader`|
|CSV|`CSVLoader`|
|Web page|`WebBaseLoader`|
|Word|`UnstructuredWordDocumentLoader`|
|Markdown|`UnstructuredMarkdownLoader`|

---

# 📄 2. PDF Loading

For today's project we used:

```python
from langchain_community.document_loaders import PyPDFLoader
```

The loader is initialized with the PDF path:

```python
loader = PyPDFLoader(file_path)
```

Then the document is loaded:

```python
documents = loader.load()
```

For a three-page PDF:

```text
PDF
 ↓
PyPDFLoader
 ↓
3 Document objects
```

---

# 🧩 3. LangChain Document

The loader does not simply return one large string.

It returns `Document` objects.

Conceptually:

```python
Document(
    page_content="The content of the page...",
    metadata={
        "page": 0,
        "source": "sample.pdf"
    }
)
```

The two most important properties are:

### `page_content`

Contains the extracted text.

```python
document.page_content
```

### `metadata`

Contains information about the document and its origin.

```python
document.metadata
```

Our PDF produced metadata similar to:

```python
{
    "source": "documents/sample.pdf",
    "total_pages": 3,
    "page": 0,
    "page_label": "1"
}
```

Metadata becomes extremely important for source tracking and RAG.

---

# 🏗️ 4. Project Architecture

Today's application:

```text
User
 ↓
Streamlit UI
 ↓
PDF Upload
 ↓
Temporary File
 ↓
PDFLoader
 ↓
Document Objects
 ↓
Page Content + Metadata
 ↓
Context
 ↓
Gemini
 ↓
Answer
```

---

# 📁 5. Project Structure

```text
ai-pdf-chat/
│
├── app/
│   ├── __init__.py
│   ├── loader.py
│   └── chat.py
│
├── documents/
│   └── sample.pdf
│
├── main.py
├── ui.py
├── requirements.txt
├── .env
└── .gitignore
```

The actual PDF should remain local when it contains private information.

---

# 🔧 6. PDF Loader

`app/loader.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:
    def load(self, file_path: str):
        loader = PyPDFLoader(file_path)

        documents = loader.load()

        return documents
```

The application now has a small abstraction around the LangChain loader.

This means document-loading logic isn't scattered throughout the application.

---

# 🧪 7. Testing the Loader

We tested the loader using:

```python
from app.loader import PDFLoader


pdf_loader = PDFLoader()

documents = pdf_loader.load(
    "documents/sample.pdf"
)

print(f"Pages loaded: {len(documents)}")

for document in documents:
    print("=" * 60)

    print("Metadata:")
    print(document.metadata)

    print("\nContent:")
    print(document.page_content[:500])
```

The result showed:

```text
Pages loaded: 3
```

and each page was represented by a separate `Document`.

---

# 🤖 8. Connecting Documents to Gemini

The next step was to give the extracted document content to Gemini.

`app/chat.py`

```python
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class PDFChat:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-3.6-flash"
            ),
            google_api_key=os.getenv(
                "GEMINI_API_KEY"
            ),
        )

    def answer(self, question: str, documents) -> str:

        context_parts = []

        for document in documents:
            page = document.metadata.get(
                "page_label"
            )

            context_parts.append(
                f"[Page {page}]\n"
                f"{document.page_content}"
            )

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are a helpful document assistant.

Answer the user's question using ONLY the information
provided in the document below.

When answering, mention the page number where the
information was found when possible.

If the answer cannot be found in the document, say:
"I couldn't find that information in the document."

Document:
{context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts = []

            for block in content:
                if (
                    isinstance(block, dict)
                    and block.get("type") == "text"
                ):
                    text_parts.append(
                        block.get("text", "")
                    )

            return "\n".join(text_parts)

        return str(content)
```

---

# 📍 9. Page-Aware Context

Instead of sending only:

```text
some extracted text
```

we created context like:

```text
[Page 1]
...

[Page 2]
Allergies
NO KNOWN ALLERGIES

[Page 3]
...
```

This allows the model to associate information with its source page.

The resulting answer was:

```text
Based on Page 2 of the document, the patient has
"NO KNOWN ALLERGIES".
```

---

# 🎯 10. Grounding

We explicitly instructed the model:

```text
Answer using ONLY the information provided
in the document.
```

And:

```text
If the answer cannot be found in the document, say:
"I couldn't find that information in the document."
```

We tested this with a question that wasn't present in the PDF:

```text
What is the patient's favorite programming language?
```

The model correctly returned:

```text
I couldn't find that information in the document.
```

This is an early example of **grounding**.

---

# 🧠 11. Grounded vs Ungrounded AI

Without grounding:

```text
Question
   ↓
LLM
   ↓
Answer
```

The model can potentially use information from its general knowledge.

With our document grounding:

```text
Question
   ↓
Document Context
   ↓
LLM
   ↓
Grounded Answer
```

The goal is to constrain the answer to the supplied source.

---

# 💻 12. Command-Line PDF Chat

`main.py`

```python
from app.loader import PDFLoader
from app.chat import PDFChat


pdf_loader = PDFLoader()
chat = PDFChat()

documents = pdf_loader.load(
    "documents/sample.pdf"
)

print(f"Loaded {len(documents)} pages.")

question = input(
    "\nAsk a question about the PDF: "
)

answer = chat.answer(
    question,
    documents
)

print("\nAnswer:")
print(answer)
```

Run:

```powershell
python main.py
```

---

# 🌐 13. Streamlit UI

We then upgraded the project into a simple web application.

The UI supports:

- PDF upload
    
- page loading
    
- question input
    
- AI answer
    
- error handling
    

The architecture is:

```text
Browser
   ↓
Streamlit
   ↓
Upload PDF
   ↓
Temporary File
   ↓
PDFLoader
   ↓
PDFChat
   ↓
Gemini
   ↓
Answer
```

---

# 📦 14. Temporary Uploaded Files

Streamlit provides the uploaded PDF as an uploaded object.

Our loader expects a file path.

Therefore:

```text
Uploaded PDF
     ↓
Temporary file
     ↓
PDFLoader
     ↓
Documents
     ↓
Gemini
     ↓
Answer
     ↓
Temporary file deleted
```

The temporary file is cleaned up with:

```python
finally:
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
```

This is an important application-engineering pattern.

---

# 🔐 15. Privacy Consideration

The test PDF contained sensitive personal information.

Therefore the PDF should **not** be committed to GitHub.

Our `.gitignore` contains:

```gitignore
.venv/
__pycache__/
*.pyc
.env
documents/*.pdf
```

The code can be public while private user documents remain local.

---

# ⚠️ 16. PDF Extraction Limitations

Document loading does not guarantee perfect document understanding.

PDF extraction can have problems with:

- unusual fonts
    
- icons
    
- tables
    
- multiple columns
    
- headers and footers
    
- scanned documents
    
- complex layouts
    
- images containing text
    

For example, some PDF icons were extracted as unusual characters.

This teaches an important engineering lesson:

> **Document loading is not the same as perfect document understanding.**

Production document pipelines often require additional parsing, OCR, layout analysis, or specialized loaders depending on the document type.

---

# 🚨 17. The Biggest Limitation of Today's Approach

Our current approach sends the **entire document** to the LLM.

```text
PDF
 ↓
ALL pages
 ↓
Prompt
 ↓
LLM
```

This works for a small three-page document.

But imagine a 500-page document:

```text
500 pages
   ↓
Entire document
   ↓
Huge prompt
   ↓
High token usage
   ↓
Higher latency
   ↓
Higher cost
   ↓
Possible context-window problems
```

We need a better solution.

That solution is **chunking + retrieval**.

---

# 🔄 18. Document QA vs RAG

Today's system:

```text
PDF
 ↓
Load
 ↓
ALL document content
 ↓
LLM
 ↓
Answer
```

A RAG system will eventually look like:

```text
PDF
 ↓
Load
 ↓
Split into chunks
 ↓
Embeddings
 ↓
Vector Database
 ↓
Retriever
 ↓
Relevant chunks
 ↓
LLM
 ↓
Answer + Sources
```

The key difference:

> Today's application gives the LLM the whole document.

> RAG retrieves only the relevant pieces.

---

# 🧠 19. Why Metadata Matters for RAG

Suppose we eventually have:

```text
Chunk 1 → Page 1
Chunk 2 → Page 2
Chunk 3 → Page 3
...
Chunk 1000 → Page 250
```

When the retriever finds:

```text
Chunk 731
```

its metadata can tell us:

```text
Source: annual_report.pdf
Page: 184
```

We can then provide:

```text
Answer:
...

Sources:
annual_report.pdf — Page 184
```

Therefore:

> **Metadata isn't decoration. It enables traceability.**

---

# 💼 20. Practical Real-World Scenario

Imagine an enterprise employee uploads:

```text
Company HR Policy.pdf
```

and asks:

```text
How many days of parental leave are available?
```

A simple document QA system can load the document and ask the LLM.

But a production system should eventually:

```text
HR Policy
 ↓
Parse
 ↓
Chunk
 ↓
Embed
 ↓
Vector DB
 ↓
Retrieve relevant policy section
 ↓
LLM
 ↓
Answer
 ↓
Source + page
```

This makes the system more scalable and auditable.

---

# 🎤 21. Interview Corner

### Q1. What is a document loader?

A component that loads external documents and converts them into a representation usable by an AI application.

---

### Q2. What does `PyPDFLoader` do?

It extracts content from a PDF and represents the extracted pages as LangChain `Document` objects.

---

### Q3. What is a LangChain `Document`?

A structured representation containing:

```text
page_content
metadata
```

---

### Q4. Why is metadata important?

It allows the application to preserve information about the origin of content, such as:

```text
source
page
document identifier
```

This enables source attribution and traceability.

---

### Q5. Is document loading the same as RAG?

No.

Document loading is the ingestion stage.

RAG additionally involves retrieving relevant document content for a user query.

---

### Q6. Why shouldn't we send an entire large PDF to an LLM?

Because it can cause:

- high token usage
    
- higher cost
    
- higher latency
    
- context-window limitations
    
- unnecessary irrelevant context
    

---

### Q7. What comes after document loading?

Typically:

```text
Loading
 ↓
Chunking
 ↓
Embedding
 ↓
Indexing
 ↓
Retrieval
 ↓
Generation
```

---

# 🏆 22. Project Completed

## AI PDF Chat

### Features

- PDF upload
    
- PDF parsing
    
- Page extraction
    
- LangChain `Document` objects
    
- Metadata preservation
    
- Gemini integration
    
- Grounded answers
    
- Page-aware responses
    
- Unknown-answer handling
    
- Streamlit UI
    
- Temporary-file cleanup
    
- Private PDF protection through `.gitignore`
    

---

# 🧠 23. Day 15 Mental Model

Remember:

> **A document loader is the ingestion gateway into your AI application.**

The core pipeline:

```text
Document
   ↓
Loader
   ↓
Document objects
   ↓
page_content + metadata
   ↓
AI application
```

And the future RAG pipeline:

```text
Document
   ↓
Loader
   ↓
Splitter
   ↓
Embeddings
   ↓
Vector DB
   ↓
Retriever
   ↓
LLM
```

---

# 📌 24. Key Takeaways

- Document loaders connect files to AI applications.
    
- `PyPDFLoader` can extract PDF pages.
    
- LangChain represents extracted content as `Document` objects.
    
- `page_content` contains the text.
    
- `metadata` contains source information.
    
- Metadata enables traceability.
    
- Grounding helps constrain answers to supplied content.
    
- Sending an entire large document doesn't scale.
    
- Chunking and retrieval solve this problem.
    
- Document loading is an ingestion step, not the complete RAG pipeline.
    
- Private documents should not be committed to public repositories.
    

---

# 🚀 Next Step

### Day 16 — Text Splitters & Chunking

We'll take:

```text
3-page document
```

and learn how to transform it into:

```text
Document
 ↓
Chunks
 ↓
Chunk metadata
```

We'll investigate:

- Why chunking is necessary
    
- Chunk size
    
- Chunk overlap
    
- Recursive character splitting
    
- Why naive splitting fails
    
- How chunk size affects retrieval
    
- How chunking affects token cost
    
- Practical chunking experiments
    

This is one of the most important foundations of **RAG engineering**.

> **Day 15 complete — Document ingestion.**
> 
> **Day 16 begins the journey toward efficient retrieval.**