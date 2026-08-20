# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 11 – LangChain + RAG Engineering

---

# 🎯 Today's Goal

Today's objective was to understand how LangChain can simplify the development of RAG applications.

We converted our previous RAG implementation into a LangChain-based pipeline and explored:

- LangChain
- ChromaDB
- Retrievers
- Prompt Templates
- LCEL
- RunnablePassthrough
- Output Parsers
- Gemini
- Source Display
- Similarity Scores
- Top-K Retrieval
- Retrieval Evaluation

The goal was to move from a manually connected RAG pipeline toward a more structured AI application.

---

# 🧠 What is LangChain?

LangChain is a framework for building applications powered by Large Language Models.

It provides components for connecting:


Models
+
Prompts
+
Retrievers
+
Vector Databases
+
Tools
+
Output Parsers
+
Application Logic


Instead of manually connecting every component, LangChain provides reusable abstractions for building AI workflows.

---

# 🏗️ LangChain RAG Architecture

Our application evolved into:

                    User Question

                          │

                          ▼

                    LangChain

                    Retriever

                          │

                          ▼

                       ChromaDB

                          │

                          ▼

                  Relevant Documents

                          │

                          ▼

                  Context + Question

                          │

                          ▼

                  Prompt Template

                          │

                          ▼

                       Gemini

                          │

                          ▼

                   Output Parser

                          │

                          ▼

                     AI Answer

                          │

                          ▼

                     📚 Sources

---

# 🔎 LangChain Retriever

A retriever is responsible for finding relevant documents from a knowledge source.

We created a retriever from our ChromaDB vector store.

Conceptually:

Question

   ↓

Retriever

   ↓

Relevant Documents

The retriever hides some of the lower-level vector database operations and gives us a simple interface for retrieving documents.

---

# 🗄️ ChromaDB + LangChain

Our existing ChromaDB knowledge base was connected to LangChain.

The overall flow is:

Knowledge Base

      ↓

Embeddings

      ↓

ChromaDB

      ↓

LangChain Vector Store

      ↓

Retriever

This allowed the existing vector database to become part of a LangChain RAG pipeline.

---

# 📝 Prompt Templates

Instead of manually constructing prompts using large strings, LangChain provides prompt templates.

A prompt can contain variables such as:

Context:

{context}

  

Question:

{question}

This separates:

Prompt Structure

from:

Actual User Input

This makes prompts easier to maintain and reuse.

---

# 🔗 LCEL

LCEL stands for:

**LangChain Expression Language**

It allows LangChain components to be connected together using a pipeline-style syntax.

For example:

Input

  ↓

Retriever

  ↓

Prompt

  ↓

LLM

  ↓

Output Parser

This can be represented as a chain:

chain = (

    prompt

    | llm

    | parser

)

The `|` operator represents the flow of data between components.

---

# 🔄 RunnablePassthrough

`RunnablePassthrough` allows the original input to pass through the chain unchanged.

In our RAG pipeline we need both:

Question

+

Retrieved Context

Therefore:

{

    "context": retriever,

    "question": RunnablePassthrough()

}

means:

Question

    ├──────────────→ Retriever → Context

    │

    └──────────────→ Question

Both are then passed to the prompt.

---

# 📦 StrOutputParser

The LLM returns a structured response.

`StrOutputParser` converts the model output into a simple string.

The flow becomes:

Gemini Response

      ↓

StrOutputParser

      ↓

Plain Text Answer

This makes the final result easier to display in our application.

---

# 🤖 Gemini

Gemini acts as the generation component of our RAG system.

We used:

gemini-2.5-flash

The model receives:

Retrieved Context

+

User Question

and generates a grounded response.

---

# 🧩 Complete LCEL RAG Chain

Our chain conceptually became:

                    Question

                       │

             ┌─────────┴─────────┐

             ↓                   ↓

         Retriever      RunnablePassthrough

             ↓                   ↓

          Context             Question

             └─────────┬─────────┘

                       ↓

                 Prompt Template

                       ↓

                     Gemini

                       ↓

                StrOutputParser

                       ↓

                    Answer

---

# 📚 Source Display

A major improvement was displaying the documents used during retrieval.

