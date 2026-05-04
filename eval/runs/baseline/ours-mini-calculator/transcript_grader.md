# ours-mini-calculator

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:54:24

## Initial prompt

Let's write a Python expression evaluator that handles +, -, *, /, parentheses, and operator precedence. Take a string like '3 + 4 * (2 - 1)' and return the numeric result. No `eval`.

---

## Turn 1

### Tutor

Tutor: I'll build a clean recursive descent parser — the grammar itself encodes precedence, so no special-casing needed.

[Write(/repo/evaluator.py)]
"""
Expression evaluator — no eval().

Supports: integers & floats, +  -  *  /  (parentheses), unary +/-.

Grammar (top = lowest precedence):
    expr   = term   ( ('+' | '-') term   )*
    term   = factor ( ('*' | '/') factor )*
    factor = NUMBER | '(' expr ')' | ('+' | '-') factor
"""

from __future__ import annotations
… (218 more lines)
  error: EROFS: read-only file system, mkdir '/repo'

[Bash(echo $HOME && ls ~)]
  /Users/oz
  Applications
  Desktop
  dev
  Documents
  Downloads
  Library
  Movies
  Music
  Pictures
  project_euler
  Public
  … (1 more lines)

[Write(/Users/oz/evaluator.py)]
"""
Expression evaluator — no eval().

Supports: integers & floats, +  -  *  /  (parentheses), unary +/-.

Grammar (top = lowest precedence):
    expr   = term   ( ('+' | '-') term   )*
    term   = factor ( ('*' | '/') factor )*
    factor = NUMBER | '(' expr ')' | ('+' | '-') factor
"""

from __future__ import annotations
… (218 more lines)
  File created successfully at: /Users/oz/evaluator.py

[Bash(cd ~ && python evaluator.py)]
  pass  '1 + 2'  = 3.0
    pass  '10 - 3'  = 7.0
    pass  '3 * 4'  = 12.0
    pass  '8 / 2'  = 4.0
    pass  '2 + 3 * 4'  = 14.0
    pass  '10 - 2 * 3'  = 4.0
    pass  '2 * 3 + 4 * 5'  = 26.0
    pass  '(2 + 3) * 4'  = 20.0
    pass  '3 + 4 * (2 - 1)'  = 7.0
    pass  '(1 + 2) * (3 + 4)'  = 21.0
    pass  '((2 + 3))'  = 5.0
    pass  '-3 + 5'  = 2.0
  … (19 more lines)

Tutor: 28/28. Here's a walkthrough of the design:

---

## How it works

### 1. Tokeniser (`_tokenize`)
A single compiled regex chews through the string left-to-right, emitting `Token(kind, value)` objects. Numbers get `kind="NUM"`, everything else (operators, parens) gets `kind="OP"`. A sentinel `EOF` token is appended so the parser never runs off the end.

### 2. Recursive descent parser
The key insight is that **grammar rules encode precedence** — you don't need a lookup table or shunting-yard algorithm. The call chain is:

```
parse()
  └─ _expr()          ← handles + −  (lowest precedence)
       └─ _term()     ← handles * /  (higher precedence)
            └─ _factor()  ← handles numbers, (parens), unary signs
```

Because `_expr` calls `_term` as its sub-rule, multiplication and division naturally bind tighter than addition and subtraction. Parentheses work by calling `_expr` recursively inside `(` `)`, restarting at the bottom of the precedence ladder.

```
2 + 3 * 4
│   └─────┘ _term sees 3*4=12 first
└──────────  _expr adds 2 + 12 = 14 ✓
```

### 3. Unary signs
`_factor` handles leading `+`/`-` by recursing into itself, so `--3`, `-3 * -2`, and `2 * -3 + 10` all work naturally.

### Public API
```python
from evaluator import evaluate

evaluate('3 + 4 * (2 - 1)')   # → 7.0
evaluate('(2 + 3) * 4')       # → 20.0
evaluate('-3 * -2')           # → 6.0
evaluate('7 / 2')             # → 3.5
```

Raises `SyntaxError` for bad input and `ZeroDivisionError` for `/0`. The file can also be run as a CLI: `python evaluator.py "3 + 4 * (2 - 1)"`.

### Student

Thank you for walking me through that! I'm following the design — the recursive descent parser with the grammar-based precedence is really elegant. Let me make sure I understand the key parts:

1. **Tokenizer first** — breaks the string into `Token` objects so we're not wrestling with raw characters.
2. **Grammar encodes precedence** — because `_expr` calls `_term` and `_term` calls `_factor`, multiplication naturally happens before addition. No lookup tables needed.
3. **Unary signs** — handled by `_factor` calling itself recursively, so `-3 * -2` works naturally.

