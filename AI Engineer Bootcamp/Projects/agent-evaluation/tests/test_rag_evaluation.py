
import pytest

from app.evaluator import (
    evaluate_retrieval_precision,
    evaluate_retrieval_recall,
    evaluate_context_relevance,
    evaluate_faithfulness,
    evaluate_answer_correctness
)


def test_retrieval_precision():
    retrieved = ["c1", "c2", "c5"]
    relevant = ["c1", "c2", "c3", "c4"]

    assert round(
        evaluate_retrieval_precision(retrieved, relevant), 2
    ) == 66.67


def test_retrieval_recall():
    retrieved = ["c1", "c2", "c5"]
    relevant = ["c1", "c2", "c3", "c4"]

    assert evaluate_retrieval_recall(retrieved, relevant) == 50.0


def test_context_relevance():
    assert evaluate_context_relevance(4) == 80.0

    with pytest.raises(ValueError):
        evaluate_context_relevance(6)


def test_faithfulness():
    assert round(evaluate_faithfulness(2, 3), 2) == 66.67
    assert evaluate_faithfulness(4, 4) == 100.0
    assert evaluate_faithfulness(0, 0) == 0.0


def test_answer_correctness():
    expected = "Python is used for data science."
    actual = "Python is used for data science."

    assert evaluate_answer_correctness(expected, actual) is True

    actual = "Python is used for web development."
    assert evaluate_answer_correctness(expected, actual) is False