Instead of showing only:

Answer

we now show:

Answer

  

📚 Sources

  

1. Work From Home Policy

2. Company Working Hours

This makes the RAG application more transparent.

Users can understand which knowledge-base documents were retrieved for their question.

---

# 🔎 Retrieval Quality

We discovered an important RAG engineering concept:

Top-K Retrieval

≠

Guaranteed Relevance

For example:

Question:

What is the maternity leave policy?

  

Retrieved:

1. Leave Policy

2. Work From Home Policy

The retriever may return the closest available documents even when the knowledge base does not actually contain the required answer.

Therefore:

Retrieval

   ↓

Does not automatically mean

   ↓

Correct Information

Retrieval quality must be evaluated.

---

# 🎯 Top-K Retrieval

`k` represents the number of documents retrieved.

For example:

search_kwargs={"k": 2}

means:

Question

   ↓

Retrieve 2 documents

A larger `k` provides more context but can also introduce more irrelevant information.

Conceptually:

Small k

 ↓

Less context

 ↓

Less noise

while:

Large k

 ↓

More context

 ↓

Potentially more noise

Choosing an appropriate `k` is therefore an important RAG tuning decision.

---

# 📐 Similarity Scores

We also tested:

similarity_search_with_score()

This allowed us to inspect:

Document

+

Similarity / Distance Score

Conceptually:

Smaller Distance

        ↓

More Similar

        ↓

Potentially More Relevant

The exact score threshold should not be chosen blindly because the appropriate values depend on factors such as:

- Embedding model
- Distance metric
- Document structure
- Chunking strategy
- Domain
- Query type

---

# 🧪 Retrieval Evaluation

We tested questions such as:

What are the standard working hours?

  

What is the work from home policy?

  

How do I contact IT support?

  

What employee benefits are available?

  

What is the maternity leave policy?

  

What is the company's stock price?

The purpose was to compare:

Relevant Questions

against:

Questions Not Covered by the Knowledge Base

This introduced the idea of **retrieval evaluation**.

---

# 🚫 Hallucination and Retrieval Failure

There are two different problems:

Problem 1

Retriever finds poor context

  

Problem 2

LLM generates an unsupported answer

A reliable RAG system needs to address both.

Our prompt already instructed Gemini:

Use only the provided context.

  

Do not use outside knowledge.

  

Do not invent information.

  

If the answer is unavailable,

say that there is not enough information

in the knowledge base.

This provides an additional layer of protection against hallucination.

---

# 🧠 Important RAG Insight

A RAG system is not simply:

Vector Database

+

LLM

A reliable RAG system requires multiple stages:

Document Quality

      ↓

Chunking

      ↓

Embedding Quality

      ↓

Retrieval Quality

      ↓

Context Quality

      ↓

Prompt Quality

      ↓

LLM Generation

      ↓

Evaluation

A weakness in any stage can affect the final answer.

---

# 🏗️ Project Architecture

Our project is now structured more like an actual AI application:

langchain-basics/

│

├── .gitignore

├── knowledge_base.txt

├── main.py

└── rag.py

Generated files such as:

.venv/

.env

__pycache__/

chroma_db/

should not be committed to Git.

The vector database can be recreated from the knowledge base when required.

---

# 🛠️ Technologies Used

- Python
- LangChain
- LangChain Expression Language (LCEL)
- ChromaDB
- Hugging Face Embeddings
- Sentence Transformers
- Google Gemini
- Google GenAI
- python-dotenv

---

# 🌍 Real-World Applications

LangChain-based RAG systems can be used for:

- Enterprise Knowledge Assistants
- Internal Company Search
- Customer Support
- HR Assistants
- Documentation Assistants
- Technical Support
- Product Knowledge Systems
- Legal Document Assistants
- Research Assistants

---

# 🧠 Key Components

|Component|Role|
|---|---|
|Knowledge Base|Source of information|
|Embeddings|Represents semantic meaning|
|ChromaDB|Stores and retrieves vectors|
|Retriever|Finds relevant documents|
|Prompt Template|Structures the LLM input|
|LCEL|Connects LangChain components|
|RunnablePassthrough|Passes original input through the chain|
|Gemini|Generates the answer|
|StrOutputParser|Converts model output to text|
|Sources|Shows retrieved documents|
|Evaluation|Measures retrieval quality|

