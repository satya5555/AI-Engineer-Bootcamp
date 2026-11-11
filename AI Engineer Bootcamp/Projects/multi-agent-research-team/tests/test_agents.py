from app.agents import researcher, analyst, writer, reviewer

from app.supervisor import run_research_team

def test_researcher():
    data = [
        "AI helps detect diseases.",
        "AI improves hospital operations."
    ]

    result = researcher("AI", data)

    assert len(result["findings"]) == 2


def test_analyst():
    research = {
        "topic": "AI Healthcare",
        "findings": [
            "AI helps detect diseases.",
            "AI improves hospital operations."
        ]
    }

    result = analyst(research)

    assert "insights" in result


def test_writer():
    analysis = {
        "topic": "AI Healthcare",
        "total_findings": 3,
        "insights": [
            "AI helps doctors.",
            "AI improves hospitals.",
            "AI supports research."
        ]
    }

    result = writer(analysis)

    assert "RESEARCH REPORT" in result["report"]
    assert "Total findings: 3" in result["report"]


def test_reviewer():
    report = {
        "report": (
            "RESEARCH REPORT\n"
            "- Finding 1\n"
            "- Finding 2\n"
            "- Finding 3\n"
        )
    }

    result = reviewer(report)

    assert result["approved"] is True

def test_supervisor_workflow():
    data = [
        "AI helps doctors detect diseases.",
        "AI improves hospital operations.",
        "AI supports medical research.",
        "AI helps predict patient health risks."
    ]

    result = run_research_team("AI", data)

    assert result["review"]["approved"] is True
    assert len(result["research"]["findings"]) >= 3
    assert "RESEARCH REPORT" in result["report"]["report"]