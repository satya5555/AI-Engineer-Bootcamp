import streamlit as st

from app.agent import SimpleAgent


st.set_page_config(
    page_title="Simple AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Simple AI Agent")
st.write("An AI agent that can decide when to use tools.")

question = st.text_input(
    "Ask the agent",
    placeholder="What is 25 multiplied by 4?"
)

if st.button("Run Agent"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Agent is thinking..."):
        agent = SimpleAgent()
        answer = agent.run(question)

    st.subheader("Final Answer")
    st.write(answer)