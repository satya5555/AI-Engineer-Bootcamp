
# Fake order data for local testing only

orders = {
    "ORD1001": {
        "customer": "Alex",
        "status": "Shipped",
        "amount": 1499,
        "currency": "INR"
    },
    "ORD1002": {
        "customer": "Sam",
        "status": "Delivered",
        "amount": 799,
        "currency": "INR"
    },
    "ORD1003": {
        "customer": "Jordan",
        "status": "Processing",
        "amount": 2499,
        "currency": "INR"
    }
}

return_policy = {
    "return_window_days": 7,
    "refund_processing_days": "5-7 business days",
    "condition": "The product must be eligible for return."
}
    