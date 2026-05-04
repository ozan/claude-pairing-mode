from __future__ import annotations
import re

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

TOKEN_RE = re.compile(r'\s*(\d+(?:\.\d+)?|[+\-*/()])\s*')

def tokenize(text: str) -> list[str]:
    """Split an expression string into a list of token strings."""
    tokens = TOKEN_RE.findall(text)
    # Verify we consumed the whole input (catches unknown chars)
    consumed = ''.join(TOKEN_RE.findall(text))
    full = re.sub(r'\s', '', text)
    if consumed.replace(' ', '') != full:
        raise ValueError(f"Unexpected character in expression: {text!r}")
    return tokens


# ---------------------------------------------------------------------------
# Recursive-descent parser
# ---------------------------------------------------------------------------
# Grammar:
#   expr   → term   ( ('+' | '-') term   )*
#   term   → factor ( ('*' | '/') factor )*
#   factor → ('+' | '-') factor | NUMBER | '(' expr ')'

class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected: str | None = None) -> str:
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if expected is not None and tok != expected:
            raise ValueError(f"Expected {expected!r}, got {tok!r}")
        self.pos += 1
        return tok

    # expr → term ( ('+' | '-') term )*
    def expr(self) -> float:
        result = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            result = result + right if op == '+' else result - right
        return result

    # term → factor ( ('*' | '/') factor )*
    def term(self) -> float:
        result = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            if op == '/' and right == 0:
                raise ZeroDivisionError("Division by zero")
            result = result * right if op == '*' else result / right
        return result

    # factor → ('+' | '-') factor | NUMBER | '(' expr ')'
    def factor(self) -> float:
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if tok in ('+', '-'):
            self.consume()
            value = self.factor()          # right-recursive: binds tightly
            return -value if tok == '-' else value
        if tok == '(':
            self.consume('(')
            result = self.expr()
            self.consume(')')
            return result
        # Must be a number
        self.consume()
        return float(tok)


def evaluate(text: str) -> float:
    tokens = tokenize(text)
    parser = Parser(tokens)
    result = parser.expr()
    if parser.peek() is not None:
        raise ValueError(f"Unexpected token: {parser.peek()!r}")
    return result


# ---------------------------------------------------------------------------
# Quick smoke tests
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    cases = [
        ('3 + 4 * (2 - 1)',   7.0),
        ('10 / 2 + 3',        8.0),
        ('(1 + 2) * (3 + 4)', 21.0),
        ('100 - 4 * 5 / 2',   90.0),
        ('2.5 * 4',           10.0),
        ('-3 * 2',            -6.0),
        ('--3',                3.0),
        ('-(4 + 1)',          -5.0),
        ('-3 + 4',             1.0),   # unary minus, not -(3+4)
    ]
    for expr, expected in cases:
        got = evaluate(expr)
        status = '✓' if got == expected else '✗'
        print(f"{status}  evaluate({expr!r}) = {got}  (expected {expected})")
