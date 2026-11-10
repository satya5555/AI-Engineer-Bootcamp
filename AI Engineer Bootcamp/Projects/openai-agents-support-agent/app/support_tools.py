
from app.mock_data import orders, return_policy


def get_order_status(order_id: str):
    """Retrieve order details using an order ID."""

    order = orders.get(order_id)

    if not order:
        return {
            "success": False,
            "message": f"No order found with ID {order_id}."
        }

    return {
        "success": True,
        "order_id": order_id,
        "customer": order["customer"],
        "status": order["status"],
        "amount": order["amount"],
        "currency": order["currency"]
    }


def get_return_policy():
    """Retrieve the ShopEase return and refund policy."""

    return {
        "return_window": return_policy["return_window_days"],
        "refund_processing": return_policy["refund_processing_days"],
        "condition": return_policy["condition"]
    }
