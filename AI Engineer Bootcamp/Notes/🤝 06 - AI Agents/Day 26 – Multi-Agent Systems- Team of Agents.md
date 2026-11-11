## 1. Introduction to Multi-Agent Systems

A Multi-Agent System (MAS) consists of multiple specialised agents that collaborate to accomplish a common objective.

Instead of one agent performing every task, responsibilities are distributed among different agents.

### Why Multi-Agent Systems?

- Task specialisation
    
- Parallel task execution
    
- Better modularity
    
- Independent task management
    
- Collaborative problem-solving
    
- Improved scalability
    

### Example: AI Healthcare Research Team

|Agent|Responsibility|
|---|---|
|Researcher|Collects information|
|Analyst|Analyses research findings|
|Writer|Generates reports|
|Reviewer|Validates reports|
|Supervisor|Coordinates the workflow|

---

## 2. Multi-Agent Architecture Patterns

### 2.1 Sequential Pattern

Agents execute one after another.

**Workflow:**

Researcher → Analyst → Writer → Reviewer

Use cases:

- Document generation
    
- Research pipelines
    
- Data processing workflows
    

Implementation: `app/sequential_agents.py`

### 2.2 Parallel Pattern

Multiple independent agents execute simultaneously.

Example:

- Diagnosis Agent
    
- Surgery Agent
    
- Drug Discovery Agent
    

All three agents perform research independently.

**Implementation concept:**

```
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    tasks = [
        executor.submit(diagnosis_agent),
        executor.submit(surgery_agent),
        executor.submit(drug_agent)
    ]

    results = [task.result() for task in tasks]
```

Implementation: `app/parallel_agents.py`

**Execution comparison:**

|Pattern|Execution time|
|---|---|
|Sequential|6.01 seconds|
|Parallel|2.01 seconds|

These timings came from simulated two-second tasks.

Parallel execution reduced the elapsed time by approximately 66.6%.

**Important:** ThreadPoolExecutor is particularly useful for I/O-bound tasks. It does not generally accelerate CPU-bound Python work because of the GIL.

### 2.3 Hybrid Pattern

Combines parallel and sequential execution.

**Workflow:**

Parallel Research → Combine Findings → Analyst → Writer → Reviewer

Advantages:

- Independent tasks run concurrently.
    
- Results are aggregated.
    
- Dependent tasks execute in order.
    

Implementation: `app/hybrid_agents.py`

### 2.4 Supervisor Pattern

A central Supervisor controls the execution of worker agents.

Responsibilities:

- Task delegation
    
- Workflow coordination
    
- State management
    
- Result collection
    
- Error handling
    
- Review and revision
    

In our implementation, the Supervisor manages:

Researcher → Analyst → Writer → Reviewer

If the Reviewer rejects the report, the Supervisor asks the Writer to revise it.

Implementation: `app/supervisor.py`

### 2.5 Hierarchical Multi-Agent Pattern

Agents are organised into multiple levels.

Example:

Main Supervisor

- Research Supervisor
    
    - Researcher A
        
    - Researcher B
        
- Analysis Supervisor
    
    - Analyst A
        
    - Analyst B
        
- Writing Supervisor
    
    - Writer
        
    - Reviewer
        

Useful for:

- Large enterprise workflows
    
- Complex research systems
    
- Multiple specialised departments
    

### 2.6 Collaborative Pattern

Multiple agents exchange feedback and improve an output iteratively.

Our implementation:

Research Agent → Critic Agent → Improvement Agent

Responsibilities:

- Research Agent: Creates an initial proposal.
    
- Critic Agent: Identifies weaknesses.
    
- Improvement Agent: Revises the proposal.
    

Implementation: `app/collaborative_agents.py`

---

## 3. Agent Communication and State Sharing

Agents need to exchange information to collaborate.

Example of a shared research object:

```
research = {
    "agent": "Researcher",
    "topic": "AI Healthcare",
    "findings": combined_findings
}
```

The Analyst receives the research object.

The Writer receives the analysis.

The Reviewer receives the generated report.

### Important concepts

