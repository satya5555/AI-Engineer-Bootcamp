import streamlit as st
from app.crew import research_crew

st.set_page_config(
    page_title="AI Research Crew",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Research Crew")

st.write(
    "A multi-agent AI research system powered by CrewAI and Gemini."
)

topic = st.text_input(
    "Enter your research topic",
    placeholder="Applications of RAG in Enterprise AI"
)

if st.button("Start Research"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("AI Research Crew is working..."):

        result = research_crew.kickoff(
            inputs={"topic": topic}
        )

    st.success("Research completed!")

    st.subheader("Final Research Report")

    st.markdown(str(result))