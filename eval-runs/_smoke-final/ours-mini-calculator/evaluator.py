def tokenize(s):
    """Convert an expression string into a list of floats and operator strings."""
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        if s[i].isdigit() or s[i] == '.':
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(float(s[i:j]))
            i = j
        elif s[i] in '+-*/()':
            tokens.append(s[i])
            i += 1
        else:
            raise ValueError(f"Unexpected character: {s[i]!r}")
    return tokens


def evaluate(s):
    return Parser(tokenize(s)).parse()


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """Return the current token without consuming it, or None if exhausted."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        """Return the current token and advance position."""
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def term(self):
        """term → factor (('*' | '/') factor)*"""
        left = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            if op == '*':
                left *= right
            else:
                left /= right
        return left

    def factor(self):
        """factor → NUMBER | '(' expr ')'"""
        tok = self.peek()
        if isinstance(tok, float):
            self.consume()
            return tok
        elif tok == '(':
            self.consume()
            val = self.expr()
            if self.consume() != ')':
                raise ValueError("Expected ')'")
            return val
        else:
            raise ValueError(f"Unexpected token: {tok!r}")

    def parse(self):
        result = self.expr()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token: {self.peek()!r}")
        return result

    def expr(self):
        """expr → term (('+' | '-') term)*"""
        left = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            if op == '+':
                left += right
            else:
                left -= right
        return left