|Concept|Meaning|
|---|---|
|Task delegation|Assigning work to specialised agents|
|State sharing|Passing information between agents|
|Synchronisation|Coordinating dependent tasks|
|Validation|Checking agent outputs|
|Feedback loop|Providing improvement suggestions|

---

## 4. Concurrency in Multi-Agent Systems

Concurrency allows multiple tasks to make progress during overlapping periods.

### ThreadPoolExecutor

Python provides `ThreadPoolExecutor` through the `concurrent.futures` module.

Important methods:

- `submit()`: Schedules a function for execution.
    
- `result()`: Retrieves the task result.
    
- `as_completed()`: Iterates over tasks as they finish.
    
- `cancel()`: Attempts to cancel a task that has not started.
    

### Synchronisation

Suppose three research agents execute concurrently.

The Analyst must wait until all required results are available.

```
results = [task.result() for task in tasks]
```

This waits for each submitted task to finish before the workflow continues.

### as_completed()

```
from concurrent.futures import as_completed

for task in as_completed(tasks):
    result = task.result()
```

This processes tasks in completion order rather than submission order.

---

## 5. Failure Handling

Multi-agent systems must handle failures without unnecessarily terminating the entire workflow.

### Common failure scenarios

|Failure|Example|Handling|
|---|---|---|
|Agent failure|Python exception|Catch exception|
|Missing output|Agent returns None|Validate output|
|Timeout|Agent takes too long|Apply time limit|
|Temporary failure|API connection issue|Retry|
|Invalid response|Unexpected data|Reject or validate|

### 5.1 Retry Mechanism

A retry mechanism executes a failed task again.

Implementation: `app/retry_agents.py`

Example:

```
def run_with_retry(agent, max_retries=3):

    for attempt in range(1, max_retries + 1):

        try:
            result = agent()
            return result

        except Exception as error:
            print("Agent failed:", error)

    return None
```

Our demonstration:

- Attempt 1: Failed
    
- Attempt 2: Failed
    
- Attempt 3: Succeeded
    

**Best practices:**

- Set a maximum retry count.
    
- Retry temporary failures.
    
- Use exponential backoff where appropriate.
    
- Avoid repeatedly retrying permanent errors.
    
- Consider API rate limits and duplicate operations.
    

### 5.2 Timeout Mechanism

A timeout specifies how long the Supervisor waits for an agent's result.

Implementation: `app/timeout_agents.py`

```
task = executor.submit(agent)

try:
    result = task.result(timeout=2)

except TimeoutError:
    print("Agent timed out!")
```

**Important Python behaviour:**

A timeout on `Future.result()` limits how long the caller waits for the result. It does not forcibly terminate an already-running thread.

In our experiment:

- Research Agent sleep: 5 seconds
    
- Configured timeout: 2 seconds
    
- Timeout detected: approximately 2 seconds
    
- Total execution time: approximately 5 seconds
    

Why?

The ThreadPoolExecutor context manager waits for running tasks to finish when exiting its context.

`task.cancel()` cannot forcibly terminate a task that is already running.

Production systems may use cooperative cancellation, cancellable I/O operations or separate processes for stronger execution limits.

### 5.3 Partial Failure Handling

Implementation: `app/parallel_failure.py`

Three agents execute concurrently.

Results:

|Agent|Result|
|---|---|
|Diagnosis|Success|
|Surgery|Failed|
|Drug Discovery|Success|

Successful agents: 2/3

The Supervisor catches individual exceptions and preserves successful results.

This is called partial failure handling.

---

## 6. Agent Review and Feedback Loops

Our Reviewer validates the generated research report.

Validation conditions:

- Report length greater than 50 characters.
    
- At least three findings.
    
- Report title contains RESEARCH REPORT.
    

The Supervisor allows up to two review attempts.

If the report is rejected, the Writer receives the review feedback.

**Important limitation:** Revising a report cannot create missing research evidence automatically. A production system may need to send the task back to the Researcher.

---

## 7. Testing Multi-Agent Systems

We used Pytest for automated testing.

Installation:

```
pip install pytest
```

