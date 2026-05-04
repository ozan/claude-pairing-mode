# ours-mini-calculator

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:08:28

## Initial prompt

Let's write a Python expression evaluator that handles +, -, *, /, parentheses, and operator precedence. Take a string like '3 + 4 * (2 - 1)' and return the numeric result. No `eval`.

---

## Turn 1

### Tutor

Thinking: The user wants to build a Python expression evaluator from scratch (no `eval`). This is a classic recursive descent parser problem. Let me plan this out carefully.
  
  The approach I'll use is a **recursive descent parser** which naturally handles operator precedence:
  
  Grammar:
  ```
  expression  → term (('+' | '-') term)*
  term        → factor (('*' | '/') factor)*
  factor      → NUMBER | '(' expression ')'  | ('+' | '-') factor
  ```
  
  This naturally handles:
  - `+` and `-` have lower precedence than `*` and `/`
  - Parentheses override precedence
  - Unary minus/plus
  
  
  Now I'm building the tokenizer and parser. I'll create a lexer to break the input string into tokens, then implement the recursive descent parser that respects operator precedence and handles parentheses and unary operators.
  
  Writing the evaluator code... Building the tokenizer...
  
  Now I'm setting up the parser with a grammar that respects operator precedence—addition and subtraction at the lowest level, multiplication and division in the middle, and factors like numbers and parenthesized expressions at the highest. The parser class will track position through the token stream and provide helper methods to consume tokens and validate their types.
  
  Implementing the expression parsing rules... Writing test cases... Writing test cases... I'm starting to write out the evaluator code with the token types and tokenizer function first, then moving into the parser class that handles the recursive descent parsing, and finally the public evaluate function that ties everything together.

Tutor: I'll build this as a classic **recursive descent parser** — the cleanest approach for operator precedence. Two files: the evaluator and its tests.

[Write(/repo/evaluator.py)]
"""
Expression evaluator using a recursive descent parser.
Supports: +  -  *  /  parentheses  unary +/-  integers  floats

The grammar encodes precedence directly through the call hierarchy.
Lower precedence rules call higher precedence rules, so higher-precedence
operators end up deeper in the tree and evaluate first.

    expr   → term   (( '+' | '-' ) term  )*      ← lowest precedence
    term   → factor (( '*' | '/' ) factor)*
    factor → NUMBER | '(' expr ')' | ('+' | '-') factor   ← highest
"""
… (156 more lines)
  error: EROFS: read-only file system, mkdir '/repo'

