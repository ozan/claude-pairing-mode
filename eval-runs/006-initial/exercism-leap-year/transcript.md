# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:51:24.950Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

Thinking: The user wants to implement a `is_leap_year(year)` function in Python for the Exercism 'Leap' exercise. This is a simple but classic problem. Let me think about the best approach and present a teaching moment.
  
  The leap year rules are:
  - Divisible by 4: leap year
  - EXCEPT century years (divisible by 100): NOT a leap year
  - UNLESS also divisible by 400: IS a leap year
  
  So the logic is: `(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)`
  
  Or equivalently: `year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)`
  
  
  I'm considering how to present this clearly—whether to show the concise boolean expression or walk through a more verbose if/elif/else structure. The interesting teaching angle here is probably around short-circuit evaluation and how the order of conditions affects readability and performance. I'm considering whether to present a comparison between the correct implementation and a subtly flawed version to make the lesson more interesting. Let me verify the logic of the incorrect option—without parentheses, the operator precedence means it evaluates as `(year % 4 == 0 and year % 100 != 0) or year % 400 == 0`, which actually handles the leap year rules correctly anyway since years divisible by 400 are caught by the second condition. I'm realizing the leap year logic with operator precedence is actually equivalent to the parenthesized version since 400 is divisible by 4. Let me try constructing a genuinely incorrect option by tweaking the logic slightly, though I'm finding that most variations end up being equivalent anyway. I'm comparing two correct implementations that differ in their efficiency through short-circuit evaluation—checking divisibility by 4 first eliminates about 75% of years immediately, making it more efficient than checking 400 first, which is a useful teaching point about operator ordering.

Assistant: Quick question before we write it — both expressions below are logically valid, but which would you prefer, and why?

OPTIONS:
[A] Check % 4 first
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

[B] Check % 400 first
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Both are correct — the difference is about **short-circuit evaluation efficiency**. Which do you pick?

---

## Turn 2

**User:**

Ah, I see it now — **I'd pick A**.

With option A, since about 75% of years aren't divisible by 4, we short-circuit and return False on the first check alone. Option B checks divisibility by 400 first, which is False almost all the time, so we'd end up evaluating the second condition most of the time anyway.

So option A is faster in the common case because most years fail the first test immediately. That makes sense.

Go with A?

**Pair:**

Thinking: The user picked option A, which is my preference. Let me agree briefly and write the file.

Assistant: Exactly right. Let's write it.

[Glob(leap.py)]
  No files found

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


Assistant: Done. The logic mirrors the rules in order of frequency:

1. **`% 4 != 0`** → not a leap year (exits ~75% of the time here)
2. **`% 100 != 0`** → is a leap year (ordinary 4-year cycles)
3. **`% 400 == 0`** → is a leap year (century exception)

---

## Turn 3 (final)

**User:**

Perfect—that makes total sense now. Thanks for walking me through the efficiency angle; I can see how short-circuit evaluation actually matters when you're writing code that'll run a lot. The condition ordering really does reflect how likely each case is, which is a neat way to think about it.

<done/>

---

**Run end**: done after 2 turns (49s)
