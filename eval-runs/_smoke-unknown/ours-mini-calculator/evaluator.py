def tokenize(s):
    tokens, i = [], 0
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i].isdigit() or s[i] == '.':
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(s[i:j])
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

    def parse_expr(self):
        """Handles + and - (lowest precedence)."""
        left = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            left = left + right if op == '+' else left - right
        return left

    def parse_term(self):
        """Handles * and / (higher precedence)."""
        left = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_factor()
            left = left * right if op == '*' else left / right
        return left

    def parse_factor(self):
        """Handles numbers and parenthesised sub-expressions."""
        tok = self.peek()
        if tok == '(':
            self.consume()          # eat '('
            val = self.parse_expr() # recurse from the top
            self.consume()          # eat ')'
            return val
        else:
            return float(self.consume())


def evaluate(s):
    tokens = tokenize(s)
    parser = Parser(tokens)
    result = parser.parse_expr()
    # Return int if the result is a whole number, for cleaner output
    return int(result) if result == int(result) else result


if __name__ == '__main__':
    tests = [
        ('3 + 4 * (2 - 1)', 7),
        ('10 / 2 + 3',       8),
        ('(1 + 2) * (3 + 4)', 21),
        ('2 * 3 + 4 * 5',    26),
        ('100',              100),
    ]
    for expr, expected in tests:
        got = evaluate(expr)
        status = '✓' if got == expected else '✗'
        print(f"{status}  {expr!r:30s} → {got}  (expected {expected})")
