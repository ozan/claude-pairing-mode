# ours-mini-calculator

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T08:47:51.919Z

---

## Turn 1

**User:**

Let's write a Python expression evaluator that handles +, -, *, /, parentheses, and operator precedence. Take a string like '3 + 4 * (2 - 1)' and return the numeric result. No `eval`.

**Pair:**

Assistant: Classic parsing problem — and a great one. First architectural decision: how do we handle operator precedence?

Assistant: Let me just proceed with the best approach and explain the tradeoff.

The two main strategies are:

**A — Shunting-yard algorithm**: Convert infix → postfix using a stack, then evaluate. Classic Dijkstra. Two-phase.

**B — Recursive descent parser**: Encode precedence directly in the grammar (`expr → term ((+|-) term)*`, `term → factor ((*|/) factor)*`). One pass, naturally handles parens via recursion.

Recursive descent is the better pick here — it's cleaner, directly mirrors the grammar, and is the technique used in real-world parsers. Shunting-yard is clever but a specialized trick. Let's go with recursive descent.

Here's the plan:
- `parse_expr` handles `+` / `-` (lowest precedence)
- `parse_term` handles `*` / `/` (higher precedence)
- `parse_factor` handles numbers and `(...)` (highest precedence)

Let me check the working directory and create the file:

[Glob(evaluator.py)]
  No files found

[Write(evaluator.py)]
"""
Recursive-descent expression evaluator.

Grammar (lowest → highest precedence):
    expr   ::= term   (('+' | '-') term)*
    term   ::= factor (('*' | '/') factor)*
    factor ::= NUMBER | '(' expr ')'
"""


class Parser:
    def __init__(self, text: str):
… (107 more lines)

[Bash(python evaluator.py)]
  error: Exit code 127

[Bash(python3 evaluator.py)]
  ✓  '3 + 4 * (2 - 1)'              => 7.0 (expected 7.0)
  ✓  '10 / 2 + 3'                   => 8.0 (expected 8.0)
  ✓  '(1 + 2) * (3 + 4)'            => 21.0 (expected 21.0)
  ✓  '2 * 3 + 4 * 5'                => 26.0 (expected 26.0)
  ✓  '100 - 50 / 5'                 => 90.0 (expected 90.0)

Assistant: All 5 pass. Here's what to notice about the design:

**Precedence falls out of the call graph.** `parse_expr` calls `parse_term`, which calls `parse_factor`. Since lower-precedence rules call higher-precedence ones, `*`/`/` always bind tighter than `+`/`-` — no explicit precedence table needed.

**Parentheses are free.** `parse_factor` just recurses back to `parse_expr` when it sees `(`. The grammar handles nesting at any depth automatically.

**Each rule is a `while` loop, not recursion.** This makes `+`, `-`, `*`, `/` left-associative (e.g. `8 - 3 - 2 = 3`, not `7`). If you used right-recursion (`parse_expr` calling itself) you'd get right-associativity — which would be wrong for subtraction/division.

Want to extend this — unary minus, exponentiation (`**`), or variables? Or shall we add proper error messages with position info?

---

## Turn 2

**User:**

The design is really clean — I like how precedence just falls out of the call hierarchy instead of needing an explicit table. And the left-associativity via `while` loops instead of right-recursive calls is a good catch.

The tests all pass and it handles the original ask perfectly (parentheses, all four ops, correct precedence). 

I'd want to add **error messages with position info** — right now if you feed it `'3 + 4 *'` or mismatched parens, the error messages are opaque. Would be worth doing before shipping this.

Should we add that, or is this far enough?

**Pair:**

Assistant: Good call — error messages are where users spend most of their debugging time. Before we add position tracking, there's a key design question: right now `tokenize` returns `list[str]`, losing all position info. We need to carry positions forward.

[Read(evaluator.py)]
  1	"""
  2	Recursive-descent expression evaluator.
  3	
  4	Grammar (lowest → highest precedence):
  5	    expr   ::= term   (('+' | '-') term)*
  6	    term   ::= factor (('*' | '/') factor)*
  7	    factor ::= NUMBER | '(' expr ')'
  8	"""
  9	
  10	
  11	class Parser:
  12	    def __init__(self, text: str):
  … (107 more lines)

Assistant: How should each token carry its source position? Which of these two approaches do you prefer?

Assistant: The `propose_options` tool isn't available in this session, so I'll just call it: **named tuple** is the right move.

The alternative — two parallel lists `tokens` and `positions` — is tempting but fragile: they have to be indexed in lockstep, and nothing in the type system enforces that. If you ever slice one or pass one without the other, you get silent misalignment. Bundling value + position together in a `Token` means you can't have one without the other.

Here's the full update — position tracking through tokenizer → parser → error messages:

