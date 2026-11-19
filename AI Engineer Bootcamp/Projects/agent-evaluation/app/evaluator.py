
def evaluate_tool_selection(expected_tool, actual_tool):
    """Check whether the agent selected the expected tool."""
    return expected_tool == actual_tool


def evaluate_tool_call(expected_tool, actual_tool,
                       expected_arguments, actual_arguments):
    """Check both tool selection and arguments."""
    return (
        expected_tool == actual_tool
        and expected_arguments == actual_arguments
    )


def evaluate_task_completion(expected_outcome, actual_outcome):
    """Check whether the agent achieved the expected outcome."""
    return expected_outcome == actual_outcome


def evaluate_failure_rate(results):
    """Calculate the percentage of failed tasks."""
    if not results:
        return 0.0

    failed_tasks = sum(
        1 for result in results
        if result["status"] == "failure"
    )

    return failed_tasks / len(results) * 100

def evaluate_trajectory(expected_steps, actual_steps):
    """Check whether the agent followed the expected sequence."""
    return expected_steps == actual_steps


def evaluate_retrieval_precision(retrieved_chunks, relevant_chunks):
    """Percentage of retrieved chunks that are relevant."""
    if not retrieved_chunks:
        return 0.0

    relevant_retrieved = set(retrieved_chunks) & set(relevant_chunks)

    return len(relevant_retrieved) / len(retrieved_chunks) * 100


def evaluate_retrieval_recall(retrieved_chunks, relevant_chunks):
    """Percentage of all relevant chunks that were retrieved."""
    if not relevant_chunks:
        return 0.0

    relevant_retrieved = set(retrieved_chunks) & set(relevant_chunks)

    return len(relevant_retrieved) / len(relevant_chunks) * 100


def evaluate_context_relevance(rating):
    """Convert a manually assigned 1-5 rating into a percentage."""
    if not 1 <= rating <= 5:
        raise ValueError("Context relevance rating must be between 1 and 5")

    return rating / 5 * 100


def evaluate_faithfulness(supported_claims, total_claims):
    """Measure how many answer claims are supported by context."""
    if total_claims <= 0:
        return 0.0

    if not 0 <= supported_claims <= total_claims:
        raise ValueError("Invalid supported claim count")

    return supported_claims / total_claims * 100


def evaluate_answer_correctness(expected_answer, actual_answer):
    """Simple exact-match baseline for answer correctness."""
    return expected_answer.strip().casefold() == actual_answer.strip().casefold()
