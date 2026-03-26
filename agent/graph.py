from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import (
    support_llm_node,
    history_tool_node,
    human_escalation_node,
    route_decision
)
from memory.store import memory


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("llm", support_llm_node)
    builder.add_node("history", history_tool_node)
    builder.add_node("human", human_escalation_node)

    builder.set_entry_point("llm")

    builder.add_conditional_edges(
        "llm",
        route_decision,
        {
            "history": "history",
            "human": "human"
        }
    )

    builder.add_edge("history", END)
    builder.add_edge("human", END)

    return builder.compile(checkpointer=memory)
