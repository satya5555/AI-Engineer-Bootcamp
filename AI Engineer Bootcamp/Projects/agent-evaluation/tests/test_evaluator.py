
from app.evaluator import (
    evaluate_tool_selection,
    evaluate_tool_call,
    evaluate_task_completion,
    evaluate_failure_rate,
    evaluate_trajectory
)


def test_tool_selection():
    assert evaluate_tool_selection("add", "add") is True
    assert evaluate_tool_selection("add", "greet") is False


def test_tool_call():
    assert evaluate_tool_call(
        "add", "add",
        {"a": 10, "b": 20},
        {"a": 10, "b": 20}
    ) is True

    assert evaluate_tool_call(
        "add", "add",
        {"a": 10, "b": 20},
        {"a": 10, "b": 15}
    ) is False


def test_task_completion():
    assert evaluate_task_completion(30, 30) is True
    assert evaluate_task_completion(30, 25) is False


def test_failure_rate():
    results = [
        {"status": "success"},
        {"status": "failure"},
        {"status": "success"},
        {"status": "failure"}
    ]

    assert evaluate_failure_rate(results) == 50.0
    assert evaluate_failure_rate([]) == 0.0


def test_trajectory():
    expected = ["search", "summarize", "respond"]
    actual = ["search", "summarize", "respond"]

    assert evaluate_trajectory(expected, actual) is True

    actual = ["search", "respond"]
    assert evaluate_trajectory(expected, actual) is False
