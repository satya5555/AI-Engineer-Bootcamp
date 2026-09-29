import os
import tempfile
import streamlit as st

from app.loader import PDFLoader
from app.splitter import TextSplitter
from app.vectorstore import VectorStore
from app.keyword_search import KeywordSearch
from app.semantic_search import SemanticSearch
from app.hybrid_search import HybridSearch
from app.chat import RAGChat


st.set_page_config(
    page_title="Hybrid Search",
    page_icon="🔎",
    layout="wide"
)


st.title("🔎 Hybrid RAG Search")
st.caption(
    "BM25 Keyword Search + Semantic Search + RRF"
)


uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


if uploaded_file:

    # ---------------------------------------------
    # Save uploaded PDF temporarily
    # ---------------------------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        temp_path = temp_file.name


    # ---------------------------------------------
    # Load PDF
    # ---------------------------------------------

    loader = PDFLoader()

    documents = loader.load(
        temp_path
    )


    # ---------------------------------------------
    # Split document
    # ---------------------------------------------

    splitter = TextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split(
        documents
    )


    st.success(
        f"Loaded {len(documents)} pages "
        f"and created {len(chunks)} chunks."
    )


    # ---------------------------------------------
    # Create retrievers
    # ---------------------------------------------

    keyword_search = KeywordSearch(
        chunks
    )

    vector_store = VectorStore()

    semantic_search = SemanticSearch(
        vector_store.get_store()
    )

    hybrid_search = HybridSearch(
        keyword_search,
        semantic_search
    )

    chat = RAGChat()


    # ---------------------------------------------
    # Question
    # ---------------------------------------------

    question = st.text_input(
        "Ask a question about your document"
    )


    if question:

        with st.spinner(
            "Searching and generating answer..."
        ):

            results = hybrid_search.search(
                question,
                k=4
            )

            answer, sources = chat.answer(
                question,
                results
            )


        # -----------------------------------------
        # Answer
        # -----------------------------------------

        st.subheader("Answer")

        st.write(answer)


        # -----------------------------------------
        # Sources
        # -----------------------------------------

        st.subheader("Sources")

        if sources:

            for source in sources:

                st.write(
                    f"📄 Page {source['page']} "
                    f"| RRF: "
                    f"{source['rrf_score']:.6f}"
                )

        else:

            st.write(
                "No sources found."
            )


        # -----------------------------------------
        # Retrieval details
        # -----------------------------------------

        with st.expander(
            "🔍 Retrieval Details"
        ):

            for index, result in enumerate(
                results
            ):

                document = result["document"]

                page = document.metadata.get(
                    "page",
                    0
                ) + 1

                st.write(
                    f"### Result {index + 1}"
                )

                st.write(
                    f"**Page:** {page}"
                )

                st.write(
                    f"**RRF:** "
                    f"{result['rrf_score']:.6f}"
                )

                st.write(
                    f"**BM25:** "
                    f"{result['keyword_score']:.6f}"
                )

                st.write(
                    f"**Semantic:** "
                    f"{result['semantic_score']:.6f}"
                )

                st.write(
                    document.page_content
                )


    os.remove(temp_path)