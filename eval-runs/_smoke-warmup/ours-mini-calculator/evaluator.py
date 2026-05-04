"""
Expression evaluator: +, -, *, /, parentheses, operator precedence.
Uses a recursive-descent parser over a token stream.

Grammar:
    expr   → term   ( ('+' | '-') term   )*
    term   → factor ( ('*' | '/') factor )*
    factor → NUMBER | '(' expr ')'
"""

import re


# ---------------------------------------------------------------------------
# Tokeniser
# ---------------------------------------------------------------------------

def tokenise(text: str) -> list[str]:
    """Return a flat list of tokens (numbers and single-char operators)."""
    tokens = re.findall(r'\d+\.?\d*|[+\-*/()]', text)
    return tokens


# ---------------------------------------------------------------------------
# Parser  (holds mutable position state in a list so subfunctions can share it)
# ---------------------------------------------------------------------------

def parse(tokens: list[str]) -> float:
    pos = [0]  # mutable cursor shared across recursive calls

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def consume():
        tok = tokens[pos[0]]
        pos[0] += 1
        return tok

    def expr() -> float:
        result = term()
        while peek() in ('+', '-'):
            op = consume()
            right = term()
            result = result + right if op == '+' else result - right
        return result

    def term() -> float:
        result = factor()
        while peek() in ('*', '/'):
            op = consume()
            right = factor()
            if op == '/':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result /= right
            else:
                result *= right
        return result

    def factor() -> float:
        tok = peek()
        if tok is None:
            raise SyntaxError("unexpected end of expression")
        if tok == '(':
            consume()          # eat '('
            result = expr()
            if consume() != ')':
                raise SyntaxError("expected ')'")
            return result
        # must be a number
        consume()
        return float(tok)

    result = expr()
    if peek() is not None:
        raise SyntaxError(f"unexpected token: {peek()!r}")
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def evaluate(expression: str) -> float:
    tokens = tokenise(expression)
    return parse(tokens)


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    cases = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('10 / 2 + 3',       8.0),
        ('(1 + 2) * (3 + 4)', 21.0),
        ('100 - 50 / 5',     90.0),
    ]
    for expr_str, expected in cases:
        got = evaluate(expr_str)
        status = '✓' if got == expected else f'✗ (expected {expected})'
        print(f"  {expr_str!r:30s} = {got}  {status}")
