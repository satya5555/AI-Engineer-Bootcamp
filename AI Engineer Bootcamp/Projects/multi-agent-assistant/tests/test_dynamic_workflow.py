
import pytest

from app.core import supervisor
from app.core.supervisor import run_workflow, resume_workflow


@pytest.fixture(autouse=True)
def mock_workflow(monkeypatch):

    def fake_llm(system_prompt, user_prompt):
        return "AI has benefits and challenges in healthcare."

    monkeypatch.setattr(
        supervisor,
        "save_memory",
        lambda state: None
    )

    monkeypatch.setattr(
        "app.agents.researcher.generate_response",
        fake_llm
    )

    monkeypatch.setattr(
        "app.agents.analyst.generate_response",
        fake_llm
    )

    monkeypatch.setattr(
        "app.agents.writer.generate_response",
        fake_llm
    )

    monkeypatch.setattr(
        "app.agents.researcher.retrieve_relevant_memories",
        lambda request: []
    )


def test_research_workflow():
    state = run_workflow("Research AI in healthcare")

    assert state["plan"] == [
        "researcher",
        "analyst",
        "writer"
    ]

    assert state["status"] == "awaiting_approval"


def test_analysis_workflow():
    state = run_workflow("Analyze the healthcare AI findings")

    assert state["plan"] == [
        "analyst",
        "writer"
    ]

    assert state["status"] == "awaiting_approval"


def test_writing_workflow():
    state = run_workflow("Summarize the findings")

    assert state["plan"] == ["writer"]
    assert state["status"] == "awaiting_approval"

    state = resume_workflow(state, approved=True)

    print("\nWRITER ERROR DETAILS:")
    print(state["errors"])

    print("\nFINAL WORKFLOW STATE:")
    print(state)

    assert state["status"] == "completed"
    assert state["final_response"] != ""


def test_research_workflow_completion():
    state = run_workflow("Research AI in healthcare")

    state = resume_workflow(state, approved=True)

    assert state["status"] == "completed"
    assert state["human_approved"] is True
