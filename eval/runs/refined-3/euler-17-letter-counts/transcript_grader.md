# euler-17-letter-counts

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:53:20

## Initial prompt

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

---

## Turn 1

### Tutor

Tutor: Fun one. Before writing code, let me check your thinking on the structure.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Generate strings, then count
Write a `number_to_words(n)` function that returns the full English string (e.g. `"three hundred and forty-two"`), then sum `len(s.replace(' ','').replace('-',''))` over 1–1000.

[B] Accumulate letter counts directly
Skip building strings entirely. Pre-compute the letter count of each word token (`"three"→5`, `"hundred"→7`, etc.) and accumulate totals arithmetically as you iterate 1–1000.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to take?

### Student

I think I'd like to go with **[A]** — generate strings, then count.

My reasoning is that it feels more straightforward to me right now. I can write out the logic for converting a number to its English word form, see it actually work, and then just strip spaces and hyphens and count the letters. It's easier to debug and verify that way.

Option B sounds more efficient, but I'm worried I might mess up the arithmetic and not catch mistakes. With strings, I can at least print out what I'm generating and sanity-check it.

Where should I start?

---

## Turn 2

### Tutor

Tutor: Exactly right — and a good instinct for debugging. Now, the `number_to_words` function has to handle three tiers: 1–19 (irregular), 20–99 (tens + optional ones), and 100–999 (hundreds + optional remainder). Worth a quick structural question before writing it:

OPTIONS:
[A] Factor out a sub-100 helper
Write a `say_below_100(n)` helper, then `number_to_words(n)` calls it for both the remainder after hundreds and the 1–99 range directly. The hundreds logic becomes a clean one-liner on top.

[B] One flat function
Handle everything inside a single `number_to_words(n)` with if/elif branches: one block for 1–19, one for 20–99, one for 100–999, one for 1000.

(Reply with A or B, or ask a follow-up question.)

### Student

I like **[A]** — factor out a sub-100 helper.

I can see how that would keep things cleaner. If I write `say_below_100(n)` to handle both the 1–19 irregulars and the 20–99 tens+ones logic, then the hundreds case becomes way simpler: just extract the hundreds digit, say it, add "hundred and", then call `say_below_100` on the remainder. And `number_to_words(1000)` is just a special case.

Plus, if I mess up the 1–99 logic, I only have to debug it in one place.

Should I start by building the lookup tables for the ones (1–19) and tens (20, 30, 40, etc.)?

---

## Turn 3

### Tutor

Tutor: Yes, exactly — start with the word lists. There's actually a subtle choice in how you index them:

OPTIONS:
[A] Minimal lists, offset arithmetic
```diff
+++ euler17.py
@@ -0,0 +1,6 @@
+ones = ['one','two','three','four','five','six','seven',
+        'eight','nine','ten','eleven','twelve','thirteen',
+        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
+tens = ['twenty','thirty','forty','fifty',
+        'sixty','seventy','eighty','ninety']
+# access: ones[n-1], tens[n//10 - 2]
```

