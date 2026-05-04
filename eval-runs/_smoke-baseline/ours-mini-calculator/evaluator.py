"""
Arithmetic expression evaluator — no eval().

Supports: integers, decimals, scientific notation, +  -  *  /,
          parentheses, and unary + / -.

Grammar (EBNF):
    expr   := term   ( ('+' | '-') term   )*
    term   := factor ( ('*' | '/') factor )*
    factor := ['+' | '-'] ( NUMBER | '(' expr ')' )

Operator precedence (low → high):
  1. +  -    addition / subtraction     (left-associative)
  2. *  /    multiplication / division  (left-associative)
  3. unary + / -                        (right-associative)
  4. number literal or parenthesised expression
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto


# ── Token types ────────────────────────────────────────────────────────────────

class TT(Enum):
    NUMBER  = auto()
    PLUS    = auto()
    MINUS   = auto()
    STAR    = auto()
    SLASH   = auto()
    LPAREN  = auto()
    RPAREN  = auto()
    EOF     = auto()


_SYMBOL: dict[str, TT] = {
    '+': TT.PLUS,  '-': TT.MINUS,
    '*': TT.STAR,  '/': TT.SLASH,
    '(': TT.LPAREN, ')': TT.RPAREN,
}


@dataclass
class Token:
    type:  TT
    value: float | None = None

    def __repr__(self) -> str:
        return f"Token({self.type.name}" + (f", {self.value}" if self.value is not None else "") + ")"


# ── Lexer ───────────────────────────────────────────────────────────────────────

# Matches either:
#   group 1 — a number: integer, decimal, or scientific notation
#   group 2 — a single operator or parenthesis
_TOKEN_RE = re.compile(
    r"\s*"
    r"(?:"
    r"(\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)"  # group 1: number
    r"|([+\-*/()])"                        # group 2: operator / paren
    r")\s*"
)


def tokenize(text: str) -> list[Token]:
    """Convert *text* into a flat list of Tokens, terminated by EOF."""
    tokens: list[Token] = []
    pos = 0
    while pos < len(text):
        m = _TOKEN_RE.match(text, pos)
        if not m:
            raise SyntaxError(
                f"Unexpected character {text[pos]!r} at position {pos}"
            )
        pos = m.end()
        num, sym = m.group(1), m.group(2)
        if num:
            tokens.append(Token(TT.NUMBER, float(num)))
        else:
            tokens.append(Token(_SYMBOL[sym]))
    tokens.append(Token(TT.EOF))
    return tokens


# ── Parser ──────────────────────────────────────────────────────────────────────

class _Parser:
    """Recursive-descent parser; every grammar method returns a float."""

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos    = 0

    # ── internal helpers ───────────────────────────────────────────────────────

    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _consume(self, *expected: TT) -> Token:
        tok = self._peek()
        if expected and tok.type not in expected:
            names = " or ".join(t.name for t in expected)
            raise SyntaxError(f"Expected {names}, got {tok.type.name}")
        self._pos += 1
        return tok

    # ── grammar rules ──────────────────────────────────────────────────────────

    def parse(self) -> float:
        result = self._expr()
        self._consume(TT.EOF)   # nothing should remain
        return result

    def _expr(self) -> float:
        """expr := term ( ('+' | '-') term )*"""
        value = self._term()
        while (tt := self._peek().type) in (TT.PLUS, TT.MINUS):
            self._consume()
            right = self._term()
            value = value + right if tt == TT.PLUS else value - right
        return value

    def _term(self) -> float:
        """term := factor ( ('*' | '/') factor )*"""
        value = self._factor()
        while (tt := self._peek().type) in (TT.STAR, TT.SLASH):
            self._consume()
            right = self._factor()
            if tt == TT.SLASH:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                value /= right
            else:
                value *= right
        return value

    def _factor(self) -> float:
        """factor := ['+' | '-'] ( NUMBER | '(' expr ')' )"""
        tok = self._peek()

        if tok.type == TT.PLUS:      # unary +
            self._consume()
            return +self._factor()

        if tok.type == TT.MINUS:     # unary -
            self._consume()
            return -self._factor()

        if tok.type == TT.LPAREN:    # parenthesised sub-expression
            self._consume()
            value = self._expr()
            self._consume(TT.RPAREN)
            return value

        tok = self._consume(TT.NUMBER)  # plain number literal
        return tok.value  # type: ignore[return-value]


# ── Public API ──────────────────────────────────────────────────────────────────

def evaluate(expression: str) -> float:
    """
    Parse and evaluate an arithmetic *expression* string without using eval().

    Args:
        expression: Arithmetic expression, e.g. ``'3 + 4 * (2 - 1)'``.

    Returns:
        Numeric result as a ``float``.

    Raises:
        SyntaxError:       The expression is malformed.
        ZeroDivisionError: A division by zero was attempted.

    Examples::

        >>> evaluate('3 + 4 * (2 - 1)')
        7.0
        >>> evaluate('10 / (2 + 3)')
        2.0
        >>> evaluate('-3 * -2')
        6.0
        >>> evaluate('1e2 + 0.5e1')
        105.0
    """
    return _Parser(tokenize(expression)).parse()


# ── CLI ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    expr = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("expr> ")
    print(evaluate(expr))
