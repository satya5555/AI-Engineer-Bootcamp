from app.core.state import create_initial_state

from app.agents import researcher, analyst, writer


def fake_llm(system_prompt, user_prompt):
    return "AI can improve healthcare operations, but privacy is important."


def test_researcher_agent(monkeypatch):
    monkeypatch.setattr(
        researcher,
        "generate_response",
        fake_llm
    )
    monkeypatch.setattr(
    researcher,
    "retrieve_relevant_memories",
    lambda request: []
)

    state = create_initial_state(
        "Research AI in healthcare"
    )

    researcher.research_agent(state)

    assert len(state["research_findings"]) > 0
    assert state["status"] == "research_completed"


def test_analyst_agent(monkeypatch):
    monkeypatch.setattr(
        analyst,
        "generate_response",
        fake_llm
    )

    state = create_initial_state(
        "Research AI in healthcare"
    )

    state["research_findings"] = ["AI supports healthcare"]

    analyst.analyst_agent(state)

    assert state["analysis"] != ""
    assert state["status"] == "analysis_completed"


def test_writer_agent(monkeypatch):
    monkeypatch.setattr(
        writer,
        "generate_response",
        fake_llm
    )

    state = create_initial_state(
        "Research AI in healthcare"
    )

    state["research_findings"] = ["AI supports healthcare"]
    state["analysis"] = "AI has benefits and challenges."

    writer.writer_agent(state)

    assert state["final_response"] != ""
    assert state["status"] == "completed"



def test_writer_with_analysis_without_research():
    state = create_initial_state(
        "Research AI in healthcare"
    )

    state["analysis"] = "Some analysis"

    result = writer.writer_agent(state)

    assert result["status"] == "completed"
    assert result["final_response"] != ""
