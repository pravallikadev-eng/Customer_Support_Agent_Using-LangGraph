import os
from agent.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


def trim_and_filter_messages(messages):
    filtered = [
        m for m in messages
        if m["content"].lower() not in ["hi", "hello", "hey"]
    ]
    return filtered[-5:]


def support_llm_node(state: AgentState):
    state["messages"] = trim_and_filter_messages(state["messages"])

    # Convert LangGraph messages → Gemini format
    prompt = "\n".join(
        f"{m['role']}: {m['content']}" for m in state["messages"]
    )

    response = llm.invoke(
        f"""
You are a customer support agent for TechTrend Innovations.
Answer common support questions clearly.
If the issue is complex, say 'ESCALATE_TO_HUMAN'.

Conversation:
{prompt}
"""
    )

    answer = response.content

    if "ESCALATE_TO_HUMAN" in answer.upper():
        state["needs_human"] = True
        answer = "This issue requires human assistance."
    else:
        state["needs_human"] = False

    state["messages"].append({"role": "assistant", "content": answer})

    state["user_history"].append({
        "query": state["messages"][-2]["content"],
        "resolution": answer
    })

    return state


def history_tool_node(state: AgentState):
    if state["user_history"]:
        last = state["user_history"][-1]
        state["messages"].append({
            "role": "assistant",
            "content": f"Previously, you asked: {last['query']}"
        })
    return state


def human_escalation_node(state: AgentState):
    state["messages"].append({
        "role": "assistant",
        "content": "A human support agent will review this issue shortly."
    })
    return state


def route_decision(state: AgentState):
    return "human" if state["needs_human"] else "history"
