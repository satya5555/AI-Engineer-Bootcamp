## 1. Introduction to AI Evaluation

AI Evaluation is the process of measuring the quality, correctness, reliability, and performance of AI applications.

Building an AI application is not enough. We must determine whether it:

- Produces correct answers.
    
- Retrieves relevant information.
    
- Selects appropriate tools.
    
- Completes user tasks.
    
- Responds within acceptable time.
    
- Uses tokens and resources efficiently.
    
- Behaves reliably in production.
    

### Three major areas of AI Evaluation

1. Agent Evaluation
    
2. RAG Evaluation
    
3. Production Evaluation
    

---

# 2. Agent Evaluation

Agent Evaluation measures how effectively an AI agent selects tools, executes actions, follows the expected workflow, and completes tasks.

### 2.1 Tool Selection Accuracy

Measures whether the agent selects the correct tool for a given task.

Example:

- User request: Add 10 and 20.
    
- Expected tool: `add`
    
- Actual tool: `add`
    
- Result: Correct.
    

Formula:

Tool Selection Accuracy = (Correct tool selections / Total tool selections) × 100

### 2.2 Tool-Call Accuracy

Measures whether the agent selects the correct tool and supplies the correct arguments.

Example:

Expected: `add(10, 20)`

Actual: `add(10, 20)`

Result: Correct.

If the actual call is `add(10, 15)`, tool selection is correct, but tool-call accuracy is incorrect.

### 2.3 Task Completion Rate

Measures the percentage of eligible tasks successfully completed by the agent.

Formula:

Task Completion Rate = (Successfully completed tasks / Total eligible tasks) × 100

Example:

- Total eligible tasks: 10
    
- Completed tasks: 8
    
- Completion rate: 80%
    

### 2.4 Failure Rate

Measures the percentage of tasks that result in failure.

Formula:

Failure Rate = (Failed tasks / Total tasks) × 100

Example:

- Total tasks: 10
    
- Failed tasks: 2
    
- Failure rate: 20%
    

Important distinction: An expected failure, such as a correctly rejected unsupported tool request, is not necessarily an evaluation error. Compare expected and actual statuses separately.

### 2.5 Trajectory Evaluation

An agent may execute multiple steps to complete a task.

Trajectory Evaluation checks whether the agent follows the expected sequence of actions.

Example:

Expected trajectory:

`search → summarize → respond`

Actual trajectory:

`search → summarize → respond`

Result: Correct.

An agent that skips a necessary step may have an incorrect trajectory.

Our implementation uses exact sequence comparison. Advanced evaluation can also consider alternative valid paths, unnecessary steps, and partially correct trajectories.

---

# 3. RAG Evaluation

RAG (Retrieval-Augmented Generation) Evaluation measures the quality of retrieved information and the correctness of generated answers.

### RAG Evaluation Pipeline

User Query → Retriever → Retrieved Context → LLM Answer → Evaluation

Five important RAG evaluation metrics:

1. Retrieval Precision
    
2. Retrieval Recall
    
3. Context Relevance
    
4. Faithfulness
    
5. Answer Correctness
    

## 3.1 Retrieval Precision

Measures how many retrieved chunks are actually relevant.

Formula:

Precision = Relevant Retrieved Chunks / Total Retrieved Chunks

Example:

- Retrieved chunks: 5
    
- Relevant chunks: 4
    

Precision = 4 / 5 = 80%

High precision means the retriever returns fewer irrelevant chunks.

## 3.2 Retrieval Recall

Measures how many of the available relevant chunks were successfully retrieved.

Formula:

Recall = Relevant Retrieved Chunks / Total Relevant Chunks Available

Example:

- Total relevant chunks available: 8
    
- Relevant chunks retrieved: 4
    

Recall = 4 / 8 = 50%

High recall means the retriever finds a larger proportion of relevant information.

### Precision vs Recall

|Precision|Recall|
|---|---|
|Measures retrieval quality|Measures retrieval coverage|
|Focuses on retrieved chunks|Focuses on all relevant available chunks|
|Penalizes irrelevant retrievals|Penalizes missed relevant chunks|

A RAG system can have high precision but low recall if it retrieves only a few relevant chunks while missing many others.

## 3.3 Context Relevance

Measures whether the retrieved context is relevant to the user's question.

Example:

Question: What is Python used for?

Relevant context:

- Python programming.
    
- Python data science libraries.
    
- Python automation.
    

Irrelevant context:

- JavaScript frameworks.
    
- Computer hardware specifications.
    

Context relevance can be evaluated using human annotations or an LLM-based evaluator.

Our implementation uses a manual rating from 1 to 5.

