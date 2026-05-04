def tokenize(s):
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i].isdigit() or s[i] == '.':
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(float(s[i:j]) if '.' in s[i:j] else int(s[i:j]))
            i = j
        elif s[i] in '+-*/()':
            tokens.append(s[i])
            i += 1
        else:
            raise ValueError(f"Unexpected character: {s[i]!r}")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        token = self.tokens[self.pos]
        if expected is not None and token != expected:
            raise ValueError(f"Expected {expected!r}, got {token!r}")
        self.pos += 1
        return token

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            left = left + self.parse_term() if op == '+' else left - self.parse_term()
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_factor()
            left = left * right if op == '*' else left / right
        return left

    def parse_factor(self):
        if self.peek() == '(':
            self.consume('(')
            val = self.parse_expr()
            self.consume(')')
            return val
        return self.consume()   # must be a number


def evaluate(s):
    tokens = tokenize(s)
    parser = Parser(tokens)
    return parser.parse_expr()