[Edit(evaluator.py)]
--- before
"""
Recursive-descent expression evaluator.

Grammar (lowest → highest precedence):
    expr   ::= term   (('+' | '-') term)*
    term   ::= factor (('*' | '/') factor)*
    factor ::= NUMBER | '(' expr ')'
"""


class Parser:
    def __init__(self, text: str):
        self.tokens = tokenize(text)
        self.pos = 0

    # --- token helpers ---

    def peek(self):
        """Return the current token without consuming it, or None at end."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        """Return and advance past the current token."""
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, value):
        """Consume and assert the next token equals *value*."""
        tok = self.consume()
        if tok != value:
            raise ValueError(f"Expected {value!r}, got {tok!r}")
        return tok

    # --- grammar rules ---

    def parse_expr(self) -> float:
        """expr ::= term (('+' | '-') term)*"""
        result = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            if op == '+':
                result += right
            else:
                result -= right
        return result

    def parse_term(self) -> float:
        """term ::= factor (('*' | '/') factor)*"""
        result = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_factor()
            if op == '*':
                result *= right
            else:
                result /= right
        return result

    def parse_factor(self) -> float:
        """factor ::= NUMBER | '(' expr ')'"""
        tok = self.peek()
        if tok == '(':
            self.consume()          # eat '('
            result = self.parse_expr()
            self.expect(')')
            return result
        # must be a number
        self.consume()
        return float(tok)


def tokenize(text: str) -> list[str]:
    """Split expression into a flat list of number strings and operator/paren chars."""
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch in '+-*/()':
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == '.':
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            tokens.append(text[i:j])
            i = j
        else:
            raise ValueError(f"Unexpected character: {ch!r}")
    return tokens


def evaluate(expression: str) -> float:
    """Parse and evaluate an arithmetic expression string."""
    parser = Parser(expression)
    result = parser.parse_expr()
    if parser.peek() is not None:
        raise ValueError(f"Unexpected token: {parser.peek()!r}")
    return result
--- after
"""
Recursive-descent expression evaluator.

Grammar (lowest → highest precedence):
    expr   ::= term   (('+' | '-') term)*
    term   ::= factor (('*' | '/') factor)*
    factor ::= NUMBER | '(' expr ')'
"""
from typing import NamedTuple


class Token(NamedTuple):
    value: str
    pos: int   # character offset in the original expression string


class ParseError(ValueError):
    def __init__(self, message: str, expr: str, pos: int):
        # Build a caret line pointing at the bad position, e.g.:
        #   3 + 4 *
        #           ^ expected a number or '('
        caret = ' ' * pos + '^'
        super().__init__(f"{message}\n  {expr}\n  {caret}")


class Parser:
    def __init__(self, text: str):
        self.text = text
        self.tokens: list[Token] = tokenize(text)
        self.pos = 0

    # --- token helpers ---

    def peek(self) -> Token | None:
        """Return the current token without consuming it, or None at end."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self) -> Token:
        """Return and advance past the current token."""
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, value: str) -> Token:
        """Consume and assert the next token's value equals *value*."""
        tok = self.peek()
        if tok is None:
            raise ParseError(
                f"Expected {value!r} but reached end of expression",
                self.text, len(self.text),
            )
        if tok.value != value:
            raise ParseError(
                f"Expected {value!r}, got {tok.value!r}",
                self.text, tok.pos,
            )
        return self.consume()

    # --- grammar rules ---

    def parse_expr(self) -> float:
        """expr ::= term (('+' | '-') term)*"""
        result = self.parse_term()
        while (tok := self.peek()) and tok.value in ('+', '-'):
            op = self.consume().value
            right = self.parse_term()
            result = result + right if op == '+' else result - right
        return result

    def parse_term(self) -> float:
        """term ::= factor (('*' | '/') factor)*"""
        result = self.parse_factor()
        while (tok := self.peek()) and tok.value in ('*', '/'):
            op = self.consume().value
            right = self.parse_factor()
            result = result * right if op == '*' else result / right
        return result

    def parse_factor(self) -> float:
        """factor ::= NUMBER | '(' expr ')'"""
        tok = self.peek()
        if tok is None:
            raise ParseError(
                "Expected a number or '(' but reached end of expression",
                self.text, len(self.text),
            )
        if tok.value == '(':
            self.consume()
            result = self.parse_expr()
            self.expect(')')
            return result
        try:
            self.consume()
            return float(tok.value)
        except ValueError:
            raise ParseError(
                f"Expected a number or '(', got {tok.value!r}",
                self.text, tok.pos,
            )


