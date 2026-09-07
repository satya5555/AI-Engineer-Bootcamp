import streamlit as st
from app.utility import AIUtility


st.set_page_config(
    page_title="AI Utility",
    page_icon="🧠",
    layout="centered",
)


st.title("🧠 AI Utility")
st.write(
    "A simple AI toolkit powered by LangChain and Gemini."
)


operation = st.selectbox(
    "Choose an operation",
    [
        "Summarize",
        "Rewrite",
        "Classify",
        "Analyze Support Ticket",
    ],
)


text = st.text_area(
    "Enter your text",
    height=200,
    placeholder="Enter some text here...",
)


if st.button("Run AI", type="primary"):

    if not text.strip():
        st.warning("Please enter some text first.")

    else:
        ai = AIUtility()

        try:
            with st.spinner("AI is processing..."):

                if operation == "Summarize":

                    result = ai.summarize(text)

                    st.subheader("📝 Summary")
                    st.write(result)

                elif operation == "Rewrite":

                    result = ai.rewrite(text)

                    st.subheader("✍️ Rewritten Text")
                    st.write(result)

                elif operation == "Classify":

                    result = ai.classify(text)

                    st.subheader("🏷️ Classification")
                    st.write(result)

                elif operation == "Analyze Support Ticket":

                    result = ai.analyze_ticket(text)

                    st.subheader("🎫 Ticket Analysis")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Category",
                            result.category,
                        )

                    with col2:
                        st.metric(
                            "Priority",
                            result.priority,
                        )

                    st.write("### Summary")
                    st.write(result.summary)

                    st.write("### Sentiment")
                    st.write(result.sentiment)

        except Exception as error:
            st.error(
                "Something went wrong while processing your request."
            )

            st.exception(error)

