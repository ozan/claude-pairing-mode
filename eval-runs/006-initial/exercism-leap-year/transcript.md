# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:38:48.231Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

Assistant: The tool isn't available in this session, so I'll just pose the question directly.

Before writing the function — which of these would you use?

**Option A** — verbose, names each condition:
```python
def is_leap_year(year):
    divisible_by_4   = year % 4   == 0
    divisible_by_100 = year % 100 == 0
    divisible_by_400 = year % 400 == 0
    return divisible_by_4 and divisible_by_100 or divisible_by_400
```

**Option B** — single boolean expression:
```python
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

Which would you pick?

---

## Turn 2

**User:**

I'd pick **B**.

Option A looks cleaner with those named variables, but the logic is actually broken. Let me trace through a century year like 1900:
- `divisible_by_4 = True`, `divisible_by_100 = True`, `divisible_by_400 = False`
- Returns: `(True and True) or False` → `True` 

But 1900 is NOT a leap year (divisible by 100 but not by 400). Option A would incorrectly mark it as a leap year.

Option B correctly chains the conditions: first check divisibility by 4, then carve out the exception for century years (they need divisibility by 400). The logic is sound.

**Pair:**

Assistant: Exactly right — nice trace. `and` binds tighter than `or`, so Option A reads as `(divisible_by_4 and divisible_by_100) or divisible_by_400`, which incorrectly passes century years that aren't divisible by 400.

[Glob(leap.py)]
  No files found

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


Assistant: Done. The parentheses in `(year % 100 != 0 or year % 400 == 0)` are load-bearing — they keep the `or` from being swallowed by the outer `and`. One thing worth knowing: Python's operator precedence biting you there is exactly the kind of bug that passes a quick read but fails on edge cases like 1900. Good instinct to trace through a concrete example.

---

## Turn 3 (final)

**User:**

looks good — the logic is clean and handles all the cases correctly.

<done/>

---

**Run end**: done after 2 turns (92s)
