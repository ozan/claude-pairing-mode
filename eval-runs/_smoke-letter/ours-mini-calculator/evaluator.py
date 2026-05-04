class Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos] == ' ':
            self.pos += 1

    def parse_expr(self):
        """Handles + and - (lowest precedence)."""
        left = self.parse_term()
        self.skip_whitespace()
        while self.pos < len(self.text) and self.text[self.pos] in ('+', '-'):
            op = self.text[self.pos]; self.pos += 1
            right = self.parse_term()
            left = left + right if op == '+' else left - right
            self.skip_whitespace()
        return left

    def parse_term(self):
        """Handles * and / (medium precedence)."""
        left = self.parse_factor()
        self.skip_whitespace()
        while self.pos < len(self.text) and self.text[self.pos] in ('*', '/'):
            op = self.text[self.pos]; self.pos += 1
            right = self.parse_factor()
            left = left * right if op == '*' else left / right
            self.skip_whitespace()
        return left

    def parse_factor(self):
        """Handles numbers and parenthesised sub-expressions (highest precedence)."""
        self.skip_whitespace()
        if self.text[self.pos] == '(':
            self.pos += 1          # consume '('
            val = self.parse_expr()
            self.skip_whitespace()
            self.pos += 1          # consume ')'
            return val
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos] in '0123456789.':
            self.pos += 1
        return float(self.text[start:self.pos])


def evaluate(expr: str) -> float:
    return Parser(expr).parse_expr()
