import streamlit as st

from app.chat import ChatService


st.set_page_config(
    page_title="AI Chat Memory",
    page_icon="🧠",
    layout="centered",
)


st.title("🧠 AI Chat Memory")
st.caption("A conversational AI assistant with session-based memory.")


# Initialize chat service once per session
if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()


# Initialize displayed messages
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input
user_input = st.chat_input(
    "Ask something..."
)


if user_input:
    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_service.chat(
                user_input
            )

        st.write(response)
        st.caption(
        f"Memory: {len(st.session_state.messages)} messages"
)

    # Store AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# Clear conversation
if st.button("🗑️ Clear Conversation"):
    st.session_state.chat_service.clear()
    st.session_state.messages = []
    st.rerun()