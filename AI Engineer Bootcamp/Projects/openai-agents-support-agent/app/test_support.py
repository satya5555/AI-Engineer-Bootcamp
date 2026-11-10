
from app.support_tools import get_order_status, get_return_policy

print("TEST 1: Existing Order")
print(get_order_status("ORD1001"))

print("\nTEST 2: Another Existing Order")
print(get_order_status("ORD1002"))

print("\nTEST 3: Invalid Order")
print(get_order_status("ORD9999"))

print("\nTEST 4: Return Policy")
print(get_return_policy())
