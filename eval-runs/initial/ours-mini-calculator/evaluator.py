import re

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------
# Token types
NUMBER, PLUS, MINUS, STAR, SLASH, LPAREN, RPAREN, EOF = (
    'NUMBER', '+', '-', '*', '/', '(', ')', 'EOF'
)

def tokenize(text):
    """Return a flat list of (type, value) pairs."""
    token_re = re.compile(r'\s*(\d+\.?\d*|[+\-*/()])\s*')
    tokens = []
    pos = 0
    while pos < len(text):
        m = token_re.match(text, pos)
        if not m:
            raise ValueError(f"Unexpected character at position {pos}: {text[pos]!r}")
        tok = m.group(1)
        if tok.replace('.', '', 1).isdigit():
            tokens.append((NUMBER, float(tok) if '.' in tok else int(tok)))
        else:
            tokens.append((tok, tok))
        pos = m.end()
    tokens.append((EOF, None))
    return tokens


# ---------------------------------------------------------------------------
# Recursive-descent parser / evaluator
# ---------------------------------------------------------------------------
# Grammar:
#   expr   → term   ( ('+' | '-') term   )*
#   term   → factor ( ('*' | '/') factor )*
#   factor → NUMBER | '(' expr ')'
#
# Lower in the call chain = higher precedence (binds tighter).

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos][0]

    def consume(self, expected=None):
        tok_type, tok_val = self.tokens[self.pos]
        if expected and tok_type != expected:
            raise ValueError(f"Expected {expected!r}, got {tok_type!r}")
        self.pos += 1
        return tok_val

    # expr → term (('+' | '-') term)*
    def expr(self):
        result = self.term()
        while self.peek() in (PLUS, MINUS):
            op = self.consume()
            right = self.term()
            result = result + right if op == PLUS else result - right
        return result

    # term → factor (('*' | '/') factor)*
    def term(self):
        result = self.factor()
        while self.peek() in (STAR, SLASH):
            op = self.consume()
            right = self.factor()
            result = result * right if op == STAR else result / right
        return result

    # factor → NUMBER | '(' expr ')'
    def factor(self):
        if self.peek() == NUMBER:
            return self.consume(NUMBER)
        if self.peek() == LPAREN:
            self.consume(LPAREN)
            result = self.expr()
            self.consume(RPAREN)
            return result
        raise ValueError(f"Unexpected token: {self.peek()!r}")


def evaluate(expression: str):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    result = parser.expr()
    if parser.peek() != EOF:
        raise ValueError(f"Unexpected token after expression: {parser.peek()!r}")
    return result


# ---------------------------------------------------------------------------
# Quick smoke tests
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    cases = [
        ('3 + 4 * (2 - 1)', 7),
        ('10 / 2 + 3',      8),
        ('(1 + 2) * (3 + 4)', 21),
        ('100 - 50 * 2',    0),
        ('2 * (3 + (4 - 1))', 12),
    ]
    for expr, expected in cases:
        got = evaluate(expr)
        status = '✓' if got == expected else f'✗ (expected {expected})'
        print(f"  {expr:30s} = {got}  {status}")
