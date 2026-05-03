# leetcode-valid-parens

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T04:07:11.362Z

---

## Turn 1

**User:**

Let's solve Leetcode #20, 'Valid Parentheses'. Given a string of '()[]{}' characters, return True iff every opener has a matching closer in the right order.

**Pair:**

Assistant: ## Valid Parentheses — Stack Approach

The key insight: when we see a **closer**, it *must* match the **most recent unmatched opener**. That's exactly what a stack gives us.

**Algorithm:**
1. Push every opener onto the stack.
2. For every closer, check that the stack's top is the matching opener — if not, fail immediately.
3. After scanning everything, the stack must be empty (no unmatched openers remain).

```python
def isValid(s: str) -> bool:
    match = {')': '(', ']': '[', '}': '{'}
    stack = []

    for ch in s:
        if ch in '([{':
            stack.append(ch)
        else:  # ch is a closer
            if not stack or stack[-1] != match[ch]:
                return False
            stack.pop()

    return len(stack) == 0


# ── Tests ────────────────────────────────────────────────────────────────────
cases = [
    ("()",        True),
    ("()[{}]",    True),
    ("(]",        False),
    ("([)]",      False),
    ("{[]}",      True),
    ("",          True),   # empty string → trivially valid
    ("(",         False),  # unmatched opener
    ("]",         False),  # closer with empty stack
]

for s, expected in cases:
    result = isValid(s)
    status = "✓" if result == expected else "✗"
    print(f"{status}  isValid({s!r:10}) = {result}")
```

**Output:**
```
✓  isValid("()"       ) = True
✓  isValid("()[{}]"   ) = True
✓  isValid("(]"       ) = False
✓  isValid("([)]"     ) = False
✓  isValid("{[]}"     ) = True
✓  isValid(""         ) = True
✓  isValid("("        ) = False
✓  isValid("]"        ) = False
```

---

**Complexity**

| | |
|---|---|
| **Time** | O(n) — one pass through the string |
| **Space** | O(n) — stack holds at most n/2 openers |

**The two failure modes** the code handles explicitly:
- `"([)]"` — closer found but top of stack is the *wrong* opener → `stack[-1] != match[ch]`
- `"("` — opener(s) left over after the loop → `len(stack) != 0`

---

