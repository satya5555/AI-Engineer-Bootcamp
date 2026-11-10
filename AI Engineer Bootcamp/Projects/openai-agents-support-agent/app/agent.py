
from agents import Agent, function_tool

from app.support_tools import (
    get_order_status,
    get_return_policy
)


@function_tool
def lookup_order(order_id: str) -> str:
    """
    Look up an order using its order ID.
    """

    result = get_order_status(order_id)

    return str(result)


@function_tool
def check_return_policy() -> str:
    """
    Retrieve the return and refund policy.
    """

    result = get_return_policy()

    return str(result)


support_agent = Agent(
    name="ShopEaseSupportAgent",
    model="gpt-4.1-mini",
    instructions="""
    You are a customer support assistant for ShopEase.

    Your responsibilities:

    1. Help customers check their order status.
    2. Answer questions about returns and refunds.
    3. Use lookup_order when a customer asks about an order.
    4. Use check_return_policy when a customer asks
       about return or refund policies.
    5. Never invent order information.
    6. Be polite and concise.

    If an order does not exist, clearly explain that
    it could not be found.
    """,
    tools=[
        lookup_order,
        check_return_policy
    ]
)
