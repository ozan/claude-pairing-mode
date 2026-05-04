# exercism-leap-year

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:23:43

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

Thinking: The user wants to implement a `is_leap_year(year)` function in Python for the Exercism 'Leap' exercise. 
  
  The rules are:
  - Divisible by 4 → leap year
  - EXCEPT century years (divisible by 100) → NOT leap year
  - UNLESS also divisible by 400 → leap year
  
  So the logic is: `(year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)`
  
  This is a good teaching moment. Let me think about what options to present.
  
  There are a few ways to express this:
  
  
  Option A checks the rarest case first (divisible by 400), then falls back to the common case (divisible by 4 but not 100). Option B starts with the most common divisibility check and handles the exceptions. Both are logically equivalent, but they differ in how they read against the problem statement and which conditions get evaluated first.
  
  The real question is whether to express this as a single boolean expression or break it into an if/elif/else chain—one is more concise, the other more explicit about the decision tree.
  
  I'm also considering which boolean formulation makes the best teaching example. Option A uses explicit parentheses to clarify the logic, while Option B relies on operator precedence, which is technically correct but creates a readability trap that could confuse learners.

Tutor: Good small problem — but it has a nice boolean structure question worth pausing on. Let me present the core expression choice.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me propose the options for the core boolean expression structure.

OPTIONS:
[A] Rely on precedence
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 400 == 0 or year % 100 != 0 and year % 4 == 0
```

[B] Explicit parentheses
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=Option A is technically correct — Python's `and` binds tighter than `or`, so `year % 100 != 0 and year % 4 == 0` is evaluated first. But relying on that silently makes the code fragile: a reader has to know the precedence rules, and a small refactor (swapping `or`/`and`) could introduce a bug. Option B uses explicit parentheses to make grouping unambiguous, and also orders checks from most-common (div by 4 — eliminates 75% of years immediately) to least-common (div by 400), which is slightly better for short-circuit evaluation. Explicit > implicit for boolean logic.

Tutor: Which expression structure would you go with?

### Student

I'd go with **B**.

Here's my reasoning: Even though option A is correct (Python's `or` and `and` precedence will evaluate it right), option B is much clearer to read. When I look at option B, I can immediately understand the logic: "divisible by 4 AND (not a century year OR divisible by 400)."

Option A requires me to mentally parse the precedence rules to understand what's actually happening. Since this is a small function that future maintainers (including future me!) will read, I'd rather have the explicit parentheses make the intent obvious.

Plus, the way B is structured mirrors how I'd explain the rule in words, which feels natural.

---

## Turn 2

### Tutor

Thinking: The user picked option B, which is my preference. I should express brief agreement and apply the changes (write the file).

Tutor: Exactly right — and you've nailed the key principle: **code is read far more often than it's written**. When the parentheses map directly to how you'd explain the rule in English, that's a strong signal you've got the right structure.

Let me write the file:

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

  File created successfully at: leap.py

Tutor: Done. One line, no ambiguity. 

Worth knowing: `and` *does* bind tighter than `or` in Python (just like `*` > `+` in arithmetic), so Option A would have evaluated correctly — but as you said, forcing a reader to recall that rule is a tax on every future read. Parentheses are free.

### Student

That makes total sense. I appreciate you pointing out that `and` does bind tighter than `or` — I didn't want to assume the precedence rules, so the explicit parentheses felt like the safer choice anyway. Now I know I was right for the right reason.

Let me verify the logic works by tracing through a couple test cases in my head:
- Year 2000: `2000 % 4 == 0` ✓, and `(2000 % 100 != 0 or 2000 % 400 == 0)` → `(False or True)` = True → result: True ✓
- Year 1900: `1900 % 4 == 0` ✓, and `(1900 % 100 != 0 or 1900 % 400 == 0)` → `(False or False)` = False → result: False ✓
- Year 2004: `2004 % 4 == 0` ✓, and `(2004 % 100 != 0 or ...)` → `(True or ...)` = True → result: True ✓
- Year 2001: `2001 % 4 == 0` ✗ → result: False ✓

Looks good. I've got a solid, readable solution that handles all the cases.

<done/>

---

**Run end:** done after 2 turn(s) in 40.6s
