# euler-17-letter-counts

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:03:29

## Initial prompt

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good problem. First design decision — how should the core logic work?

OPTIONS:
[A] Build the string, then count
Write a `number_to_words(n)` function that returns the full English phrase (e.g. `"three hundred and forty two"`), then sum `len(s.replace(' ','').replace('-',''))` over 1–1000.

[B] Count letters arithmetically
Skip building strings entirely. Precompute letter counts for each word and accumulate totals using arithmetic (e.g. each hundreds digit contributes its word-length × 100 + `len("hundred")` × 100, etc.).

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to take?

### Student

I think I'll go with **A** — build the string, then count.

It feels more straightforward to me right now. I can write a function that converts a number to its English words representation, and then just strip out spaces and hyphens and count what's left. That way I can also easily verify my output by printing out a few examples to make sure the English is correct (especially the "and" placement for British English).

Option B sounds clever, but I'm worried I might mess up the arithmetic and not realize it. With option A, I can at least sanity-check by eye before I sum everything up.

Should I start by building the `number_to_words()` function?

---

## Turn 2

### Tutor

Tutor: Exactly right. Let's build `number_to_words` bottom-up. First question: how should the lookup tables be structured?

OPTIONS:
[A] ones covers 1–19
```diff
+++ euler17.py
@@ -0,0 +1,7 @@
+ones = [
+    "", "one", "two", "three", "four", "five",
+    "six", "seven", "eight", "nine", "ten",
+    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
+    "sixteen", "seventeen", "eighteen", "nineteen"
+]
+tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
```
Index directly: `ones[n]` for any `n` in 1–19, no extra branch needed.

[B] ones covers 1–9 only
```diff
+++ euler17.py
@@ -0,0 +1,7 @@
+ones  = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
+teens = ["ten", "eleven", "twelve", "thirteen", "fourteen",
+         "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
+tens  = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
```
Requires a separate `elif 10 <= n <= 19: return teens[n-10]` branch every time.

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** — ones covers 1–19.

It's cleaner. I'd rather have one lookup table that handles the irregular teens all in one place than branch on a conditional every time I need to convert a two-digit number. The extra empty strings don't bother me, and indexing is straightforward.

---

## Turn 3

### Tutor

Tutor: Good call. Let me write the file with the tables, then we'll tackle the conversion logic.

