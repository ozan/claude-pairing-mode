# ours-mini-calculator

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T00:15:01.738Z

---

## Turn 1

**User:**

Let's write a Python expression evaluator that handles +, -, *, /, parentheses, and operator precedence. Take a string like '3 + 4 * (2 - 1)' and return the numeric result. No `eval`.

**Pair:**

Assistant: I'll build this as a **recursive-descent parser** — the classic no-`eval` approach. The grammar encodes precedence directly:

```
expr   := term   (('+' | '-') term)*       ← lowest precedence
term   := factor (('*' | '/') factor)*
factor := ['+' | '-'] ( NUMBER | '(' expr ')' )  ← highest
```

[Write(/home/user/evaluator.py)]
"""
Arithmetic expression evaluator — no eval().

Supports: integers, decimals, scientific notation, +  -  *  /,
          parentheses, and unary + / -.

Grammar (EBNF):
    expr   := term   ( ('+' | '-') term   )*
    term   := factor ( ('*' | '/') factor )*
    factor := ['+' | '-'] ( NUMBER | '(' expr ')' )

Operator precedence (low → high):
… (187 more lines)

[Bash(echo $HOME && pwd)]
  /Users/oz
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-60QZSL

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-60QZSL/evaluator.py)]
"""
Arithmetic expression evaluator — no eval().

Supports: integers, decimals, scientific notation, +  -  *  /,
          parentheses, and unary + / -.

Grammar (EBNF):
    expr   := term   ( ('+' | '-') term   )*
    term   := factor ( ('*' | '/') factor )*
    factor := ['+' | '-'] ( NUMBER | '(' expr ')' )

Operator precedence (low → high):
… (187 more lines)

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-60QZSL/test_evaluator.py)]
import pytest
from evaluator import evaluate


# ── basic arithmetic ───────────────────────────────────────────────────────────

def test_addition():              assert evaluate("1 + 2")             == 3.0
def test_subtraction():           assert evaluate("5 - 3")             == 2.0
def test_multiplication():        assert evaluate("4 * 3")             == 12.0
def test_division():              assert evaluate("10 / 4")            == 2.5


… (71 more lines)

[Bash(python -m pytest test_evaluator.py -v 2>&1)]
  error: Exit code 127

[Bash(python3 -m pytest test_evaluator.py -v 2>&1)]
  error: Exit code 2

Assistant: Python 3.9 — `slots=True` on dataclasses arrived in 3.10. Quick fix:

[Edit(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-60QZSL/evaluator.py)]
--- before
@dataclass(slots=True)
class Token:
    type:  TT
    value: float | None = None
--- after
@dataclass
class Token:
    type:  TT
    value: float | None = None

