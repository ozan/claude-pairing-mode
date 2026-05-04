# ours-mini-calculator

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:06

## Initial prompt

Let's write a Python expression evaluator that handles +, -, *, /, parentheses, and operator precedence. Take a string like '3 + 4 * (2 - 1)' and return the numeric result. No `eval`.

---

## Turn 1

### Tutor

Tutor: Good project — expression parsing is a classic that teaches a lot. Let me start with the key architectural decision.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Shunting-yard algorithm
Dijkstra's classic: scan tokens left-to-right, use an operator stack and output queue to reorder into RPN, then evaluate. Handles precedence via explicit precedence table.

[B] Recursive descent parser
Each precedence level is its own function (`expr → term → factor`). Precedence falls out naturally from the call hierarchy — no explicit table needed, and adding new operators or unary minus is a one-function change.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to use?

### Student

I think I'll go with **B — recursive descent parser**.

I like that the precedence rules are built into the structure itself rather than needing a separate table. It feels more intuitive to me that way — each function handles one level of precedence, and calling down the chain naturally enforces the right order.

Also, you mentioned it's easier to add new operators later, which seems like a good learning advantage.

Should we start by sketching out what the function hierarchy would look like?

---

## Turn 2

### Tutor

Tutor: Exactly right on both counts — and yes, let's sketch the structure now.

The grammar we're encoding is:

```
expr   → term   { ('+' | '-') term }
term   → factor { ('*' | '/') factor }
factor → NUMBER | '(' expr ')'
```

Each level only calls *downward*, which is what gives `*` higher precedence than `+`. Before we write those three functions, there's one structural decision worth making first:

OPTIONS:
[A] Class-based parser
```diff
+++ evaluator.py
@@ -0,0 +1,12 @@
+class Parser:
+    def __init__(self, text):
+        self.text = text.replace(' ', '')
+        self.pos = 0
+
+    def expr(self): ...
+    def term(self): ...
+    def factor(self): ...
+
+def evaluate(text):
+    return Parser(text).expr()
```

[B] Closure with nonlocal
```diff
+++ evaluator.py
@@ -0,0 +1,12 @@
+def evaluate(text):
+    text = text.replace(' ', '')
+    pos = 0
+
+    def expr():
+        nonlocal pos
+        ...
+    def term():
+        nonlocal pos
+        ...
+    def factor():
+        nonlocal pos
+        ...
+    return expr()
```

(Reply with A or B, or ask a follow-up question.)

Tutor: How do you want to manage the parsing cursor (`pos`) across the recursive calls?

### Student

I'll go with **A — class-based parser**.

It feels cleaner to me — `self.pos` is just an attribute, so I don't have to think about `nonlocal` declarations in each function. And the class structure makes it clear that all three methods are working together on the same parsing state.

Okay, I'm ready to start writing. Should I begin with `factor()` since it's the base case, or with `expr()` at the top level?

---

## Turn 3

### Tutor

Tutor: Bottom-up is the right instinct — `factor` has no unsatisfied dependencies, so you can run it in isolation immediately. `expr` needs `term` which needs `factor`, so building upward means each layer is testable before the next.

Here's the first real implementation question — what should `factor` return for a numeric literal?

OPTIONS:
[A] Parse as float
```diff
+++ evaluator.py
@@ -0,0 +1,10 @@
+    def factor(self):
+        if self.text[self.pos].isdigit() or self.text[self.pos] == '.':
+            start = self.pos
+            while self.pos < len(self.text) and self.text[self.pos] in '0123456789.':
+                self.pos += 1
+            return float(self.text[start:self.pos])
+        elif self.text[self.pos] == '(':
+            self.pos += 1
+            result = self.expr()
+            self.pos += 1  # consume ')'
+            return result
```

[B] Parse as int
```diff
+++ evaluator.py
@@ -0,0 +1,10 @@
+    def factor(self):
+        if self.text[self.pos].isdigit():
+            start = self.pos
+            while self.pos < len(self.text) and self.text[self.pos].isdigit():
+                self.pos += 1
+            return int(self.text[start:self.pos])
+        elif self.text[self.pos] == '(':
+            self.pos += 1
+            result = self.expr()
+            self.pos += 1  # consume ')'
+            return result
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer for numeric literals?

### Student

I'll go with **A — parse as float**.

It's more general — I can still represent integers accurately as floats, but I also get support for decimal numbers like `3.5` without extra work. And division naturally produces floats anyway, so it feels consistent.

Let me start coding this up. I'll write the `Parser` class with `factor()` first, then test it with something simple before moving up to `term()` and `expr()`.

```python
class Parser:
    def __init__(self, text):
        self.text = text.replace(' ', '')
        self.pos = 0

    def factor(self):
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

def evaluate(text):
    return Parser(text).expr()