Percentage = (Rating / 5) × 100

Example: Rating 4 = 80%.

## 3.4 Faithfulness

Measures whether the generated answer is supported by the retrieved context.

Example:

Retrieved context:  
"Python is commonly used for automation and data science."

Generated answer:  
"Python is used for automation, data science, and web development."

If web development is not supported by the retrieved context, that claim reduces faithfulness.

Formula:

Faithfulness = Supported Answer Claims / Total Answer Claims

Example:

- Total claims: 3
    
- Supported claims: 2
    

Faithfulness = 2 / 3 = 66.67%

## 3.5 Answer Correctness

Measures whether the generated answer is factually correct compared with the expected reference answer.

Example:

Expected answer:  
"Python is used for data science."

Actual answer:  
"Python is used for data science."

Result: Correct.

An answer can be faithful to retrieved context but still factually incorrect if the source itself contains incorrect information.

### Faithfulness vs Answer Correctness

|Faithfulness|Answer Correctness|
|---|---|
|Checks support from retrieved context|Checks factual correctness|
|Focuses on grounding|Focuses on correctness|
|Detects unsupported claims|Detects incorrect answers|

Our implementation uses exact string matching as a basic correctness baseline. Real systems should use semantic evaluation, reference-based metrics, or human/LLM judging.

---

# 4. Production Evaluation

Production Evaluation measures the operational performance of an AI application.

Five important metrics:

1. Latency
    
2. Token Consumption
    
3. Cost
    
4. Throughput
    
5. Reliability
    

## 4.1 Latency

Measures the time taken to process a request and return a response.

Example:

- Request 1: 1.2 seconds
    
- Request 2: 2.0 seconds
    
- Request 3: 1.8 seconds
    

Average Latency = Total Request Latency / Number of Requests

Average = (1.2 + 2.0 + 1.8) / 3 = 1.67 seconds.

Lower latency generally provides a better user experience.

Other useful latency measures include:

- P50 latency: Median response time.
    
- P95 latency: 95% of requests complete within this time.
    
- P99 latency: 99% of requests complete within this time.
    

## 4.2 Token Consumption

Measures the number of tokens processed by an LLM.

Two categories:

- Input tokens: Tokens sent to the model.
    
- Output tokens: Tokens generated by the model.
    

Total Tokens = Input Tokens + Output Tokens

Example:

- Input tokens: 950
    
- Output tokens: 450
    
- Total tokens: 1,400
    

Token consumption affects cost and performance.

## 4.3 Cost

Measures the financial cost of executing AI requests.

Cost generally depends on:

- Model selection.
    
- Input tokens.
    
- Output tokens.
    
- Model-specific pricing.
    
- Additional services such as retrieval or hosting.
    

A simplified formula:

Total Cost = Input Token Cost + Output Token Cost

Use the selected provider's actual pricing rates when calculating real costs.

## 4.4 Throughput

Measures how many requests an application can process within a given time.

Formula:

Throughput = Total Requests / Total Elapsed Time

Example:

- Requests: 100
    
- Time: 10 seconds
    

Throughput = 100 / 10 = 10 requests per second.

Higher throughput indicates greater request-processing capacity under the measured conditions.

## 4.5 Reliability

Measures the percentage of requests successfully processed.

Formula:

Reliability = (Successful Requests / Total Requests) × 100

Example:

- Total requests: 100
    
- Successful requests: 99
    

Reliability = 99%.

Reliability is important for production AI systems because failures can directly affect users and business operations.

---

# 5. Hands-on Project – AI Evaluation Framework

## Project Objective

Build a Python-based evaluation framework covering:

- AI Agent Evaluation.
    
- RAG Evaluation.
    
- Production Evaluation.
    
- Automated tests.
    
- Evaluation reports.
    

## Technology Stack

- Python 3.12
    
- JSON
    
- Pytest
    
- Python standard library
    

## Project Structure

