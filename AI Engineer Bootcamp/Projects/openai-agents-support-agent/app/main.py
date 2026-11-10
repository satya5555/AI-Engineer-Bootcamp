
from dotenv import load_dotenv
from agents import Runner
from app.agent import support_agent

# Load API key
load_dotenv()

def main():
    print("Welcome to ShopEase Customer Support!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Thank you for contacting ShopEase!")
            break

        result = Runner.run_sync(
            support_agent,
            user_input
        )

        print("\nSupport Agent:", result.final_output)
        print()

if __name__ == "__main__":
    main()
