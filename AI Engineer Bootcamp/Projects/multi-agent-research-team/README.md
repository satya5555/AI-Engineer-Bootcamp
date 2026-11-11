# Multi-Agent Research Team

A Python-based multi-agent research system demonstrating how specialised agents collaborate to collect information, analyse findings, generate reports, and validate output.

## Project Objectives

- Understand multi-agent system architecture.
- Implement sequential, parallel and hybrid execution.
- Explore supervisor and hierarchical patterns.
- Demonstrate collaborative agents and feedback loops.
- Implement retries, timeout detection and failure handling.
- Understand agent synchronisation.
- Test individual agents and the complete workflow.

## Architecture

### Sequential Workflow

Researcher → Analyst → Writer → Reviewer

### Parallel Workflow

- Diagnosis Agent
- Surgery Agent
- Drug Discovery Agent

Independent agents execute concurrently.

### Hybrid Workflow

Parallel research → Result aggregation → Analyst → Writer → Reviewer

### Collaborative Workflow

Research Agent → Critic Agent → Improvement Agent

### Supervisor Workflow

The Supervisor coordinates agent execution, manages results and controls the review process.

## Project Structure

```text
multi-agent-research-team/
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
├── data/
│   └── research_data.txt
├── tests/
│   └── test_agents.py
├── requirements.txt
└── README.md
```

## Technologies

- Python 3.12
- ThreadPoolExecutor
- Concurrent Futures
- Pytest

## Setup

Clone the repository and navigate to the project directory.

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the main application:

```powershell
python -m app.main
```

Run the tests:

```powershell
python -m pytest -v
```

## Key Concepts Learned

1. Sequential multi-agent execution
2. Parallel multi-agent execution
3. Hybrid workflows
4. Supervisor architecture
5. Hierarchical architecture
6. Collaborative agents
7. Feedback loops
8. Retry mechanisms
9. Timeout detection
10. Synchronisation
11. Partial failure handling
12. Unit and integration testing

## Current Limitations

- Agents are deterministic Python functions, not autonomous LLM-powered agents.
- Agent collaboration is simulated using predefined logic.
- Timeout detection does not forcibly terminate an already-running thread.
- Research data is currently local and predefined.
- No external LLM APIs are integrated.

## Learning Outcome

Built a foundational multi-agent architecture demonstrating task delegation, concurrency, feedback, error handling and workflow orchestration.
