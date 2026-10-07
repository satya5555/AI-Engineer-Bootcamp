import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.tools import add, multiply, get_word_count

load_dotenv()


class SimpleAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0
        )

        self.tools = {
            "add": add,
            "multiply": multiply,
            "get_word_count": get_word_count
        }
    def execute_tool(self, tool_name, args):
        if tool_name == "add":
            return self.tools["add"](int(args[0]), int(args[1]))

        if tool_name == "multiply":
            return self.tools["multiply"](int(args[0]), int(args[1]))

        if tool_name == "get_word_count":
            return self.tools["get_word_count"](args[0])

        return None

    def run(self, question):
        prompt = f"""
    You are a simple AI agent.

    User question:
    {question}

    Available tools:

    1. add(a, b)
    Use for addition.

    2. multiply(a, b)
    Use for multiplication.

    3. get_word_count(text)
    Use for counting words.

    Decide whether a tool is required.

    If a tool is required, respond ONLY in this format:

    TOOL: tool_name
    ARGS: argument1, argument2

    If no tool is required, respond ONLY:

    DIRECT: your answer
    """

        response = self.llm.invoke(prompt)
        decision = response.content

        if isinstance(decision, list):
            decision = decision[0]["text"]

        if decision.startswith("DIRECT:"):
            return decision.replace("DIRECT:", "").strip()

        if decision.startswith("TOOL:"):
            lines = decision.splitlines()

            tool_name = lines[0].replace("TOOL:", "").strip()
            args_text = lines[1].replace("ARGS:", "").strip()

            args = [item.strip() for item in args_text.split(",")]

            result = self.execute_tool(tool_name, args)

            if result is None:
                return "Unknown tool."

            final_prompt = f"""
            User question:
            {question}

            The tool `{tool_name}` was executed.

            Tool result:
            {result}

            Give the user a clear final answer based on this result.
            """

            final_response = self.llm.invoke(final_prompt)
            final_answer = final_response.content

            if isinstance(final_answer, list):
                final_answer = final_answer[0]["text"]

            return final_answer

        return "Could not understand the agent decision."