import uuid
import streamlit as st

from langchain_core.messages import HumanMessage
from app.graph import agent

def get_text(content):

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []

            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(item.get("text", ""))

            return "\n".join(parts)

        return str(content)

st.set_page_config(
    page_title="LangGraph AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# Initialize conversation
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}


st.title("🤖 LangGraph AI Assistant")
st.caption("Stateful AI Assistant powered by Gemini and LangGraph")


# Sidebar
with st.sidebar:

    st.subheader("Conversation Settings")

    if st.button("New Conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    if st.button("Clear Chat", use_container_width=True):

        agent.update_state(
            config,
            {"messages": []},
            as_node="assistant"
        )

        st.rerun()

    st.divider()

    st.write("**Current Thread ID**")
    st.caption(st.session_state.thread_id)


# Load conversation history
state = agent.get_state(config)
messages = state.values.get("messages", []) if state.values else []


# Display previous messages
for message in messages:

    if message.type in ["human", "ai"]:

        role = "user" if message.type == "human" else "assistant"

        with st.chat_message(role):
            st.markdown(get_text(message.content))


# User input
question = st.chat_input("Ask me anything...")

if question:

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = agent.invoke(
                {
                    "messages": [
                        HumanMessage(content=question)
                    ]
                },
                config=config
            )

            response = get_text(result["messages"][-1].content)

            st.markdown(response)

    st.rerun()