```
agent-evaluation/
│
├── app/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── production_evaluator.py
│   ├── run_evaluation.py
│   └── generate_report.py
│
├── datasets/
│   ├── agent_tasks.json
│   ├── rag_cases.json
│   └── production_requests.json
│
├── reports/
│   ├── evaluation_report.json
│   └── evaluation_report.md
│
├── tests/
│   ├── test_evaluator.py
│   ├── test_rag_evaluation.py
│   └── test_production_evaluator.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Implementation Details

### A. Agent Evaluation

Implemented functions:

- `evaluate_tool_selection()`
    
- `evaluate_tool_call()`
    
- `evaluate_task_completion()`
    
- `evaluate_failure_rate()`
    
- `evaluate_trajectory()`
    

The agent dataset contains sample tasks for addition, greeting, and an unsupported multiplication request.

Agent outputs are simulated for this educational project.

### B. RAG Evaluation

Implemented functions:

- `evaluate_retrieval_precision()`
    
- `evaluate_retrieval_recall()`
    
- `evaluate_context_relevance()`
    
- `evaluate_faithfulness()`
    
- `evaluate_answer_correctness()`
    

The RAG dataset contains queries, retrieved chunk IDs, relevant chunk IDs, manual relevance ratings, and answer annotations.

### C. Production Evaluation

Implemented in `production_evaluator.py`:

- `evaluate_latency()`
    
- `evaluate_token_consumption()`
    
- `evaluate_cost()`
    
- `evaluate_throughput()`
    
- `evaluate_reliability()`
    

Production data is simulated and stored in `production_requests.json`.

### D. Automated Testing

Used Pytest to validate all evaluation functions.

Test files:

- `test_evaluator.py`
    
- `test_rag_evaluation.py`
    
- `test_production_evaluator.py`
    

Total automated tests: 15.

Run tests:

```
python -m pytest -v
```

### E. Evaluation Reports

The project generates two reports:

1. `evaluation_report.json` – structured machine-readable results.
    
2. `evaluation_report.md` – human-readable evaluation summary.
    

Generate reports:

```
python -m app.generate_report
```

The report combines Agent, RAG, and Production Evaluation results.

---

# 6. Important Limitations and Future Improvements

The current project is an educational evaluation framework.

Its limitations include:

1. Agent outputs are simulated rather than generated by a live LLM.
    
2. RAG relevance and faithfulness values are manually annotated.
    
3. Answer correctness uses exact string matching.
    
4. Production measurements are simulated rather than measured from a live service.
    
5. Trajectory evaluation uses exact sequence comparison.
    

### Possible Future Improvements

- Integrate actual agent execution traces.
    
- Evaluate real retrieval results from ChromaDB.
    
- Introduce semantic answer correctness.
    
- Implement LLM-as-a-judge evaluation.
    
- Measure actual token usage and latency.
    
- Calculate P50, P95, and P99 latency.
    
- Compare different models and retrieval configurations.
    
- Add evaluation dashboards and historical comparisons.
    

---

# 7. Interview Questions and Answers

### Q1. What is AI Evaluation?

AI Evaluation is the process of measuring the quality, correctness, reliability, and performance of AI applications.

### Q2. What is the difference between precision and recall in RAG?

Precision measures how many retrieved chunks are relevant, whereas recall measures how many of all available relevant chunks were retrieved.

### Q3. What is faithfulness in RAG?

Faithfulness measures whether the generated answer is supported by the retrieved context.

### Q4. What is context relevance?

It measures whether the retrieved information is related to the user's query.

### Q5. What is the difference between faithfulness and answer correctness?

Faithfulness checks whether the answer is grounded in retrieved context. Answer correctness checks whether the answer is factually correct.

### Q6. What is tool selection accuracy?

It measures whether an agent chooses the appropriate tool for a user request.

### Q7. What is trajectory evaluation?

It evaluates the sequence of actions or tool calls performed by an agent to complete a task.

### Q8. What is throughput?

Throughput measures how many requests an application processes per unit of time.

### Q9. Why is latency important in AI applications?

Latency directly affects response time and user experience. High latency can make an otherwise accurate AI application difficult to use.

### Q10. Why do we evaluate token consumption?

Token consumption affects model usage limits, response capacity, and API costs.

### Q11. What is LLM-as-a-judge?

LLM-as-a-judge uses another language model to evaluate AI-generated outputs against defined criteria, such as relevance, correctness, and faithfulness.

### Q12. Can a RAG system have high precision but low recall?

Yes. It can retrieve only a few highly relevant chunks while missing many other relevant chunks.

---

# 8. Day 29 Summary

|Evaluation Area|Metrics|
|---|---|
|Agent Evaluation|Tool selection, tool-call accuracy, task completion, failure rate, trajectory|
|RAG Evaluation|Precision, recall, context relevance, faithfulness, answer correctness|
|Production Evaluation|Latency, token consumption, cost, throughput, reliability|

### Key Takeaway

Building an AI application is only one part of AI engineering.

A production-ready AI engineer must also evaluate its quality, measure its performance, identify failures, and continuously improve the system.

**Build → Evaluate → Secure → Deploy → Monitor → Optimize**

---

**Day 29 Status:** Completed – AI Evaluation Framework

**Next Roadmap Topic:** Day 30 – Mini Project #3: Multi-Agent Assistant.