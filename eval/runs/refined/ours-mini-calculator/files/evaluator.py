import re

TOKEN_RE = re.compile(r'\d+\.?\d*|[+\-*/()]')

def tokenize(text):
    return TOKEN_RE.findall(text)

def evaluate(text):
    tokens = tokenize(text)
    pos = 0

    def factor():
        nonlocal pos
        token = tokens[pos]
        if token == '(':
            pos += 1
            result = expr()
            pos += 1  # skip ')'
            return result
        elif token == '-':
            pos += 1
            return -factor()
        else:
            pos += 1
            return float(token)

    def term():
        nonlocal pos
        result = factor()
        while pos < len(tokens) and tokens[pos] in ('*', '/'):
            op = tokens[pos]
            pos += 1
            if op == '*':
                result *= factor()
            else:
                result /= factor()
        return result

    def expr():
        nonlocal pos
        result = term()
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            if op == '+':
                result += term()
            else:
                result -= term()
        return result

    return expr()
