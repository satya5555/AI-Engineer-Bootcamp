from app.calculator import Calculator


calculator = Calculator()

question = "What is 50 plus 75?"

print(f"Question: {question}")

try:
    answer = calculator.calculate(question)
    print(f"Answer: {answer}")

except Exception as error:
    print(f"Error: {error}")