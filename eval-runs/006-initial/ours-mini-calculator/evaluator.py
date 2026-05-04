def tokenize(expr):
    tokens, i = [], 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        elif expr[i].isdigit() or expr[i] == '.':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(float(expr[i:j]))
            i = j
        elif expr[i] in '+-*/()':
            tokens.append(expr[i])
            i += 1
        else:
            raise ValueError(f"Unexpected character: {expr[i]}")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.tokens[self.pos]; self.pos += 1; return tok

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            left = left + right if op == '+' else left - right
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_factor()
            left = left * right if op == '*' else left / right
        return left

    def parse_factor(self):
        tok = self.consume()
        if isinstance(tok, float):
            return tok
        if tok == '(':
            val = self.parse_expr()
            self.consume()  # ')'
            return val
        raise ValueError(f"Unexpected token: {tok}")


def evaluate(expr):
    tokens = tokenize(expr)
    parser = Parser(tokens)
    result = parser.parse_expr()
    if parser.peek() is not None:
        raise ValueError(f"Unexpected token: {parser.peek()}")
    return result
