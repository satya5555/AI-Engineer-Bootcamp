import ast
import operator

from langchain_core.tools import tool


operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow
}


def calculate(node):

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.UAdd):
            return calculate(node.operand)

        if isinstance(node.op, ast.USub):
            return -calculate(node.operand)

    if isinstance(node, ast.BinOp):
        op = operations.get(type(node.op))

        if op is None:
            raise ValueError("Unsupported operation")

        left = calculate(node.left)
        right = calculate(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large")

        return op(left, right)

    raise ValueError("Invalid expression")


@tool
def calculator(expression: str) -> str:
    """Perform basic arithmetic calculations."""

    try:
        if len(expression) > 100:
            return "Expression is too long."

        tree = ast.parse(expression, mode="eval")
        result = calculate(tree.body)

        return str(result)

    except Exception:
        return "Unable to calculate this expression."