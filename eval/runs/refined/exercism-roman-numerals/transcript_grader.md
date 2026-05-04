# exercism-roman-numerals

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:41:37

## Initial prompt

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Greedy value table
Build one flat list of `(value, symbol)` pairs — including all 13 subtractive pairs — then greedily peel off the largest value that fits.

```diff
+++ roman_numerals.py
@@ -0,0 +1,12 @@
+VALUES = [
+    (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
+    (100,"C"), (90,"XC"), (50,"L"), (40,"XL"),
+    (10,"X"),  (9,"IX"),  (5,"V"), (4,"IV"), (1,"I"),
+]
+
+def to_roman(n):
+    result = []
+    for value, symbol in VALUES:
+        while n >= value:
+            result.append(symbol)
+            n -= value
+    return "".join(result)
```

[B] Per-digit lookup tables
Store four separate arrays — one per decimal place — and index into them with each digit.

```diff
+++ roman_numerals.py
@@ -0,0 +1,11 @@
+THOUSANDS = ["","M","MM","MMM"]
+HUNDREDS  = ["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"]
+TENS      = ["","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"]
+ONES      = ["","I","II","III","IV","V","VI","VII","VIII","IX"]
+
+def to_roman(n):
+    return (THOUSANDS[n // 1000] +
+            HUNDREDS[n % 1000 // 100] +
+            TENS    [n % 100  // 10 ] +
+            ONES    [n % 10        ])
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer?

### Student

I think I'd like to go with **A** — the greedy value table approach.

My reasoning: it feels more straightforward to understand at a glance. I can see all 13 value-symbol pairs listed out in order, and the algorithm itself is simple — just keep subtracting the largest value that fits and append the symbol. It's easy to trace through mentally.

Option B is clever and probably more efficient, but I'd have to think harder about why indexing into those four separate arrays works. Right now I want to focus on getting a working solution that I understand clearly.

Let me start coding option A. Should I write out the function and test it, or do you want to walk through the logic first?

---

## Turn 2

### Tutor

Tutor: Good call — and your instinct is right about B: that cleverness is also its weakness. If someone asks "why does `HUNDREDS[4]` equal `"CD"`?" you have to reconstruct the logic mentally. A encodes the *rules*, B encodes the *answers*.

Let's just write it:

[Write(roman_numerals.py)]
VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100,  "C"), (90,  "XC"), (50,  "L"), (40,  "XL"),
    (10,   "X"), (9,   "IX"), (5,   "V"), (4,   "IV"),
    (1,    "I"),
]

def to_roman(n):
    result = []
    for value, symbol in VALUES:
        while n >= value:
            result.append(symbol)
… (3 more lines)
  File created successfully at: roman_numerals.py

Tutor: Let's do a quick sanity check across the interesting edge cases:

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

Tutor: All green. Worth tracing one case manually — here's `1994`:

```
1994 ≥ 1000 → "M",   n=994
 994 ≥  900 → "CM",  n=94
  94 ≥   90 → "XC",  n=4
   4 ≥    4 → "IV",  n=0
```
→ `MCMXCIV` ✓

One small thing worth thinking about — the inner loop is `while`, not `if`. Quick question:

OPTIONS:
[A] while is necessary
`while` handles repeated symbols like `MMM` (3000). With `if`, `to_roman(3000)` would return `"M"` instead of `"MMM"` — the loop moves on after the first match.

[B] if would work fine
Each value in the table can only appear a bounded number of times, so `if` would still terminate correctly and produce the right output.

(Reply with A or B, or ask a follow-up question.)

Tutor: Why `while` instead of `if` — does it matter?

### Student

**A** — `while` is necessary.

I see it now: if we used `if`, we'd only subtract the value once per iteration of the outer loop. So for 3000, we'd match `(1000, "M")` in the outer loop, append `"M"` once with the `if`, then move on to `(900, "CM")` — which doesn't fit — and keep going. We'd end up with just `"M"` instead of `"MMM"`.

The `while` loop keeps subtracting the same value as long as it fits. So 3000 would:
- First iteration of outer loop, value=1000: `while 3000 >= 1000` → append `"M"`, n=2000
- Still `while 2000 >= 1000` → append `"M"`, n=1000  
- Still `while 1000 >= 1000` → append `"M"`, n=0
- Now 0 < 1000, so exit the while and move to the next value in the table

That's the key difference — we need to keep applying the same symbol until it no longer fits.

<done/>

---

**Run end:** done after 2 turn(s) in 48.2s
