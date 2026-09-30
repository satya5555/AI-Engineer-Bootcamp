## Objective

Learn how to evaluate an AI/RAG application systematically instead of judging responses manually.

The Day 19 evaluation layer was added to the existing:

`Projects/ai-hybrid-search`

project.

---

## 1. Why AI Evaluation Matters

An AI application can fail at different stages:

```text
User Question
      ↓
Retrieval
      ↓
Context
      ↓
LLM Generation
      ↓
Final Answer
```

A poor answer does not always mean the LLM is the problem.

The relevant information may not have been retrieved in the first place.

Therefore, evaluation should help identify:

- Retrieval problems
    
- Generation problems
    
- Unsupported questions
    
- Incorrect answers
    
- Evaluation-data problems
    

---

## 2. Evaluation Dataset

Created:

```text
evaluation_questions.json
```

The dataset contains questions, expected answers, and expected keywords.

Example:

```json
{
    "question": "What is the hospital name?",
    "expected_answer": "MEDICOVER HOSPITALS",
    "expected_keywords": ["MEDICOVER"]
}
```

Unsupported questions use an empty keyword list:

```json
{
    "question": "What is the recipe for pasta?",
    "expected_answer": "The information is not available in the document.",
    "expected_keywords": []
}
```

---

## 3. Evaluation Pipeline

Created:

```text
app/evaluator.py
app/metrics.py
evaluate.py
```

The evaluation flow is:

```text
Evaluation Question
        ↓
Hybrid Search
        ↓
Retrieved Documents
        ↓
RAG Answer Generation
        ↓
Evaluation Metrics
        ↓
Result Classification
        ↓
Evaluation Summary
```

---

## 4. Retrieval Hit

The retrieval metric checks whether the retrieved chunks contain the expected information.

```text
Retrieval Hit = 1
```

means relevant information was retrieved.

```text
Retrieval Hit = 0
```

means relevant information was not found in the retrieved chunks.

This helps distinguish retrieval failures from generation failures.

---

## 5. Keyword Match

Keyword matching checks whether important expected terms appear in the generated answer.

Example:

```text
Expected keyword:
MEDICOVER

Generated answer:
MEDICOVER HOSPITALS
```

Result:

```text
Keyword Match = 1.0
```

Text normalization was added so differences such as capitalization, punctuation, and whitespace do not unnecessarily cause failures.

---

## 6. Answer Match

`answer_match()` compares the generated answer against the expected answer.

It first normalizes the text and checks whether the expected answer appears in the generated answer.

If it does not completely match, word overlap is used to calculate a partial score.

This provides a simple deterministic baseline for answer evaluation.

---

## 7. Unsupported Query Evaluation

An important evaluation case is a question that cannot be answered from the document.

Example:

```text
What is the recipe for pasta?
```

Expected behavior:

```text
I could not find the information in the document.
```

Instead of comparing the exact wording of the refusal, a separate:

```text
refusal_match()
```

metric checks whether the system correctly refused to answer.

This avoids false evaluation failures caused by different refusal wording.

---

## 8. Result Classification

Added:

```text
classify_result()
```

The evaluator can classify results as:

### PASS

Relevant information was retrieved and the answer matched the expected answer.

### RETRIEVAL_FAILURE

Relevant information was not retrieved.

### GENERATION_FAILURE

Relevant information was retrieved, but the generated answer did not satisfy the expected answer.

### UNSUPPORTED_QUERY_HANDLED

The question cannot be answered from the document and the system correctly refused.

### UNSUPPORTED_QUERY_FAILURE

The question cannot be answered, but the system failed to handle it correctly.

---

## 9. Evaluation Results

Final evaluation contained five questions:

|Question Type|Result|
|---|---|
|Main topic|PASS|
|Medicine|PASS|
|Patient appetite|PASS|
|Hospital name|PASS|
|Unsupported pasta question|UNSUPPORTED_QUERY_HANDLED|

Final metrics:

```text
Average Retrieval Hit: 1.00
Average Keyword Match: 1.00
Average Answer Match:  1.00
```

---

## 10. Important Finding

The unsupported pasta question exposed an important retrieval limitation.

Although the question was unrelated to the document, the hybrid retriever still returned top-k chunks.

```text
Page 3
Page 2
```

This happens because top-k retrieval always attempts to return candidates.

Therefore:

```text
Retrieved ≠ Relevant
```

This is an important production RAG consideration.

Possible future improvements include:

- Relevance thresholds
    
- Reranking
    
- Better retrieval scoring
    
- Query classification
    
- Retrieval evaluation datasets
    
- LLM-based evaluation
    

---

## 11. Evaluation Data Can Also Fail

During testing, the first evaluation dataset incorrectly expected:

```text
medical
```

for the question:

```text
What is the main topic of the document?
```

The actual answer was:

```text
Discharge Summary
```

The RAG system was correct, but the evaluator produced:

```text
0.00
```

This demonstrated an important principle:

> A bad evaluation dataset can make a good AI system look bad.

Evaluation quality is therefore as important as application quality.

---

## 12. API Quota Issue

During testing, Gemini returned:

```text
429 RESOURCE_EXHAUSTED
```

because the free-tier request quota for the selected model had been exceeded.

This was an API quota limitation rather than an application evaluation failure.

Earlier successful evaluation runs already verified the evaluation pipeline.

---

## 13. Day 19 Architecture

```text
                Evaluation Dataset
                       │
                       ↓
                 Evaluation Runner
                       │
                       ↓
                 Hybrid Retrieval
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        Keyword Search     Semantic Search
             │                   │
             └─────────┬─────────┘
                       ↓
                    RRF
                       ↓
                 Retrieved Chunks
                       ↓
                    Gemini
                       ↓
                  Final Answer
                       ↓
              ┌────────┴────────┐
              ↓                 ↓
       Retrieval Metrics   Answer Metrics
              │                 │
              └────────┬────────┘
                       ↓
                Result Classification
                       ↓
                 Evaluation Report
```

---

## 14. Interview Questions

### What is RAG evaluation?

RAG evaluation measures whether a retrieval-augmented generation system retrieves relevant information and generates an accurate, grounded answer.

### Why evaluate retrieval separately?

Because an incorrect answer may be caused by retrieving the wrong context rather than by the LLM itself.

### What is retrieval hit rate?

It measures how often the retrieval system returns relevant information for an evaluation question.

### What is answer evaluation?

It measures whether the generated answer satisfies the expected answer or reference criteria.

### What is an unsupported query?

A question whose answer cannot be found in the available knowledge source.

### Why shouldn't unsupported queries be evaluated using normal answer matching?

Because the correct behavior is refusal, not factual answering.

### What is failure classification?

It identifies where an AI system failed, such as retrieval, generation, or unsupported-query handling.

---

## 15. Key Takeaways

- AI applications need systematic evaluation.
    
- Retrieval and generation should be evaluated separately.
    
- Simple deterministic metrics are useful as a baseline.
    
- Evaluation datasets must themselves be reliable.
    
- Unsupported queries require different evaluation criteria.
    
- Top-k retrieval does not guarantee relevance.
    
- Evaluation should identify failure causes, not just produce a score.
    
- Production systems can later use rerankers and LLM-as-a-judge evaluation.
    
- API failures such as quota exhaustion should be distinguished from application failures.
    

## Day 19 Status

**Completed ✅**

Topics covered:

- Evaluation datasets
    
- Retrieval evaluation
    
- Answer evaluation
    
- Keyword matching
    
- Answer matching
    
- Unsupported-query evaluation
    
- Failure classification
    
- Evaluation reporting
    
- RAG failure analysis
    
- Production evaluation considerations