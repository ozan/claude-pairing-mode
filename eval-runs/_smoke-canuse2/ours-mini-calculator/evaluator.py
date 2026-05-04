def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
        elif text[i].isdigit():
            j = i
            while j < len(text) and text[j].isdigit():
                j += 1
            tokens.append(int(text[i:j]))
            i = j
        elif text[i] in '+-*/()':
            tokens.append(text[i])
            i += 1
        else:
            raise ValueError(f"Unexpected character: {text[i]!r}")
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

    def expr(self):
        # expr → term (('+' | '-') term)*
        result = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            result = result + self.term() if op == '+' else result - self.term()
        return result

    def term(self):
        # term → factor (('*' | '/') factor)*
        result = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            result = result * self.factor() if op == '*' else result / self.factor()
        return result

    def factor(self):
        # factor → NUMBER | '(' expr ')'
        tok = self.peek()
        if tok == '(':
            self.consume()          # '('
            result = self.expr()
            self.consume()          # ')'
            return result
        elif isinstance(tok, int):
            return self.consume()
        else:
            raise ValueError(f"Unexpected token: {tok!r}")


def evaluate(text):
    tokens = tokenize(text)
    return Parser(tokens).expr()
