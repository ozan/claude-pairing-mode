# exercism-leap-year

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:04:54

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

Tutor: ```python
def is_leap_year(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
```

---

**How it works — three rules, evaluated in order:**

| Condition | Verdict | Example |
|---|---|---|
| `year % 400 == 0` | ✅ Leap | 2000 |
| `year % 100 == 0` (implied by the `!= 0` check) | ❌ Not leap | 1900 |
| `year % 4 == 0` | ✅ Leap | 2024 |
| anything else | ❌ Not leap | 2023 |

**The key insight** is short-circuit evaluation with `or` / `and`:

```
year % 400 == 0           →  true  ⇒ done (leap), skip rest
    OR
year % 4 == 0             →  true
    AND year % 100 != 0   →  true  ⇒ leap
                          →  false ⇒ not leap (century non-400)
```

**Quick sanity checks:**
```python
is_leap_year(2000)  # True  — divisible by 400
is_leap_year(1900)  # False — century but not ÷400
is_leap_year(2024)  # True  — divisible by 4, not a century
is_leap_year(2023)  # False — not divisible by 4
```

### Student

Thanks for walking me through this! I can see the logic now.

So the key is that we check the most restrictive rule first (`% 400 == 0`), and then handle the tricky case where a year is divisible by 100 but *not* by 400 (those are the non-leap centuries). The `year % 100 != 0` check screens those out before we apply the general "divisible by 4" rule.

Let me trace through one example to make sure I've got it:
- **2100**: `2100 % 400 = 300` (not 0, so first check fails) → `2100 % 4 = 0` (true) AND `2100 % 100 = 0` (so `!= 0` is false) → whole `and` expression is false → result is False ✓

And one more:
- **2020**: `2020 % 400 = 20` (not 0) → `2020 % 4 = 0` (true) AND `2020 % 100 = 20` (so `!= 0` is true) → whole `and` expression is true → result is True ✓

Got it. The solution is clean and the short-circuit evaluation makes it efficient. Thanks!

<done/>

---

**Run end:** done after 1 turn(s) in 12.7s
