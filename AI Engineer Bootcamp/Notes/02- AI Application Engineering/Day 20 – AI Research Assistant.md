## Objective

Build a practical AI Research Assistant that can:

- Accept a research question
    
- Search the web for relevant information
    
- Collect evidence from multiple sources
    
- Use an LLM to synthesize the evidence
    
- Generate a structured research report
    
- Provide source references
    
- Evaluate basic source coverage
    
- Expose the workflow through a Streamlit UI
    

---

# 1. Project Overview

Project:

```text
Projects/ai-research-assistant
```

The application combines the concepts learned throughout Sprint 2:

```text
LangChain
    ↓
Search
    ↓
Evidence Collection
    ↓
LLM Synthesis
    ↓
Source Attribution
    ↓
Evaluation
    ↓
Streamlit UI
```

---

# 2. Research Assistant vs RAG

A traditional RAG application generally works with a known knowledge base:

```text
Question
   ↓
Known Documents
   ↓
Retrieval
   ↓
LLM
   ↓
Answer
```

The Research Assistant introduces an external research step:

```text
Question
   ↓
Web Search
   ↓
Multiple Sources
   ↓
Evidence Collection
   ↓
LLM Synthesis
   ↓
Research Report
```

The key idea is that the assistant first gathers evidence and then uses the evidence to construct the answer.

---

# 3. Architecture

```text
                  User
                   │
                   ↓
             Research Question
                   │
                   ↓
              WebSearch
                   │
                   ↓
              Researcher
                   │
                   ↓
            Evidence Set
          ┌────────┼────────┐
          ↓        ↓        ↓
       Source 1 Source 2 Source 3
          │        │        │
          └────────┼────────┘
                   ↓
              Synthesizer
                   │
                   ↓
              Gemini LLM
                   │
                   ↓
          Structured Research
                Answer
                   │
             ┌─────┴─────┐
             ↓           ↓
          Sources     Evaluator
                         │
                         ↓
                  Evaluation Metrics
                         │
                         ↓
                   Streamlit UI
```

---

# 4. Project Structure

```text
ai-research-assistant/
│
├── app/
│   ├── __init__.py
│   ├── search.py
│   ├── researcher.py
│   ├── synthesizer.py
│   └── evaluator.py
│
├── main.py
├── ui.py
├── requirements.txt
└── .gitignore
```

---

# 5. Web Search Layer

Created:

```text
app/search.py
```

The `WebSearch` class performs web searches and converts raw search results into a consistent structure.

Each result contains:

```text
title
url
snippet
```

Example structure:

```python
{
    "title": "...",
    "url": "...",
    "snippet": "..."
}
```

The project initially used `duckduckgo-search`.

The package produced a rename warning, so it was changed to:

```text
ddgs
```

This demonstrated the importance of keeping external dependencies current.

---

# 6. Researcher Layer

Created:

```text
app/researcher.py
```

The researcher acts as the evidence collection layer.

```text
Research Question
       ↓
    Search
       ↓
Raw Results
       ↓
Structured Evidence
```

The researcher does not generate the final answer.

Instead, it returns structured evidence containing:

```text
Title
URL
Snippet
```

This separation makes the application easier to debug and evaluate.

---

# 7. Synthesis Layer

Created:

```text
app/synthesizer.py
```

The synthesizer uses Gemini to transform the collected evidence into a research report.

The prompt instructs the model to:

- Use only the supplied evidence
    
- Avoid inventing information
    
- Combine information from multiple sources
    
- Identify insufficient evidence
    
- Reference sources
    
- Produce a concise structured report
    

---

# 8. Structured Research Output

The research response was designed around:

```text
Summary
Key Findings
Evidence
Limitations
Sources
```

This is more useful than returning an unstructured paragraph because users can quickly understand:

- The overall answer
    
- Important findings
    
- Supporting evidence
    
- Research limitations
    
- Sources used
    

---

# 9. Source References

The synthesizer was instructed to reference evidence using:

```text
[Source 1]
[Source 2]
[Source 3]
```

This allows the generated answer to be connected back to the evidence collected by the researcher.

Example:

```text
RAG is increasingly used for enterprise knowledge retrieval. [Source 1]
```

---

# 10. Evaluation Layer

Created:

```text
app/evaluator.py
```

The evaluator checks whether the generated research answer references the evidence sources.

The evaluation tracks:

```text
Evidence Count
Sources Used
Source Coverage
Evaluation Status
```

---

# 11. Source Coverage

Source coverage is calculated as:

```text
Sources Referenced
------------------
Total Evidence Sources
```

For example:

```text
Evidence Count = 5
Sources Used = 3
Source Coverage = 0.60
```

