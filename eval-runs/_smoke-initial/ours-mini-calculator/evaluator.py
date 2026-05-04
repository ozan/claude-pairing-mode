import re


def tokenize(text):
    return re.findall(r'\d+\.?\d*|[+\-*/()]', text)


def parse(text):
    tokens = tokenize(text)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def expr():
        """Handles + and - (lowest precedence)."""
        left = term()
        while peek() in ('+', '-'):
            op = consume()
            right = term()
            left = left + right if op == '+' else left - right
        return left

    def term():
        """Handles * and / (higher precedence)."""
        left = factor()
        while peek() in ('*', '/'):
            op = consume()
            right = factor()
            left = left * right if op == '*' else left / right
        return left

    def factor():
        """Handles numbers and parenthesized sub-expressions."""
        tok = consume()
        if tok == '(':
            val = expr()
            consume()  # ')'
            return val
        return float(tok)

    return expr()


if __name__ == '__main__':
    cases = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('10 / 2 + 3',       8.0),
        ('(1 + 2) * (3 + 4)', 21.0),
        ('2 * (3 + (4 - 1))', 12.0),
    ]
    for expr_str, expected in cases:
        result = parse(expr_str)
        status = '✓' if result == expected else '✗'
        print(f'{status}  {expr_str} = {result}  (expected {expected})')
