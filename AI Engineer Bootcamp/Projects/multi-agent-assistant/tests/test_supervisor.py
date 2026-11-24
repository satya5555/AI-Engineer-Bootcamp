import pytest
from app.agents import researcher, analyst, writer
from app.core.supervisor import run_workflow, resume_workflow
from app.core import supervisor

@pytest.fixture(autouse=True)
def mock_llm(monkeypatch):
    def fake_llm(system_prompt, user_prompt):
        return "AI has benefits and challenges in healthcare."

    monkeypatch.setattr(researcher, "generate_response", fake_llm)
    monkeypatch.setattr(analyst, "generate_response", fake_llm)
    monkeypatch.setattr(writer, "generate_response", fake_llm)
    monkeypatch.setattr(
    researcher,
    "retrieve_relevant_memories",
    lambda request: []
)
    monkeypatch.setattr(
    supervisor,
    "save_memory",
    lambda state: None
)


def test_workflow_without_approval():
    state = run_workflow(
        "Research AI in healthcare"
    )

    assert state["status"] == "awaiting_approval"
    assert state["human_approved"] is False
    assert state["final_response"] == ""


def test_workflow_with_approval():
    state = run_workflow(
        "Research AI in healthcare",
        human_approved=True
    )

    assert state["status"] == "completed"
    assert state["human_approved"] is True
    assert state["final_response"] != ""



def test_workflow_plan():
    state = run_workflow(
        "Research AI in healthcare"
    )

    assert state["plan"] == [
        "researcher",
        "analyst",
        "writer"
    ]

    assert state["status"] == "awaiting_approval"



def test_agent_execution_history():
    state = run_workflow(
        "Research AI in healthcare",
        human_approved=True
    )

    agents = [
        item["agent"]
        for item in state["agent_history"]
    ]

    assert "researcher" in agents
    assert "analyst" in agents
    assert "writer" in agents
    assert "supervisor" in agents


def test_workflow_rejects_empty_request():
    state = run_workflow("")

    assert state["status"] == "failed"
    assert len(state["errors"]) > 0