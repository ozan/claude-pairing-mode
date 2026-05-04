# exercism-roman-numerals

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:24:46

## Initial prompt

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Greedy table lookup
Build one flat list of all 13 `(value, symbol)` pairs in descending order — including subtractive forms like `(9, 'IX')`, `(4, 'IV')`. Loop: while `n >= value`, append symbol and subtract value.

```diff
+++ roman_numerals.py
@@ -0,0 +1,14 @@
+NUMERALS = [
+    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
+    (100,  'C'), (90,  'XC'), (50,  'L'), (40,  'XL'),
+    (10,   'X'), (9,   'IX'), (5,   'V'), (4,   'IV'),
+    (1,    'I'),
+]
+
+def to_roman(n):
+    result = []
+    for value, symbol in NUMERALS:
+        while n >= value:
+            result.append(symbol)
+            n -= value
+    return ''.join(result)
```

[B] Digit-by-digit arrays
Decompose `n` into thousands/hundreds/tens/ones digits, each with its own lookup array. Subtractive forms are baked in per-position.

```diff
+++ roman_numerals.py
@@ -0,0 +1,14 @@
+T = ['','M','MM','MMM']
+H = ['','C','CC','CCC','CD','D','DC','DCC','DCCC','CM']
+X = ['','X','XX','XXX','XL','L','LX','LXX','LXXX','XC']
+O = ['','I','II','III','IV','V','VI','VII','VIII','IX']
+
+def to_roman(n):
+    return (T[n // 1000] +
+            H[n % 1000 // 100] +
+            X[n % 100  // 10] +
+            O[n % 10])
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you use?

### Student

I think I'd go with **A** — the greedy table lookup.

Here's my reasoning: Option A feels more straightforward to understand at first glance. I can see the list of value-symbol pairs right there, including the subtractive forms like `(9, 'IX')` and `(4, 'IV')`, and then the algorithm just greedily consumes from largest to smallest. It's easier to verify that I haven't missed a case.

Option B is clever — decomposing by digit position is efficient — but those pre-built arrays feel more like "magic" to me right now. I'd have to reason through why each position's array is constructed the way it is, and I'm less confident I could build them from scratch if I had to.

With A, if I got stuck or made a mistake, I think it'd be easier to debug because the logic is simpler. Should I go ahead and code it up?

---

## Turn 2

### Tutor

Tutor: Exactly right — and your debugging point is the real clincher. When the greedy loop produces the wrong output, you can `print(n)` after each step and watch it unwind. With the digit arrays you'd have to audit 40 hardcoded strings.

Let me write the file:

[Write(roman_numerals.py)]
NUMERALS = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100,  'C'), (90,  'XC'), (50,  'L'), (40,  'XL'),
    (10,   'X'), (9,   'IX'), (5,   'V'), (4,   'IV'),
    (1,    'I'),
]

def to_roman(n):
    result = []
    for value, symbol in NUMERALS:
        while n >= value:
            result.append(symbol)
… (3 more lines)
  File created successfully at: roman_numerals.py

Tutor: Now a small but interesting refinement — the inner `while` loop:

OPTIONS:
[A] Keep the while loop
```diff
+++ roman_numerals.py
@@ -9,4 +9,4 @@
     for value, symbol in NUMERALS:
         while n >= value:
             result.append(symbol)
             n -= value
```
Straightforward; each iteration subtracts once and appends once.

[B] Replace with divmod
```diff
+++ roman_numerals.py
@@ -9,4 +9,3 @@
     for value, symbol in NUMERALS:
