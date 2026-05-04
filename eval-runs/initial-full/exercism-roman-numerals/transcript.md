# exercism-roman-numerals

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:47:21.263Z

---

## Turn 1

**User:**

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

**Pair:**

Assistant: Good exercise. One key design question before we write anything:

OPTIONS:
[A] Dict lookup table
```diff
+++ roman_numerals.py
@@ -0,0 +1,12 @@
+def to_roman(n):
+    table = {
+        1000:'M', 900:'CM', 500:'D', 400:'CD',
+        100:'C',  90:'XC', 50:'L',  40:'XL',
+        10:'X',   9:'IX',  5:'V',   4:'IV', 1:'I',
+    }
+    result = ''
+    for val, sym in table.items():
+        while n >= val:
+            result += sym
+            n -= val
+    return result
```

[B] List-of-tuples table
```diff
+++ roman_numerals.py
@@ -0,0 +1,12 @@
+def to_roman(n):
+    table = [
+        (1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),
+        (100,'C'), (90,'XC'),(50,'L'), (40,'XL'),
+        (10,'X'),  (9,'IX'), (5,'V'),  (4,'IV'),(1,'I'),
+    ]
+    result = ''
+    result = ''
+    for val, sym in table:
+        while n >= val:
+            result += sym
+            n -= val
+    return result
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which structure would you reach for to hold the value→symbol mapping?

---

## Turn 2

**User:**

I'll pick **A**.

Option B has a bug—there's a duplicate `result = ''` assignment on lines 7 and 8. That's a red flag.

Option A is cleaner too. Dicts in Python 3.7+ maintain insertion order, so iterating over the dict written with values in descending order will work correctly for the greedy algorithm.

**Pair:**

Assistant: Fair catch on the duplicate — that was a typo on my end, not the intended trap. Sorry for the noise.

The real reason I'd reach for the list-of-tuples: a `dict` is semantically a *mapping*, not an ordered sequence. The ordering here is **load-bearing** — swap any two entries and the algorithm breaks. A `list` of tuples makes that explicit. A reader seeing `table.items()` has to know that CPython 3.7+ preserves insertion order to trust the code; a reader seeing `for val, sym in table:` immediately understands it's an ordered traversal.

That said — you're right it works perfectly in modern Python, and some people find the dict literal visually cleaner. Want to go with the dict, or switch to list-of-tuples?

---

## Turn 3

**User:**

You're right — I see the point. The ordering is **semantically critical** to the algorithm working, and a list of tuples makes that constraint visible in the code structure itself, not buried behind "we rely on dict insertion order."

Switch to **list-of-tuples (B)**, but let's fix the duplicate `result = ''` while we're at it.

**Pair:**

[Glob(roman_numerals.py)]
  No files found

[Write(roman_numerals.py)]
def to_roman(n):
    table = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'),  (90, 'XC'), (50, 'L'),  (40, 'XL'),
        (10,  'X'),  (9,  'IX'), (5,  'V'),  (4,  'IV'), (1, 'I'),
    ]
    result = ''
    for val, sym in table:
        while n >= val:
            result += sym
            n -= val
    return result
… (1 more lines)

Assistant: Clean. Let's verify it on a few cases that exercise the tricky paths:

[Bash(python3 -c "
from roman_numerals import to_roman
cases = [(1,'I'),(4,'IV'),(9,'IX'),(14,'XIV'),(40,'XL'),(90,'XC'),
         (399,'CCCXCIX'),(400,'CD'),(900,'CM'),(1994,'MCMXCIV'),(3999,'MMMCMXCIX')]
for n, expected in cases:
    got = to_roman(n)
    status = '✓' if got == expected else f'✗ expected {expected}'
    print(f'{n:>5} → {got:<12} {status}')
"
)]
  1 → I            ✓
      4 → IV           ✓
      9 → IX           ✓
     14 → XIV          ✓
     40 → XL           ✓
     90 → XC           ✓
    399 → CCCXCIX      ✓
    400 → CD           ✓
    900 → CM           ✓
   1994 → MCMXCIV      ✓
   3999 → MMMCMXCIX    ✓

Assistant: All green. The alignment in the table is a nice touch — makes the 13-entry structure scannable at a glance, so a future reader can immediately see the pattern of (value, value−next\_magnitude) pairs for each symbol tier.

---

## Turn 4 (final)

**User:**

Looks good. The solution is working correctly across all the critical test cases—basic numerals, all six subtractive pairs, and the edge cases at both ends of the range.

The code is clean, the table structure is explicit about its ordering constraint, and the greedy algorithm (repeatedly subtracting the largest remaining value) correctly handles the full 1–3999 range with subtractive notation.

<done/>

---

**Run end**: done after 3 turns (161s)
