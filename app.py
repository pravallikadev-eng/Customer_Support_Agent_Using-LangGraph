import streamlit as st
from agent.graph import build_graph

graph = build_graph()

st.title("TechTrend Innovations – AI Customer Support (Gemini)")

user_id = st.text_input("User ID", "user_001")
query = st.text_input("Ask your question")

if st.button("Send"):
    state = {
        "user_id": user_id,
        "thread_id": user_id,
        "messages": [{"role": "user", "content": query}],
        "user_history": [],
        "needs_human": False
    }

    result = graph.invoke(state)

    for msg in result["messages"]:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
