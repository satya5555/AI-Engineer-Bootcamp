import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class PDFChat:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

    def answer(self, question: str, documents) -> str:
        context_parts = []

        for document in documents:
            page = document.metadata.get("page_label")

            context_parts.append(
                f"[Page {page}]\n{document.page_content}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a helpful document assistant.

Answer the user's question using ONLY the information
provided in the document below.

When answering, mention the page number where the
information was found when possible.

If the answer cannot be found in the document, say:
"I couldn't find that information in the document."

Document:
{context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts = []

            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))

            return "\n".join(text_parts)

        return str(content)