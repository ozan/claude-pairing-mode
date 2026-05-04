"""
Expression evaluator — no eval().

Grammar (lowest → highest precedence):
  expr   → term   (('+' | '-') term)*
  term   → factor (('*' | '/') factor)*
  factor → NUMBER | '(' expr ')'
"""

import re
from typing import Optional


def tokenize(text: str) -> list[str]:
    """Split input into number and operator tokens, ignoring whitespace."""
    token_re = re.compile(r'\d+\.?\d*|[+\-*/()]')
    tokens = token_re.findall(text)
    if not tokens:
        raise ValueError(f"No valid tokens found in: {text!r}")
    return tokens


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0

    # ── helpers ──────────────────────────────────────────────────────────────

    def peek(self) -> Optional[str]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected: Optional[str] = None) -> str:
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if expected is not None and tok != expected:
            raise ValueError(f"Expected {expected!r}, got {tok!r}")
        self.pos += 1
        return tok

    # ── grammar rules ────────────────────────────────────────────────────────

    def expr(self) -> float:
        """expr → term (('+' | '-') term)*"""
        value = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            value = value + right if op == '+' else value - right
        return value

    def term(self) -> float:
        """term → factor (('*' | '/') factor)*"""
        value = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            if op == '/' and right == 0:
                raise ZeroDivisionError("Division by zero")
            value = value * right if op == '*' else value / right
        return value

    def factor(self) -> float:
        """factor → NUMBER | '(' expr ')'"""
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if tok == '(':
            self.consume('(')
            value = self.expr()
            self.consume(')')
            return value
        # Must be a number
        self.consume()
        return float(tok)


def evaluate(expression: str) -> float:
    tokens = tokenize(expression)
    parser = Parser(tokens)
    result = parser.expr()
    if parser.peek() is not None:
        raise ValueError(f"Unexpected token: {parser.peek()!r}")
    # Return int if result is a whole number
    return int(result) if result == int(result) else result


# ── quick smoke tests ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    cases = [
        ('3 + 4 * (2 - 1)', 7),
        ('(1 + 2) * (3 + 4)', 21),
        ('10 / 2 + 3', 8),
        ('100 - 50 * 2', 0),
        ('2 * (3 + (4 - 1))', 12),
    ]
    for expr, expected in cases:
        result = evaluate(expr)
        status = '✓' if result == expected else '✗'
        print(f"{status}  {expr!r:35s} = {result}  (expected {expected})")