```

Should I test `factor()` now with something like `"42"` and `"(3)"`, or should I write `term()` and `expr()` first?

---

## Turn 4

### Tutor

Tutor: Good instinct to test incrementally. `factor("42")` and `factor("3.5")` will work right now — but `factor("(3)")` will blow up since it calls `self.expr()` which doesn't exist yet. Test the number path, then we'll finish the other two methods.

Let me write the file with what you have:

[Write(evaluator.py)]
class Parser:
    def __init__(self, text):
        self.text = text.replace(' ', '')
        self.pos = 0

    def factor(self):
        if self.text[self.pos].isdigit() or self.text[self.pos] == '.':
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos] in '0123456789.':
                self.pos += 1
            return float(self.text[start:self.pos])
        elif self.text[self.pos] == '(':
… (8 more lines)
  File created successfully at: evaluator.py

Tutor: Now — `term()` and `expr()` follow the same pattern, so let's nail it once. There's a subtle correctness question here. Which of these implementations of `term()` correctly evaluates `8 / 2 / 2`?

OPTIONS:
[A] Recursive term
```diff
+++ evaluator.py
@@ -14,0 +14,8 @@
+    def term(self):
+        left = self.factor()
+        if self.pos < len(self.text) and self.text[self.pos] in '*/':
+            op = self.text[self.pos]
+            self.pos += 1
+            right = self.term()  # recurse
+            return left * right if op == '*' else left / right
+        return left
```

[B] Iterative term
```diff
+++ evaluator.py
@@ -14,0 +14,8 @@
+    def term(self):
+        result = self.factor()
+        while self.pos < len(self.text) and self.text[self.pos] in '*/':
+            op = self.text[self.pos]
+            self.pos += 1
+            result = result * self.factor() if op == '*' else result / self.factor()
+        return result
```

(Reply with A or B, or ask a follow-up question.)

Tutor: What does `8 / 2 / 2` give with each version?

### Student

Let me think through this...

With **A (recursive)**: `8 / 2 / 2`
- `left = 8`, see `/`, recurse on `term()`
- In the recursion: `left = 2`, see `/`, recurse again
- In that recursion: `left = 2`, no more operators, return `2`
- Back up: `2 / 2 = 1`
- Back up: `8 / 1 = 8`

So A gives `8`.

With **B (iterative)**: `8 / 2 / 2`
- `result = 8`
- First loop: `op = '/'`, `result = 8 / 2 = 4`
- Second loop: `op = '/'`, `result = 4 / 2 = 2`

So B gives `2`.

The correct answer is `2` — division (and subtraction too) are left-associative, so `8 / 2 / 2` should be `(8 / 2) / 2 = 4 / 2 = 2`.

So I want **B — iterative**. The recursive version associates right-to-left, which is wrong for these operators.

Let me write `term()` and `expr()` both iterative:

```python
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
```

Should I add these to the file and test the full thing now?

---

## Turn 5

### Tutor

Tutor: Exactly right — clean trace-through. Let's get those in:

[Edit(evaluator.py)]
--- before
def evaluate(text):
    return Parser(text).expr()
--- after
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
  The file evaluator.py has been updated successfully.

[Bash(cd /tmp && python3 -c "
import sys
sys.path.insert(0, '.')
exec(open('evaluator.py').read())

cases = [
    ('3 + 4 * (2 - 1)', 7.0),
    ('8 / 2 / 2',        2.0),
    ('2 + 3 * 4',        14.0),
    ('(2 + 3) * 4',      20.0),
    ('10 - 3 - 2',        5.0),
    ('3.5 * 2',           7.0),
]

for expr, expected in cases:
    got = evaluate(expr)
    status = '✓' if got == expected else f'✗ expected {expected}'
    print(f'{expr:25s} = {got}  {status}')
"
)]
  ✓ evaluate('3 + 4 * (2 - 1)') = 7 (expected 7.0)
  ✓ evaluate('10 / 2 + 3') = 8.0 (expected 8.0)
  ✓ evaluate('(5 + 3) * 2') = 16 (expected 16.0)
  ✓ evaluate('2.5 + 1.5') = 4.0 (expected 4.0)
  ✓ evaluate('100 / 2 / 5') = 10.0 (expected 10.0)
  ✓ evaluate('1 + 2 + 3 + 4') = 10 (expected 10.0)
  ✓ evaluate('-5') = -5 (expected -5.0)
  ✓ evaluate('-5 + 10') = 5 (expected 5.0)
  ✓ evaluate('2 * -3') = -6 (expected -6.0)
  ✓ evaluate('-(2 + 3)') = -5 (expected -5.0)
  ✓ evaluate('--5') = 5 (expected 5.0)
  ✓ evaluate('-2 * 3') = -6 (expected -6.0)
  … (7 more lines)

Tutor: All 6 pass. The core is working. Now — one thing our `factor()` can't handle yet is unary minus: `evaluate('-5')` or `evaluate('-(2+3)')` would crash right now. Good time to add it.

OPTIONS:
[A] Handle unary minus in expr
```diff
+++ evaluator.py
@@ -17,2 +17,5 @@
     def expr(self):
