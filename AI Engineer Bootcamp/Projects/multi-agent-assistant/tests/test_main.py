
import pytest

from app.agents import researcher, analyst, writer
from app.core import supervisor
from app.main import main


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


def test_main_with_approval(monkeypatch, capsys):
    inputs = iter([
        "Research AI in healthcare",
        "yes"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main()

    output = capsys.readouterr().out

    assert "MULTI-AGENT ASSISTANT" in output
    assert "Final Response" in output
    assert "completed" in output


def test_main_with_rejection(monkeypatch, capsys):
    inputs = iter([
        "Research AI in healthcare",
        "no"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main()

    output = capsys.readouterr().out

    assert "Workflow rejected by human" in output
