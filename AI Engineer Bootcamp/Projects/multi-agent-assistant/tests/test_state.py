
import pytest

from app.core.state import (
    create_initial_state,
    update_state,
    record_agent_activity,
    record_error
)


def test_create_initial_state():
    state = create_initial_state("Research AI in healthcare")

    assert state["user_request"] == "Research AI in healthcare"
    assert state["status"] == "started"
    assert state["research_findings"] == []
    assert state["analysis"] == ""
    assert state["final_response"] == ""
    assert state["human_approved"] is False


def test_empty_request():
    with pytest.raises(ValueError):
        create_initial_state("")


def test_update_state():
    state = create_initial_state("Research AI")

    update_state(state, {
        "research_findings": ["Finding 1", "Finding 2"],
        "status": "research_completed"
    })

    assert len(state["research_findings"]) == 2
    assert state["status"] == "research_completed"


def test_prevent_invalid_state_update():
    state = create_initial_state("Research AI")

    with pytest.raises(ValueError):
        update_state(state, {
            "user_request": "Change the original request"
        })


def test_record_agent_activity():
    state = create_initial_state("Research AI")

    record_agent_activity(
        state,
        "researcher",
        "Research completed"
    )

    assert len(state["agent_history"]) == 1
    assert state["agent_history"][0]["agent"] == "researcher"


def test_record_error():
    state = create_initial_state("Research AI")

    record_error(
        state,
        "analyst",
        "No research findings provided"
    )

    assert state["status"] == "failed"
    assert len(state["errors"]) == 1
    assert state["errors"][0]["agent"] == "analyst"
