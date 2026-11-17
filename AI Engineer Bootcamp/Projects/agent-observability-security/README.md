# Agent Observability and AI Security

A Python-based demonstration of observability and security practices for AI agent workflows.

## Project Objectives

- Implement structured JSON logging.
- Trace multi-agent workflows using OpenTelemetry.
- Capture agent execution time and failures.
- Demonstrate prompt injection risks.
- Redact sensitive information.
- Implement tool allowlisting and input validation.
- Test observability and security components using pytest.

## Architecture

Research Workflow:

Researcher → Analyst → Writer

Each agent runs inside an OpenTelemetry span.

The workflow is represented by a parent span, with individual agent spans as children.

## Project Structure

```text
agent-observability-security/
├── app/
│   ├── __init__.py
│   ├── agents.py
│   ├── tracing.py
│   ├── security.py
│   └── main.py
├── tests/
│   ├── test_security.py
│   └── test_tracing.py
├── logs/
├── requirements.txt
└── README.md
```

## Technologies

- Python
- OpenTelemetry
- Pytest
- Python JSON logging

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

## Run the Application

```powershell
python -m app.main
```

## Run Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

## Security Demonstrations

1. Prompt injection simulation.
2. Basic sensitive data redaction.
3. Tool allowlisting.
4. Input validation.
5. Unauthorized tool rejection.

## Observability Demonstrations

1. Structured JSON logs.
2. Workflow-level tracing.
3. Agent-level spans.
4. Trace and span relationships.
5. Exception recording and error status.
6. Execution duration attributes.

## Test Results

9 automated tests covering security and tracing.

## Important Limitations

This project is an educational demonstration.

- Prompt injection detection uses simple keyword matching.
- Redaction uses basic regular expressions.
- Tool authorization is implemented locally.
- Production deployments require stronger security controls, authentication, permission isolation, and monitoring.

## Learning Outcome

Understand how to monitor AI agent workflows, investigate failures, protect sensitive information, and restrict agent tool access.
