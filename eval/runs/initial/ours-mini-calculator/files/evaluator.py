class Parser:
    def __init__(self, text):
        self.text = text.replace(' ', '')
        self.pos = 0

    def factor(self):
        if self.text[self.pos] == '-':
            self.pos += 1
            return -self.factor()

        if self.text[self.pos].isdigit() or self.text[self.pos] == '.':
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos] in '0123456789.':
                self.pos += 1
            return float(self.text[start:self.pos])
        elif self.text[self.pos] == '(':
            self.pos += 1
            result = self.expr()
            self.pos += 1  # consume ')'
            return result

    def term(self):
        result = self.factor()
        while self.pos < len(self.text) and self.text[self.pos] in '*/':
            op = self.text[self.pos]
            self.pos += 1
            result = result * self.factor() if op == '*' else result / self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.pos < len(self.text) and self.text[self.pos] in '+-':
            op = self.text[self.pos]
            self.pos += 1
            result = result + self.term() if op == '+' else result - self.term()
        return result

def evaluate(text):
    return Parser(text).expr()
