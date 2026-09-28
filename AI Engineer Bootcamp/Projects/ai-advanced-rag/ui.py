import os
import tempfile

import streamlit as st

from app.loader import PDFLoader
from app.splitter import TextSplitter
from app.vectorstore import VectorStore
from app.retriever import DocumentRetriever
from app.chat import RAGChat


st.set_page_config(
    page_title="Advanced RAG",
    page_icon="📚",
    layout="wide"
)


st.title("📚 Advanced Document Chat")
st.caption(
    "Ask questions about your PDF using "
    "retrieval-augmented generation."
)


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        pdf_path = temp_file.name

    try:

        # Load PDF
        loader = PDFLoader()

        documents = loader.load(
            pdf_path
        )

        st.success(
            f"Loaded {len(documents)} pages."
        )

        # Split documents
        splitter = TextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split(
            documents
        )

        st.info(
            f"Created {len(chunks)} chunks."
        )

        # Create vector store
        vector_store = VectorStore()

        vector_store.add_documents(
            chunks
        )

        retriever = DocumentRetriever(
            vector_store.get_store()
        )

        chat = RAGChat()

        # --------------------------------------------------
        # Question
        # --------------------------------------------------

        question = st.text_input(
            "Ask a question about the document"
        )

        if question:

            with st.spinner(
                "Searching the document..."
            ):

                results = retriever.search(
                    question,
                    k=4,
                    max_distance=0.70
                )

            if not results:

                st.warning(
                    "I couldn't find sufficiently "
                    "relevant information in the document."
                )

            else:

                st.write(
                    f"Retrieved {len(results)} "
                    f"relevant chunks."
                )

                with st.spinner(
                    "Generating answer..."
                ):

                    answer, sources = chat.answer(
                        question,
                        results
                    )

                # --------------------------------------------------
                # Answer
                # --------------------------------------------------

                st.subheader("Answer")

                st.write(answer)

                # --------------------------------------------------
                # Sources
                # --------------------------------------------------

                st.subheader("Sources")

                for source in sources:

                    st.write(
                        f"📄 Page {source['page']} "
                        f"(distance: "
                        f"{source['score']:.4f})"
                    )

    finally:

        if os.path.exists(pdf_path):
            os.remove(pdf_path)