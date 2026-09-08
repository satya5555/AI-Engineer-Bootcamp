import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.memory import ChatMemory


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

memory = ChatMemory()

print("=" * 60)
print("🧠 AI Chat Memory")
print("=" * 60)
print("Type 'exit' to end the conversation.")
print()

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("\nGoodbye!")
        break

    if not user_input.strip():
        continue

    memory.add_user_message(user_input)

    response = llm.invoke(
        memory.get_history()
    )

    memory.add_ai_message(response.content)

    print(f"\nAI: {response.content}\n")
