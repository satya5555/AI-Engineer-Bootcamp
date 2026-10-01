import streamlit as st
from app.search import WebSearch
from app.researcher import Researcher
from app.synthesizer import Synthesizer
from app.evaluator import ResearchEvaluator


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI Research Assistant")
st.write(
    "Ask a research question and get a structured answer "
    "based on web evidence."
)


question = st.text_input(
    "Research Question",
    placeholder="What are the latest applications of RAG in enterprise AI?"
)


if st.button("Research"):
    if not question.strip():
        st.warning("Please enter a research question.")
        st.stop()

    with st.spinner("Researching..."):

        search = WebSearch()
        researcher = Researcher(search)
        synthesizer = Synthesizer()
        evaluator = ResearchEvaluator()

        evidence = researcher.research(question)

        answer = synthesizer.synthesize(
            question,
            evidence
        )

        evaluation = evaluator.evaluate(
            answer,
            evidence
        )

    st.subheader("Research Answer")
    st.markdown(answer)

    st.subheader("Sources")

    for index, item in enumerate(evidence, start=1):
        with st.expander(
            f"Source {index}: {item['title']}"
        ):
            st.write(item["snippet"])
            st.write(item["url"])

    st.subheader("Evaluation")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Evidence Count",
            evaluation["evidence_count"]
        )

    with col2:
        st.metric(
            "Sources Used",
            evaluation["sources_used"]
        )

    with col3:
        st.metric(
            "Source Coverage",
            f"{evaluation['source_coverage']:.2f}"
        )

    st.caption(
        f"Evaluation Status: {evaluation['status']}"
    )