[Bash(pwd && ls ~)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-5sop70hv
  __pycache__
  Applications
  bowling
  Desktop
  dev
  Documents
  Downloads
  evaluator.py
  Library
  Movies
  Music
  … (4 more lines)

Thinking: The files should go in the home directory. Let me write to `~/evaluator.py` and `~/test_evaluator.py`.

[Write(/Users/jbeno/evaluator.py)]
"""
Expression evaluator using a recursive descent parser.
Supports: +  -  *  /  parentheses  unary +/-  integers  floats

The grammar encodes precedence directly through the call hierarchy.
Lower-precedence rules call higher-precedence rules, so deeper calls
evaluate first — no explicit precedence table needed.

    expr   → term   (( '+' | '-' ) term  )*      ← lowest  precedence
    term   → factor (( '*' | '/' ) factor)*
    factor → NUMBER | '(' expr ')' | ('+' | '-') factor   ← highest
"""
… (156 more lines)
  error: EACCES: permission denied, mkdir '/Users/jbeno'

[Bash(echo $HOME && ls $HOME/dev 2>/dev/null || echo "no dev dir")]
  /Users/oz
  ai-pair-proto
  anthropics
  bowling
  scratch

[Write(/Users/oz/dev/scratch/evaluator.py)]
"""
Expression evaluator using a recursive descent parser.
Supports: +  -  *  /  parentheses  unary +/-  integers  floats

The grammar encodes precedence directly through the call hierarchy.
Lower-precedence rules call higher-precedence rules, so deeper calls
evaluate first — no explicit precedence table needed.

    expr   → term   (( '+' | '-' ) term  )*      ← lowest  precedence
    term   → factor (( '*' | '/' ) factor)*
    factor → NUMBER | '(' expr ')' | ('+' | '-') factor   ← highest
"""
… (156 more lines)
  File created successfully at: /Users/oz/dev/scratch/evaluator.py

[Write(/Users/oz/dev/scratch/test_evaluator.py)]
"""Tests for evaluator.py"""

import pytest
from evaluator import evaluate, tokenise, TT


# ── tokeniser ─────────────────────────────────────────────────────────────────

def test_tokenise_basic():
    toks = tokenise("1 + 2")
    types = [t.type for t in toks]
    assert types == [TT.NUMBER, TT.PLUS, TT.NUMBER, TT.EOF]
… (84 more lines)
  File created successfully at: /Users/oz/dev/scratch/test_evaluator.py

[Bash(cd /Users/oz/dev/scratch && python -m pytest test_evaluator.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python
  cachedir: .pytest_cache
  rootdir: /Users/oz/dev/scratch
  plugins: anyio-4.13.0
  collecting ... collected 22 items
  
  test_evaluator.py::test_tokenise_basic PASSED                            [  4%]
  test_evaluator.py::test_tokenise_float PASSED                            [  9%]
  test_evaluator.py::test_tokenise_unknown_char PASSED                     [ 13%]
  test_evaluator.py::test_precedence_and_parens[3 + 4 * (2 - 1)-7.0] PASSED [ 18%]
  test_evaluator.py::test_precedence_and_parens[2 + 3 * 4-14.0] PASSED     [ 22%]
  … (20 more lines)

Tutor: 22/22 ✅. Here's how it works:

---

## Architecture: Recursive Descent Parser

The key insight is that **the grammar itself encodes precedence** — no table or special logic needed. There are two phases:

### Phase 1 — Tokeniser
Converts the raw string into a flat list of `Token` objects using a single regex:
```
"3 + 4 * (2 - 1)"
→ [NUMBER(3), PLUS, NUMBER(4), STAR, LPAREN, NUMBER(2), MINUS, NUMBER(1), RPAREN, EOF]
```

### Phase 2 — Recursive Descent Parser
Three methods call each other in a specific order that naturally enforces precedence:

```
_expr()          handles  +  -        ← called first, lowest precedence
  └─ _term()     handles  *  /
       └─ _factor()  handles numbers, parens, unary
```

**Why this works:** `_expr` calls `_term` to get its operands. So when `_expr` sees `3 + 4 * 2`, it evaluates `3` as a term, then `4 * 2` as a term (because `_term` eagerly consumes `*`). The multiplication happens *inside* the term, so it's done before the addition ever sees it.

**Parens** work by having `_factor` call `_expr()` recursively — resetting the entire precedence ladder from scratch inside the parentheses.

**Unary minus** (`-3`, `--3`) is handled in `_factor` by recursing on itself: `-` consumes one token, then calls `_factor` again for the operand.

### The grammar in BNF
```
expr   → term   (( '+' | '-' ) term  )*      ← lowest precedence
term   → factor (( '*' | '/' ) factor)*
factor → NUMBER | '(' expr ')' | ('+' | '-') factor   ← highest
```

Each `*` loop makes each level **left-associative** (`10 - 3 - 2 = 5`, not `9`).

### Student

Thanks for walking me through that! This is really clear. I can see how the grammar structure creates the precedence hierarchy — by having `_expr` call `_term` and `_term` call `_factor`, the multiplication and division get evaluated "deeper" in the recursion tree before the addition and subtraction ever process them.

A couple of quick questions to make sure I really understand:

1. **Left-associativity via the loop:** In `_expr`, the `while` loop `(( '+' | '-' ) term )*` means we keep consuming `+` and `-` from left to right. So `10 - 3 - 2` processes as `(10 - 3) - 2`. Is that because each iteration stores the running result back in `result`?

2. **Resetting precedence in parentheses:** When `_factor` encounters `(`, it calls `_expr` again — so the precedence rules restart. That's elegant. Does that mean `(3 + 4) * 2` correctly forces the addition before the multiplication, even though `*` would normally bind tighter?

3. **Unary operators:** The unary `-` in `_factor` calls `_factor` again recursively, which lets us chain them like `-(-3)`. Does the recursion just keep consuming unary operators until it hits a number or `(`?

I think I've got the gist, but I want to be solid on these details before we wrap.

---

## Turn 2

### Tutor

Thinking: The user is asking three conceptual questions about the recursive descent parser. These are all great questions that show they're genuinely engaging with the material. Let me answer each one precisely and clearly.
  
  1. **Left-associativity via the loop** - Yes, exactly right. The `left = left op right` assignment on each iteration accumulates the running result. Let me trace through `10 - 3 - 2`:
     - `left = _term()` → 10
     - iteration 1: op = `-`, right = `_term()` → 3, `left = 10 - 3 = 7`
     - iteration 2: op = `-`, right = `_term()` → 2, `left = 7 - 2 = 5`
     - return 5
     
     So `left` keeps building up the result as we process each operator.
  
  2. **Resetting precedence in parentheses** - Exactly. When `_factor` encounters `(`, it calls `_expr()` which starts fresh at the lowest precedence level. This means for `(3 + 4) * 2`, the parenthesized expression gets fully evaluated before the multiplication happens, effectively giving it higher precedence.
  
  3. **Unary operators** - The recursion chains through unary operators until reaching a base value. For `--3`, each `-` triggers another `_factor()` call, stacking the negations until we hit the number itself.
  
  The right-associativity from recursion works fine here since unary negation is self-inverse anyway. Now I should give the user clear, direct answers to their questions since they're nearly there.

Tutor: All three are exactly right. Let me confirm each one with a trace so the intuition becomes concrete.

---

### 1. Left-associativity: yes, `left` is the accumulator

Each loop iteration folds the new `right` into the running `left`:

```python
# 10 - 3 - 2

left = _term()          # left = 10

# iteration 1
op    = consume(MINUS)
right = _term()         # right = 3
left  = left - right    # left = 10 - 3 = 7   ← stored back

# iteration 2
op    = consume(MINUS)
right = _term()         # right = 2
left  = left - right    # left = 7  - 2 = 5   ← stored back

return 5  ✓
```

Right-associativity would look different — it would use recursion instead of a loop: `return left - _expr()`. That's actually how `_factor` handles unary (below).

---

### 2. Parens restart the whole ladder — that's the trick

For `(3 + 4) * 2`, the call stack looks like this:

```
_term()                          ← entry point for the whole expression
  _factor()                      ← left operand of *
    sees '(' → calls _expr()     ← precedence ladder restarts from the bottom
      _term()  → 3
      sees '+' → _term() → 4
      returns 7                  ← addition finishes completely
    consumes ')'
    returns 7                    ← _factor returns 7 as a single "number"
  left = 7
  sees '*' → _factor() → 2
  left = 7 * 2 = 14
```

The `*` is processed by `_term`, but by the time `_term` reaches it, `(3 + 4)` has already collapsed into a single value `7`. The outer `_term` never "sees" the `+` at all — it's already gone.

---

### 3. Unary: right-recursive, consumes all leading operators

```python
# --3
_factor()           # sees '-', recurses
  _factor()         # sees '-', recurses
    _factor()       # sees '3', returns 3.0
  return -(3.0)     # = -3.0
return -(-3.0)      # =  3.0  ✓
```

Yes — it keeps consuming one unary operator per call until it hits something that isn't `+` or `-`. The recursion is naturally right-to-left, but for unary that doesn't matter: `-(-(-3))` associating any direction gives the same result.

The contrast with the binary operators is worth noting explicitly:

| | mechanism | associativity |
|---|---|---|
| `+` `-` `*` `/` | `while` loop, fold into `left` | **left** |
| unary `+` `-` | tail recursion into `_factor` | right (irrelevant) |

The loop is the direct cause of left-associativity. Swap it for recursion and you'd get right-associativity — which is actually correct for exponentiation (`2^3^2 = 2^9`, not `8^2`), if you ever wanted to add `**`.

### Student

Okay, that makes it crystal clear! The loop with the accumulator is the key to left-associativity, and recursion would flip it. And I really like how you showed that parens work because `_expr()` gets called again — it's not special logic, it just falls out of the structure.

One thing is clicking for me now: the reason `(3 + 4) * 2` works correctly isn't because the parser "knows" to do addition first — it's because by the time `_term()` ever looks for a `*`, the addition has already been evaluated and turned into a single number by the recursive call to `_expr()`. The precedence doesn't exist as a rule; it exists because of the *shape* of the code.

I feel solid on this. Let me just run through the original test case one more time in my head to make sure:

`'3 + 4 * (2 - 1)'`

1. `_expr()` calls `_term()`, gets `3`
2. `_expr()` sees `+`, calls `_term()` again
3. That `_term()` calls `_factor()` and gets `4`, then sees `*`
4. `_term()` stays in its while loop, calls `_factor()` for the right side
5. `_factor()` sees `(`, calls `_expr()` again, which evaluates `2 - 1 = 1`
6. `_factor()` returns `1`, `_term()` does `4 * 1 = 4`
7. `_term()` returns `4` to the outer `_expr()`
8. `_expr()` does `3 + 4 = 7`

That flow is exactly what we want. I think I've got it. Thanks for the detailed trace — that really cemented it.

<done/>

---

**Run end:** done after 2 turn(s) in 130.4s
