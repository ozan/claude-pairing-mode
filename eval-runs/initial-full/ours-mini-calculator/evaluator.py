"""
Recursive-descent expression evaluator.

Grammar (lowest → highest precedence):
    expr   ::= term   (('+' | '-') term)*
    term   ::= factor (('*' | '/') factor)*
    factor ::= NUMBER | '(' expr ')'
"""
from __future__ import annotations
from typing import NamedTuple


class Token(NamedTuple):
    value: str
    pos: int   # character offset in the original expression string


class ParseError(ValueError):
    def __init__(self, message: str, expr: str, pos: int):
        # Build a caret line pointing at the bad position, e.g.:
        #   3 + 4 *
        #           ^ expected a number or '('
        caret = ' ' * pos + '^'
        super().__init__(f"{message}\n  {expr}\n  {caret}")


class Parser:
    def __init__(self, text: str):
        self.text = text
        self.tokens: list[Token] = tokenize(text)
        self.pos = 0

    # --- token helpers ---

    def peek(self) -> Token | None:
        """Return the current token without consuming it, or None at end."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self) -> Token:
        """Return and advance past the current token."""
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, value: str) -> Token:
        """Consume and assert the next token's value equals *value*."""
        tok = self.peek()
        if tok is None:
            raise ParseError(
                f"Expected {value!r} but reached end of expression",
                self.text, len(self.text),
            )
        if tok.value != value:
            raise ParseError(
                f"Expected {value!r}, got {tok.value!r}",
                self.text, tok.pos,
            )
        return self.consume()

    # --- grammar rules ---

    def parse_expr(self) -> float:
        """expr ::= term (('+' | '-') term)*"""
        result = self.parse_term()
        while (tok := self.peek()) and tok.value in ('+', '-'):
            op = self.consume().value
            right = self.parse_term()
            result = result + right if op == '+' else result - right
        return result

    def parse_term(self) -> float:
        """term ::= factor (('*' | '/') factor)*"""
        result = self.parse_factor()
        while (tok := self.peek()) and tok.value in ('*', '/'):
            op = self.consume().value
            right = self.parse_factor()
            result = result * right if op == '*' else result / right
        return result

    def parse_factor(self) -> float:
        """factor ::= NUMBER | '(' expr ')'"""
        tok = self.peek()
        if tok is None:
            raise ParseError(
                "Expected a number or '(' but reached end of expression",
                self.text, len(self.text),
            )
        if tok.value == '(':
            self.consume()
            result = self.parse_expr()
            self.expect(')')
            return result
        try:
            self.consume()
            return float(tok.value)
        except ValueError:
            raise ParseError(
                f"Expected a number or '(', got {tok.value!r}",
                self.text, tok.pos,
            )


def tokenize(text: str) -> list[Token]:
    """Split expression into Token objects, each carrying its source position."""
    tokens: list[Token] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch in '+-*/()':
            tokens.append(Token(ch, i))
            i += 1
        elif ch.isdigit() or ch == '.':
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            tokens.append(Token(text[i:j], i))
            i = j
        else:
            raise ParseError(f"Unexpected character: {ch!r}", text, i)
    return tokens


def evaluate(expression: str) -> float:
    """Parse and evaluate an arithmetic expression string."""
    parser = Parser(expression)
    result = parser.parse_expr()
    if (leftover := parser.peek()) is not None:
        raise ParseError(
            f"Unexpected token {leftover.value!r}",
            expression, leftover.pos,
        )
    return result


if __name__ == '__main__':
    good = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('10 / 2 + 3',       8.0),
        ('(1 + 2) * (3 + 4)', 21.0),
        ('2 * 3 + 4 * 5',    26.0),
        ('100 - 50 / 5',     90.0),
    ]
    for expr, expected in good:
        got = evaluate(expr)
        status = '✓' if got == expected else '✗'
        print(f"{status}  {expr!r:30s} => {got} (expected {expected})")

    print()
    bad = [
        '3 + 4 *',        # trailing operator — no RHS
        '(1 + 2',         # unclosed paren
        '1 + * 2',        # operator where value expected
    ]
    for expr in bad:
        try:
            evaluate(expr)
            print(f"✗  {expr!r} — should have raised")
        except ParseError as e:
            print(f"✓  caught error for {expr!r}:\n{e}")
