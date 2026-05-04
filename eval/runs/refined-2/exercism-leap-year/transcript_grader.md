# exercism-leap-year

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:23:43

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

Tutor: Good small problem — but it has a nice boolean structure question worth pausing on. Let me present the core expression choice.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

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

Tutor: Which expression structure would you go with?

### Student

I'd go with **B**.

Here's my reasoning: Even though option A is correct (Python's `or` and `and` precedence will evaluate it right), option B is much clearer to read. When I look at option B, I can immediately understand the logic: "divisible by 4 AND (not a century year OR divisible by 400)."

Option A requires me to mentally parse the precedence rules to understand what's actually happening. Since this is a small function that future maintainers (including future me!) will read, I'd rather have the explicit parentheses make the intent obvious.

Plus, the way B is structured mirrors how I'd explain the rule in words, which feels natural.

---

## Turn 2

### Tutor

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
