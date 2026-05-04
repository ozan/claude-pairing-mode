# exercism-roman-numerals

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:53:12.448Z

---

## Turn 1

**User:**

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

**Pair:**

Thinking: The user wants to implement a `to_roman(n)` function that converts integers to Roman numerals with subtractive notation. This is a classic problem with a clean elegant solution. Let me think about the best approach.
  
  The key insight is: you can define a lookup table of value→symbol pairs (including the subtractive combinations), then greedily subtract the largest value that fits.
  
  The two main approaches are:
  1. A greedy algorithm with a table of (value, symbol) pairs sorted descending
  2. Digit-by-digit lookup tables for thousands, hundreds, tens, ones
  
  
  The greedy approach with a single sorted table is more elegant and generalizable, while the digit-by-digit method requires maintaining four separate lookup arrays. I think the greedy descent approach makes for a better teaching moment—it's the kind of algorithm that feels clever once you see it.
  
  Let me check if there's already a file to work with before I start building this out.

[Glob(roman_numerals*)]
  No files found

Assistant: Good, blank slate. Before writing any code, here's a core design question:

Thinking: The tool isn't available. Let me just implement the solution directly. I'll go with the greedy descent approach as it's the better one.

Assistant: The pairing tool isn't available right now, so I'll just build it — and explain the key design choice as we go.

The cleanest approach is **greedy descent**: define all 13 value→symbol pairs (including the 6 subtractive ones) in descending order, then greedily subtract. One algorithm, no special-casing.

The alternative — four digit-by-digit lookup tables — also works, but requires manually enumerating 40 strings and doesn't generalise.

[Write(roman_numerals.py)]
# All 13 value→symbol pairs in descending order.
# Subtractive forms (CM, CD, XC, XL, IX, IV) sit naturally alongside additive ones.
VALUES = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100,  'C'), (90,  'XC'), (50,  'L'), (40,  'XL'),
    (10,   'X'), (9,   'IX'), (5,   'V'), (4,   'IV'),
    (1,    'I'),
]


def to_roman(n: int) -> str:
    """Convert an integer 1–3999 to a Roman numeral string."""
… (19 more lines)

[Bash(python roman_numerals.py)]
  error: Exit code 127

[Bash(python3 roman_numerals.py)]
  1 → I            ✓
     4 → IV           ✓
     9 → IX           ✓
    14 → XIV          ✓
    40 → XL           ✓
    58 → LVIII        ✓
    90 → XC           ✓
   399 → CCCXCIX      ✓
   400 → CD           ✓
   900 → CM           ✓
  1994 → MCMXCIV      ✓
  3999 → MMMCMXCIX    ✓

Assistant: All 12 test cases pass. A few things worth noting:

**Why greedy works here** — the subtractive pairs (`CM`, `CD`, `XC`, `XL`, `IX`, `IV`) are just values like any other. By inserting them at their correct positions in the descending list, the algorithm handles them with zero extra logic. For example, with `n=1994`: it takes `M` (994 left), then `CM` (94 left), then `XC` (4 left), then `IV` → `MCMXCIV`.

**Why the `while` loop, not `if`?** — it lets the same entry handle repeated symbols: `n=3` takes `I` three times in a row. If you used `if`, you'd need entries for `II` and `III` too.

**Quick quiz**: what's the time complexity of `to_roman(n)`? Is it O(n) or O(log n) or O(1)?

---

## Turn 2 (final)

**User:**

Oh, that's a clever question! Let me think through it...

The outer `for` loop runs 13 times (fixed list size). For each value in the table, the `while n >= value` loop runs at most a constant number of times — the subtractive notation was designed to prevent repeating any symbol more than 3 times in a row. So even for `n=3999`, we're doing roughly a bounded number of iterations.

So it's **O(1)** — constant time! The algorithm doesn't scale with the *magnitude* of n; it's always a small fixed number of steps because the Roman numeral system itself caps how many of each symbol can appear.

That's a neat property I didn't fully appreciate until you asked. The greedy descent is elegant not just for code clarity, but because the problem's constraint (1–3999) and the notation rules guarantee it's always fast.

Is there anything else about the solution you'd like me to explore, or does this feel complete?

<done/>

---

**Run end**: done after 1 turn (48s)
