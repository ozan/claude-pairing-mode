import re


def tokenize(s: str) -> list:
    """
    Convert an expression string into a flat list of tokens.
    Numbers become floats; operators and parens stay as strings.
    """
    raw = re.findall(r'\d+\.?\d*|[+\-*/()]', s)
    return [float(t) if re.fullmatch(r'\d+\.?\d*', t) else t for t in raw]


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expr(self) -> float:
        """expr → term (('+' | '-') term)*"""
        result = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            result = result + right if op == '+' else result - right
        return result

    def term(self) -> float:
        """term → factor (('*' | '/') factor)*"""
        result = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            result = result * right if op == '*' else result / right
        return result

    def factor(self) -> float:
        """factor → NUMBER | '(' expr ')'"""
        tok = self.consume()
        if isinstance(tok, float):
            return tok
        if tok == '(':
            result = self.expr()
            closing = self.consume()
            if closing != ')':
                raise ValueError(f"Expected ')' but got {closing!r}")
            return result
        raise ValueError(f"Unexpected token: {tok!r}")


def evaluate(s: str) -> float:
    """Parse and evaluate an arithmetic expression string."""
    return Parser(tokenize(s)).expr()


# --- quick sanity checks ---
if __name__ == '__main__':
    cases = [
        ('3 + 4',          [3.0, '+', 4.0]),
        ('3+4*(2-1)',       [3.0, '+', 4.0, '*', '(', 2.0, '-', 1.0, ')']),
        ('10 / 2.5',       [10.0, '/', 2.5]),
        ('(1+2) * (3-4)',   ['(', 1.0, '+', 2.0, ')', '*', '(', 3.0, '-', 4.0, ')']),
    ]
    for expr, expected in cases:
        result = tokenize(expr)
        status = '✓' if result == expected else '✗'
        print(f'{status}  tokenize({expr!r})')
        if result != expected:
            print(f'   expected: {expected}')
            print(f'   got:      {result}')

    print()
    eval_cases = [
        ('3 + 4',              7.0),
        ('3 + 4 * 2',          11.0),   # precedence: * before +
        ('(3 + 4) * 2',        14.0),   # parens override precedence
        ('3 + 4 * (2 - 1)',    7.0),    # original example
        ('1 - 2 - 3',         -4.0),    # left-associativity
        ('10 / 2 / 5',         1.0),    # left-associativity for /
        ('(1 + 2) * (3 - 4)', -3.0),
        ('100',               100.0),   # single number
        ('2.5 * 4',            10.0),   # floats
    ]
    for expr, expected in eval_cases:
        result = evaluate(expr)
        status = '✓' if result == expected else '✗'
        print(f'{status}  evaluate({expr!r}) = {result}')
        if result != expected:
            print(f'   expected: {expected}')