-        while n >= value:
-            result.append(symbol)
-            n -= value
+        count, n = divmod(n, value)
+        result.append(symbol * count)
```
Computes repetitions in one step instead of looping.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you choose here — and does the performance question factor into your thinking at all?

### Student

I'd pick **A** — stick with the while loop.

Here's my thinking: performance doesn't really matter here. The input range is only 1–3999, and we're looping through at most 13 value-symbol pairs. Even in the worst case (like `n=3888`, which would need lots of M's and C's), we're talking maybe a couple hundred iterations total across the whole function. That's negligible.

The while loop is also more explicit about what's happening: "keep subtracting this value and collecting symbols until we can't anymore." It matches the greedy algorithm I was already thinking about.

Option B with `divmod` is clever and does the same work faster, but for this problem it feels like premature optimization. And honestly, the while loop is easier for me to trace through mentally — I can picture the `n` shrinking step by step, which helps me understand *why* the algorithm works.

If this were processing millions of numbers or running on a constrained device, sure, reach for B. But for a coding exercise where clarity matters, A wins.

Should I test the code now to make sure it actually works?

---

## Turn 3

### Tutor

Tutor: Fair reasoning — and you're right that performance is a non-issue here. One small pushback though: `divmod` isn't really about speed in this context — it's more about intent. `count, n = divmod(n, value)` reads as *"how many times does this value fit?"*, which is arguably the clearest statement of the greedy idea. The `while` loop expresses the *mechanism* rather than the *intent*. Neither is wrong; just worth sitting with.

On to testing — yes, let's verify it. A few good cases to hit: the boundaries, a complex subtractive case, and the notorious `3999`:

[Bash(cd "$(dirname $(find . -name roman_numerals.py | head -1))" && python3 -c "
from roman_numerals import to_roman

cases = [
    (1,    'I'),
    (4,    'IV'),
    (9,    'IX'),
    (14,   'XIV'),
    (40,   'XL'),
    (90,   'XC'),
    (399,  'CCCXCIX'),
    (400,  'CD'),
    (900,  'CM'),
    (1994, 'MCMXCIV'),
    (2024, 'MMXXIV'),
    (3888, 'MMMDCCCLXXXVIII'),
    (3999, 'MMMCMXCIX'),
]

all_pass = True
for n, expected in cases:
    got = to_roman(n)
    status = '✓' if got == expected else '✗'
    if got != expected:
        all_pass = False
    print(f'{status}  to_roman({n:4d}) = {got!r:20s}  (expected {expected!r})')

print()
print('All tests passed!' if all_pass else 'FAILURES above.')
"
)]
  ✓  to_roman(   1) = 'I'                   (expected 'I')
  ✓  to_roman(   4) = 'IV'                  (expected 'IV')
  ✓  to_roman(   9) = 'IX'                  (expected 'IX')
  ✓  to_roman(  14) = 'XIV'                 (expected 'XIV')
  ✓  to_roman(  40) = 'XL'                  (expected 'XL')
  ✓  to_roman(  90) = 'XC'                  (expected 'XC')
  ✓  to_roman( 399) = 'CCCXCIX'             (expected 'CCCXCIX')
  ✓  to_roman( 400) = 'CD'                  (expected 'CD')
  ✓  to_roman( 900) = 'CM'                  (expected 'CM')
  ✓  to_roman(1994) = 'MCMXCIV'             (expected 'MCMXCIV')
  ✓  to_roman(2024) = 'MMXXIV'              (expected 'MMXXIV')
  ✓  to_roman(3888) = 'MMMDCCCLXXXVIII'     (expected 'MMMDCCCLXXXVIII')
  … (3 more lines)

Tutor: All 13 pass, including the tricky ones — `399` (`CCCXCIX`) chains three subtractive forms back-to-back, and `3888` produces the longest possible output at 15 characters.

The solution is clean and done. The core insight worth keeping: **subtractive notation isn't a special case** — it falls out naturally from including those pairs in the table. `CM`, `CD`, `XC`, etc. are just values that happen to map to two-character symbols. The greedy loop doesn't need to know anything about Roman numeral rules beyond that ordered table.

### Student

That's a really helpful observation about `divmod` — I appreciate that push. You're right that intent matters. Reading `count, n = divmod(n, value)` as "how many times does this value fit?" is actually clearer about what the greedy algorithm is conceptually doing. I'll keep that in mind for future code review conversations.

And wow, seeing all 13 test cases pass is satisfying — especially cases like `399` and `3888` that stress-test the subtractive logic. The fact that those complex cases just *work* without special handling reinforces your point: by including `(9, 'IX')`, `(4, 'IV')`, `(90, 'XC')`, and `(400, 'CD')` in the table, the algorithm naturally handles them. There's no if-statement saying "oh, if we need a 9 in this position, use IX" — it all falls out of the greedy descent.

I feel good about this solution. The code is readable, easy to debug if needed, and the mental model is solid. Thanks for walking through the trade-offs (while loop vs. divmod, greedy table vs. digit arrays) — that kind of reasoning about clarity and maintainability is more useful to me than just getting the right answer.

<done/>

---

**Run end:** done after 3 turn(s) in 74.2s