This means the generated answer explicitly referenced three of the five collected sources.

---

# 12. Important Evaluation Limitation

Source coverage is **not the same as factual correctness**.

For example:

```text
Source Coverage = 1.0
```

only tells us that the answer referenced the available sources.

It does not prove that:

- Every claim is correct
    
- Every citation supports the claim
    
- The sources themselves are reliable
    
- The answer contains no hallucinations
    

A production research system would require more advanced evaluation such as:

- Citation correctness
    
- Claim verification
    
- Groundedness
    
- Answer relevance
    
- Source quality
    
- LLM-as-a-judge
    
- Human evaluation
    

---

# 13. Gemini Response Handling

During development, Gemini returned response content in different formats.

The response could be:

```text
String
```

or:

```text
List of content blocks
```

The synthesizer was therefore updated to normalize the response into a usable text string.

This prevents structured Gemini responses from appearing as large serialized/Base64-like data in the UI.

---

# 14. Streamlit UI

Created:

```text
ui.py
```

The UI provides:

```text
Research Question
       ↓
     Research
       ↓
Research Answer
       ↓
Sources
       ↓
Evaluation
```

The UI displays:

- Research question input
    
- Research answer
    
- Source list
    
- Evidence snippets
    
- URLs
    
- Evidence count
    
- Sources used
    
- Source coverage
    
- Evaluation status
    

The application can be launched with:

```powershell
python -m streamlit run ui.py
```

Using `python -m streamlit` ensures Streamlit runs through the active Python environment.

---

# 15. Example Research Flow

Example question:

```text
What are the latest applications of RAG in enterprise AI?
```

The system performs:

```text
Question
   ↓
Web Search
   ↓
5 Search Results
   ↓
Evidence Collection
   ↓
Gemini Synthesis
   ↓
Structured Research Report
   ↓
Source References
   ↓
Evaluation
```

---

# 16. Error Handling During Development

### Gemini API quota

The Gemini API can return:

```text
429 RESOURCE_EXHAUSTED
```

when the configured API quota is exceeded.

This is an API/infrastructure limitation rather than an error in the research workflow itself.

### Gemini response format

The LLM response was not always a simple string.

The application was updated to handle both string and list-based content.

### Dependency rename

The original:

```text
duckduckgo-search
```

package produced a warning that it had been renamed.

The project was updated to use:

```text
ddgs
```

---

# 17. Day 20 Key Concepts

### Search

Find potentially relevant external information.

### Evidence

Structured information collected from search results.

### Research

The process of gathering and organizing evidence around a question.

### Synthesis

Combining evidence from multiple sources into a coherent answer.

### Source Attribution

Connecting generated claims to supporting sources.

### Evaluation

Measuring whether the generated response uses the collected evidence.

---

# 18. Interview Questions

### What is an AI Research Assistant?

An AI Research Assistant gathers information from external sources and uses an LLM to synthesize the collected evidence into a structured response.

### How is it different from RAG?

RAG generally retrieves information from a predefined knowledge base, while a research assistant can dynamically gather information from external sources before generating an answer.

### Why separate search and synthesis?

Separation makes the system easier to debug, evaluate, and improve. We can inspect the evidence before it reaches the LLM.

### What is source attribution?

Source attribution connects generated information to the sources used to support it.

### Does source coverage guarantee factual correctness?

No. It only measures whether sources were referenced. Citation correctness and factuality require additional evaluation.

### Why use structured research output?

It makes the answer easier to read, verify, and consume programmatically.

---

# 19. Day 20 Architecture Pattern

The project introduced an important AI application pattern:

```text
Retrieve
   ↓
Collect Evidence
   ↓
Synthesize
   ↓
Attribute
   ↓
Evaluate
```

This pattern will become increasingly important when we move into **AI Agents and AI Systems** in Sprint 3.

---

# 20. Day 20 Status

**Completed ✅**

Built:

- Web search layer
    
- Researcher layer
    
- Evidence collection
    
- Gemini synthesis
    
- Structured research reports
    
- Source references
    
- Research evaluation
    
- Streamlit interface
    
- Response normalization
    
- Basic source-coverage metric
    

## Sprint 2 Status

```text
Day 11  LangChain Fundamentals       ✅
Day 12  Prompt Templates              ✅
Day 13  Memory                        ✅
Day 14  Tool Calling                  ✅
Day 15  Document Loaders              ✅
Day 16  Text Splitters                ✅
Day 17  Advanced RAG                  ✅
Day 18  Hybrid Search                 ✅
Day 19  AI Evaluation                 ✅
Day 20  AI Research Assistant         ✅
```

**Sprint 2 complete. 🎯**

Next:

**Day 21 — AI Agents Introduction: Build a Simple Agent**