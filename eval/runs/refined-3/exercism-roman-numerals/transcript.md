# exercism-roman-numerals

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:21

## Initial prompt

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

---

## Turn 1

### Tutor

Thinking: The user wants to implement a `to_roman(n)` function for converting integers to Roman numerals. This is a classic problem with a clean greedy solution. Let me think about the best approach and present it as an options question.
  
  The key decision is how to structure the mapping. There are two main approaches:
  
  1. **Greedy with ordered list** - Keep a list of (value, symbol) pairs in descending order, including all subtractive pairs (CM, CD, XC, XL, IX, IV), then greedily subtract and append.
  
  2. **Digit-by-digit approach** - Handle thousands, hundreds, tens, and ones separately with lookup tables.
  
  
  The greedy approach with the ordered list is the standard clean solution, and the real insight is whether to include the subtractive forms like IV and IX directly in the lookup table or handle them as special cases. Including them in the ordered list makes the algorithm beautifully simple—you just iterate through and greedily subtract the largest possible value each time.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me present the first key design decision: how to handle the subtractive notation in the algorithm. The core question is whether to include the subtractive pairs (IV, IX, XL, XC, CD, CM) directly in the lookup table as first-class entries, or to try to handle them with special-case logic.

OPTIONS:
[A] Greedy with flat table
Build one ordered list of `(value, symbol)` pairs — including subtractive forms like `(900, "CM")`, `(400, "CD")`, `(4, "IV")`, etc. — then greedily subtract and accumulate. No special-casing needed.

[B] Digit-by-digit lookup
Split `n` into thousands/hundreds/tens/ones digits, then index into four separate lookup tables (one per place value). Each table is a 10-element list covering `""` through the full symbol for that place.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=The greedy flat-table approach is the canonical, elegant solution. By treating subtractive pairs as first-class entries (e.g. 900→"CM"), the single loop handles all cases uniformly with no branching. The digit-by-digit approach works but requires four separate lookup tables and ties the implementation to base-10 structure, making it harder to extend or understand. The greedy approach is both simpler and more general.

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

Thinking: The user picked option A, which is my preferred option. Let me write the code. First, let me check if a file already exists.

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

PRIVATE: best=A
PRIVATE: rationale=Both produce correct output. The `parts` list + `"".join()` pattern is preferable in Python because string concatenation (`result += symbol`) creates a new string object on each iteration — O(k²) in the number of symbols appended. `list.append` + `join` is O(k). For Roman numerals the strings are tiny (max ~15 chars) so it makes no practical difference here, but the join pattern is idiomatic Python and builds the right habit. Worth noting as a teaching moment.

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

Thinking: The user picked option A, which is my preferred option. They also gave a good explanation of why. Let me write the file now.

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

PRIVATE: best=A
PRIVATE: rationale=Both are correct and the performance difference is negligible. However, `divmod` produces `symbol * count` which creates an intermediate string (e.g. "MMM"), then that gets joined — slightly more allocation. The `while` loop appends single-char strings incrementally, which join handles efficiently. More importantly, the `while` loop is idiomatic for this greedy pattern and slightly clearer in intent. The `divmod` version is a neat trick but not obviously better — it's worth presenting as a question about whether "clever" == "better".

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
