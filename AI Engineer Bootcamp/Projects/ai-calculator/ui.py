import streamlit as st

from app.calculator import Calculator


st.set_page_config(
    page_title="AI Calculator",
    page_icon="🧮",
    layout="centered",
)


st.title("🧮 AI Calculator")
st.caption(
    "An AI-powered calculator using Gemini tool calling"
)


if "calculator" not in st.session_state:
    st.session_state.calculator = Calculator()


question = st.text_input(
    "Ask a calculation",
    placeholder="Example: What is 125 multiplied by 8?",
)


if st.button("Calculate", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Thinking..."):

            answer = st.session_state.calculator.calculate(
                question
            )

        st.subheader("Result")
        st.write(answer)