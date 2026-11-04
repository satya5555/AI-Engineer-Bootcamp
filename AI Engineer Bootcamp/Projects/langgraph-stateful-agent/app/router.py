from app.state import AgentState


def route_question(state: AgentState):

    if state["tool_name"] == "calculator":
        if state.get("steps", 0) < 3:
            return "execute_tool"

        return "generate_answer"

    return "save_turn"


def route_after_tool(state: AgentState):

    if state.get("steps", 0) < 3:
        return "process_question"

    return "generate_answer"