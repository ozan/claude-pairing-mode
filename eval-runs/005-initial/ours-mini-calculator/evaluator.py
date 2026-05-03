import re

def tokenize(expr: str) -> list[str]:
    return re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', expr)

def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume() -> str:
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def parse_expr() -> float:   # lowest precedence: + -
        left = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_term()
            left = left + right if op == '+' else left - right
        return left

    def parse_term() -> float:   # higher precedence: * /
        left = parse_factor()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_factor()
            left = left * right if op == '*' else left / right
        return left

    def parse_factor() -> float: # highest: numbers and ()
        tok = peek()
        if tok in ('+', '-'):
            consume()
            return parse_factor() if tok == '+' else -parse_factor()
        if tok == '(':
            consume()
            val = parse_expr()
            consume()  # ')'
            return val
        return float(consume())

    return float(parse_expr())


if __name__ == '__main__':
    cases = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('10 / 2 + 3',       8.0),
        ('(1 + 2) * (3 + 4)', 21.0),
    ]
    for expr, expected in cases:
        result = evaluate(expr)
        status = '✓' if result == expected else f'✗ expected {expected}'
        print(f'{expr!r:30s} = {result}  {status}')
