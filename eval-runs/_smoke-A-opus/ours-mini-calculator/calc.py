def tokenize(s):
    tokens = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c in '+-*/()':
            tokens.append(c)
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            num_str = s[i:j]
            tokens.append(float(num_str) if '.' in num_str else int(num_str))
            i = j
        else:
            raise ValueError(f"Unexpected character: {c}")
    return tokens


def evaluate(s):
    return Parser(tokenize(s)).expr()


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

    def expr(self):
        value = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            if op == '+':
                value = value + right
            else:
                value = value - right
        return value

    def term(self):
        value = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            if op == '*':
                value = value * right
            else:
                value = value / right
        return value

    def factor(self):
        tok = self.consume()
        if tok == '(':
            value = self.expr()
            self.consume()  # discard ')'
            return value
        return tok  # a number


if __name__ == '__main__':
    cases = [
        ([3, '+', 4, '*', '(', 2, '-', 1, ')'], 7),
        ([1, '-', 2, '-', 3], -4),                    # left-assoc
        ([8, '/', 4, '/', 2], 1.0),                   # left-assoc, division
        (['(', '(', 1, '+', 2, ')', '*', 3, ')'], 9), # nested parens
        ([2, '+', 3, '*', 4, '-', 5], 9),             # mixed precedence
    ]
    for toks, expected in cases:
        got = Parser(toks).expr()
        print(f'{toks} -> {got} (expected {expected})')
        assert got == expected

    string_cases = [
        ('3 + 4 * (2 - 1)', 7),
        ('1 - 2 - 3', -4),
        ('(1 + 2) * (3 + 4)', 21),
        ('10 / 4', 2.5),
        ('2.5 * 4', 10.0),
    ]
    for s, expected in string_cases:
        got = evaluate(s)
        print(f'{s!r} -> {got} (expected {expected})')
        assert got == expected
