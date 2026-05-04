# exercism-leap-year

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:50:36

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

[Glob(**/leap/**)]
  No files found

Tutor: No existing files, so I'll create the solution from scratch:

[Write(/leap/leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

  error: EROFS: read-only file system, mkdir '/leap'

[Bash(find . -name "leap.py" 2>/dev/null | head -5)]
  (Bash completed with no output)

Tutor: Here's the solution — one clean, idiomatic line:

```python
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

---

### How the logic works

The rule breaks into two parts, combined with `and`:

| Condition | Meaning |
|---|---|
| `year % 4 == 0` | Must be divisible by 4 (necessary condition) |
| `year % 100 != 0` | **Not** a century year → done, it's a leap year |
| `year % 400 == 0` | **Is** a century year but also divisible by 400 → still a leap year |

The `or` short-circuits: if it's not a century year we stop; only century years need the extra `% 400` check.

---

### Test cases to verify

| Year | Divisible by 4 | Century? | Div by 400? | Leap? |
|------|---------------|----------|-------------|-------|
| 1900 | ✅ | ✅ | ❌ | **No** |
| 2000 | ✅ | ✅ | ✅ | **Yes** |
| 2024 | ✅ | ❌ | — | **Yes** |
| 2023 | ❌ | — | — | **No** |

### Student

Thanks for walking through the logic! I think I understand the structure now. Let me trace through one example to make sure I've got it:

For **1900**:
- `1900 % 4 == 0` → true (divisible by 4) ✓
- `1900 % 100 != 0` → false (it *is* a century year, so this part fails)
- Since the first part is true but the `or` needs to evaluate the right side (because left is false), we check `1900 % 400 == 0` → false
- So overall: `true and (false or false)` = `true and false` = **false** ✓

And for **2000**:
- `2000 % 4 == 0` → true ✓
- `2000 % 100 != 0` → false (it's a century year)
- `2000 % 400 == 0` → true (divisible by 400)
- So: `true and (false or true)` = `true and true` = **true** ✓

That makes sense! The parentheses around `(year % 100 != 0 or year % 400 == 0)` are key—they let us handle the special century-year case before returning true.

Is the solution ready to submit, or do we need to test it against any actual test cases?

---

## Turn 2

### Tutor

Tutor: Your trace is **perfect** — you've got it exactly right!

The solution is ready to submit as-is. It's the idiomatic Python approach and handles all four cases Exercism tests:

- **Divisible by 4, not a century year** → leap (e.g. 2024)
- **Century year, not divisible by 400** → not leap (e.g. 1900)
- **Divisible by 400** → leap (e.g. 2000)
- **Not divisible by 4 at all** → not leap (e.g. 2023) — fails the very first check and short-circuits immediately

One small clarification on your trace — the parentheses aren't strictly *necessary* (operator precedence would actually evaluate it correctly without them), but they're worth keeping because they make the intent immediately readable: *"divisible by 4, AND passes the century-year check."*

Go ahead and submit! 🎯

### Student

Perfect, thanks for the clarification on operator precedence! I appreciate you pointing out that the parentheses are more about readability than necessity—that's a good habit to develop early.

I feel confident about the solution now. The logic is clear, it handles all four cases, and I understand *why* each part is there. I'm ready to move on.

<done/>

---

**Run end:** done after 2 turn(s) in 26.3s
