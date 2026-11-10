import asyncio

from agents import Runner
from agents.testing import (
    ScriptedModel,
    function_call,
    assistant_message
)

from app.agent import support_agent


async def main():

    # Step 1: Define simulated model responses
    scripted_model = ScriptedModel(
        steps=[
            {
                "output": [
                    function_call(
                        name="lookup_order",
                        arguments={"order_id": "ORD1001"},
                        call_id="call_001"
                    )
                ]
            },
            {
                "output": [
                    assistant_message(
                        "Your order ORD1001 has been shipped. "
                        "The order amount is ₹1,499."
                    )
                ]
            }
        ]
    )

    # Step 2: Clone the agent with the scripted model
    test_agent = support_agent.clone(
        model=scripted_model
    )

    # Step 3: Run the agent
    result = await Runner.run(
        test_agent,
        "Where is my order ORD1001?"
    )

    # Step 4: Display the response
    print("\nCUSTOMER QUERY:")
    print("Where is my order ORD1001?")

    print("\nAGENT RESPONSE:")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())