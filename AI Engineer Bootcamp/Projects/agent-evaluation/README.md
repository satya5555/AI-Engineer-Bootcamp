# AI Evaluation Framework

A Python-based educational framework for evaluating AI agents,
RAG applications, and production performance.

## Project Overview

This project demonstrates three major areas of AI evaluation.

### 1. Agent Evaluation

- Tool selection accuracy
- Tool-call accuracy
- Task completion rate
- Failure rate
- Trajectory evaluation

### 2. RAG Evaluation

- Retrieval precision
- Retrieval recall
- Context relevance
- Faithfulness
- Answer correctness

### 3. Production Evaluation

- Latency
- Token consumption
- Cost
- Throughput
- Reliability

## Project Structure

```text
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
└── README.md
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run Evaluation

Run agent and production evaluation:

```powershell
python -m app.run_evaluation
```

Generate the combined evaluation report:

```powershell
python -m app.generate_report
```

## Run Tests

```powershell
python -m pytest -v
```

## Reports

The project generates:

- `reports/evaluation_report.json`
- `reports/evaluation_report.md`

## Technical Notes

This is an educational evaluation framework.

Agent outputs and production measurements are simulated.
RAG relevance and faithfulness annotations are manually supplied.

Answer correctness uses exact string matching as a baseline.
These methods can be extended with real agent traces,
retrieval datasets, semantic evaluation, and live metrics.

## Technologies

- Python
- JSON
- Pytest
- Python standard library
