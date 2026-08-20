import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.2
)


prompt = ChatPromptTemplate.from_template(
    """
You are an AI tutor.

Answer the following question clearly.

Question:
{question}

Keep the answer concise and beginner-friendly.
"""
)


parser = StrOutputParser()


chain = (
    {
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | parser
)


question = input("Ask a question: ")

response = chain.invoke(question)

print("\nAI Response:")
print("-" * 50)
print(response)