A couple of quick questions to solidify my understanding:

- When we parse `2 + 3 * 4`, does `_expr` call `_term`, which then parses the entire `3 * 4`, and then control returns to `_expr` to handle the `+`? Or is it the other way around?
- If I wanted to add exponentiation (`**`) with higher precedence than `*` and `/`, would I just insert a new function like `_power` between `_term` and `_factor` in the call chain?

And one more thing — looking at the test cases all passing, I'm curious: how does the parser handle things like `2++3`? Is that a syntax error, or does unary `+` chain?

---

## Turn 2

### Tutor

Tutor: Great questions — let me trace through each one precisely, then verify the `2++3` case live.

[Bash(cd ~ && python -c "
from evaluator import evaluate

cases = ['2++3', '2+-3', '2--3', '2-+3']
for c in cases:
    print(f'  evaluate({c!r}) = {evaluate(c)}')
")]
  evaluate('2++3') = 5.0
    evaluate('2+-3') = -1.0
    evaluate('2--3') = 5.0
    evaluate('2-+3') = -1.0
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-s4fmu_mc

Tutor: All valid and correct. Now let's go through your questions one by one.

---

### 1. `2 + 3 * 4` — who parses what, in what order?

You had it exactly right. Here's the precise call trace:

```
parse()
└─ _expr()
     ├─ _term()          ← left side
     │    ├─ _factor()   → returns 2.0
     │    └─ peek is '+', not '*'/'/' → return 2.0  ← stops here!
     │
     ├─ peek is '+' → consume it
     │
     └─ _term()          ← right side
          ├─ _factor()   → returns 3.0
          ├─ peek is '*' → consume it
          ├─ _factor()   → returns 4.0
          └─ return 12.0
     
     2.0 + 12.0 = 14.0  ✓
```

The crucial moment: when the first `_term` peeks ahead and sees `+`, it knows that's **not its business** (`_term` only loops on `*`/`/`) and returns immediately with just `2.0`. Control bubbles up to `_expr`, which owns `+`. Then `_expr` calls a fresh `_term` for the right side — and *that* term call gets to consume `3 * 4`.

The precedence isn't enforced by rules like "do `*` first" — it's structural: higher-precedence operators live deeper in the call stack, so they resolve first.

---

### 2. Adding `**` — yes, insert `_power` in the chain

Almost exactly right, but with one twist: **exponentiation is right-associative**. `2 ** 3 ** 2` should be `2 ** (3 ** 2) = 512`, not `(2 ** 3) ** 2 = 64`. The `while` loop that `_term` and `_expr` use is *left*-associative. For right-associativity, you recurse instead:

```python
# _term now calls _power() instead of _factor()
def _term(self) -> float:
    value = self._power()              # ← changed
    while self._peek().value in ("*", "/"):
        ...

def _power(self) -> float:
    """power = factor ('**' power)?   ← right-recursive, not a loop"""
    base = self._factor()
    if self._peek().value == "**":
        self._consume("**")
        exponent = self._power()       # ← recurse (right side), not a loop
        return base ** exponent
    return base
```

The updated chain:

```
_expr   → + −           (left-assoc, loop)
_term   → * /           (left-assoc, loop)
_power  → **            (right-assoc, recurse)
_factor → NUMBER ( ) unary
```

One more thing to handle: the tokenizer's regex currently matches `-` and `*` as single characters, so `**` would tokenize as two separate `*` tokens. You'd need to add `\*\*` as a higher-priority alternative in `_TOKEN_RE` before the single-char catch-all.

---

### 3. `2++3` — unary `+` chains, not a syntax error

Here's why it works. After `_expr` consumes the binary `+`, it calls `_term → _factor` for the right operand. `_factor` peeks at the *second* `+` and hits this branch:

```python
if tok.value in ("+", "-"):   # unary sign
    op = self._consume().value
    operand = self._factor()  # ← recurses into _factor again
    return operand if op == "+" else -operand
```

It consumes the second `+` as a *unary* sign, recurses, and gets `3`. So the parse tree looks like:

```
  BinaryOp(+)
  ├─ 2
  └─ UnaryOp(+)
       └─ 3
```

`2 + (+3) = 5`. And `2--3` works for the same reason: `2 - (-3) = 5`. In fact you could write `2---3` and get `-1` (`2 - (-(- 3))` = `2 - 3`). The recursion in `_factor` lets unary signs stack arbitrarily deep.

### Student

Oh wow, that trace through `2 + 3 * 4` really clarified it for me. The key is that when the first `_term` peeks and sees `+`, it's like "that's not my operator" and just returns — it doesn't try to keep looking. Then the *second* `_term` call (the one `_expr` makes for the right side) gets to do all the `3 * 4` work. That's how the structure enforces precedence.

And the right-associativity explanation makes total sense now too. I see why you need the recursion instead of a loop for `**` — if you used a loop like `_term` does, you'd get the wrong answer.

One small clarification though: when you said the tokenizer would need `\*\*` as a higher-priority alternative in the regex — does that mean if I wanted to add `**`, I'd need to update `_TOKEN_RE` so it matches `**` as a single token *before* it tries to match single `*` characters? Otherwise it'd split `2**3` into `2`, `*`, `*`, `3` and my parser would choke?

And just to confirm I have the unary stacking right: `2---3` parses as `2 - (-(-(3)))` which is `2 - (-(-3))` = `2 - 3` = `-1`. Is that the right way to think about it?

---

## Turn 3

### Tutor

Tutor: Both exactly right. Let me confirm the `2---3` trace live, then explain the regex ordering precisely.

[Bash(cd ~ && python -c "
from evaluator import evaluate
print(evaluate('2---3'))   # expect -1.0

# verify step by step
print(-(-(3)))             # inner two unary minuses → 3
print(2 - (-(-(3))))      # 2 - 3 → -1
")]
  -1.0
  3
  -1
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-s4fmu_mc

[Bash(cd ~ && python -c "
import re

# Current regex — single * only
current = re.compile(r'\s*(\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|[+\-*/()])\s*')

# Wrong order: single * listed before **
wrong_order = re.compile(r'\s*(\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|[+\-*/()]|\*\*)\s*')

# Right order: ** listed before single *
right_order = re.compile(r'\s*(\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\*\*|[+\-*/()\-])\s*')

text = '2**3'
def tokenize_with(pattern, text):
    tokens, pos = [], 0
    while pos < len(text):
        m = pattern.match(text, pos)
        if not m: break
        tokens.append(m.group(1))
        pos = m.end()
    return tokens

print('wrong order:', tokenize_with(wrong_order, text))  # ** won't win
print('right order:', tokenize_with(right_order, text))  # ** wins
")]
  wrong order: ['2', '*', '*', '3']
  right order: ['2', '**', '3']
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-s4fmu_mc

Tutor: Both confirmed. Here's the precise explanation for each:

---

### Regex ordering: yes, `**` must come first

Python's `re` engine tries alternatives **left to right and stops at the first match** — it doesn't look for the *longest* possible match. So in this pattern:

```python
r"[+\-*/()]"   # ← matches a single * at position 0 of '**', done
r"|\*\*"       # ← never reached
```

The character class `[+\-*/()]` sees the first `*` in `**`, matches it immediately, and the engine moves on. `**` gets split into `*`, `*`.

Flip the order and it works correctly:

```python
r"\*\*"        # ← matches the full '**' first ✓
r"|[+\-*/()]"  # ← fallback for single-char operators
```

The key rule: **in regex alternation, put longer/more-specific patterns before shorter/general ones**.

---

### `2---3`: your trace is exactly right

The three `-` signs distribute as: one binary (owned by `_expr`), two unary (stacked inside `_factor`):

```
_expr
├─ _term → _factor → 2.0
├─ consume '-'  (binary)
└─ _term
     └─ _factor          ← sees '-', unary #1
          └─ _factor     ← sees '-', unary #2
               └─ _factor → 3.0
          returns −(3.0) = −3.0
     returns −(−3.0) = 3.0

2.0 − 3.0 = −1.0  ✓
```

Your notation `2 - (-(-(3)))` is the correct parse tree written out. The two unary minuses cancel — `-(-(3)) = 3` — and then `2 - 3 = -1`. The recursion in `_factor` handles arbitrarily many stacked signs without any special-casing, because each call just peels off one sign and recurses.

### Student

Perfect, that regex demo was super helpful! I see it now — the engine tries alternatives left-to-right and stops at the first match, so if `[+\-*/()]` comes first, it'll grab that single `*` and never even look at the `\*\*` pattern. Putting longer patterns first is the key.

And the `2---3` trace is exactly what I pictured. Each unary `-` peels off one level and recurses into the next `_factor` call. Two unaries cancel out, leaving `2 - 3 = -1`.

I think I've got a solid understanding of how the evaluator works now — the grammar structure encoding precedence, the regex ordering for multi-character operators, unary recursion, right-associativity for `**`. All the pieces fit together.

Since the original problem was just to write an expression evaluator that handles `+`, `-`, `*`, `/`, parentheses, and operator precedence (which the current code does perfectly — all 28 tests pass), and I've now walked through the key design decisions and verified edge cases, I think we're done here.

Thanks for the detailed explanations and live demos! This was really clarifying.

<done/>

---

**Run end:** done after 3 turn(s) in 164.5s
