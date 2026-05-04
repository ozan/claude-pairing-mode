# exercism-roman-numerals

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:21

## Initial prompt

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Greedy with flat table
Build one ordered list of `(value, symbol)` pairs — including subtractive forms like `(900, "CM")`, `(400, "CD")`, `(4, "IV")`, etc. — then greedily subtract and accumulate. No special-casing needed.

[B] Digit-by-digit lookup
Split `n` into thousands/hundreds/tens/ones digits, then index into four separate lookup tables (one per place value). Each table is a 10-element list covering `""` through the full symbol for that place.

(Reply with A or B, or ask a follow-up question.)

Tutor: Two ways to attack this — which feels cleaner to you?

**A: Greedy with flat table** — Build one ordered list of `(value, symbol)` pairs — including subtractive forms like `(900, "CM")`, `(400, "CD")`, `(4, "IV")`, etc. — then greedily subtract and accumulate. No special-casing needed.

**B: Digit-by-digit lookup** — Split `n` into thousands/hundreds/tens/ones digits, then index into four separate lookup tables (one per place value). Each table is a 10-element list covering `""` through the full symbol for that place.

### Student

I think I'll go with **A: Greedy with flat table**.

It seems more straightforward to me — I like that there's just one list to maintain, and the algorithm is simple: keep subtracting the largest value that fits and building up the roman numeral string. I don't have to think about splitting digits or managing four separate tables.

Plus, once I include all the subtractive forms in the right order, the greedy approach should just work without any special cases. Let me start coding that up.

---

## Turn 2

### Tutor

Tutor: Exactly right — including subtractive pairs as first-class entries is the key insight. Let me write the file.

[Glob(roman_numerals.py)]
  No files found

OPTIONS:
[A] Return joined string
```diff
+++ roman_numerals.py
@@ -0,0 +1,14 @@
+NUMERALS = [
+    (1000, "M"),  (900, "CM"), (500, "D"),  (400, "CD"),
+    (100,  "C"),  (90,  "XC"), (50,  "L"),  (40,  "XL"),
+    (10,   "X"),  (9,   "IX"), (5,   "V"),  (4,   "IV"),
+    (1,    "I"),
+]
+
+def to_roman(n):
+    parts = []
+    for value, symbol in NUMERALS:
+        while n >= value:
+            parts.append(symbol)
+            n -= value
+    return "".join(parts)
```

[B] Accumulate into string
```diff
+++ roman_numerals.py
@@ -0,0 +1,13 @@
+NUMERALS = [
+    (1000, "M"),  (900, "CM"), (500, "D"),  (400, "CD"),
+    (100,  "C"),  (90,  "XC"), (50,  "L"),  (40,  "XL"),
+    (10,   "X"),  (9,   "IX"), (5,   "V"),  (4,   "IV"),
+    (1,    "I"),
+]
+
+def to_roman(n):
+    result = ""
+    for value, symbol in NUMERALS:
+        while n >= value:
+            result += symbol
+            n -= value
+    return result
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Both are correct — but one is more idiomatic Python. Which accumulation style do you prefer?

**A: Return joined string** — Append symbols to a `parts` list, return `"".join(parts)` at the end.

**B: Accumulate into string** — Build the result with `result += symbol` directly in the loop, return `result`.

### Student

I'll go with **A: Return joined string**.

I know that in Python, string concatenation with `+=` can be inefficient because strings are immutable, so each `+=` creates a new string object. Using a list and `join()` at the end is the more idiomatic and performant approach, especially since we don't know how many iterations we'll have.

Let me code that up and test it.

---

## Turn 3

### Tutor

Tutor: Spot on. The O(k²) concern is real in general — good habit even when k is small.

[Write(roman_numerals.py)]
NUMERALS = [
    (1000, "M"),  (900, "CM"), (500, "D"),  (400, "CD"),
    (100,  "C"),  (90,  "XC"), (50,  "L"),  (40,  "XL"),
    (10,   "X"),  (9,   "IX"), (5,   "V"),  (4,   "IV"),
    (1,    "I"),
]

def to_roman(n):
    parts = []
    for value, symbol in NUMERALS:
        while n >= value:
            parts.append(symbol)
… (3 more lines)
  File created successfully at: roman_numerals.py

[Bash(python3 -c "
from roman_numerals import to_roman
cases = [(1,'I'),(4,'IV'),(9,'IX'),(14,'XIV'),(40,'XL'),(90,'XC'),
         (399,'CCCXCIX'),(400,'CD'),(900,'CM'),(1994,'MCMXCIV'),(3999,'MMMCMXCIX')]
for n, expected in cases:
    got = to_roman(n)
    status = '✓' if got == expected else f'✗ expected {expected}'
    print(f'{n:>5} → {got:<15} {status}')
"
)]
  1 → I               ✓
      4 → IV              ✓
      9 → IX              ✓
     14 → XIV             ✓
     40 → XL              ✓
     90 → XC              ✓
    399 → CCCXCIX         ✓
    400 → CD              ✓
    900 → CM              ✓
   1994 → MCMXCIV         ✓
   3999 → MMMCMXCIX       ✓

Tutor: All 11 cases pass, including the tricky subtractive boundaries.

One small thing worth thinking about — the `while` loop is doing repeated work for large values like `M`. For example, `to_roman(3000)` appends `"M"` three times via three `while` iterations.

OPTIONS:
[A] Keep the while loop
Leave it as-is. The `while` loop is simple, readable, and the total iterations are bounded — Roman numerals max out at ~15 symbols, so it never does meaningful work.

[B] Replace with divmod
```diff
+++ roman_numerals.py
@@ -9,5 +9,5 @@
 def to_roman(n):
     parts = []
     for value, symbol in NUMERALS:
-        while n >= value:
-            parts.append(symbol)
-            n -= value
+        count, n = divmod(n, value)
+        parts.append(symbol * count)
     return "".join(parts)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which version do you prefer — and does the `divmod` form actually buy us anything?

**A: Keep the while loop** — Leave it as-is. The `while` loop is simple, readable, and the total iterations are bounded — Roman numerals max out at ~15 symbols, so it never does meaningful work.

**B: Replace with divmod** — Replace the `while` with a single `divmod` call per entry, multiplying the symbol by the quotient.

### Student

I'll go with **A: Keep the while loop**.

You're right that the `while` loop is bounded and simple — Roman numerals max out at around 15 symbols total, so there's no real performance concern. The `while` version is also clearer to read: it directly expresses the logic "keep subtracting this value and appending this symbol until we can't anymore."

The `divmod` version is clever, but it adds a bit of cognitive overhead with the string multiplication. For a problem like this where clarity matters and performance isn't a bottleneck, I think the straightforward `while` loop wins.

The code is working perfectly on all the test cases, so I'm happy with it as-is.

<done/>

---

**Run end:** done after 3 turn(s) in 63.4s
