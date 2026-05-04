import re


def tokenize(expr: str) -> list:
    """Break expression string into a list of floats and operator/paren strings."""
    raw = re.findall(r'\d+\.?\d*|[+\-*/()]', expr)
    tokens = []
    for tok in raw:
        try:
            tokens.append(float(tok))
        except ValueError:
            tokens.append(tok)
    return tokens


# --- Parser ---
# Grammar (low → high precedence):
#   expr   ::= term   (('+' | '-') term)*
#   term   ::= factor (('*' | '/') factor)*
#   factor ::= NUMBER | '(' expr ')'

def parse_expr(tokens: list, pos: int) -> tuple[float, int]:
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op, pos = tokens[pos], pos + 1
        right, pos = parse_term(tokens, pos)
        left = left + right if op == '+' else left - right
    return left, pos


def parse_term(tokens: list, pos: int) -> tuple[float, int]:
    left, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('*', '/'):
        op, pos = tokens[pos], pos + 1
        right, pos = parse_factor(tokens, pos)
        left = left * right if op == '*' else left / right
    return left, pos


def parse_factor(tokens: list, pos: int) -> tuple[float, int]:
    tok = tokens[pos]
    if isinstance(tok, float):
        return tok, pos + 1
    if tok == '(':
        value, pos = parse_expr(tokens, pos + 1)  # skip '('
        if tokens[pos] != ')':
            raise ValueError(f"Expected ')' at position {pos}")
        return value, pos + 1  # skip ')'
    raise ValueError(f"Unexpected token {tok!r} at position {pos}")


def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    value, pos = parse_expr(tokens, 0)
    if pos != len(tokens):
        raise ValueError(f"Unexpected token {tokens[pos]!r} after expression")
    return value
