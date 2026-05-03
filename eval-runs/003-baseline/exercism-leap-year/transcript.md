# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-02T23:15:40.748Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

Assistant: ```python
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

**How it works:**

The three rules collapse into one expression:

| Condition | Leap? |
|-----------|-------|
| Not divisible by 4 | No |
| Divisible by 4, not by 100 | **Yes** |
| Divisible by 100, not by 400 | No (century exception) |
| Divisible by 400 | **Yes** (overrides century exception) |

Reading the expression left-to-right:
1. `year % 4 == 0` — must pass the basic test first
2. `year % 100 != 0` — if it's *not* a century year, done — it's a leap year
3. `or year % 400 == 0` — if it *is* a century year, it still qualifies if divisible by 400

Quick sanity checks:
- `2000` → 400 ✓ → **leap**
- `1900` → 4 ✓, 100 ✓, 400 ✗ → **not leap**
- `2024` → 4 ✓, 100 ✗ → **leap**
- `2023` → 4 ✗ → **not leap**

---

## Turn 2 (final)

**User:**

That solution is correct and clean. The logic maps perfectly to the leap year rules:
- base divisibility by 4 ✓
- exception for century years (the `year % 100 != 0 or year % 400 == 0` part) ✓

I traced through the test cases you showed—2000, 1900, 2024, 2023—and they all work. The explanation's also helpful for understanding why that one-liner actually handles all three cases.

<done/>

---

**Run end**: done after 1 turn (26s)