def tokenize(text: str) -> list[Token]:
    """Split expression into Token objects, each carrying its source position."""
    tokens: list[Token] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch in '+-*/()':
            tokens.append(Token(ch, i))
            i += 1
        elif ch.isdigit() or ch == '.':
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            tokens.append(Token(text[i:j], i))
            i = j
        else:
            raise ParseError(f"Unexpected character: {ch!r}", text, i)
    return tokens


def evaluate(expression: str) -> float:
    """Parse and evaluate an arithmetic expression string."""
    parser = Parser(expression)
    result = parser.parse_expr()
    if (leftover := parser.peek()) is not None:
        raise ParseError(
            f"Unexpected token {leftover.value!r}",
            expression, leftover.pos,
        )
    return result

Assistant: Now update the test block to exercise the error cases too:

[Edit(evaluator.py)]
--- before
if __name__ == '__main__':
    tests = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('10 / 2 + 3',       8.0),
        ('(1 + 2) * (3 + 4)', 21.0),
        ('2 * 3 + 4 * 5',    26.0),
        ('100 - 50 / 5',     90.0),
    ]
    for expr, expected in tests:
        got = evaluate(expr)
        status = '✓' if got == expected else '✗'
        print(f"{status}  {expr!r:30s} => {got} (expected {expected})")
--- after
if __name__ == '__main__':
    good = [
        ('3 + 4 * (2 - 1)', 7.0),
        ('10 / 2 + 3',       8.0),
        ('(1 + 2) * (3 + 4)', 21.0),
        ('2 * 3 + 4 * 5',    26.0),
        ('100 - 50 / 5',     90.0),
    ]
    for expr, expected in good:
        got = evaluate(expr)
        status = '✓' if got == expected else '✗'
        print(f"{status}  {expr!r:30s} => {got} (expected {expected})")

    print()
    bad = [
        '3 + 4 *',        # trailing operator — no RHS
        '(1 + 2',         # unclosed paren
        '1 + * 2',        # operator where value expected
    ]
    for expr in bad:
        try:
            evaluate(expr)
            print(f"✗  {expr!r} — should have raised")
        except ParseError as e:
            print(f"✓  caught error for {expr!r}:\n{e}")

[Bash(python3 evaluator.py)]
  error: Exit code 1

Assistant: Python < 3.10 — `X | None` in annotations needs `from __future__ import annotations` (or use `Optional`). Easy fix:

[Edit(evaluator.py)]
--- before
from typing import NamedTuple
--- after
from __future__ import annotations
from typing import NamedTuple

[Bash(python3 evaluator.py)]
  ✓  '3 + 4 * (2 - 1)'              => 7.0 (expected 7.0)
  ✓  '10 / 2 + 3'                   => 8.0 (expected 8.0)
  ✓  '(1 + 2) * (3 + 4)'            => 21.0 (expected 21.0)
  ✓  '2 * 3 + 4 * 5'                => 26.0 (expected 26.0)
  ✓  '100 - 50 / 5'                 => 90.0 (expected 90.0)
  
  ✓  caught error for '3 + 4 *':
  Expected a number or '(' but reached end of expression
    3 + 4 *
           ^
  ✓  caught error for '(1 + 2':
  Expected ')' but reached end of expression
  … (6 more lines)

Assistant: All good. The caret points exactly at the problem in each case.

A few things worth noting about what changed:

**`from __future__ import annotations`** — defers evaluation of all annotations to strings, which is how `X | None` works pre-3.10. It's the cleanest backport; the alternative is `Optional[Token]` from `typing`, which is more verbose and deprecated in 3.10+.

**`ParseError` subclasses `ValueError`** — callers who just do `except ValueError` still catch it, but callers who want to distinguish parse errors from other value errors (e.g. divide-by-zero) can catch `ParseError` specifically. Always worth keeping your exception hierarchy narrow.

**The walrus operator in `while`** — `while (tok := self.peek()) and tok.value in ('+', '-')` lets us peek once and bind the result, instead of calling `peek()` twice. Small thing but avoids a subtle bug if `peek()` ever had side effects.

Want to tackle unary minus next (`-3`, `-(1+2)`)? It fits naturally into `parse_factor`.

---

## Turn 3 (final)

**User:**

Yeah, I like the caret error messages — much easier to debug than before. And the position tracking through the Token namedtuple is solid.

But I think we're at a natural stopping point here. The original ask was "handles +, -, *, /, parentheses, and operator precedence" — and we've nailed that. Plus we went the extra mile with error messages and position info, which rounds it out nicely.

Unary minus would be a fun extension, but it feels like scope creep at this point. The evaluator does what was asked, handles errors well, and the code is clean enough to extend later if needed.

I'd call this done. Good recursive descent parser, proper error reporting, all the tests pass.

<done/>

---

**Run end**: done after 2 turns (158s)
