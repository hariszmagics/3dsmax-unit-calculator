"""Pure conversion logic; independent of Max and Qt."""
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_UP
import ast

UNITS = ("mm", "cm", "m", "in", "ft")
FACTORS = dict(zip(UNITS, map(Decimal, ("1", "10", "1000", "25.4", "304.8"))))
MODES = ("Diameter → Radius", "Radius → Diameter", "Units only")
MULTIPLIERS = (Decimal("0.5"), Decimal("2"), Decimal("1"))


def number(text):
    try:
        value = Decimal(str(text).strip())
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a number, for example 200 or 25.4.") from None
    if not value.is_finite() or abs(value) > Decimal("1e15"):
        raise ValueError("Enter a finite measurement between -1e15 and 1e15.")
    return value


def convert(value, from_unit, to_unit, mode=0):
    with localcontext() as context:
        context.prec = 32
        return number(value) * FACTORS[from_unit] / FACTORS[to_unit] * MULTIPLIERS[mode]


def equivalent_input(mm_value, input_unit, mode):
    """Seed the input so opening/reading the tool preserves the current output."""
    return number(mm_value) / FACTORS[input_unit] / MULTIPLIERS[mode]


def display(value):
    value = Decimal(str(value))
    with localcontext() as context:
        context.prec = 48
        rounded = value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    if not rounded:
        return "0"
    return format(rounded, "f").rstrip("0").rstrip(".")


def evaluate(expression, value=None):
    """Decimal arithmetic only: no eval(), function calls or Python access."""
    text = str(expression).strip().replace("×", "*").replace("÷", "/").replace("−", "-")
    if not text or len(text) > 256:
        raise ValueError("Enter a calculation, such as 2400 / 3.")
    try:
        tree = ast.parse(text, mode="eval")
    except (SyntaxError, RecursionError):
        raise ValueError("Complete the calculation, for example (2400 + 100) / 3.") from None
    if len(list(ast.walk(tree))) > 80:
        raise ValueError("This calculation is too long.")

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return number(ast.get_source_segment(text, node))
        if isinstance(node, ast.Name) and node.id == "value" and value is not None:
            return number(value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            result = visit(node.operand)
            return result if isinstance(node.op, ast.UAdd) else -result
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): result = left + right
            elif isinstance(node.op, ast.Sub): result = left - right
            elif isinstance(node.op, ast.Mult): result = left * right
            else:
                if right == 0:
                    raise ValueError("Cannot divide by zero.")
                result = left / right
            return number(result)
        raise ValueError("Use numbers, +, -, ×, ÷, parentheses, or the loaded value.")

    with localcontext() as context:
        context.prec = 32
        return visit(tree.body)
