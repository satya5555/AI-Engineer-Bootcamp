
import pytest

from app.agents import researcher, analyst, writer
from app.core import supervisor
from app.core.supervisor import run_workflow, resume_workflow


@pytest.fixture(autouse=True)
def mock_llm(monkeypatch):

    def fake_llm(system_prompt, user_prompt):
        return "AI has benefits and challenges in healthcare."

    monkeypatch.setattr(researcher, "generate_response", fake_llm)
    monkeypatch.setattr(analyst, "generate_response", fake_llm)
    monkeypatch.setattr(writer, "generate_response", fake_llm)

    # Prevent tests from modifying actual persistent memory
    monkeypatch.setattr(
        supervisor,
        "save_memory",
        lambda state: None
    )
    monkeypatch.setattr(
    researcher,
    "retrieve_relevant_memories",
    lambda request: []
)
    monkeypatch.setattr(
    researcher,
    "retrieve_relevant_memories",
    lambda request: []
)


def test_resume_after_approval():
    state = run_workflow("Research AI in healthcare")

    assert state["status"] == "awaiting_approval"

    state = resume_workflow(state, approved=True)

    assert state["status"] == "completed"
    assert state["human_approved"] is True
    assert state["final_response"] != ""


def test_resume_after_rejection():
    state = run_workflow("Research AI in healthcare")

    state = resume_workflow(state, approved=False)

    assert state["status"] == "rejected"
    assert state["final_response"] == ""


def test_resume_invalid_workflow():
    state = run_workflow(
        "Research AI in healthcare",
        human_approved=True
    )

    with pytest.raises(ValueError):
        resume_workflow(state, approved=True)
