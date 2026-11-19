
from app.production_evaluator import (
    evaluate_latency,
    evaluate_token_consumption,
    evaluate_cost,
    evaluate_throughput,
    evaluate_reliability
)


sample_requests = [
    {
        "latency_seconds": 1.2,
        "input_tokens": 300,
        "output_tokens": 150,
        "cost_usd": 0.002,
        "status": "success"
    },
    {
        "latency_seconds": 2.0,
        "input_tokens": 400,
        "output_tokens": 200,
        "cost_usd": 0.003,
        "status": "success"
    },
    {
        "latency_seconds": 1.8,
        "input_tokens": 250,
        "output_tokens": 100,
        "cost_usd": 0.0015,
        "status": "failure"
    }
]


def test_latency():
    assert round(evaluate_latency(sample_requests), 2) == 1.67
    assert evaluate_latency([]) == 0.0


def test_token_consumption():
    result = evaluate_token_consumption(sample_requests)

    assert result["input_tokens"] == 950
    assert result["output_tokens"] == 450
    assert result["total_tokens"] == 1400


def test_cost():
    assert round(evaluate_cost(sample_requests), 4) == 0.0065


def test_throughput():
    assert evaluate_throughput(sample_requests, 5.0) == 0.6
    assert evaluate_throughput(sample_requests, 0) == 0.0


def test_reliability():
    assert round(evaluate_reliability(sample_requests), 2) == 66.67
    assert evaluate_reliability([]) == 0.0
