def tokenize(text):
    tokens, i = [], 0
    while i < len(text):
        if text[i].isspace():
            i += 1
        elif text[i].isdigit():
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            s = text[i:j]
            tokens.append(float(s) if '.' in s else int(s))
            i = j
        else:
            tokens.append(text[i])
            i += 1
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        if self.pos >= len(self.tokens):
            raise ValueError("Unexpected end of expression")
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expr(self):
        left = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            left = left + right if op == '+' else left - right
        return left

    def term(self):
        left = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            left = left * right if op == '*' else left / right
        return left

    def factor(self):
        tok = self.consume()
        if isinstance(tok, (int, float)):
            return tok
        if tok == '(':
            val = self.expr()
            self.consume()  # closing ')'
            return val
        raise ValueError(f"Unexpected token: {tok!r}")


def evaluate(text):
    parser = Parser(tokenize(text))
    result = parser.expr()
    if parser.peek() is not None:
        raise ValueError(f"Unexpected token: {parser.peek()!r}")
    return result
