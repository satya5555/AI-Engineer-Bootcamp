import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


class RAGChat:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-3.6-flash"
            ),
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def answer(self, question: str, documents):

        # No relevant documents
        if not documents:
            return (
                "I couldn't find sufficiently relevant "
                "information in the document.",
                []
            )

        context_parts = []
        sources = []
        seen_sources = set()

        # Build structured context
        for document, score in documents:

            page = document.metadata.get(
                "page",
                None
            )

            if isinstance(page, int):
                page_number = page + 1
            else:
                page_number = "Unknown"

            context_parts.append(
                f"[Source: Page {page_number}]\n"
                f"{document.page_content}"
            )

            # Avoid duplicate source pages
            source_key = page_number

            if source_key not in seen_sources:
                sources.append({
                    "page": page_number,
                    "score": score
                })

                seen_sources.add(source_key)

        # Combine chunks
        context = "\n\n".join(context_parts)

        # Grounded RAG prompt
        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer is not supported by the context,
   say that you could not find the information
   in the document.
4. Give a concise and direct answer.

Context:
{context}

Question:
{question}

Answer:
"""

        # Generate answer
        response = self.llm.invoke(prompt)

        # Normalize Gemini response
        if isinstance(response.content, str):

            answer = response.content

        elif isinstance(response.content, list):

            text_parts = []

            for item in response.content:

                if isinstance(item, dict):

                    text = item.get("text")

                    if text:
                        text_parts.append(text)

            answer = "\n".join(text_parts)

        else:

            answer = str(response.content)

        return answer, sources