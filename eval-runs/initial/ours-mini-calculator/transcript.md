# ours-mini-calculator

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T19:52:27.222Z

---

## Turn 1

**User:**

Let's write a Python expression evaluator that handles +, -, *, /, parentheses, and operator precedence. Take a string like '3 + 4 * (2 - 1)' and return the numeric result. No `eval`.

**Pair:**

Assistant: Good project — this is a classic parsing problem. The core design choice is how to handle operator precedence. Let me ask upfront:

OPTIONS:
[A] Recursive descent
Encode precedence in the grammar itself: `expr → term ((+|-) term)*`, `term → factor ((*|/) factor)*`, `factor → number | '(' expr ')'`. Each level is a function that calls the next.

[B] Shunting-yard
Scan tokens left-to-right, use two stacks (operators + operands), and flush operators by precedence. Classic Dijkstra algorithm — no recursion needed.

(Reply with A or B, or ask a follow-up question.)

Assistant: **Which parsing strategy?**

**A — Recursive descent**
Encode precedence in the grammar itself: `expr → term ((+|-) term)*`, `term → factor ((*|/) factor)*`, `factor → number | '(' expr ')'`. Each level is a function that calls the next.

**B — Shunting-yard**
Scan tokens left-to-right, use two stacks (operators + operands), and flush operators by precedence. Classic Dijkstra algorithm — no recursion needed.

---

## Turn 2

**User:**

I've laid out the two main approaches. Which one appeals to you?

**A — Recursive descent:** Builds the parse tree structure directly into function calls. More intuitive to read and modify later (especially if you want to add unary operators like `-5` or exponentiation). Slightly harder to debug because the stack trace involves multiple function levels.

**B — Shunting-yard:** More compact, fewer recursive calls, all the logic in one main loop. Historically celebrated in compiler courses. Harder to extend (adding precedence levels requires careful stack management).

For a learning exercise, I'd lean **A** — it *shows* the grammar. But if you want to see how the classic algorithm works, **B** is the move. Pick one, and I'll implement it with explanations along the way.

**Pair:**

Assistant: Recursive descent, without hesitation — the grammar structure maps directly to the code, so it's self-documenting. Let's build it.

First, the tokenizer. Then I'll ask one more key question before the parser.

[Bash(ls evaluator.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(evaluator.py)]
import re

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------
# Token types
NUMBER, PLUS, MINUS, STAR, SLASH, LPAREN, RPAREN, EOF = (
    'NUMBER', '+', '-', '*', '/', '(', ')', 'EOF'
)

def tokenize(text):
    """Return a flat list of (type, value) pairs."""
… (97 more lines)

[Bash(python evaluator.py)]
  error: Exit code 127

[Bash(python3 evaluator.py)]
  error: Exit code 1

[Edit(evaluator.py)]
--- before
def evaluate(expression: str) -> float | int:
--- after
def evaluate(expression: str):

[Bash(python3 evaluator.py)]
  3 + 4 * (2 - 1)                = 7  ✓
    10 / 2 + 3                     = 8.0  ✓
    (1 + 2) * (3 + 4)              = 21  ✓
    100 - 50 * 2                   = 0  ✓
    2 * (3 + (4 - 1))              = 12  ✓

Assistant: All green. Here's the key insight in the code — notice how **precedence falls out of the call chain**:

```
evaluate()
  └─ expr()       ← handles + and -  (lowest precedence)
       └─ term()  ← handles * and /  (higher precedence)
            └─ factor()  ← handles numbers and ()  (tightest binding)
```

`term()` is called *inside* `expr()`, so `*`/`/` always gets evaluated first. You never have to compare precedence levels — the structure enforces it.

---

Now, a question about `factor()` — the part that handles unary minus, like `-5` or `-(3+2)`. Currently it raises an error on those. Which signature handles it correctly?

OPTIONS:
[A] Unary in factor()
```diff
+++ evaluator.py
@@ -67,6 +67,10 @@
     # factor → NUMBER | '(' expr ')'
     def factor(self):
+        if self.peek() == MINUS:
+            self.consume(MINUS)
+            return -self.factor()
         if self.peek() == NUMBER:
             return self.consume(NUMBER)
```

[B] Unary in expr()
```diff
+++ evaluator.py
+++ evaluator.py
@@ -52,6 +52,9 @@
     # expr → term (('+' | '-') term)*
     def expr(self):
+        if self.peek() == MINUS:
+            self.consume(MINUS)
+            return -self.term()
         result = self.term()
```

(Reply with A or B, or ask a follow-up question.)

Assistant: To support `-5` or `-(3+2)`, where should we handle unary minus?

**A — Unary in `factor()`**
```diff
+++ evaluator.py
@@ -67,6 +67,10 @@
    # factor → NUMBER | '(' expr ')'
    def factor(self):
+        if self.peek() == MINUS:
+            self.consume(MINUS)
+            return -self.factor()
        if self.peek() == NUMBER:
            return self.consume(NUMBER)
```

**B — Unary in `expr()`**
```diff
+++ evaluator.py
+++ evaluator.py
@@ -52,6 +52,9 @@
    # expr → term (('+' | '-') term)*
    def expr(self):
+        if self.peek() == MINUS:
+            self.consume(MINUS)
+            return -self.term()
        result = self.term()
```

---

## Turn 3 (final)

**User:**

**A — Unary in `factor()`** is the right call.

Here's why: **unary operators bind tighter than binary operators**. If `-5 + 3` appears, you want `(-5) + 3 = -2`, not `-(5 + 3) = -8`. 

Since `factor()` is the tightest-binding level in our grammar (deepest in the call chain), putting unary `-` there ensures it grabs what comes next *before* binary `+/-` ever see it. And recursively calling `factor()` means `-(-5)` and `-(3+2)` just work.

If we put it in `expr()` (option B), we'd accidentally parse `-5 + 3` as `-(5 + 3)` — wrong precedence.

Let me apply **A**:Perfect — all tests pass! And I can see the implementation **already chose option A** — unary operators are handled in `factor()` (lines 40–43):

```python
def factor(tokens: list, pos: int) -> tuple[float, int]:
    if isinstance(tokens[pos], str) and tokens[pos] in ('+', '-'):
        op, pos = tokens[pos], pos + 1
        val, pos = factor(tokens, pos)  # ← recursive call
        return (-val if op == '-' else val), pos
```

Notice the **recursive call to `factor()`** — this is what makes `-(-5)` and `--3` work correctly. The unary operator strips off, then recurses to whatever comes next (could be another unary, a number, or a parenthesized expr).

Also observe:
- **Left-associativity** is automatic in the `expr()` and `term()` while loops (lines 23–26, 32–35). We compute left-to-right, so `10 - 5 - 2` becomes `(10 - 5) - 2 = 3`, not `10 - (5 - 2) = 7`.
- The tokenizer (line 9) is elegantly compact: one regex finds all numbers and operators.

---

**The evaluator is complete.** All core requirements ✓:
- ✓ Handles `+, -, *, /`
- ✓ Respects parentheses and operator precedence
- ✓ Supports unary minus
- ✓ No `eval()`

Any follow-ups? (E.g., add exponentiation, variables, error messages, etc.?)

<done/>

---

**Run end**: done after 2 turns (102s)
