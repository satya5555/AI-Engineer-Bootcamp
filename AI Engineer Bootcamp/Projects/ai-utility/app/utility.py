import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.models import TicketAnalysis
from app.prompts import (
    summarize_prompt,
    rewrite_prompt,
    classify_prompt,
)

load_dotenv()


class AIUtility:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2,
        )

        self.parser = StrOutputParser()

    def summarize(self, text: str) -> str:
        chain = summarize_prompt | self.llm | self.parser

        return chain.invoke({
            "text": text
        })

    def rewrite(self, text: str) -> str:
        chain = rewrite_prompt | self.llm | self.parser

        return chain.invoke({
            "text": text
        })

    def classify(self, text: str) -> str:
        chain = classify_prompt | self.llm | self.parser

        return chain.invoke({
            "text": text
        })

    def analyze_ticket(self, text: str) -> TicketAnalysis:
        structured_llm = self.llm.with_structured_output(
            TicketAnalysis
        )

        prompt = """
        Analyze the following customer support message.

        Customer message:
        {text}
        """

        chain = (
            ChatPromptTemplate.from_template(prompt)
            | structured_llm
        )

        return chain.invoke({
            "text": text
        })