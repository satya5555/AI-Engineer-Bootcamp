
def evaluate_latency(requests):
    """Calculate average request latency in seconds."""
    if not requests:
        return 0.0

    total_latency = sum(
        request["latency_seconds"] for request in requests
    )

    return total_latency / len(requests)


def evaluate_token_consumption(requests):
    """Calculate total input, output, and combined tokens."""
    input_tokens = sum(
        request["input_tokens"] for request in requests
    )

    output_tokens = sum(
        request["output_tokens"] for request in requests
    )

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }


def evaluate_cost(requests):
    """Calculate total request cost in USD."""
    return sum(
        request["cost_usd"] for request in requests
    )


def evaluate_throughput(requests, total_elapsed_seconds):
    """Calculate requests handled per second."""
    if total_elapsed_seconds <= 0:
        return 0.0

    return len(requests) / total_elapsed_seconds


def evaluate_reliability(requests):
    """Calculate percentage of successful requests."""
    if not requests:
        return 0.0

    successful_requests = sum(
        1 for request in requests
        if request["status"] == "success"
    )

    return successful_requests / len(requests) * 100
