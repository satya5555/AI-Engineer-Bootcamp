from app.support_tools import get_order_status, get_return_policy
from app.agent import support_agent


def main():

    print("TEST 1: Lookup Order")
    print(get_order_status("ORD1001"))

    print("\nTEST 2: Invalid Order")
    print(get_order_status("ORD9999"))

    print("\nTEST 3: Check Return Policy")
    print(get_return_policy())

    print("\nTEST 4: Verify SDK Agent Tools")

    for tool in support_agent.tools:
        print(f"Registered tool: {tool.name}")


if __name__ == "__main__":
    main()