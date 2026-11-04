import sqlite3

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

from app.state import AgentState
from app.nodes import assistant
from app.tools import calculator


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("assistant", assistant)
    graph.add_node("tools", ToolNode([calculator]))

    graph.add_edge(START, "assistant")

    graph.add_conditional_edges(
        "assistant",
        tools_condition
    )

    graph.add_edge("tools", "assistant")

    conn = sqlite3.connect(
        "checkpoints.sqlite",
        check_same_thread=False
    )

    memory = SqliteSaver(conn)
    memory.setup()

    return graph.compile(checkpointer=memory)


agent = build_graph()