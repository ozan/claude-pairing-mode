# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:38:19.653Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

[Bash(ls leap.py 2>/dev/null && echo exists || echo missing)]
  missing

Assistant: The `propose_options` tool isn't loading, so I'll present the choice directly. Before writing the file — which implementation do you prefer?

---

**Option A**
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 or year % 400 == 0 and year % 100 != 0
```

**Option B**
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

Both are one-liners. Which is correct?

---

## Turn 2

**User:**

I've set up the choice — now it's your turn. 

**Quick recap:**
- **Option A** uses `or` as the main operator with `and` on the right
- **Option B** uses `and` as the main operator with `or` nested inside parentheses

The difference matters because of operator precedence. Test them mentally:
- Year 1900 (divisible by 100 but NOT 400) — should be **False**
- Year 2000 (divisible by 400) — should be **True**  
- Year 2004 (divisible by 4, not 100) — should be **True**

Which option handles all three correctly? Pick **A** or **B**.

**Pair:**

Assistant: **B** — and here's why A is subtly broken.

Python's `and` binds tighter than `or`, so Option A parses as:

```
year % 4 == 0  or  (year % 400 == 0 and year % 100 != 0)
```

That second clause is *always* False — anything divisible by 400 is also divisible by 100, so `% 100 != 0` can never be True when `% 400 == 0`. Option A collapses to just `year % 4 == 0`, which wrongly marks 1900, 1800, 1700 as leap years.

Option B is correct:

```python
year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

Read it as: *"must be divisible by 4, AND must either not be a century OR be a 400-year."* The parentheses override precedence to make `or` evaluate first — that's the key.

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


Assistant: Done. The general pattern worth internalizing: when mixing `and`/`or` in a boolean expression, **always parenthesize explicitly** if the intended grouping differs from left-to-right — even when precedence would give the right answer, it makes the logic self-documenting.

---

## Turn 3 (final)

**User:**

Looking good! Let me verify the file was created correctly and then test it with the three cases we discussed:Perfect! All test cases pass. ✓

**Summary:**
- **1900** (century, not 400-divisible) → False ✓
- **2000** (400-divisible) → True ✓  
- **2004** (regular 4-divisible) → True ✓

The implementation correctly handles the three rules:
1. Divisible by 4 → leap year
2. Divisible by 100 → NOT a leap year (exception)
3. Divisible by 400 → IS a leap year (exception to the exception)

The parentheses in Option B are crucial — they ensure `or` groups before `and`, so the "century years" logic (`year % 100 != 0 or year % 400 == 0`) evaluates as a single unit before the main `and` check.

<done/>

---

**Run end**: done after 2 turns (88s)
