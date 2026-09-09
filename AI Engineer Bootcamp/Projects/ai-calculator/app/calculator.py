import os

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.tools import add, subtract, multiply, divide


load_dotenv()


class Calculator:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        self.tools = [
            add,
            subtract,
            multiply,
            divide,
        ]

        self.tool_map = {
            "add": add,
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide,
        }

        self.llm_with_tools = self.llm.bind_tools(
            self.tools
        )

    def execute_tool_calls(self, response):
        tool_messages = []

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            tool = self.tool_map.get(tool_name)

            if tool is None:
                raise ValueError(
                    f"Unknown tool: {tool_name}"
                )

            try:
                result = tool(**tool_args)

                tool_messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call_id,
                    )
                )

            except Exception as error:
                tool_messages.append(
                    ToolMessage(
                        content=f"Tool error: {error}",
                        tool_call_id=tool_call_id,
                    )
                )

        return tool_messages

    def calculate(self, question: str) -> str:

        try:
            # Step 1: Ask Gemini
            response = self.llm_with_tools.invoke(question)

            # No tool required
            if not response.tool_calls:
                return response.content

            # Step 2: Execute tools
            tool_messages = self.execute_tool_calls(
                response
            )

            # Step 3: Send tool results back to Gemini
            messages = [
                question,
                response,
                *tool_messages,
            ]

            # Step 4: Generate final answer
            final_response = self.llm.invoke(
                messages
            )

            return final_response.content

        except Exception as error:
            error_message = str(error)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                return (
                    "Gemini API quota has been exceeded. "
                    "Please try again later."
                )

            return f"An unexpected error occurred: {error}"