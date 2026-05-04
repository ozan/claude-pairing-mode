# exercism-roman-numerals

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:01:29

## Initial prompt

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good — let's start with the core algorithm decision:

OPTIONS:
[A] Per-digit lookup tables
```diff
+++ roman_numerals.py
@@ -0,0 +1,9 @@
+def to_roman(n):
+    thousands = ['', 'M', 'MM', 'MMM']
+    hundreds  = ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
+    tens      = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
+    ones      = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
+    return (thousands[n // 1000]
+          + hundreds[n % 1000 // 100]
+          + tens[n % 100 // 10]
+          + ones[n % 10])
```

[B] Greedy value table
```diff
+++ roman_numerals.py
@@ -0,0 +1,12 @@
+def to_roman(n):
+    table = [
+        (1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),
+        (100,'C'), (90,'XC'), (50,'L'), (40,'XL'),
+        (10,'X'),  (9,'IX'),  (5,'V'),  (4,'IV'),
+        (1,'I'),
+    ]
+    result = ''
+    for value, symbol in table:
+        while n >= value:
+            result += symbol
+            n -= value
+    return result
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to go with?

### Student

I think I'll go with **B** — the greedy value table approach.

My reasoning: option A is clever and efficient with the per-digit lookup, but I find option B more intuitive to understand at a glance. The table makes it really obvious what the subtractive pairs are (like 900→'CM', 400→'CD'), and the greedy algorithm is straightforward to follow: just repeatedly subtract the largest remaining value and append its symbol. It feels easier to verify correctness by reading through the logic.

Plus, if I need to debug or add test cases later, the table is easier to reason about than doing modular arithmetic on digit positions.

Let's go with B!

---

## Turn 2

### Tutor

Tutor: Exactly right — the table is self-documenting and the algorithm mirrors how you'd explain Roman numerals to someone. Let's write it.

[Glob(roman_numerals.py)]
  No files found

[Write(roman_numerals.py)]
def to_roman(n):
    table = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'),  (90, 'XC'),  (50, 'L'),  (40, 'XL'),
        (10,  'X'),  (9,  'IX'),  (5,  'V'),  (4,  'IV'),
        (1,   'I'),
    ]
    result = ''
    for value, symbol in table:
        while n >= value:
            result += symbol
            n -= value
… (2 more lines)
  File created successfully at: roman_numerals.py

Tutor: Done. Let's do a quick sanity check on the interesting edge cases:

[Bash(python3 -c "
from roman_numerals import to_roman
cases = [(1,'I'),(4,'IV'),(9,'IX'),(14,'XIV'),(40,'XL'),(90,'XC'),
         (399,'CCCXCIX'),(400,'CD'),(900,'CM'),(1994,'MCMXCIV'),(3999,'MMMCMXCIX')]
all_pass = True
for n, expected in cases:
    got = to_roman(n)
    status = '✓' if got == expected else f'✗ (got {got})'
    print(f'{n:>4} → {expected:<12} {status}')
    if got != expected:
        all_pass = False
print('All passed!' if all_pass else 'FAILURES above')
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
  All passed!

Tutor: All 11 cases pass, including the tricky chained subtractives like 1994 → `MCMXCIV` (M + CM + XC + IV).

One thing worth noting: the `while` loop (rather than `if`) is what handles repeated symbols — e.g. 3000 hits the `M` row three times. The table order guarantees you always take the largest possible chunk first, which is exactly the greedy property that makes correctness easy to prove: at each step you're not "missing" a bigger symbol because bigger ones were already exhausted.

### Student

That makes sense! I see why the `while` loop is crucial — it lets a single value like 1000 get used multiple times. So when we hit 3000, we keep subtracting 1000 and appending 'M' until `n < 1000`, which gives us 'MMM'. If we'd used `if` instead, we'd only get one 'M' and miss the rest.

And I really like how the table order guarantees the greedy property works. Since the values are in descending order, we always process the largest chunks first, so there's no way we could accidentally "waste" a smaller symbol and then find out we should've used a bigger one. The algorithm is correct by construction.

The 1994 → 'MCMXCIV' example is perfect — it clearly shows all the subtractive pairs working together: we get M (1000), then CM (900), then XC (90), then IV (4). Each step just peels off the next largest value.

I feel pretty confident about this solution. It's clear, correct, and handles all the edge cases including the subtractive notation. Thanks for walking through the algorithm choice and the test cases!

<done/>

---

**Run end:** done after 2 turn(s) in 52.9s
