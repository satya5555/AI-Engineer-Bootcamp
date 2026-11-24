
from app.core.state import (
    update_state,
    record_agent_activity
)
from app.core.llm_client import generate_response


def writer_agent(state):

    findings = state["research_findings"]
    analysis = state["analysis"]

    if not findings and not analysis:
        raise ValueError(
            "No research findings or analysis available"
        )

    system_prompt = """
    You are a professional AI writing agent.

    Your task is to create a clear and useful response
    using only the supplied information.

    If analysis is available, incorporate it.
    If analysis is unavailable, write directly from
    the supplied research findings.

    Do not invent facts, statistics, or references.
    """

    user_prompt = f"""
    User request:
    {state["user_request"]}

    Research findings:
    {findings}

    Analysis:
    {analysis}

    Previous workflow context:
    {state.get("retrieved_memories", [])}

    Write a well-structured response that addresses
    the user's request.
    """

    result = generate_response(
        system_prompt,
        user_prompt
    )

    update_state(state, {
        "final_response": result,
        "current_agent": "writer",
        "status": "completed"
    })

    record_agent_activity(
        state,
        "writer",
        "Generated final response"
    )

    return state
