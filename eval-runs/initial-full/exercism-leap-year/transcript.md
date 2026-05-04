# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:39:21.713Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

Assistant: Good classic problem — and there's a subtle trap in how you write the boolean. Let me offer two implementations:

[Glob(leap.py)]
  No files found

Assistant: Which of these correctly implements the leap year rule?

**Option A**
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

**Option B**
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 or year % 400 == 0 and year % 100 != 0
```

Both use the same three conditions — which one is right, and why?

---

## Turn 2

**User:**

**Option A** is correct.

Here's why: operator precedence. In Option B, `and` binds tighter than `or`, so it's really:
```
year % 4 == 0  or  (year % 400 == 0 and year % 100 != 0)
```

That second part is a trap — it's actually impossible (no number divisible by 400 can avoid being divisible by 100). The real problem: Option B would incorrectly mark **1900 as a leap year** because it's divisible by 4, and the `or` short-circuits without ever checking the century rule.

Option A says it clearly: divisible by 4 **and** (not a century year **or** divisible by 400). That correctly excludes 1900.

Please choose **A**.

**Pair:**

Assistant: Exactly right — and nice catch that `year % 400 == 0 and year % 100 != 0` is a logical impossibility (vacuously never true), making Option B equivalent to just `year % 4 == 0`. 1900 is the canonical gotcha test case for this problem.

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


Assistant: Done. The logic reads cleanly in English too: "divisible by 4, and either not a century year or divisible by 400" — which matches the spec exactly.

Want to add tests for the edge cases (1900, 2000, 2024, etc.), or move on to the next Exercism problem?

---

## Turn 3

**User:**

Let's add tests — it's a good habit, and edge cases like 1900 and 2000 are exactly what can bite you if you don't verify. Plus it'll let us make sure the function actually works.

**Pair:**

[Glob(test_leap.py)]
  No files found

[Write(test_leap.py)]
import pytest
from leap import is_leap_year


@pytest.mark.parametrize("year, expected", [
    (1997, False),  # not divisible by 4
    (1996, True),   # divisible by 4, not a century year
    (1900, False),  # century year, not divisible by 400
    (2000, True),   # divisible by 400
    (2024, True),   # recent leap year
    (1800, False),  # another century non-leap
    (2100, False),  # future century non-leap
… (4 more lines)

[Bash(python -m pytest test_leap.py -v)]
  error: Exit code 127

[Bash(python3 -m pytest test_leap.py -v)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-leap-year-klC1YG
  collecting ... collected 7 items
  
  test_leap.py::test_is_leap_year[1997-False] PASSED                       [ 14%]
  test_leap.py::test_is_leap_year[1996-True] PASSED                        [ 28%]
  test_leap.py::test_is_leap_year[1900-False] PASSED                       [ 42%]
  test_leap.py::test_is_leap_year[2000-True] PASSED                        [ 57%]
  test_leap.py::test_is_leap_year[2024-True] PASSED                        [ 71%]
  test_leap.py::test_is_leap_year[1800-False] PASSED                       [ 85%]
  … (3 more lines)

Assistant: 7/7. All three families of cases covered: plain non-leap, plain leap, century non-leap (1900, 1800, 2100), and century leap (2000).

Using `@pytest.mark.parametrize` is worth noting — it keeps the test function DRY while still giving you a separate, named test case for each year in the output. When one fails, you know exactly which year broke.

---

## Turn 4 (final)

**User:**

Perfect — the test suite confirms the function handles all the key cases:

- **Non-leap**: 1997 ✓
- **Plain leap** (div by 4): 1996, 2024 ✓
- **Century trap** (div by 100 but not 400): 1900, 1800, 2100 ✓
- **Century leap** (div by 400): 2000 ✓

The function is bulletproof. You've got the rule locked down, and you've proven it works on the cases that actually trip people up.

<done/>

---

**Run end**: done after 3 turns (84s)
