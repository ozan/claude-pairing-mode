def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
        elif text[i].isdigit() or (text[i] == '.' and i + 1 < len(text) and text[i+1].isdigit()):
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            tokens.append(float(text[i:j]))
            i = j
        elif text[i] in '+-*/()':
            if text[i] == '*' and i + 1 < len(text) and text[i + 1] == '*':
                tokens.append('**')
                i += 2
            else:
                tokens.append(text[i])
                i += 1
        else:
            raise ValueError(f"Unexpected character: {text[i]!r}")
    return tokens


def evaluate(text):
    tokens = tokenize(text)
    pos = [0]  # mutable so inner functions can advance it

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def consume():
        tok = tokens[pos[0]]
        pos[0] += 1
        return tok

    def parse_expr():
        left = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_term()
            left = left + right if op == '+' else left - right
        return left

    def parse_term():
        left = parse_power()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_power()
            left = left * right if op == '*' else left / right
        return left

    def parse_power():
        left = parse_factor()
        if peek() == '**':
            consume()
            return left ** parse_power()
        return left

    def parse_factor():
        tok = consume()
        if isinstance(tok, float):
            return tok
        if tok == '(':
            val = parse_expr()
            closing = consume()
            if closing != ')':
                raise ValueError(f"Expected ')' but got {closing!r}")
            return val
        if tok == '-':
            return -parse_factor()
        raise ValueError(f"Unexpected token: {tok!r}")

    result = parse_expr()
    if peek() is not None:
        raise ValueError(f"Unexpected token: {peek()!r}")
    return result


if __name__ == "__main__":
    tests = [
        ("3 + 4", 7),
        ("3 + 4 * 2", 11),
        ("(3 + 4) * 2", 14),
        ("3 + 4 * (2 - 1)", 7),
        ("10 / 2 + 3", 8),
        ("-3 + 1", -2),
        ("--3", 3),
        ("5 * -2", -10),
        ("2 ** 3", 8),
        ("2 ** 3 ** 2", 512),   # right-associative: 2**(3**2)
        ("(2 ** 3) ** 2", 64),  # explicit left grouping
        ("2 ** -1", 0.5),
    ]
    for expr, expected in tests:
        got = evaluate(expr)
        status = "✓" if got == expected else f"✗ expected {expected}"
        print(f"{expr!r:30s} = {got}  {status}")
