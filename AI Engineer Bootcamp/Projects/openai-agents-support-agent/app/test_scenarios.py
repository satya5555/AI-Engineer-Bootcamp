import asyncio

from agents import Runner
from agents.testing import (
    ScriptedModel,
    function_call,
    assistant_message
)

from app.agent import support_agent


async def run_scenario(query, tool_call, response):

    scripted_model = ScriptedModel(
        steps=[
            {
                "output": [tool_call]
            },
            {
                "output": [assistant_message(response)]
            }
        ]
    )

    test_agent = support_agent.clone(
        model=scripted_model
    )

    result = await Runner.run(test_agent, query)

    print("\nCUSTOMER QUERY:")
    print(query)

    print("\nAGENT RESPONSE:")
    print(result.final_output)

    print("-" * 50)


async def main():

    print("SCENARIO 1: Existing Order")

    await run_scenario(
        "Where is my order ORD1001?",
        function_call(
            name="lookup_order",
            arguments={"order_id": "ORD1001"},
            call_id="call_001"
        ),
        "Your order ORD1001 has been shipped."
    )

    print("\nSCENARIO 2: Invalid Order")

    await run_scenario(
        "Where is my order ORD9999?",
        function_call(
            name="lookup_order",
            arguments={"order_id": "ORD9999"},
            call_id="call_002"
        ),
        "Sorry, we could not find an order with ID ORD9999."
    )

    print("\nSCENARIO 3: Return Policy")

    await run_scenario(
        "What is your return policy?",
        function_call(
            name="check_return_policy",
            arguments={},
            call_id="call_003"
        ),
        "Our return window is 7 days. Refunds take 5-7 business days."
    )


if __name__ == "__main__":
    asyncio.run(main())