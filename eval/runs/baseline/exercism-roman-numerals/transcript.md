# exercism-roman-numerals

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:51:12

## Initial prompt

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

---

## Turn 1

### Tutor

Thinking: The user wants me to write a `to_roman(n)` function that converts an integer to a Roman numeral string, using subtractive notation.
  
  Let me write a clean implementation using a lookup table approach.

[Glob(**/*.py)]
  No files found

Tutor: No existing files — I'll create the solution from scratch.

[Write(/roman_numerals.py)]
"""Convert an integer (1–3999) to a Roman numeral string."""

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
… (19 more lines)
  error: EROFS: read-only file system, open '/roman_numerals.py'

[Bash(ls /tmp)]
  acronym.py
  allergies_options.json
  allergies-test
  bun-extract
  bun-node-bf2e2cecf
  bun.zip
  caesar.py
  capture_claude.py
  capture_edit_diff.py
  cc_capture.bin
  cc_capture.py
  cc-inspect
  … (93 more lines)

Thinking: There's already a `roman_numerals.py` in `/tmp`. Let me read it first, then write my solution there.

Tutor: There's already a `/tmp/roman_numerals.py`. Let me read it first, then write the solution.

[Read(/tmp/roman_numerals.py)]
  1	NUMERALS = [
  2	    (1000, "M"),
  3	    ( 900, "CM"),
  4	    ( 500, "D"),
  5	    ( 400, "CD"),
  6	    ( 100, "C"),
  7	    (  90, "XC"),
  8	    (  50, "L"),
  9	    (  40, "XL"),
  10	    (  10, "X"),
  11	    (   9, "IX"),
  12	    (   5, "V"),
  … (12 more lines)

Thinking: There's already a solution. Let me improve it slightly — use `divmod` for cleaner code and add input validation. I'll also make the lookup table private with underscore prefix.

Tutor: There's an existing stub. I'll improve it — use `divmod` (avoids the `while` loop), make the table private, and add input validation:

[Write(/tmp/roman_numerals.py)]
"""Convert an integer (1–3999) to a Roman numeral string."""

# Ordered from largest to smallest, subtractive pairs included.
_NUMERALS = [
    (1000, "M"),
    ( 900, "CM"),
    ( 500, "D"),
    ( 400, "CD"),
    ( 100, "C"),
    (  90, "XC"),
    (  50, "L"),
    (  40, "XL"),
… (20 more lines)
  The file /tmp/roman_numerals.py has been updated successfully.

Tutor: Now let's verify with a broad set of test cases:

[Bash(python3 - <<'EOF'
from tmp.roman_numerals import to_roman   # absolute path import trick
EOF
python3 /tmp/roman_numerals.py 2>/dev/null; python3 -c "
import sys; sys.path.insert(0, '/tmp')
from roman_numerals import to_roman

cases = [
    (1,    'I'),
    (2,    'II'),
    (3,    'III'),
    (4,    'IV'),      # subtractive
    (5,    'V'),
    (9,    'IX'),      # subtractive
    (14,   'XIV'),
    (40,   'XL'),      # subtractive
    (49,   'XLIX'),
    (90,   'XC'),      # subtractive
    (399,  'CCCXCIX'),
    (400,  'CD'),      # subtractive
    (900,  'CM'),      # subtractive
    (1994, 'MCMXCIV'),
    (2024, 'MMXXIV'),
    (3999, 'MMMCMXCIX'),
]

all_ok = True
for n, expected in cases:
    got = to_roman(n)
    status = '✓' if got == expected else '✗'
    if got != expected:
        all_ok = False
    print(f'  {status}  to_roman({n:4d}) = {got!r:15s}  (expected {expected!r})')

# Boundary / error checks
try:
    to_roman(0)
    print('  ✗  to_roman(0) should raise ValueError')
    all_ok = False
except ValueError:
    print('  ✓  to_roman(0) raises ValueError')

try:
    to_roman(4000)
    print('  ✗  to_roman(4000) should raise ValueError')
    all_ok = False
except ValueError:
    print('  ✓  to_roman(4000) raises ValueError')

print()
print('All tests passed!' if all_ok else 'SOME TESTS FAILED')
"
)]
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  ModuleNotFoundError: No module named 'tmp'
    ✓  to_roman(   1) = 'I'              (expected 'I')
    ✓  to_roman(   2) = 'II'             (expected 'II')
    ✓  to_roman(   3) = 'III'            (expected 'III')
    ✓  to_roman(   4) = 'IV'             (expected 'IV')
    ✓  to_roman(   5) = 'V'              (expected 'V')
    ✓  to_roman(   9) = 'IX'             (expected 'IX')
    ✓  to_roman(  14) = 'XIV'            (expected 'XIV')
    ✓  to_roman(  40) = 'XL'             (expected 'XL')
    ✓  to_roman(  49) = 'XLIX'           (expected 'XLIX')
  … (11 more lines)

Tutor: All 18 tests pass. Here's the final solution:

```python
"""Convert an integer (1–3999) to a Roman numeral string."""

# Ordered from largest to smallest, subtractive pairs included.
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
    (   4, "IV"),
    (   1, "I"),
]


def to_roman(n: int) -> str:
    """Return the Roman numeral representation of n (1 ≤ n ≤ 3999)."""
    if not 1 <= n <= 3999:
        raise ValueError(f"n must be between 1 and 3999, got {n}")

    parts = []
    for value, numeral in _NUMERALS:
        count, n = divmod(n, value)
        parts.append(numeral * count)   # appends "" when count == 0

    return "".join(parts)
```

---

### How it works

**The key insight** is that all subtractive pairs (`IV`, `IX`, `XL`, `XC`, `CD`, `CM`) are treated as first-class entries in the lookup table, ordered by descending value alongside the additive symbols:

| Value | Symbol | Notes |
|------:|--------|-------|
| 1000 | `M` | |
| 900 | `CM` | subtractive |
| 500 | `D` | |
| 400 | `CD` | subtractive |
| … | … | |
| 4 | `IV` | subtractive |
| 1 | `I` | |

**The algorithm** — one pass through the table:
1. `divmod(n, value)` gives `count` (how many times this symbol fits) and the new remainder `n`.
2. `numeral * count` repeats the symbol — e.g. `"M" * 3 → "MMM"`.
3. When `n` is exhausted, all remaining `count`s are 0 and append `""`.
4. `"".join(parts)` assembles the final string.

Since every subtractive form is listed *before* its components (900 before 500/100, 4 before 5/1, etc.), they are consumed first whenever they fit — no special-casing needed.

### Student

Thanks for walking through that! I can see how treating the subtractive pairs as entries in the lookup table is much cleaner than trying to handle them separately. The `divmod` approach is elegant too — it avoids a `while` loop and keeps the logic really straightforward.

Let me make sure I understand the flow by tracing through one example. For `to_roman(49)`:
- `49 ÷ 1000` → count=0, remainder=49 → append `""` 
- `49 ÷ 900` → count=0, remainder=49 → append `""`
- ... (skip ahead)
- `49 ÷ 40` → count=1, remainder=9 → append `"XL"`
- `9 ÷ 10` → count=0, remainder=9 → append `""`
- `9 ÷ 9` → count=1, remainder=0 → append `"IX"`
- `0 ÷ 5` → count=0, remainder=0 → append `""`
- Final: `"XLIX"` ✓

That makes sense. And the input validation at the top catches anything outside 1–3999. All the test cases pass, including boundary cases and error conditions.

This solution feels complete and well-tested. I'm happy with how it turned out!

<done/>

---

**Run end:** done after 1 turn(s) in 39.4s
