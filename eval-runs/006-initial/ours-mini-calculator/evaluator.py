import re

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

def tokenize(s: str) -> list:
    """Split expression string into a flat list of ints/floats and operator chars."""
    raw = re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', s)
    return [float(t) if re.fullmatch(r'\d+(?:\.\d+)?', t) else t for t in raw]


# ---------------------------------------------------------------------------
# Recursive-descent parser
# Grammar:
#   expr   → term   (('+' | '-') term)*
#   term   → factor (('*' | '/') factor)*
#   factor → NUMBER | '(' expr ')'
# ---------------------------------------------------------------------------

def expr(tokens: list, pos: int) -> tuple[float, int]:
    left, pos = term(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op, pos = tokens[pos], pos + 1
        right, pos = term(tokens, pos)
        left = left + right if op == '+' else left - right
    return left, pos


def term(tokens: list, pos: int) -> tuple[float, int]:
    left, pos = factor(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('*', '/'):
        op, pos = tokens[pos], pos + 1
        right, pos = factor(tokens, pos)
        left = left * right if op == '*' else left / right
    return left, pos


def factor(tokens: list, pos: int) -> tuple[float, int]:
    if isinstance(tokens[pos], str) and tokens[pos] in ('+', '-'):
        op, pos = tokens[pos], pos + 1
        val, pos = factor(tokens, pos)
        return (-val if op == '-' else val), pos
    if isinstance(tokens[pos], float):
        return tokens[pos], pos + 1
    if tokens[pos] == '(':
        val, pos = expr(tokens, pos + 1)
        if tokens[pos] != ')':
            raise ValueError("Expected ')'")
        return val, pos + 1
    raise ValueError(f"Unexpected token: {tokens[pos]!r}")


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def evaluate(s: str) -> float:
    tokens = tokenize(s)
    result, pos = expr(tokens, 0)
    if pos != len(tokens):
        raise ValueError(f"Unexpected token at position {pos}: {tokens[pos]!r}")
    return result


if __name__ == '__main__':
    tests = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('10 - 5 - 2',       3.0),   # left-assoc
        ('8 / 4 / 2',        1.0),   # left-assoc
        ('2 * (3 + 4)',      14.0),
        ('-3 + 4',           1.0),   # unary: binds tight
        ('-(3 + 4)',        -7.0),   # unary over parens
        ('--3',              3.0),   # double negation
        ('-3 * -2',          6.0),   # unary on both sides
    ]
    for expr_str, expected in tests:
        got = evaluate(expr_str)
        status = '✓' if got == expected else '✗'
        print(f'{status}  {expr_str!r:30s}  →  {got}  (expected {expected})')
