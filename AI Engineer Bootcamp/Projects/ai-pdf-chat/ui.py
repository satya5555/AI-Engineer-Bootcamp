import os
import tempfile

import streamlit as st

from app.loader import PDFLoader
from app.chat import PDFChat


st.set_page_config(
    page_title="AI PDF Chat",
    page_icon="📄",
    layout="centered",
)

st.title("📄 AI PDF Chat")
st.caption(
    "Ask questions about a PDF using document-aware AI"
)

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"],
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getbuffer()
        )

        pdf_path = temp_file.name

    try:
        loader = PDFLoader()
        documents = loader.load(pdf_path)

        st.success(
            f"Loaded {len(documents)} pages."
        )

        question = st.text_input(
            "Ask a question about the PDF",
            placeholder="Example: What allergies are mentioned?",
        )

        if st.button("Ask", type="primary"):

            if not question.strip():
                st.warning(
                    "Please enter a question."
                )

            else:
                with st.spinner("Reading the document..."):

                    chat = PDFChat()

                    answer = chat.answer(
                        question,
                        documents
                    )

                st.subheader("Answer")
                st.write(answer)

    except Exception as error:

        st.error(
            f"Something went wrong: {error}"
        )

    finally:

        if os.path.exists(pdf_path):
            os.remove(pdf_path)