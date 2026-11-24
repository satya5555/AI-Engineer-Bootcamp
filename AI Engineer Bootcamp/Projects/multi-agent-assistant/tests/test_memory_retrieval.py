from app.core.memory import (
    save_memory,
    retrieve_relevant_memories
)


def test_retrieve_relevant_memory(tmp_path):
    path = tmp_path / "memory.json"

    state = {
        "user_request": "Research AI in healthcare",
        "research_findings": [
            "AI helps doctors analyze medical images"
        ],
        "analysis": "Healthcare AI has privacy challenges",
        "final_response": "Healthcare AI summary",
        "status": "completed"
    }

    save_memory(state, path)

    results = retrieve_relevant_memories(
        "What are the challenges of AI in healthcare?",
        path=path
    )

    assert len(results) == 1
    assert results[0]["user_request"] == "Research AI in healthcare"


def test_no_relevant_memory(tmp_path):
    path = tmp_path / "memory.json"

    results = retrieve_relevant_memories(
        "Research space exploration",
        path=path
    )

    assert results == []


def test_memory_limit(tmp_path):
    path = tmp_path / "memory.json"

    state = {
        "user_request": "Research AI in healthcare",
        "research_findings": ["AI medical research"],
        "analysis": "Healthcare analysis",
        "final_response": "Summary",
        "status": "completed"
    }

    for _ in range(4):
        save_memory(state, path)

    results = retrieve_relevant_memories(
        "Research AI healthcare",
        limit=2,
        path=path
    )

    assert len(results) == 2