[Bash(ls euler17.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(euler17.py)]
ones = [
    "", "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen"
]
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

  File created successfully at: euler17.py

Tutor: Now, for the conversion logic — should we extract a helper for the sub-100 case?

OPTIONS:
[A] Extract sub_hundred helper
```diff
+++ euler17.py
@@ -10,0 +11,10 @@
+def sub_hundred(n):
+    if n < 20:
+        return ones[n]
+    return tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
+
+def number_to_words(n):
+    if n == 1000:
+        return "one thousand"
+    if n >= 100:
+        rest = n % 100
+        return ones[n // 100] + " hundred" + (" and " + sub_hundred(rest) if rest else "")
+    return sub_hundred(n)
```

[B] Single flat function
```diff
+++ euler17.py
@@ -10,0 +11,14 @@
+def number_to_words(n):
+    if n == 1000:
+        return "one thousand"
+    result = ""
+    if n >= 100:
+        result += ones[n // 100] + " hundred"
+        n %= 100
+        if n:
+            result += " and "
+    if n >= 20:
+        result += tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
+    elif n > 0:
+        result += ones[n]
+    return result
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which structure would you prefer — A (with the `sub_hundred` helper) or B (flat function)?

### Student

I'll go with **A** — extract the `sub_hundred` helper.

I like that it isolates the logic for handling numbers under 100 in one place. That makes the main `number_to_words` function easier to read and reason about — it's clear that we handle the hundreds place separately, then delegate the remainder to `sub_hundred`. Plus, if I need to test or debug the sub-100 logic later, it's already in its own function.

Option B works too, but it feels like it's doing more at once, and I'd probably have to trace through the logic more carefully to make sure I haven't missed any cases.

---

## Turn 4

### Tutor

Tutor: Agreed — and that separation will pay off when we verify edge cases. Let me apply it.

[Edit(euler17.py)]
--- before
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
--- after
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def sub_hundred(n):
    if n < 20:
        return ones[n]
    return tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")

def number_to_words(n):
    if n == 1000:
        return "one thousand"
    if n >= 100:
        rest = n % 100
        return ones[n // 100] + " hundred" + (" and " + sub_hundred(rest) if rest else "")
    return sub_hundred(n)
  The file euler17.py has been updated successfully.

Tutor: Now the final piece — summing up the letters. Quick question before we wire it together:

OPTIONS:
[A] Filter then len
```diff
+++ euler17.py
@@ -20,0 +21,4 @@
+def letter_count(s):
+    return sum(1 for c in s if c.isalpha())
+
+print(sum(letter_count(number_to_words(n)) for n in range(1, 1001)))
```

[B] Replace then len
```diff
+++ euler17.py
@@ -20,0 +21,2 @@
+print(sum(len(number_to_words(n).replace(" ", "").replace("-", ""))
+          for n in range(1, 1001)))
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** — filter then len.

It's clearer what we're doing: we're counting letters. The `c.isalpha()` check is explicit about what we consider a "letter," which makes it easier to understand at a glance. Plus, wrapping it in a `letter_count` helper function gives us a reusable piece that we can test independently if we need to.

Option B works too, but chaining two `.replace()` calls feels a bit less readable to me. With A, the intent is immediately obvious.

---

## Turn 5

### Tutor

Tutor: Good instinct. Applying it:

[Edit(euler17.py)]
--- before
def number_to_words(n):
    if n == 1000:
        return "one thousand"
    if n >= 100:
        rest = n % 100
        return ones[n // 100] + " hundred" + (" and " + sub_hundred(rest) if rest else "")
    return sub_hundred(n)
--- after
def number_to_words(n):
    if n == 1000:
        return "one thousand"
    if n >= 100:
        rest = n % 100
        return ones[n // 100] + " hundred" + (" and " + sub_hundred(rest) if rest else "")
    return sub_hundred(n)

def letter_count(s):
    return sum(1 for c in s if c.isalpha())

print(sum(letter_count(number_to_words(n)) for n in range(1, 1001)))
  The file euler17.py has been updated successfully.

Tutor: Let's sanity-check a few examples first, then run it:

[Bash(cd /Users/jaredsilver/dev/repos/pair-coding && python3 -c "
import euler17
for n in [1, 12, 20, 21, 100, 101, 110, 342, 999, 1000]:
    s = euler17.number_to_words(n)
    print(f'{n:4d} → \"{s}\" ({euler17.letter_count(s)} letters)')
")]
  error: Exit code 1

[Bash(python3 -c "
import euler17
for n in [1, 12, 20, 21, 100, 101, 110, 342, 999, 1000]:
    s = euler17.number_to_words(n)
    print(f'{n:4d} → \"{s}\" ({euler17.letter_count(s)} letters)')
")]
  21124
     1 → "one" (3 letters)
    12 → "twelve" (6 letters)
    20 → "twenty" (6 letters)
    21 → "twenty-one" (9 letters)
   100 → "one hundred" (10 letters)
   101 → "one hundred and one" (16 letters)
   110 → "one hundred and ten" (16 letters)
   342 → "three hundred and forty-two" (23 letters)
   999 → "nine hundred and ninety-nine" (24 letters)
  1000 → "one thousand" (11 letters)

Tutor: All the edge cases look right — "one hundred" has no "and", "one hundred and one" does, "three hundred and forty-two" matches the problem's own example. And the answer printed at the top:

**21124**

The final file:

[Read(euler17.py)]
  1	ones = [
  2	    "", "one", "two", "three", "four", "five",
  3	    "six", "seven", "eight", "nine", "ten",
  4	    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
  5	    "sixteen", "seventeen", "eighteen", "nineteen"
  6	]
  7	tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
  8	
  9	def sub_hundred(n):
  10	    if n < 20:
  11	        return ones[n]
  12	    return tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
  … (14 more lines)

Tutor: Clean and readable. The decisions that paid off most here:
- `ones[0..19]` eliminated a teen-branch in every caller
- `sub_hundred` made the hundreds case read like a spec
- `isalpha()` handled the filtering without enumerating what to exclude

### Student

Great! That's really satisfying. Looking back at the choices we made:

1. **Option A (build strings, then count)** let me verify the logic by eye — I could literally see "three hundred and forty-two" and know it was right.

2. **The `ones[0..19]` lookup** was a small choice that simplified everything downstream. No branching needed.

3. **The `sub_hundred` helper** kept the main function clean and readable. I could understand the structure at a glance: hundreds digit + "hundred" + (optional "and" + remainder).

4. **`isalpha()` for filtering** was more declarative than manually removing spaces and hyphens.

And the sanity checks were crucial — seeing that 342 matched the problem's own example gave me confidence the answer was right before we even submitted it.

Thanks for walking me through the design trade-offs. I learned that sometimes the "simpler looking" option (like building actual strings) can be easier to reason about and debug than trying to be clever with arithmetic. And breaking down the problem into helpers makes the main logic way easier to follow.

<done/>

---

**Run end:** done after 5 turn(s) in 129.2s
