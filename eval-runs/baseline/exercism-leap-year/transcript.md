# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:27:50.761Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

Assistant: ```python
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

The logic in one line, reading left-to-right through the rules:

| Condition | Meaning |
|---|---|
| `year % 4 == 0` | Must be divisible by 4 (necessary condition) |
| `year % 100 != 0` | **Not** a century year → done, it's a leap year |
| `year % 400 == 0` | Century year redeemed by being divisible by 400 |

**Key test cases:**

```python
is_leap_year(2000)  # True  — divisible by 400
is_leap_year(1900)  # False — century, not divisible by 400
is_leap_year(2024)  # True  — divisible by 4, not a century
is_leap_year(2023)  # False — not divisible by 4
```

The `or` short-circuits: if `% 100 != 0` is true, Python never evaluates `% 400 == 0`, so it's efficient too.

---

## Turn 2 (final)

**User:**

Perfect! The solution is complete and correct. Here's what makes it work:

**The logic:**
- `year % 4 == 0` checks the base rule (must be divisible by 4)
- `(year % 100 != 0 or year % 400 == 0)` handles the exception:
  - If it's **not** a century year (`% 100 != 0`), we're done ✓
  - If it **is** a century year, it must be divisible by 400 (`% 400 == 0`) ✓

**Why this order matters:**
The first condition (`% 4 == 0`) acts as a gatekeeper. If it's false, the entire expression is false—no need to check the second part. This means non-leap years are rejected immediately without extra modulo operations.

**All cases covered:**
- ✅ 2024: divisible by 4, not century → True
- ✅ 2000: divisible by 4, century but also divisible by 400 → True
- ❌ 1900: divisible by 4, century, not divisible by 400 → False
- ❌ 2023: not divisible by 4 → False

The solution is clean, efficient, and passes all Exercism tests.

<done/>

---

**Run end**: done after 1 turn (18s)
