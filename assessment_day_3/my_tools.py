from pathlib import Path
import ast
import operator
import re

BASE_DIR = Path(__file__).resolve().parent

# -------------------------------
# Tool 1: Read a local HTML page
# -------------------------------

def read_webpage(path):
    """Read a local HTML file and return its text content."""

    requested_path = Path(path)

    if not requested_path.is_absolute():
        requested_path = BASE_DIR / requested_path

    try:
        resolved_path = requested_path.resolve()
        resolved_path.relative_to(BASE_DIR.resolve())
    except (ValueError, OSError):
        return "Error: Access outside the project folder is not allowed."

    if not resolved_path.is_file():
        return f"Error: File not found: {path}"

    try:
        html = resolved_path.read_text(encoding="utf-8")

        # Remove script, style, and HTML tags.
        html = re.sub(
            r"<(script|style)\b[^>]*>.*?</\1>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL
        )
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    except OSError as error:
        return f"Error reading webpage: {error}"


# -------------------------------
# Tool 2: Safe calculator
# -------------------------------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_expression(node):
    """Evaluate only supported arithmetic expressions."""

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric values are allowed.")

    if isinstance(node, ast.BinOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported arithmetic operator.")

        left = evaluate_expression(node.left)
        right = evaluate_expression(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large.")

        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            if right == 0:
                raise ValueError("Division by zero is not allowed.")

        result = operation(left, right)

        if isinstance(result, (int, float)) and abs(result) > 1e100:
            raise ValueError("Result is too large.")

        return result

    if isinstance(node, ast.UnaryOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported unary operator.")

        return operation(evaluate_expression(node.operand))

    raise ValueError("Invalid arithmetic expression.")


def calculator(expression):
    """Calculate a basic arithmetic expression safely."""

    try:
        if len(expression) > 200:
            return "Error: Expression is too long."

        tree = ast.parse(expression, mode="eval")
        result = evaluate_expression(tree.body)

        return f"Calculation result: {result}"

    except (ValueError, SyntaxError, TypeError, OverflowError,
            ZeroDivisionError) as error:
        return f"Calculator error: {error}"


# -------------------------------
# Tool schemas
# -------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": (
                "Read a local HTML report and return its text. "
                "Use this to inspect the student attendance report."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Relative path, for example "
                            "data/attendance.html"
                        )
                    }
                },
                "required": ["path"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Calculate a basic arithmetic expression. "
                "Example: (85 / 100) * 100"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression to calculate."
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "read_webpage": read_webpage,
    "calculator": calculator
}


if __name__ == "__main__":
    print("TEST 1: Read attendance report")
    print(read_webpage("data/attendance.html"))

    print("\nTEST 2: Calculate attendance")
    print(calculator("(85 / 100) * 100"))

    print("\nTEST 3: Missing file")
    print(read_webpage("data/missing.html"))

    print("\nTEST 4: Division by zero")
    print(calculator("10 / 0"))