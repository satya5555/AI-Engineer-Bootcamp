import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.memory import ChatMemory


load_dotenv()


class ChatService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        self.memory = ChatMemory(
            max_messages=10
        )

    def chat(self, user_input: str) -> str:
        self.memory.add_user_message(user_input)
        print("\n--- Conversation History ---")
        
        for message in self.memory.get_history():
            print(
                        f"{message.type}: {message.content}"
                    )
        print("-----------------------------\n")
        
        response = self.llm.invoke(
            self.memory.get_history()
        )

        self.memory.add_ai_message(
            response.content
        )

        return response.content
        

    def clear(self):
        self.memory.clear()