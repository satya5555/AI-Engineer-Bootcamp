from app.tools import add, subtract, multiply, divide


print("Add:", add(10, 5))
print("Subtract:", subtract(10, 5))
print("Multiply:", multiply(10, 5))
print("Divide:", divide(10, 5))


try:
    divide(10, 0)
except ValueError as error:
    print("Division Error:", error)