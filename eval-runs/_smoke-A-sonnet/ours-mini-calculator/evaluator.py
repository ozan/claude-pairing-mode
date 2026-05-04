import re


def tokenize(text):
    return re.findall(r'\d+\.?\d*|[+\-*/()]', text)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        result = self.expr()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token: {self.peek()!r}")
        return result

    def expr(self):
        """Handles + and - (lowest precedence)."""
        left = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            left = left + right if op == '+' else left - right
        return left

    def term(self):
        """Handles * and / (higher precedence)."""
        left = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            left = left * right if op == '*' else left / right
        return left

    def factor(self):
        """Handles numbers and parenthesised sub-expressions (highest precedence)."""
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if tok == '(':
            self.consume()          # drop '('
            result = self.expr()    # recurse for the sub-expression
            if self.consume() != ')':
                raise ValueError("Expected ')'")
            return result
        # must be a number
        self.consume()
        try:
            return int(tok) if '.' not in tok else float(tok)
        except ValueError:
            raise ValueError(f"Unexpected token: {tok!r}")


def evaluate(text):
    tokens = tokenize(text)
    return Parser(tokens).parse()


if __name__ == "__main__":
    tests = [
        ("3 + 4 * (2 - 1)", 7),
        ("5 - 3 - 2",        0),
        ("10 / 2 / 5",       1.0),
        ("2 * (3 + 4)",      14),
        ("(1 + 2) * (3 + 4)", 21),
    ]
    for expr, expected in tests:
        result = evaluate(expr)
        status = "✓" if result == expected else "✗"
        print(f"{status}  {expr!r:30s} = {result}  (expected {expected})")
