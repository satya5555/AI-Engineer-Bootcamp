
from datetime import datetime, timezone


def create_initial_state(user_request):
    """Create the initial state for a multi-agent workflow."""

    if not user_request or not user_request.strip():
        raise ValueError("User request cannot be empty")

    return {
        "user_request": user_request,
        "plan": [],
        "research_findings": [],
        "retrieved_memories": [],
        "analysis": "",
        "final_response": "",
        "status": "started",
        "current_agent": None,
        "agent_history": [],
        "agent_messages": [],
        "errors": [],
        "human_approved": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }


def update_state(state, updates):
    """Update workflow state using approved fields."""

    allowed_fields = {
        "plan",
        "research_findings",
        "retrieved_memories",
        "analysis",
        "final_response",
        "status",
        "current_agent",
        "human_approved",
        "agent_messages"
    }

    for key, value in updates.items():
        if key not in allowed_fields:
            raise ValueError(
                f"State field cannot be updated: {key}"
            )

        state[key] = value

    return state


def record_agent_activity(state, agent_name, action):
    """Record agent activity."""

    activity = {
        "agent": agent_name,
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    state["agent_history"].append(activity)

    return state


def record_agent_message(state, sender, receiver, content):
    """Record communication between agents."""

    message = {
        "sender": sender,
        "receiver": receiver,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    state["agent_messages"].append(message)

    return state


def record_error(state, agent_name, error_message):
    """Record workflow errors."""

    state["errors"].append({
        "agent": agent_name,
        "error": str(error_message),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    state["status"] = "failed"

    return state
