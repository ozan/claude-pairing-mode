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
            tokens.append(float(s[i:j]))
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

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    # expr → term (('+' | '-') term)*
    def expr(self):
        left = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            left = left + right if op == '+' else left - right
        return left

    # term → factor (('*' | '/') factor)*
    def term(self):
        left = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            left = left * right if op == '*' else left / right
        return left

    # factor → NUMBER | '(' expr ')'
    def factor(self):
        tok = self.peek()
        if isinstance(tok, float):
            return self.consume()
        if tok == '(':
            self.consume()          # eat '('
            val = self.expr()
            if self.consume() != ')':
                raise ValueError("Expected ')'")
            return val
        raise ValueError(f"Unexpected token: {tok!r}")


def evaluate(s):
    tokens = tokenize(s)
    return Parser(tokens).expr()


if __name__ == '__main__':
    tests = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('8 - 3 - 2',        3.0),
        ('10 / 2 / 5',       1.0),
        ('(1 + 2) * (3 + 4)', 21.0),
        ('2 * (3 + (4 - 1))', 12.0),
    ]
    for expr_str, expected in tests:
        result = evaluate(expr_str)
        status = '✓' if result == expected else '✗'
        print(f"{status}  {expr_str!r:30s} = {result}  (expected {expected})")