Run tests:

```
python -m pytest -v
```

### Unit Testing

Tests individual functions:

- `test_researcher()`
    
- `test_analyst()`
    
- `test_writer()`
    
- `test_reviewer()`
    

### Integration Testing

Tests how multiple agents work together.

`test_supervisor_workflow()` validates:

- Research findings are generated.
    
- Report generation succeeds.
    
- Reviewer approves the final report.
    

### Testing principles

- Validate expected outputs.
    
- Test invalid inputs.
    
- Test agent failures.
    
- Test retry behaviour.
    
- Test workflow integration.
    
- Test edge cases.
    

---

## 8. Project Structure

```
multi-agent-research-team/
│
├── app/
│   ├── __init__.py
│   ├── agents.py
│   ├── supervisor.py
│   ├── main.py
│   ├── parallel_agents.py
│   ├── sequential_agents.py
│   ├── hybrid_agents.py
│   ├── collaborative_agents.py
│   ├── retry_agents.py
│   ├── timeout_agents.py
│   └── parallel_failure.py
│
├── data/
│   └── research_data.txt
│
├── tests/
│   └── test_agents.py
│
├── requirements.txt
└── README.md
```

## 9. Technologies Used

|Technology|Purpose|
|---|---|
|Python 3.12|Main programming language|
|ThreadPoolExecutor|Concurrent execution|
|concurrent.futures|Future objects and task management|
|Pytest|Automated testing|
|PowerShell|Project execution environment|

## 10. Limitations of This Implementation

This project demonstrates foundational multi-agent architecture.

However:

1. Agents are deterministic Python functions, not autonomous LLM-powered agents.
    
2. Collaboration uses predefined logic rather than independent LLM reasoning.
    
3. Research information comes from local predefined data.
    
4. No external LLM API is integrated.
    
5. Timeout detection does not forcibly terminate running threads.
    
6. Persistent shared state and distributed orchestration are not implemented.
    

These are important distinctions when describing the project in interviews.

## 11. Interview Questions

**Q1. What is a Multi-Agent System?**

A system where multiple specialised agents collaborate to accomplish a common objective.

**Q2. What is the difference between sequential and parallel agents?**

Sequential agents execute one after another, while parallel agents execute independent tasks concurrently.

**Q3. What is a Supervisor Agent?**

A central coordinator that delegates tasks, manages execution and collects results from worker agents.

**Q4. What is a hierarchical multi-agent system?**

A system where multiple levels of supervisors coordinate specialised groups of agents.

**Q5. What is a feedback loop?**

A process in which an agent reviews another agent's output and provides feedback for improvement.

**Q6. Why is ThreadPoolExecutor useful?**

It allows multiple I/O-bound tasks to execute concurrently using a pool of worker threads.

**Q7. What is partial failure handling?**

Handling an individual agent's failure while preserving successful results from other agents.

**Q8. What is the difference between retry and timeout?**

Retry attempts a failed task again, while timeout limits how long the system waits for a task.

**Q9. What is synchronisation?**

Coordinating concurrent tasks so dependent operations proceed when their required results are available.

**Q10. What are the challenges of multi-agent systems?**

- Coordination complexity
    
- State management
    
- Communication overhead
    
- Failure handling
    
- Concurrency issues
    
- Cost and latency
    
- Output validation
    

---

## 12. Day 26 Learning Summary

By completing this project, I learned:

- Multi-agent architecture patterns.
    
- Sequential, parallel and hybrid execution.
    
- Supervisor and hierarchical patterns.
    
- Collaborative agents and feedback loops.
    
- Agent communication and state passing.
    
- ThreadPoolExecutor and concurrency.
    
- Retry and timeout mechanisms.
    
- Synchronisation and partial failure handling.
    
- Unit testing and integration testing.
    

**Day 26 Outcome:** Built a foundational Multi-Agent Research Team using Python, demonstrating task delegation, concurrency, feedback, error handling and workflow orchestration.

### Key takeaway

A successful multi-agent system is not simply a collection of agents. It requires proper coordination, communication, state management, validation and failure handling.