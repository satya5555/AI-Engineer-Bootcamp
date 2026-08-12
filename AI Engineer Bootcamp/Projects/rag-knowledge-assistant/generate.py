import os

from dotenv import load_dotenv
from google import genai


load_dotenv(".env.local")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, context):
    prompt = f"""
You are a helpful company knowledge assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided knowledge base."

Do not invent or assume information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    answer = generate_answer(
        "What are the working hours?",
        "The standard working hours are from 9:00 AM to 6:00 PM, Monday through Friday."
    )

    print(answer)