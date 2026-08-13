from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL


class Generator:

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY was not found."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(self, question, context):

        context_text = "\n\n".join(context)

        prompt = f"""
You are a company knowledge assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the context does not contain the answer, say:
"I don't have enough information in the provided knowledge base."
4. Keep the answer concise and clear.

Context:
{context_text}

Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text