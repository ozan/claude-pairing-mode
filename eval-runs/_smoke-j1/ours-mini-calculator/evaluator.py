import re


def tokenize(expr: str) -> list:
    """Convert an expression string into a flat list of tokens.

    Numbers become floats; operators and parentheses stay as strings.
    Whitespace is ignored automatically (findall skips unmatched gaps).
    """
    token_re = re.compile(r'\d+(?:\.\d+)?|[+\-*/()]')
    result = []
    for raw in token_re.findall(expr):
        try:
            result.append(float(raw))
        except ValueError:
            result.append(raw)
    return result


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """Return current token without consuming it, or None if exhausted."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        """Return current token and advance position."""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    # expr → term (('+' | '-') term)*
    def parse_expr(self):
        left = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            left = left + right if op == '+' else left - right
        return left

    # term → factor (('*' | '/') factor)*
    def parse_term(self):
        left = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_factor()
            left = left * right if op == '*' else left / right
        return left

    # factor → NUMBER | '(' expr ')' | '-' factor
    def parse_factor(self):
        token = self.peek()
        if token == '(':
            self.consume()          # drop '('
            value = self.parse_expr()
            self.consume()          # drop ')'
            return value
        if token == '-':
            self.consume()
            return -self.parse_factor()   # unary minus; recursive handles '--x'
        if isinstance(token, float):
            return self.consume()
        raise SyntaxError(f"Unexpected token: {token!r}")


def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    parser = Parser(tokens)
    result = parser.parse_expr()
    if parser.peek() is not None:
        raise SyntaxError(f"Unexpected token: {parser.peek()!r}")
    return result
