from langchain_core.messages import HumanMessage
from app.graph import agent


def main():

    config = {
        "configurable": {
            "thread_id": "conversation_1"
        }
    }

    print("LangGraph Native Tool Calling Assistant")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            },
            config=config
        )

        print("\nAI:", result["messages"][-1].content)
        print()


if __name__ == "__main__":
    main()