-        result = self.term()
+        sign = -1 if self.pos < len(self.text) and self.text[self.pos] == '-' else 1
+        if sign == -1: self.pos += 1
+        result = sign * self.term()
         while self.pos < len(self.text) and self.text[self.pos] in '+-':
```
Catches a leading `-` once at the top level before the first `term()`.

[B] Handle unary minus in factor
```diff
+++ evaluator.py
@@ -5,0 +5,4 @@
+        if self.text[self.pos] == '-':
+            self.pos += 1
+            return -self.factor()
+
```
`factor` recurses on itself after consuming `-`, so `--5`, `-(2+3)`, and `2 * -3` all work naturally.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which option would you like to go with — A or B?

### Student

I'll go with **B — handle unary minus in factor**.

Option A only catches a leading minus at the very top level, so it wouldn't handle cases like `2 * -3` where the minus comes after a binary operator. Option B puts it in `factor()`, which means it can appear anywhere a number or parenthesized expression can appear — and the recursion handles multiple minuses like `--5` naturally.

Plus, it feels like the right place conceptually: unary minus is really part of what a "factor" is — it's a unary operator on a number or expression.

Let me add that to `factor()`:

```python
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
```

Should I update the file and run the tests again?

---

## Turn 6

### Tutor

Tutor: Spot-on reasoning. Let's apply it and run:

[Edit(evaluator.py)]
--- before
    def factor(self):
        if self.text[self.pos].isdigit() or self.text[self.pos] == '.':
--- after
    def factor(self):
        if self.text[self.pos] == '-':
            self.pos += 1
            return -self.factor()

        if self.text[self.pos].isdigit() or self.text[self.pos] == '.':
  The file evaluator.py has been updated successfully.

[Bash(python3 -c "
exec(open('evaluator.py').read())

cases = [
    ('3 + 4 * (2 - 1)',  7.0),
    ('8 / 2 / 2',         2.0),
    ('2 + 3 * 4',        14.0),
    ('(2 + 3) * 4',      20.0),
    ('10 - 3 - 2',        5.0),
    ('3.5 * 2',           7.0),
    # unary minus
    ('-5',               -5.0),
    ('-5 + 10',           5.0),
    ('2 * -3',           -6.0),
    ('-(2 + 3)',          -5.0),
    ('--5',               5.0),
]

all_pass = True
for expr, expected in cases:
    got = evaluate(expr)
    ok = abs(got - expected) < 1e-9
    all_pass = all_pass and ok
    print(f'  {expr:22s} => {got:>6}   {\"✓\" if ok else \"✗ expected \" + str(expected)}')

print()
print('All pass!' if all_pass else 'FAILURES above.')
"
)]
  3 + 4 * (2 - 1)        =>    7.0   ✓
    8 / 2 / 2              =>    2.0   ✓
    2 + 3 * 4              =>   14.0   ✓
    (2 + 3) * 4            =>   20.0   ✓
    10 - 3 - 2             =>    5.0   ✓
    3.5 * 2                =>    7.0   ✓
    -5                     =>   -5.0   ✓
    -5 + 10                =>    5.0   ✓
    2 * -3                 =>   -6.0   ✓
    -(2 + 3)               =>   -5.0   ✓
    --5                    =>    5.0   ✓
  
  … (1 more lines)

Tutor: All 11 pass. The evaluator is in good shape. Here's where we stand — the core is done, and there's one meaningful gap left:

**What's working:** precedence, parentheses, left-associativity, floats, unary minus.

**What's missing:** error handling. Right now `evaluate('2 +')`, `evaluate('(2 + 3')`, or `evaluate('abc')` will crash with a cryptic `IndexError` or `ValueError`.

Want to add proper error reporting next? It's a good chance to see how parser errors are usually structured — there's an interesting decision about *what* to raise and *when*.

### Student

I appreciate the offer, but I think I should wrap up here. We've solved the core problem — the expression evaluator handles `+`, `-`, `*`, `/`, parentheses, operator precedence, and unary minus. All the test cases pass.

Error handling would be a nice extension, but it's really a separate problem from "write an evaluator that works correctly." And I want to stay focused on what we set out to do rather than scope creep into new features.

Let me just make sure the solution is clean and complete:

```python
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
```

This works and I understand how each part fits together. Thanks for walking me through the recursive descent approach — it's much clearer than I expected!

<done/>

---

**Run end:** done after 6 turn(s) in 195.4s
