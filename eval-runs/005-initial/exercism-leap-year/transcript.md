# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T01:46:46.627Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

[Glob(leap.py)]
  No files found

Assistant: The core logic fits in one expression. Which formulation do you prefer?

Assistant: The MCP tool isn't wired here, so I'll present the choice directly.

**Option A**
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 400 == 0 or year % 100 == 0 and year % 4 == 0
```

**Option B**
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

One of these has a subtle bug. Which would you go with, and why?

---

## Turn 2

**User:**

I'll pick **Option B**.

Let me walk through the logic:

Option A (`year % 400 == 0 or year % 100 == 0 and year % 4 == 0`):
- Due to operator precedence, this is: `year % 400 == 0 or (year % 100 == 0 and year % 4 == 0)`
- Test with 1900: not divisible by 400, but IS divisible by both 100 and 4 → evaluates to TRUE (incorrectly marks it as a leap year)
- **Bug**: 1900 is a century year not divisible by 400, so it should NOT be a leap year.

Option B (`year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`):
- Test with 1900: divisible by 4 (TRUE) but then `(100 != 0 (FALSE) or 400 == 0 (FALSE))` → `FALSE` → overall FALSE ✓
- Test with 2000: divisible by 4 (TRUE) and `(100 != 0 (FALSE) or 400 == 0 (TRUE))` → `TRUE and TRUE` → TRUE ✓
- Test with 2004: divisible by 4 (TRUE) and `(100 != 0 (TRUE) or ...)` → `TRUE and TRUE` → TRUE ✓

Option B correctly implements the rule: "leap if divisible by 4, *except* century years must also be divisible by 400."

**Pair:**

Assistant: Exactly right — and you spotted the most interesting part: the bug in A isn't a typo, it's a plausible-looking rearrangement that fails specifically on 1900/2100/2200/2300, the century-year edge case most people don't test first.

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


Assistant: Done. B is also the most readable formulation — it mirrors the English rule directly: *"divisible by 4, unless it's a century, unless that century is also divisible by 400."* The short-circuit evaluation even reflects the frequency of each case (most years hit `% 4`, far fewer hit `% 100`).

---

## Turn 3 (final)

**User:**

Looks good—appreciate the clear walkthrough of the edge cases. You've got a solid mental model of how operator precedence interacts with the leap year rules. That's the kind of reasoning that catches bugs before they ship.

<done/>

---

**Run end**: done after 2 turns (80s)
