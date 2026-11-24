from app.core.llm_client import generate_response
from app.core.state import (
    update_state,
    record_agent_activity,
    record_agent_message
)
from app.core.memory import retrieve_relevant_memories

from app.tools.registry import execute_tool



def research_agent(state):
    """Retrieve local knowledge and create an LLM research summary."""

    request = state["user_request"]
    previous_memories = retrieve_relevant_memories(request)

    update_state(state, {
        "retrieved_memories": previous_memories
    })

    search_results = execute_tool(
    "search_knowledge",
    query=request,
    limit=5
)

    source_data = "\n".join(
    f"- {item['content']}"
    for item in search_results
)

    system_prompt = """
    You are a research assistant.

    Use only the supplied source information.
    Do not invent statistics, studies or references.
    Clearly explain the relevant findings.
    """

    user_prompt = f"""
User request:
{request}

Available source information:
{source_data}

Relevant information from previous workflows:
{previous_memories}

Use the available source information to answer the current request.
Use previous memories only as supporting context.
Do not present previous findings as newly verified facts.

Identify relevant findings and summarize them clearly.
"""

    result = generate_response(
        system_prompt,
        user_prompt
    )

    update_state(state, {
        "research_findings": [result],
        "current_agent": "researcher",
        "status": "research_completed"
    })
    record_agent_message(
    state,
    "researcher",
    "analyst",
    result
)

    record_agent_activity(
        state,
        "researcher",
        "Generated research summary using Qwen"
    )

    return state