[B] Padded lists, direct indexing
```diff
+++ euler17.py
@@ -0,0 +1,6 @@
+ones = ['','one','two','three','four','five','six','seven',
+        'eight','nine','ten','eleven','twelve','thirteen',
+        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
+tens = ['','','twenty','thirty','forty','fifty',
+        'sixty','seventy','eighty','ninety']
+# access: ones[n], tens[n//10]
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **[B]** — padded lists, direct indexing.

It feels less error-prone to me. With option A, I'd have to remember to subtract 1 when accessing `ones` and subtract 2 when accessing `tens`, and I'd probably mess that up or introduce an off-by-one bug. With padded lists, I can just use the number directly as the index — `ones[n]` and `tens[n//10]` — which is way more intuitive to read and less likely to break.

The tiny bit of wasted space (a couple of empty strings) seems worth it for clarity and correctness.

Should I start coding `say_below_100(n)` now?

---

## Turn 4

### Tutor

Tutor: Yes — let's write the file. I'll put the word lists in and then pause on one thing worth thinking about in `say_below_100`:

OPTIONS:
[A] Explicit zero guard
```diff
+++ euler17.py
@@ -0,0 +1,12 @@
+ones = ['','one','two','three','four','five','six','seven',
+        'eight','nine','ten','eleven','twelve','thirteen',
+        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
+tens = ['','','twenty','thirty','forty','fifty',
+        'sixty','seventy','eighty','ninety']
+
+def say_below_100(n):
+    if n == 0:
+        return ''
+    if n < 20:
+        return ones[n]
+    return tens[n//10] + ('-' + ones[n%10] if n%10 else '')
```

[B] Let the padding do the work
```diff
+++ euler17.py
@@ -0,0 +1,11 @@
+ones = ['','one','two','three','four','five','six','seven',
+        'eight','nine','ten','eleven','twelve','thirteen',
+        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
+tens = ['','','twenty','thirty','forty','fifty',
+        'sixty','seventy','eighty','ninety']
+
+def say_below_100(n):
+    if n < 20:
+        return ones[n]   # ones[0] == '' covers n=0
+    return tens[n//10] + ('-' + ones[n%10] if n%10 else '')
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Waiting for your pick on A vs B before writing the file!

### Student

I'll go with **[B]** — let the padding do the work.

Since we already padded `ones` with an empty string at index 0, we don't need an explicit `if n == 0` check. When `n` is 0, `ones[0]` just returns `''`, which is exactly what we want anyway. It's simpler and keeps the function shorter without losing clarity.

The `if n < 20` branch handles both 0 and 1–19 elegantly that way.

---

## Turn 5

### Tutor

Tutor: Exactly right — the padding earns its keep. Let me write the file:

[Write(euler17.py)]
ones = ['','one','two','three','four','five','six','seven',
        'eight','nine','ten','eleven','twelve','thirteen',
        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
tens = ['','','twenty','thirty','forty','fifty',
        'sixty','seventy','eighty','ninety']

def say_below_100(n):
    if n < 20:
        return ones[n]   # ones[0] == '' covers n=0
    return tens[n//10] + ('-' + ones[n%10] if n%10 else '')

  File created successfully at: euler17.py

Tutor: Good. Now `number_to_words` — and this is where the British English rule matters. How should "and" be handled after "hundred"?

OPTIONS:
[A] Always append and
```diff
+++ euler17.py
@@ -9,0 +10,5 @@
+def number_to_words(n):
+    if n == 1000:
+        return 'one thousand'
+    if n >= 100:
+        return ones[n//100] + ' hundred and ' + say_below_100(n%100)
+    return say_below_100(n)
```

[B] Only and when remainder exists
```diff
+++ euler17.py
@@ -9,0 +10,7 @@
+def number_to_words(n):
+    if n == 1000:
+        return 'one thousand'
+    if n >= 100:
+        remainder = n % 100
+        tail = ' and ' + say_below_100(remainder) if remainder else ''
+        return ones[n//100] + ' hundred' + tail
+    return say_below_100(n)
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **[B]** — only and when remainder exists.

In British English, you say "one hundred and forty-two" but also just "one hundred" (not "one hundred and"). So we should only add the "and" if there's actually a remainder after the hundreds digit. Option B handles that correctly by checking `if remainder` before appending the " and " clause.

Option A would give us things like "one hundred and " with nothing after it, which would be wrong.

---

## Turn 6

### Tutor

Tutor: Right. Applying it:

[Edit(euler17.py)]
--- before
def say_below_100(n):
    if n < 20:
        return ones[n]   # ones[0] == '' covers n=0
    return tens[n//10] + ('-' + ones[n%10] if n%10 else '')
--- after
def say_below_100(n):
    if n < 20:
        return ones[n]   # ones[0] == '' covers n=0
    return tens[n//10] + ('-' + ones[n%10] if n%10 else '')

def number_to_words(n):
    if n == 1000:
        return 'one thousand'
    if n >= 100:
        remainder = n % 100
        tail = ' and ' + say_below_100(remainder) if remainder else ''
        return ones[n//100] + ' hundred' + tail
    return say_below_100(n)
  The file euler17.py has been updated successfully.

Tutor: One last choice — the counting expression:

OPTIONS:
[A] Strip with replace
```diff
+++ euler17.py
@@ -19,0 +20,1 @@
+print(sum(len(number_to_words(n).replace(' ','').replace('-','')) for n in range(1, 1001)))
```

[B] Count with isalpha
```diff
+++ euler17.py
@@ -19,0 +20,1 @@
+print(sum(c.isalpha() for c in number_to_words(n) for n in range(1, 1001)))
```
Wait — that's a syntax error. Does the iteration order matter here?

(Reply with A or B, or ask a follow-up question.)

### Student

Good catch — **[A]** is the way to go.

Option B has the nested loop backwards. It should be `for n in range(1, 1001) for c in number_to_words(n)`, but that's getting a bit convoluted. 

Option A is much clearer: for each number from 1 to 1000, convert it to words, strip out spaces and hyphens, count the remaining letters with `len()`, and sum them all up. It's straightforward and easy to verify that it does what we want.

Let's go with A.

---

## Turn 7

### Tutor

Tutor: Spot on — nested generator order trips up a lot of people. Applying and running:

[Edit(euler17.py)]
--- before
def number_to_words(n):
    if n == 1000:
        return 'one thousand'
    if n >= 100:
        remainder = n % 100
        tail = ' and ' + say_below_100(remainder) if remainder else ''
        return ones[n//100] + ' hundred' + tail
    return say_below_100(n)
--- after
def number_to_words(n):
    if n == 1000:
        return 'one thousand'
    if n >= 100:
        remainder = n % 100
        tail = ' and ' + say_below_100(remainder) if remainder else ''
        return ones[n//100] + ' hundred' + tail
    return say_below_100(n)

print(sum(len(number_to_words(n).replace(' ','').replace('-','')) for n in range(1, 1001)))
  The file euler17.py has been updated successfully.

[Bash(cd /Users/codepalace/dev/sandbox && python euler17.py)]
  error: Exit code 1

[Bash(python euler17.py)]
  21124

Tutor: **21124** — and that's the correct Project Euler answer.

Let's do a quick sanity check on a couple of values to make sure the logic is solid:

[Bash(python -c "
from euler17 import number_to_words
for n in [1, 12, 20, 42, 100, 115, 342, 1000]:
    s = number_to_words(n)
    print(f'{n:4d}  {s!r:35s}  letters={len(s.replace(\" \",\"\").replace(\"-\",\"\"))}')
")]
  21124
     1  'one'                                letters=3
    12  'twelve'                             letters=6
    20  'twenty'                             letters=6
    42  'forty-two'                          letters=8
   100  'one hundred'                        letters=10
   115  'one hundred and fifteen'            letters=20
   342  'three hundred and forty-two'        letters=23
  1000  'one thousand'                       letters=11

Tutor: 342 → "three hundred and forty-two" → 23 letters. The problem statement uses that exact example, so we're good.

The design held up cleanly:
- Padded lists → no index arithmetic, zero handled for free
- `say_below_100` factored out → hundreds logic stayed a clean one-liner
- Conditional `and` → exact hundreds like 100 aren't corrupted

### Student

Perfect! Those spot checks are really reassuring. I can see exactly how the pieces fit together:

- The padded lists let `say_below_100` return an empty string cleanly for 0, which then flows naturally into the hundreds case
- Factoring out `say_below_100` meant I didn't have to repeat the tens+ones logic
- The conditional `and` keeps exact hundreds (like 100, 200) from getting spurious "and" in them

And 342 matching the problem's example is the best confirmation that the logic is right.

Thanks for walking through this — I learned a lot about how to structure the problem cleanly before diving into code, and how careful thinking about edge cases (like zero, or exact hundreds) actually simplifies things rather than complicates them.

<done/>

---

**Run end:** done after 7 turn(s) in 167.6s
