
import json
from pathlib import Path

from app.run_evaluation import BASE_DIR, load_dataset, simulate_agent

from app.evaluator import (
    evaluate_tool_selection,
    evaluate_tool_call,
    evaluate_task_completion,
    evaluate_failure_rate,
    evaluate_trajectory,
    evaluate_retrieval_precision,
    evaluate_retrieval_recall,
    evaluate_context_relevance,
    evaluate_faithfulness,
    evaluate_answer_correctness
)

from app.production_evaluator import (
    evaluate_latency,
    evaluate_token_consumption,
    evaluate_cost,
    evaluate_throughput,
    evaluate_reliability
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_agent():
    dataset = load_dataset()
    results = []

    for task in dataset:
        actual = simulate_agent(task)

        selection = evaluate_tool_selection(
            task["expected_tool"],
            actual["actual_tool"]
        )

        tool_call = evaluate_tool_call(
            task["expected_tool"],
            actual["actual_tool"],
            task["expected_arguments"],
            actual["actual_arguments"]
        )

        completed = None

        if task["expected_status"] == "success":
            completed = evaluate_task_completion(
                task["expected_outcome"],
                actual["actual_outcome"]
            )

        results.append({
            "task_id": task["id"],
            "tool_selection_correct": selection,
            "tool_call_correct": tool_call,
            "task_completed": completed,
            "expected_status": task["expected_status"],
            "actual_status": actual["actual_status"],
            "status_correct": (
                task["expected_status"] == actual["actual_status"]
            )
        })

    total = len(results)

    successful_tasks = [
        result for result in results
        if result["task_completed"] is not None
    ]

    return {
        "total_tasks": total,
        "tool_selection_accuracy": (
            sum(r["tool_selection_correct"] for r in results)
            / total * 100 if total else 0
        ),
        "tool_call_accuracy": (
            sum(r["tool_call_correct"] for r in results)
            / total * 100 if total else 0
        ),
        "task_completion_rate": (
            sum(r["task_completed"] for r in successful_tasks)
            / len(successful_tasks) * 100
            if successful_tasks else 0
        ),
        "failure_rate": evaluate_failure_rate([
            {"status": r["actual_status"]} for r in results
        ]),
        "expected_status_accuracy": (
            sum(r["status_correct"] for r in results)
            / total * 100 if total else 0
        ),
        "trajectory_evaluation": evaluate_trajectory(
            ["search", "summarize", "respond"],
            ["search", "summarize", "respond"]
        ),
        "individual_results": results
    }


def evaluate_rag():
    path = BASE_DIR / "datasets" / "rag_cases.json"
    dataset = load_json(path)

    results = []

    for case in dataset:
        precision = evaluate_retrieval_precision(
            case["retrieved_chunks"],
            case["relevant_chunks"]
        )

        recall = evaluate_retrieval_recall(
            case["retrieved_chunks"],
            case["relevant_chunks"]
        )

        relevance = evaluate_context_relevance(
            case["context_relevance_rating"]
        )

        faithfulness = evaluate_faithfulness(
            case["supported_answer_claims"],
            case["total_answer_claims"]
        )

        correctness = evaluate_answer_correctness(
            case["expected_answer"],
            case["actual_answer"]
        )

        results.append({
            "case_id": case["id"],
            "retrieval_precision": precision,
            "retrieval_recall": recall,
            "context_relevance": relevance,
            "faithfulness": faithfulness,
            "answer_correctness": correctness
        })

    total = len(results)

    def average(key):
        return (
            sum(result[key] for result in results) / total
            if total else 0
        )

    return {
        "total_cases": total,
        "average_retrieval_precision": average("retrieval_precision"),
        "average_retrieval_recall": average("retrieval_recall"),
        "average_context_relevance": average("context_relevance"),
        "average_faithfulness": average("faithfulness"),
        "answer_correctness_rate": (
            sum(r["answer_correctness"] for r in results)
            / total * 100 if total else 0
        ),
        "individual_results": results
    }


def evaluate_production():
    path = BASE_DIR / "datasets" / "production_requests.json"
    data = load_json(path)

    requests = data["requests"]
    elapsed = data["total_elapsed_seconds"]

    return {
        "total_requests": len(requests),
        "average_latency_seconds": evaluate_latency(requests),
        "token_consumption": evaluate_token_consumption(requests),
        "total_cost_usd": evaluate_cost(requests),
        "throughput_requests_per_second": evaluate_throughput(
            requests, elapsed
        ),
        "reliability_percentage": evaluate_reliability(requests),
        "measurement_type": "simulated"
    }


def create_markdown_report(report):
    agent = report["agent_evaluation"]
    rag = report["rag_evaluation"]
    production = report["production_evaluation"]
    tokens = production["token_consumption"]

    return f"""# AI Evaluation Report

## 1. Overview

This report combines agent evaluation, RAG evaluation,
and production evaluation.

**Important:** This project uses simulated agent outputs
and production measurements, along with manually annotated
RAG evaluation data. These are educational evaluation results,
not measurements from a live AI service.

## 2. Agent Evaluation

- Total tasks: {agent["total_tasks"]}
- Tool selection accuracy: {agent["tool_selection_accuracy"]:.2f}%
- Tool-call accuracy: {agent["tool_call_accuracy"]:.2f}%
- Task completion rate: {agent["task_completion_rate"]:.2f}%
- Raw failure rate: {agent["failure_rate"]:.2f}%
- Expected status accuracy: {agent["expected_status_accuracy"]:.2f}%
- Trajectory evaluation: {agent["trajectory_evaluation"]}

## 3. RAG Evaluation

- Total test cases: {rag["total_cases"]}
- Retrieval precision: {rag["average_retrieval_precision"]:.2f}%
- Retrieval recall: {rag["average_retrieval_recall"]:.2f}%
- Context relevance: {rag["average_context_relevance"]:.2f}%
- Faithfulness: {rag["average_faithfulness"]:.2f}%
- Answer correctness rate: {rag["answer_correctness_rate"]:.2f}%

## 4. Production Evaluation

- Measurement type: {production["measurement_type"]}
- Total requests: {production["total_requests"]}
- Average latency: {production["average_latency_seconds"]:.2f} seconds
- Input tokens: {tokens["input_tokens"]}
- Output tokens: {tokens["output_tokens"]}
- Total tokens: {tokens["total_tokens"]}
- Total cost: ${production["total_cost_usd"]:.4f}
- Throughput: {production["throughput_requests_per_second"]:.2f} requests/second
- Reliability: {production["reliability_percentage"]:.2f}%

## 5. Evaluation Summary

The evaluation covers three areas:

1. Agent behavior and task execution.
2. Retrieval quality and answer quality.
3. Runtime performance and operational reliability.

## 6. Limitations

- Agent execution is simulated.
- RAG relevance and faithfulness labels are manually supplied.
- Answer correctness currently uses exact string matching.
- Production latency, tokens, cost, throughput, and reliability
  use simulated request data.
- Trajectory evaluation currently uses an exact sequence comparison.

A real production evaluation should use actual agent traces,
retrieval results, reference answers, and measured runtime data.
"""


def generate_report():
    report = {
        "agent_evaluation": evaluate_agent(),
        "rag_evaluation": evaluate_rag(),
        "production_evaluation": evaluate_production()
    }

    report_dir = BASE_DIR / "reports"
    report_dir.mkdir(exist_ok=True)

    json_path = report_dir / "evaluation_report.json"
    markdown_path = report_dir / "evaluation_report.md"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    markdown = create_markdown_report(report)

    with open(markdown_path, "w", encoding="utf-8") as file:
        file.write(markdown)

    print("\nEvaluation reports generated successfully!")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")


if __name__ == "__main__":
    generate_report()
