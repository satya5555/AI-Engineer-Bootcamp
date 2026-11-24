from app.core.planner import create_dynamic_plan


def test_research_plan():
    plan = create_dynamic_plan(
        "Research AI in healthcare"
    )

    assert plan == [
        "researcher",
        "analyst",
        "writer"
    ]


def test_analysis_plan():
    plan = create_dynamic_plan(
        "Analyze the healthcare AI findings"
    )

    assert plan == [
        "analyst",
        "writer"
    ]


def test_writing_plan():
    plan = create_dynamic_plan(
        "Summarize the findings"
    )

    assert plan == ["writer"]


def test_comparison_plan():
    plan = create_dynamic_plan(
        "Compare AI technologies"
    )

    assert plan == [
        "researcher",
        "analyst",
        "writer"
    ]