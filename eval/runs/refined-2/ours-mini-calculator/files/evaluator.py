def tokenize(text):
    tokens, i = [], 0
    while i < len(text):
        if text[i].isspace():
            i += 1
        elif text[i].isdigit() or text[i] == '.':
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            tokens.append(float(text[i:j]))
            i = j
        elif text[i] in '+-*/()':
            tokens.append(text[i])
            i += 1
        else:
            raise ValueError(f"Unknown character: {text[i]!r}")
    return tokens


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
        result = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            result = result + right if op == '+' else result - right
        return result

    def term(self):
        result = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            result = result * right if op == '*' else result / right
        return result

    def factor(self):
        tok = self.peek()
        if tok == '(':
            self.consume()
            result = self.expr()
            if self.peek() != ')':
                raise ValueError("Expected ')'")
            self.consume()
            return result
        elif isinstance(tok, (int, float)):
            self.consume()
            return tok
        else:
            raise ValueError(f"Expected number or '(', got {tok!r}")


def evaluate(text):
    tokens = tokenize(text)
    parser = Parser(tokens)
    result = parser.expr()
    if parser.peek() is not None:
        raise ValueError(f"Unexpected token: {parser.peek()!r}")
    return result


# Valid expressions
print(evaluate('3 + 4 * (2 - 1)'))   # 7.0
print(evaluate('10 / 2 - 3'))         # 2.0
print(evaluate('5 - 3 - 1'))          # 1.0  (left-assoc check)
print(evaluate('(1 + 2) * (3 + 4)'))  # 21.0

# Error cases
import traceback
for bad in ['3 + 4 ) * 2', '3 + * 2', '(1 + 2']:
    try:
        evaluate(bad)
        print(f"ERROR: should have raised for {bad!r}")
    except ValueError as e:
        print(f"OK {bad!r} → {e}")
