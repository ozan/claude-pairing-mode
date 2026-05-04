# exercism-roman-numerals

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:58:09.138Z

---

## Turn 1

**User:**

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

**Pair:**

Assistant: ## Roman Numerals

The classic **greedy subtraction** approach: build a table of every value you can "spend" (including the 6 subtractive pairs), then repeatedly peel off the largest one that fits.

[Write(/home/user/roman_numerals.py)]
NUMERALS = [
    (1000, "M"),
    ( 900, "CM"),
    ( 500, "D"),
    ( 400, "CD"),
    ( 100, "C"),
    (  90, "XC"),
    (  50, "L"),
    (  40, "XL"),
    (  10, "X"),
    (   9, "IX"),
    (   5, "V"),
… (12 more lines)

[Write(/tmp/roman_numerals.py)]
NUMERALS = [
    (1000, "M"),
    ( 900, "CM"),
    ( 500, "D"),
    ( 400, "CD"),
    ( 100, "C"),
    (  90, "XC"),
    (  50, "L"),
    (  40, "XL"),
    (  10, "X"),
    (   9, "IX"),
    (   5, "V"),
… (12 more lines)

[Bash(python3 -c "
from tmp.roman_numerals import to_roman
cases = [(1,'I'),(4,'IV'),(9,'IX'),(14,'XIV'),(40,'XL'),(90,'XC'),
         (399,'CCCXCIX'),(400,'CD'),(900,'CM'),(1999,'MCMXCIX'),(3999,'MMMCMXCIX')]
for n, expected in cases:
    got = to_roman(n)
    status = '✓' if got == expected else f'✗ expected {expected}'
    print(f'  {n:>5} → {got:<15} {status}')
" 2>/dev/null || python3 -c "
import sys; sys.path.insert(0, '/tmp')
from roman_numerals import to_roman
cases = [(1,'I'),(4,'IV'),(9,'IX'),(14,'XIV'),(40,'XL'),(90,'XC'),
         (399,'CCCXCIX'),(400,'CD'),(900,'CM'),(1999,'MCMXCIX'),(3999,'MMMCMXCIX')]
for n, expected in cases:
    got = to_roman(n)
    status = '✓' if got == expected else f'✗ expected {expected}'
    print(f'  {n:>5} -> {got:<15} {status}')
"
)]
  1 -> I               ✓
        4 -> IV              ✓
        9 -> IX              ✓
       14 -> XIV             ✓
       40 -> XL              ✓
       90 -> XC              ✓
      399 -> CCCXCIX         ✓
      400 -> CD              ✓
      900 -> CM              ✓
     1999 -> MCMXCIX         ✓
     3999 -> MMMCMXCIX       ✓

Assistant: All 11 cases pass. ✓

---

## How it works

```python
NUMERALS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    ( 100, "C"), ( 90, "XC"), ( 50, "L"), ( 40, "XL"),
    (  10, "X"), (  9, "IX"), (  5, "V"), (  4, "IV"), (1, "I"),
]

def to_roman(n: int) -> str:
    result = []
    for value, symbol in NUMERALS:
        while n >= value:
            result.append(symbol)
            n -= value
    return "".join(result)
```

**The table is the whole trick.** By including the 6 subtractive pairs (`IV 4`, `IX 9`, `XL 40`, `XC 90`, `CD 400`, `CM 900`) as first-class entries, the greedy loop handles them automatically — no special cases needed.

**Trace for 1999:**
| n remaining | largest fits | append |
|---|---|---|
| 1999 | 1000 "M" | M |
| 999 | 900 "CM" | CM |
| 99 | 90 "XC" | XC |
| 9 | 9 "IX" | IX |
| 0 | — done | — |

Result: **MCMXCIX** ✓

**Complexity:** O(1) — the table has 13 rows and the maximum output length is fixed (3999 = `MMMCMXCIX`, 9 chars).

---

## Turn 2 (final)

**User:**

Perfect! Your solution is complete and correct. The **greedy subtraction table** approach is elegant — by including all 6 subtractive pairs as first-class entries sorted by value, the loop handles them automatically without special cases.

All 11 test cases pass, including the edge cases:
- **1** → I (minimum)
- **4, 9, 40, 90, 400, 900** (subtractive pairs)
- **3999** → MMMCMXCIX (maximum)

The algorithm is O(1) time and space (fixed table, bounded output length), which is as efficient as it gets for this problem.

<done/>

---

**Run end**: done after 1 turn (31s)
