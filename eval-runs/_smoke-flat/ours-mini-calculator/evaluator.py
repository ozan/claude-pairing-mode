"""Recursive-descent expression evaluator.

Grammar:
    expr   → term   (('+' | '-') term)*
    term   → unary  (('*' | '/') unary)*
    unary  → '-' unary | factor
    factor → NUMBER | '(' expr ')'
"""

from __future__ import annotations
import re


def tokenize(text: str) -> list[str]:
    """Split expression into a flat list of tokens (numbers, operators, parens)."""
    tokens = re.findall(r'\d+\.?\d*|[+\-*/()]', text)
    return tokens


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0

    # ---------- helpers ----------

    def peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self) -> str:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    # ---------- grammar rules ----------

    def expr(self) -> float:
        """expr → term (('+' | '-') term)*"""
        left = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            left = left + right if op == '+' else left - right
        return left

    def term(self) -> float:
        """term → unary (('*' | '/') unary)*"""
        left = self.unary()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.unary()
            left = left * right if op == '*' else left / right
        return left

    def unary(self) -> float:
        """unary → '-' unary | factor"""
        if self.peek() == '-':
            self.consume()
            return -self.unary()
        return self.factor()

    def factor(self) -> float:
        """factor → NUMBER | '(' expr ')'"""
        tok = self.peek()
        if tok == '(':
            self.consume()       # eat '('
            value = self.expr()
            self.consume()       # eat ')'
            return value
        else:
            return float(self.consume())


def evaluate(expression: str) -> float:
    tokens = tokenize(expression)
    parser = Parser(tokens)
    result = parser.expr()
    if parser.peek() is not None:
        raise SyntaxError(f"Unexpected token: {parser.peek()!r}")
    return result


if __name__ == '__main__':
    tests = [
        ("3 + 4 * (2 - 1)",  7.0),
        ("10 / 2 + 3",        8.0),
        ("(1 + 2) * (3 + 4)", 21.0),
        ("100 - 50 / 5",     90.0),
        ("-3 + 10",           7.0),
        ("--3",               3.0),
        ("2 * -4",           -8.0),
        ("-(3 + 2)",         -5.0),
    ]
    for expr, expected in tests:
        got = evaluate(expr)
        status = "✓" if got == expected else f"✗ (expected {expected})"
        print(f"  {expr!r:30s} = {got}  {status}")