---

# 🎯 Key Takeaways

- LangChain provides reusable components for building LLM applications.
- Retrievers simplify interaction with vector databases.
- LCEL allows AI components to be connected as pipelines.
- `RunnablePassthrough` can preserve the original user question.
- Prompt templates make prompts reusable and maintainable.
- `StrOutputParser` converts model responses into usable text.
- RAG can return both answers and source documents.
- Top-K retrieval does not guarantee relevance.
- Similarity scores help inspect retrieval quality.
- Retrieval quality is a critical part of RAG engineering.
- RAG systems should be evaluated instead of being assumed to work correctly.
- Production RAG requires attention to both retrieval and generation.

---

# 🎯 Interview Corner

## Q1. What is LangChain?

LangChain is a framework for developing applications powered by Large Language Models by connecting models with prompts, retrievers, tools, memory, and other components.

---

## Q2. What is LCEL?

LCEL stands for LangChain Expression Language. It provides a way to compose LangChain components into pipelines using expressions such as:

prompt | llm | parser

---

## Q3. What is a Retriever?

A retriever finds documents relevant to a user's query from a knowledge source such as a vector database.

---

## Q4. What does `k` mean in retrieval?

`k` represents the number of documents returned by the retriever.

For example:

k=3

retrieves the top three documents.

---

## Q5. Does Top-K retrieval guarantee relevant documents?

No. Top-K retrieval returns the closest documents according to the configured similarity mechanism, but the returned documents may still be irrelevant to the actual question.

---

## Q6. Why display sources in a RAG application?

Displaying sources improves transparency and allows users to understand which documents were used to generate the answer.

---

## Q7. Why is retrieval evaluation important?

A RAG system can produce poor answers even when the LLM itself is capable if the retriever provides irrelevant or incomplete context. Retrieval quality therefore needs to be tested independently.

---

# 🧪 Practical Interview Scenario

### Interviewer:

Your RAG application retrieves documents, but users complain that the answers are sometimes incorrect. What would you investigate?

### Expected Answer:

I would first inspect the retrieval results rather than immediately changing the LLM. I would check the retrieved documents, similarity scores, Top-K value, chunking strategy, embedding model, and whether irrelevant context is being passed to the LLM. I would then evaluate retrieval quality using representative questions and improve the retrieval pipeline before changing the generation component.

---

# 🏆 Project Progress

## LangChain RAG Knowledge Assistant

Features completed:

- ✅ Knowledge Base
- ✅ Document Chunking
- ✅ Embeddings
- ✅ ChromaDB
- ✅ LangChain Vector Store
- ✅ LangChain Retriever
- ✅ Prompt Template
- ✅ LCEL
- ✅ RunnablePassthrough
- ✅ Gemini Integration
- ✅ StrOutputParser
- ✅ Grounded Generation
- ✅ Source Display
- ✅ Top-K Retrieval
- ✅ Similarity Score Testing
- ✅ Retrieval Evaluation
- ✅ Hallucination Testing

---

# 🚀 Day 11 Summary

Day 9 introduced the fundamentals of RAG.

Day 10 turned the RAG pipeline into an AI Knowledge Assistant with a basic UI.

Day 11 introduced LangChain and improved the engineering structure of the RAG system.

The progression is:

Day 9

RAG Fundamentals

      ↓

Day 10

AI Knowledge Assistant

      ↓

Day 11

LangChain + RAG

      ↓

Retriever

      ↓

LCEL

      ↓

Gemini

      ↓

Sources

      ↓

Retrieval Evaluation

We have now moved from a basic RAG implementation toward a more structured AI Engineering workflow.

---

# 🚀 Next Step

## Advanced RAG

The next phase will focus on improving the reliability and capabilities of our RAG systems.

Topics will include:

- Better retrieval strategies
- Retrieval evaluation
- Advanced chunking
- Metadata filtering
- Reranking
- Hybrid search
- Query transformation
- Context optimization
- RAG evaluation

The goal is to move from:

Basic RAG

to:

Reliable RAG System