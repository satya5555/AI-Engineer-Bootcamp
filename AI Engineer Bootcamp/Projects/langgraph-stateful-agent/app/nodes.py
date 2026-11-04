import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from app.state import AgentState
from app.tools import calculator
from langchain_core.messages import SystemMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

llm_with_tools = llm.bind_tools([calculator])


def assistant(state: AgentState):

    system_prompt = SystemMessage(
        content="""
        You are a helpful general-purpose AI assistant.

        You can answer general knowledge, programming,
        technical and conversational questions directly.

        You also have access to a calculator tool.

        Use the calculator only when the user requests
        a mathematical calculation.

        Do not claim that you can only perform calculations.
        If no tool is required, answer the user directly.

        Use previous conversation messages when relevant.
        """
    )

    messages = [system_prompt] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }