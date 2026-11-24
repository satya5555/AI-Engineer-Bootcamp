
from app.core.state import (
    update_state,
    record_agent_activity,
    record_agent_message
)

from app.core.llm_client import generate_response
from app.tools.registry import execute_tool


def analyst_agent(state):
    """Analyze research findings using an LLM and text analysis tool."""

    findings = state["research_findings"]

    if not findings:
        raise ValueError("No research findings available")

    # Step 1: Convert findings into text
    text = "\n".join(
        str(item) for item in findings
    )

    # Step 2: Execute the text analysis tool
    statistics = execute_tool(
        "analyze_text",
        text=text
    )

    # Step 3: Prepare the LLM prompts
    system_prompt = """
    You are an analytical AI agent.

    Analyze the supplied research findings.
    Identify benefits, challenges, opportunities and risks.
    Do not introduce unsupported facts.

    Use previous workflow context only when relevant.
    Do not treat historical information as independently
    verified current information.
    """

    user_prompt = f"""
    Research findings:

    {findings}

    Research statistics:
    {statistics}

    Previous workflow context:
    {state["retrieved_memories"]}

    Provide your analysis using these sections:

    1. Key themes
    2. Benefits
    3. Challenges
    4. Overall assessment
    """

    # Step 4: Generate the analysis
    result = generate_response(
        system_prompt,
        user_prompt
    )

    # Step 5: Update shared state
    update_state(state, {
        "analysis": result,
        "current_agent": "analyst",
        "status": "analysis_completed"
    })

    # Step 6: Record agent communication
    record_agent_message(
        state,
        "analyst",
        "writer",
        result
    )

    # Step 7: Record agent activity
    record_agent_activity(
        state,
        "analyst",
        "Analyzed research using Qwen and text analysis tool"
    )

    return state
