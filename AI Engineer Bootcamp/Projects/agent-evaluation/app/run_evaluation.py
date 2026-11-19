
import json
from pathlib import Path

from app.evaluator import (
    evaluate_tool_selection,
    evaluate_tool_call,
    evaluate_task_completion,
    evaluate_failure_rate,
    evaluate_trajectory
)

from app.production_evaluator import (
    evaluate_latency,
    evaluate_token_consumption,
    evaluate_cost,
    evaluate_throughput,
    evaluate_reliability
)

# Load evaluation dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "datasets" / "agent_tasks.json"


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# Simulate agent responses
def simulate_agent(task):
    tool = task["expected_tool"]
    args = task["expected_arguments"]

    if tool == "add":
        outcome = args["a"] + args["b"]
        status = "success"

    elif tool == "greet":
        outcome = f"Hello, {args['name']}!"
        status = "success"

    else:
        outcome = None
        status = "failure"

    return {
        "actual_tool": tool,
        "actual_arguments": args,
        "actual_outcome": outcome,
        "actual_status": status
    }


def run_production_evaluation():
    production_path = BASE_DIR / "datasets" / "production_requests.json"

    with open(production_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    requests = data["requests"]
    elapsed = data["total_elapsed_seconds"]

    latency = evaluate_latency(requests)
    tokens = evaluate_token_consumption(requests)
    cost = evaluate_cost(requests)
    throughput = evaluate_throughput(requests, elapsed)
    reliability = evaluate_reliability(requests)

    print("\n========== PRODUCTION EVALUATION ==========")
    print(f"Average latency: {latency:.2f} seconds")
    print(f"Input tokens: {tokens['input_tokens']}")
    print(f"Output tokens: {tokens['output_tokens']}")
    print(f"Total tokens: {tokens['total_tokens']}")
    print(f"Total cost: ${cost:.4f}")
    print(f"Throughput: {throughput:.2f} requests/second")
    print(f"Reliability: {reliability:.2f}%")
    print("===========================================")


def run_evaluation():
    dataset = load_dataset()

    results = []

    for task in dataset:
        actual = simulate_agent(task)

        selection_correct = evaluate_tool_selection(
            task["expected_tool"],
            actual["actual_tool"]
        )

        call_correct = evaluate_tool_call(
            task["expected_tool"],
            actual["actual_tool"],
            task["expected_arguments"],
            actual["actual_arguments"]
        )

        # Completion applies to tasks expected to succeed.
        if task["expected_status"] == "success":
            completed = evaluate_task_completion(
                task["expected_outcome"],
                actual["actual_outcome"]
            )
        else:
            completed = None

        results.append({
            "task_id": task["id"],
            "tool_selection_correct": selection_correct,
            "tool_call_correct": call_correct,
            "task_completed": completed,
            "expected_status": task["expected_status"],
            "actual_status": actual["actual_status"],
            "status_correct": (
                task["expected_status"] == actual["actual_status"]
            )
        })

    total = len(results)

    selection_accuracy = (
        sum(r["tool_selection_correct"] for r in results)
        / total * 100 if total else 0
    )

    call_accuracy = (
        sum(r["tool_call_correct"] for r in results)
        / total * 100 if total else 0
    )

    successful_tasks = [
        r for r in results if r["task_completed"] is not None
    ]

    completion_rate = (
        sum(r["task_completed"] for r in successful_tasks)
        / len(successful_tasks) * 100
        if successful_tasks else 0
    )

    failure_rate = evaluate_failure_rate([
        {"status": r["actual_status"]} for r in results
    ])

    status_accuracy = (
        sum(r["status_correct"] for r in results)
        / total * 100 if total else 0
    )

    print("\n========== AGENT EVALUATION REPORT ==========")
    print(f"Total test cases: {total}")
    print(f"Tool selection accuracy: {selection_accuracy:.2f}%")
    print(f"Tool-call accuracy: {call_accuracy:.2f}%")
    print(f"Task completion rate: {completion_rate:.2f}%")
    print(f"Raw failure rate: {failure_rate:.2f}%")
    print(f"Expected status accuracy: {status_accuracy:.2f}%")

    print("\nIndividual Task Results:")

    for result in results:
        print(
            f"{result['task_id']}: "
            f"Tool selection={result['tool_selection_correct']}, "
            f"Tool call={result['tool_call_correct']}, "
            f"Completed={result['task_completed']}, "
            f"Status correct={result['status_correct']}"
        )

    # Demonstrate trajectory evaluation
    expected_steps = ["search", "summarize", "respond"]
    actual_steps = ["search", "summarize", "respond"]

    trajectory_score = evaluate_trajectory(
        expected_steps,
        actual_steps
    )

    print(f"\nTrajectory evaluation: {trajectory_score}")
    print("=============================================")


if __name__ == "__main__":
    run_evaluation()
    run_production_evaluation()