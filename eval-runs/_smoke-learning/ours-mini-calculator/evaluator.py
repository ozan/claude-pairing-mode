"""
Arithmetic expression evaluator using recursive descent parsing.

The key insight: operator precedence falls out naturally from the grammar.
Lower-precedence operators (+/-) sit higher in the call stack, so they
are evaluated last — after the higher-precedence operators (*/) finish.

Grammar (each rule calls the one below it, which has higher precedence):

    expression = term   { ('+' | '-') term   }   ← lowest precedence
    term       = factor { ('*' | '/') factor }   ← higher precedence
    factor     = NUMBER | '(' expression ')' | '-' factor  ← atoms / grouping
"""


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

def tokenize(expr: str) -> list:
    """
    Split a raw expression string into a list of tokens.

    Numbers become floats; operators and parentheses become single-char strings.

        '3 + 4 * (2 - 1)'  →  [3.0, '+', 4.0, '*', '(', 2.0, '-', 1.0, ')']
    """
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1

        elif ch in '+-*/()':
            tokens.append(ch)
            i += 1

        elif ch.isdigit() or ch == '.':
            # Scan ahead to collect a full number (including decimals).
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(float(expr[i:j]))
            i = j

        else:
            raise ValueError(f"Unexpected character: {ch!r} at position {i}")

    return tokens


# ---------------------------------------------------------------------------
# Recursive descent parser
# ---------------------------------------------------------------------------

def evaluate(expr: str) -> float:
    """
    Evaluate an arithmetic expression and return its numeric result.

    Supports: +  -  *  /  parentheses  unary minus  decimal numbers
    Does NOT use eval().

    Examples:
        evaluate('3 + 4 * (2 - 1)')  → 7.0
        evaluate('10 / (2 + 3)')     → 2.0
        evaluate('-3 * -2')          → 6.0
    """
    tokens = tokenize(expr)
    pos = 0  # shared cursor into the token list

    # -- helpers that read from / advance the shared cursor -----------------

    def peek():
        """Return the current token without consuming it (or None at EOF)."""
        return tokens[pos] if pos < len(tokens) else None

    def consume():
        """Return the current token and advance the cursor."""
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    # -- grammar rules, from lowest to highest precedence ------------------

    def parse_expression():
        """
        expression = term { ('+' | '-') term }

        Handles addition and subtraction.  We parse a term first, then
        keep folding in more +/- terms from left to right.
        """
        left = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_term()
            left = left + right if op == '+' else left - right
        return left

    def parse_term():
        """
        term = factor { ('*' | '/') factor }

        Handles multiplication and division.  Same left-fold pattern,
        but calls parse_factor instead of parse_term — so it binds tighter.
        """
        left = parse_factor()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_factor()
            if op == '*':
                left = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero in expression")
                left = left / right
        return left

    def parse_factor():
        """
        factor = NUMBER | '(' expression ')' | '-' factor

        Atoms: a bare number, a parenthesised sub-expression that resets
        precedence back to the top, or a unary minus applied recursively.
        """
        token = peek()

        if token == '(':
            consume()                   # discard '('
            value = parse_expression()  # precedence resets inside parens
            consume()                   # discard ')'
            return value

        elif token == '-':
            consume()               # discard '-'
            return -parse_factor()  # recurse for unary chains like --3

        elif isinstance(token, float):
            return consume()

        else:
            raise SyntaxError(f"Unexpected token: {token!r}")

    result = parse_expression()

    if pos != len(tokens):
        raise SyntaxError(f"Unexpected token after expression: {peek()!r}")

    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    cases = [
        # (expression,              expected)
        ('1 + 2',                   3),
        ('10 - 3 - 2',              5),       # left-associative: (10-3)-2
        ('3 + 4 * 2',               11),      # precedence: 3 + (4*2)
        ('3 + 4 * (2 - 1)',         7),       # parens override precedence
        ('(3 + 4) * (2 - 1)',       7),
        ('10 / (2 + 3)',            2),
        ('2 * 3 + 4 * 5',          26),      # (2*3) + (4*5)
        ('2 * (3 + 4) * 5',        70),
        ('-3 + 5',                  2),       # unary minus
        ('-3 * -2',                 6),       # two unary minuses
        ('-(3 + 4)',                -7),      # unary minus on parens
        ('1.5 * 2',                 3),       # decimal input
        ('100 / 4 / 5',            5),       # left-associative division
    ]

    passed = 0
    for expr, expected in cases:
        result = evaluate(expr)
        ok = abs(result - expected) < 1e-9
        status = '✓' if ok else f'✗  (got {result})'
        print(f"  {status}  {expr!r:30s} = {expected}")
        passed += ok

    print(f"\n{passed}/{len(cases)} tests passed")
