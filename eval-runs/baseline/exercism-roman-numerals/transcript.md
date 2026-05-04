# exercism-roman-numerals

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:29:29.846Z

---

## Turn 1

**User:**

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

**Pair:**

[Glob(**/*.py)]
  No files found

Assistant: No existing file — I'll create it from scratch.

[Write(/roman_numerals.py)]
_NUMERALS = [
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
… (17 more lines)

[Bash(ls ~/)]
  Applications
  caesar_cipher.py
  Desktop
  dev
  Documents
  Downloads
  euler10.py
  evaluator.py
  exercism
  Library
  Movies
  Music
  … (5 more lines)

[Bash(ls ~/exercism/)]
  pangram

[Write(/Users/ozan/exercism/roman-numerals/roman_numerals.py)]
_NUMERALS = [
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
… (17 more lines)

[Bash(echo $HOME && mkdir -p "$HOME/exercism/roman-numerals")]
  /Users/oz

[Write(/Users/oz/exercism/roman-numerals/roman_numerals.py)]
_NUMERALS = [
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
… (17 more lines)

Assistant: Let me verify it works correctly against a range of interesting cases:

[Bash(python3 - <<'EOF'
import sys
sys.path.insert(0, "/Users/oz/exercism/roman-numerals")
from roman_numerals import to_roman

cases = [
    (1,    "I"),
    (4,    "IV"),
    (9,    "IX"),
    (14,   "XIV"),
    (40,   "XL"),
    (90,   "XC"),
    (399,  "CCCXCIX"),
    (400,  "CD"),
    (900,  "CM"),
    (1994, "MCMXCIV"),
    (2024, "MMXXIV"),
    (3999, "MMMCMXCIX"),
]

all_pass = True
for n, expected in cases:
    got = to_roman(n)
    status = "✓" if got == expected else "✗"
    if got != expected:
        all_pass = False
    print(f"  {status}  to_roman({n:>4}) = {got:<15}  (expected {expected})")

print()
print("All tests passed!" if all_pass else "FAILURES ABOVE ^^")
EOF
)]
  ✓  to_roman(   1) = I                (expected I)
    ✓  to_roman(   4) = IV               (expected IV)
    ✓  to_roman(   9) = IX               (expected IX)
    ✓  to_roman(  14) = XIV              (expected XIV)
    ✓  to_roman(  40) = XL               (expected XL)
    ✓  to_roman(  90) = XC               (expected XC)
    ✓  to_roman( 399) = CCCXCIX          (expected CCCXCIX)
    ✓  to_roman( 400) = CD               (expected CD)
    ✓  to_roman( 900) = CM               (expected CM)
    ✓  to_roman(1994) = MCMXCIV          (expected MCMXCIV)
    ✓  to_roman(2024) = MMXXIV           (expected MMXXIV)
    ✓  to_roman(3999) = MMMCMXCIX        (expected MMMCMXCIX)
  … (2 more lines)

Assistant: All 12 tests pass. Here's the solution at `~/exercism/roman-numerals/roman_numerals.py`:

---

### How it works

The core idea is a **greedy descent** through a lookup table that lists every value you'd ever want to "emit" — including all six subtractive pairs — in descending order:

```
1000 M | 900 CM | 500 D | 400 CD
 100 C |  90 XC |  50 L |  40 XL
  10 X |   9 IX |   5 V |   4 IV | 1 I
```

For each `(value, symbol)` pair, repeatedly subtract `value` from `n` and append `symbol` while `n ≥ value`. Because 900/400/90/40/9/4 are in the table as first-class entries, the subtractive forms fall out automatically — no special-casing needed.

**Example — 1994:**
| Step | n remaining | emits |
|------|-------------|-------|
| 1000 | 994 | `M` |
| 900 | 94 | `CM` |
| 90 | 4 | `XC` |
| 4 | 0 | `IV` |

→ **MCMXCIV** ✓

---

## Turn 2 (final)

**User:**

Perfect! Your solution is complete and thoroughly tested. All 12 test cases pass, including:
- Edge cases (1, 4, 9)
- Subtractive pairs in all positions (XL, XC, CD, CM)
- Complex numbers (1994, 3999)

The algorithm is elegant — by treating subtractive pairs (like 900 for "CM") as first-class entries in the value table, you avoid any special-case logic while ensuring correct subtractive notation everywhere it's needed.

You're ready to submit this to Exercism! 

<done/>

---

**Run end**: done after 1 turn (45s)
