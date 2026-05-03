import re


def evaluate(expr: str) -> float:
    tokens = _tokenize(expr)
    return _Parser(tokens).parse()


def _tokenize(expr: str) -> list[str]:
    return re.findall(r'\d+\.?\d*|[+\-*/()]', expr)


class _Parser:
    def __init__(self, tokens: list[str]):
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> str | None:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _consume(self) -> str:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def parse(self) -> float:
        result = self._expr()
        if self._peek() is not None:
            raise SyntaxError(f"unexpected token {self._peek()!r} at pos {self._pos}")
        return result

    def _expr(self) -> float:   # handles + and -
        left = self._term()
        while self._peek() in ('+', '-'):
            op = self._consume()
            left = left + self._term() if op == '+' else left - self._term()
        return left

    def _term(self) -> float:   # handles * and /
        left = self._atom()
        while self._peek() in ('*', '/'):
            op = self._consume()
            left = left * self._atom() if op == '*' else left / self._atom()
        return left

    def _atom(self) -> float:   # handles NUMBER and (expr)
        tok = self._consume()
        if tok == '-':
            return -self._atom()
        if tok == '(':
            val = self._expr()
            if self._peek() != ')':
                raise SyntaxError(f"expected ')' at position {self._pos}")
            self._consume()
            return val
        return float(tok)
