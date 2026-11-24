import pytest

from app.core.memory import (
    save_memory,
    load_memories,
    get_recent_memories
)


def sample_state():
    return {
        "user_request": "Research AI in healthcare",
        "research_findings": ["AI helps analyze medical images"],
        "analysis": "AI has benefits and challenges",
        "final_response": "Healthcare AI summary",
        "status": "completed"
    }


def test_save_memory(tmp_path):
    path = tmp_path / "memory.json"

    save_memory(sample_state(), path)

    memories = load_memories(path)

    assert len(memories) == 1
    assert memories[0]["user_request"] == "Research AI in healthcare"


def test_multiple_memories(tmp_path):
    path = tmp_path / "memory.json"

    save_memory(sample_state(), path)
    save_memory(sample_state(), path)

    memories = load_memories(path)

    assert len(memories) == 2


def test_recent_memories(tmp_path):
    path = tmp_path / "memory.json"

    save_memory(sample_state(), path)
    save_memory(sample_state(), path)

    memories = get_recent_memories(1, path)

    assert len(memories) == 1


def test_prevent_saving_incomplete_workflow(tmp_path):
    path = tmp_path / "memory.json"

    state = sample_state()
    state["status"] = "awaiting_approval"

    with pytest.raises(ValueError):
        save_memory(state, path)