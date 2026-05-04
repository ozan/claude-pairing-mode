# ours-mini-calculator

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-04T00:15:05.375Z

---

## Turn 1

**User:**

Let's write a Python expression evaluator that handles +, -, *, /, parentheses, and operator precedence. Take a string like '3 + 4 * (2 - 1)' and return the numeric result. No `eval`.

**Pair:**

[Bash(ls)]
  (Bash completed with no output)

[Write(/evaluator.py)]
"""
Arithmetic expression evaluator using recursive descent parsing.

The key insight: operator precedence falls out naturally from the grammar.
Lower-precedence operators (+/-) sit higher in the call stack, so they
are evaluated last — after the higher-precedence operators (*/) finish.

Grammar (each rule calls the one below it, which has higher precedence):

    expression = term   { ('+' | '-') term   }   ← lowest precedence
    term       = factor { ('*' | '/') factor }   ← higher precedence
    factor     = NUMBER | '(' expression ')' | '-' factor  ← atoms / grouping
… (173 more lines)

[Bash(pwd && ls ~)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-LvT3Fy
  Applications
  Desktop
  dev
  Documents
  Downloads
  Library
  Movies
  Music
  Pictures
  Public

[Write(/Users/ozan/dev/evaluator.py)]
"""
Arithmetic expression evaluator using recursive descent parsing.

The key insight: operator precedence falls out naturally from the grammar.
Lower-precedence operators (+/-) sit higher in the call stack, so they
are evaluated last — after the higher-precedence operators (*/) finish.

Grammar (each rule calls the one below it, which has higher precedence):

    expression = term   { ('+' | '-') term   }   ← lowest precedence
    term       = factor { ('*' | '/') factor }   ← higher precedence
    factor     = NUMBER | '(' expression ')' | '-' factor  ← atoms / grouping
… (173 more lines)

[Bash(ls /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-LvT3Fy/)]
  (Bash completed with no output)

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-ours-mini-calculator-LvT3Fy/evaluator.py)]
"""
Arithmetic expression evaluator using recursive descent parsing.

The key insight: operator precedence falls out naturally from the grammar.
Lower-precedence operators (+/-) sit higher in the call stack, so they
are evaluated last — after the higher-precedence operators (*/) finish.

Grammar (each rule calls the one below it, which has higher precedence):

    expression = term   { ('+' | '-') term   }   ← lowest precedence
    term       = factor { ('*' | '/') factor }   ← higher precedence
    factor     = NUMBER | '(' expression ')' | '-' factor  ← atoms / grouping
… (173 more lines)

[Bash(python evaluator.py)]
  error: Exit code 127

[Bash(python3 evaluator.py)]
  ✓  '1 + 2'                        = 3
    ✓  '10 - 3 - 2'                   = 5
    ✓  '3 + 4 * 2'                    = 11
    ✓  '3 + 4 * (2 - 1)'              = 7
    ✓  '(3 + 4) * (2 - 1)'            = 7
    ✓  '10 / (2 + 3)'                 = 2
    ✓  '2 * 3 + 4 * 5'                = 26
    ✓  '2 * (3 + 4) * 5'              = 70
    ✓  '-3 + 5'                       = 2
    ✓  '-3 * -2'                      = 6
    ✓  '-(3 + 4)'                     = -7
    ✓  '1.5 * 2'                      = 3
  … (3 more lines)

Assistant: 13/13. Here's how it works.

---

## The core idea: encode precedence in the grammar

The trick is that we don't manually check "which operator is more important." Instead, we write **three mutually-recursive functions**, and the *call order* between them is what enforces precedence.

```
parse_expression  →  handles + and -   (lowest precedence)
parse_term        →  handles * and /   (higher precedence)
parse_factor      →  handles numbers, parens, unary minus  (atoms)
```

Each rule calls the one *below* it first. So multiplication gets fully resolved before the addition that wraps it — without any explicit precedence table.

---

## Phase 1 — Tokenizer

Before parsing, we convert the raw string into a flat list of tokens:

```python
'3 + 4 * (2 - 1)'
→  [3.0, '+', 4.0, '*', '(', 2.0, '-', 1.0, ')']
```

`tokenize()` scans character by character. When it sees a digit or `.`, it keeps scanning to capture the whole number. Everything else is a single-character token.

---

## Phase 2 — The three parsing functions

**`parse_expression`** — addition and subtraction:
```python
def parse_expression():
    left = parse_term()          # always start by getting a full term
    while peek() in ('+', '-'):  # then fold in any +/- that follow
        op = consume()
        right = parse_term()
        left = left + right if op == '+' else left - right
    return left
```
It calls `parse_term` first, which means multiplication is resolved *inside* that call before addition ever sees the result. This is the whole mechanism — no special cases needed.

**`parse_term`** — multiplication and division: identical structure, but calls `parse_factor` instead.

**`parse_factor`** — the base cases:
```python
def parse_factor():
    if peek() == '(':
        consume()
        value = parse_expression()  # recursion resets precedence inside parens
        consume()
        return value
    elif peek() == '-':
        consume()
        return -parse_factor()      # unary minus: recurse for chains like --3
    else:
        return consume()            # it's a plain number
```

The parenthesis case calls back up to `parse_expression`, which is what allows arbitrary nesting.

---

## Walking through `3 + 4 * (2 - 1)`

```
parse_expression()
  → parse_term()            # gets the '3'
      → parse_factor() = 3.0
      no * or /
    returns 3.0
  sees '+', consume it
  → parse_term()            # gets '4 * (2 - 1)'
      → parse_factor() = 4.0
      sees '*', consume it
      → parse_factor()      # gets '(2 - 1)'
          consume '('
          → parse_expression()
              → parse_term() → parse_factor() = 2.0
              sees '-', consume it
              → parse_term() → parse_factor() = 1.0
            returns 2.0 - 1.0 = 1.0
          consume ')'
        returns 1.0
      left = 4.0 * 1.0 = 4.0
    returns 4.0
  left = 3.0 + 4.0 = 7.0
returns 7.0  ✓
```

---

## Turn 2 (final)

**User:**

Ah, that makes it click! So the magic is that by structuring the three functions with that call hierarchy — `expression` calls `term` calls `factor` — the lower-precedence operators naturally end up higher in the call stack and get evaluated last. It's not a lookup table or explicit precedence numbers; it's baked into the grammar itself.

And the parentheses case calling back up to `parse_expression` is what resets everything so you can nest arbitrarily.

I think I've got it. All the tests pass, the logic is clean, and I understand how the recursion wires up the precedence. This feels solid.

<done/>

---

**Run end**: done after 1 turn (108s)