[Bash(python3 -m pytest test_evaluator.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-60QZSL
  collecting ... collected 31 items
  
  test_evaluator.py::test_addition PASSED                                  [  3%]
  test_evaluator.py::test_subtraction PASSED                               [  6%]
  test_evaluator.py::test_multiplication PASSED                            [  9%]
  test_evaluator.py::test_division PASSED                                  [ 12%]
  test_evaluator.py::test_mul_before_add PASSED                            [ 16%]
  test_evaluator.py::test_mul_before_sub PASSED                            [ 19%]
  … (27 more lines)

Assistant: 31/31. Here's a tour of how it works.

---

## Architecture: two stages

### Stage 1 — Lexer (`tokenize`)

A single regex scans the string left-to-right, skipping whitespace, and emits a flat `list[Token]`:

```
'3 + 4 * (2 - 1)'
→ [NUMBER(3), PLUS, NUMBER(4), STAR, LPAREN, NUMBER(2), MINUS, NUMBER(1), RPAREN, EOF]
```

The regex matches integers, decimals (`3.14`), trailing-dot floats (`2.`), and scientific notation (`1e-3`) in group 1, and any operator/paren in group 2. Anything else raises `SyntaxError`.

### Stage 2 — Recursive-descent parser

Precedence is baked into the grammar itself. **Lower-precedence rules call higher-precedence ones**, so high-precedence operations always "bind tighter":

```
expr   ← handles + and -  (lowest precedence)
  └─ term   ← handles * and /
       └─ factor ← handles unary +/-, parentheses, numbers  (highest)
```

Each rule uses a **while loop** to handle repeated same-precedence operators left-associatively (`10 - 3 - 2` → `(10-3)-2 = 5`), while calling **the next rule** for the operands ensures higher-precedence ops win:

```python
def _expr(self) -> float:           # handles + -
    value = self._term()            # left side: already handles * /
    while peek() in (PLUS, MINUS):
        op = consume()
        right = self._term()        # right side: same
        value = value ± right
    return value
```

Unary `-` in `_factor` is **right-recursive** (`self._factor()` again), which correctly handles `--3 == 3` and chains like `-(-5)`.

---

## Key design choices

| Choice | Rationale |
|---|---|
| Separate lexer + parser | Clean separation; the parser never touches raw characters |
| Grammar encodes precedence | No explicit precedence tables; structure *is* the rule |
| `_consume(*expected)` | Single choke-point for both advancing and error-reporting |
| `ZeroDivisionError` vs `SyntaxError` | Distinct exceptions for "bad input shape" vs "bad runtime value" |
| `float` throughout | Uniform result type; integer inputs still return `7.0` not `7` |

---

## Turn 2

**User:**

That's a really clear breakdown — I can see how the grammar structure naturally enforces precedence. One thing I want to trace through to make sure I understand: can you walk me through how `3 + 4 * (2 - 1)` actually gets evaluated? Like, show me the order of recursive calls and when each operator gets consumed?

I think I follow the idea, but seeing the actual call stack unfold on that specific example would help me lock in how the parser threads through the rules.

**Pair:**

Assistant: Let me trace it call-by-call. I'll use indentation to show call depth, and annotate the token stream position as we go.

---

### Token stream (positions 0–9)

```
pos:  0          1     2          3     4       5          6      7          8       9
tok:  NUMBER(3)  PLUS  NUMBER(4)  STAR  LPAREN  NUMBER(2)  MINUS  NUMBER(1)  RPAREN  EOF
```

---

### The full call trace

```
parse()
│  calls _expr()
│
├─ _expr()                                    pos=0: NUMBER(3)
│  │  calls _term() for the left side
│  │
│  ├─ _term()                                 pos=0: NUMBER(3)
│  │  │  calls _factor()
│  │  │
│  │  ├─ _factor()                            pos=0: NUMBER(3)
│  │  │     peek=NUMBER → consume NUMBER(3)   pos advances to 1
│  │  │     return 3.0
│  │  │
│  │  │  value = 3.0
│  │  │  peek=PLUS → not STAR/SLASH, while loop never runs
│  │  │  return 3.0
│  │
│  │  value = 3.0
│  │  peek=PLUS → enters while loop
│  │     consume PLUS                         pos advances to 2
│  │     calls _term() for the right side
│  │
│  ├─ _term()                                 pos=2: NUMBER(4)
│  │  │  calls _factor()
│  │  │
│  │  ├─ _factor()                            pos=2: NUMBER(4)
│  │  │     peek=NUMBER → consume NUMBER(4)   pos advances to 3
│  │  │     return 4.0
│  │  │
│  │  │  value = 4.0
│  │  │  peek=STAR → enters while loop
│  │  │     consume STAR                      pos advances to 4
│  │  │     calls _factor() for the right side
│  │  │
│  │  ├─ _factor()                            pos=4: LPAREN
│  │  │  │  peek=LPAREN → consume LPAREN      pos advances to 5
│  │  │  │  calls _expr() inside the parens
│  │  │  │
│  │  │  ├─ _expr()                           pos=5: NUMBER(2)
│  │  │  │  │  calls _term()
│  │  │  │  │
│  │  │  │  ├─ _term()                        pos=5: NUMBER(2)
│  │  │  │  │  │  calls _factor()
│  │  │  │  │  │
│  │  │  │  │  ├─ _factor()                   pos=5: NUMBER(2)
│  │  │  │  │  │     peek=NUMBER → consume NUMBER(2)  pos advances to 6
│  │  │  │  │  │     return 2.0
│  │  │  │  │  │
│  │  │  │  │  │  value = 2.0
│  │  │  │  │  │  peek=MINUS → not STAR/SLASH, while loop never runs
│  │  │  │  │  │  return 2.0
│  │  │  │  │
│  │  │  │  │  value = 2.0
│  │  │  │  │  peek=MINUS → enters while loop
│  │  │  │  │     consume MINUS               pos advances to 7
│  │  │  │  │     calls _term() for the right side
│  │  │  │  │
│  │  │  │  ├─ _term()                        pos=7: NUMBER(1)
│  │  │  │  │  │  calls _factor()
│  │  │  │  │  │
│  │  │  │  │  ├─ _factor()                   pos=7: NUMBER(1)
│  │  │  │  │  │     peek=NUMBER → consume NUMBER(1)  pos advances to 8
│  │  │  │  │  │     return 1.0
│  │  │  │  │  │
│  │  │  │  │  │  value = 1.0
│  │  │  │  │  │  peek=RPAREN → not STAR/SLASH, while loop never runs
│  │  │  │  │  │  return 1.0
│  │  │  │  │
│  │  │  │  │  right = 1.0
│  │  │  │  │  value = 2.0 - 1.0 = 1.0
│  │  │  │  │  peek=RPAREN → not PLUS/MINUS, while loop exits
│  │  │  │  │  return 1.0
│  │  │  │
│  │  │  │  sub-expression result = 1.0
│  │  │  │  consume RPAREN                    pos advances to 9
│  │  │  │  return 1.0
│  │  │
│  │  │  right = 1.0
│  │  │  value = 4.0 * 1.0 = 4.0
│  │  │  peek=EOF → not STAR/SLASH, while loop exits
│  │  │  return 4.0
│  │
│  │  right = 4.0
│  │  value = 3.0 + 4.0 = 7.0
│  │  peek=EOF → not PLUS/MINUS, while loop exits
│  │  return 7.0
│
│  consume EOF ✓
│  return 7.0
```

---

### Why `*` beat `+`

The key moment is here, mid-way through `_expr`'s while loop:

```
_expr has consumed PLUS and now calls _term() for the right side.
_term() immediately grabs NUMBER(4) — then peeks ahead, sees STAR,
and loops to handle it *right there*, before returning to _expr.
```

`_expr` never sees the `*`. It asked `_term` for "the right operand of `+`" and got back `4.0` — but `_term` had already silently folded in the `* (2-1)`. By the time control returns to `_expr`, the multiplication is a done deal.

That's the whole trick: **each rule greedily consumes all operators at its own precedence level before returning up the call stack**, so higher-precedence operators always bind first.

---

## Turn 3 (final)

**User:**

Got it! That's perfect — I see it now. The key is that `_term()` doesn't just grab one operand and return; it loops through *all* the multiplication/division at that level before handing control back up to `_expr`. So by the time `_expr` sees the result, the `*` is already baked in.

That's a really elegant way to enforce precedence without needing a separate lookup table or priority field. The grammar *structure itself* is the precedence rules. And the parens just trigger a recursive call to `_expr()` to reset and start fresh inside them.

Thanks for walking me through that — I feel like I've got it now. This is something I can adapt if I need to add more operators later too.

<done/>

---

**Run end**: done after 2 turns (193s)
