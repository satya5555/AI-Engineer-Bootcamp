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

    def answer(self, question, results):

        if not results:
            return (
                "I couldn't find relevant information in the document.",
                []
            )

        context_parts = []
        sources = []
        seen_pages = set()

        for result in results:

            document = result["document"]

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

            if page_number not in seen_pages:

                sources.append({
                    "page": page_number,
                    "rrf_score": result["rrf_score"],
                    "keyword_score": result["keyword_score"],
                    "semantic_score": result["semantic_score"]
                })

                seen_pages.add(page_number)

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not supported by the context,
   say that you could not find the information
   in the document.
4. Give a concise and direct answer.
5. Do not mention information that is not present
   in the context.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)

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