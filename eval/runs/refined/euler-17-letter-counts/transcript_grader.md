# euler-17-letter-counts

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:43:57

## Initial prompt

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Generate strings, count chars
Write a `number_to_words(n)` function, build the full English string for each number 1–1000, then sum `len(s.replace(' ','').replace('-',''))` across all of them.

[B] Count mathematically
Analyze the structure of 1–1000 directly: compute how many times each word (one, two, hundred, and, …) appears, multiply by its letter count, and sum — no strings generated.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach appeals to you?

### Student

I think I'll go with **A** — generate strings and count characters.

It feels more straightforward to me right now. I can build a function that converts a number to its English words, then just iterate through 1 to 1000, convert each, strip out spaces and hyphens, and count the letters. That way I can test each piece as I go and make sure the `number_to_words` function is working correctly before I worry about the final sum.

Approach B sounds clever, but I'm worried I might mess up the analysis of how many times each word appears. With A, I can be more confident I'm getting the right answer because I can spot-check a few examples manually (like "three hundred and forty-two" = 3+8+3+5+2 = 21 letters).

Should I start by writing the `number_to_words` function?

---

## Turn 2

### Tutor

Tutor: Yes, exactly. Let me pose a design question before we write it — this choice shapes the whole structure:

OPTIONS:
[A] Helper for sub-100 logic
Write a `words_under_100(n)` helper (handles 1–99), then call it from the main function for both the tens portion of hundreds and for the remainder. Keeps the hundreds/thousands logic clean.

[B] One flat function
Write `number_to_words(n)` as a single function with `if/elif` branches for every range: 1–9, 10–19, 20–99, 100–999, 1000.

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** — the helper function approach.

I can already see that numbers 1–99 appear twice in the logic: once as the "tens" part of a hundreds number (like the "42" in "342"), and once on their own for 1–99. So writing `words_under_100(n)` as a reusable helper makes sense to me — it'll keep things DRY and make the main function cleaner to read.

Plus, if I test `words_under_100` thoroughly first, I know that piece works before I layer on the hundreds/thousands logic on top of it. Feels like a good way to build up confidence.

Should I start by mapping out the word mappings for 1–9, teens, and tens (20, 30, 40, etc.)?

---

## Turn 3

### Tutor

Tutor: Good instinct. Here's a decision on the lookup table structure:

OPTIONS:
[A] Split ones and teens
```diff
+++ euler17.py
@@ -0,0 +1,7 @@
+ones  = ['', 'one', 'two', 'three', 'four', 'five',
+          'six', 'seven', 'eight', 'nine']
+teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
+          'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
+tens  = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
+          'sixty', 'seventy', 'eighty', 'ninety']
```

[B] Single list for 1–19
```diff
+++ euler17.py
@@ -0,0 +1,7 @@
+ones = ['', 'one', 'two', 'three', 'four', 'five',
+         'six', 'seven', 'eight', 'nine', 'ten',
+         'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
+         'sixteen', 'seventeen', 'eighteen', 'nineteen']
+tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
+         'sixty', 'seventy', 'eighty', 'ninety']
```
Index directly: `ones[n]` for 1–19, `tens[n//10]` for the tens digit in 20–99.

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** — split ones and teens.

Even though option B is slightly more compact, I think A is clearer conceptually. The teens (10–19) are a special case linguistically — they don't follow the normal "tens digit + ones digit" pattern like 20–99 do. So keeping them separate makes the logic of `words_under_100` easier to follow: I check if the number is in the teens range, and if so, use the `teens` list; otherwise I build it from `tens` and `ones`.

Plus, it'll be easier to debug later if something goes wrong — I can clearly see which lookup table I'm using for different ranges.

Ready to write the `words_under_100` function now?

---

## Turn 4

### Tutor

Tutor: Fair enough — the explicit branching does make the intent clearer. Let's write it. Here's the key question for `words_under_100`:

OPTIONS:
[A] Guard the ones digit
```diff
+++ euler17.py
@@ -0,0 +1,8 @@
+def words_under_100(n):
+    if n < 10:
+        return ones[n]
+    elif n < 20:
+        return teens[n - 10]
+    else:
+        t, o = tens[n // 10], ones[n % 10]
+        return f"{t}-{o}" if o else t
```

[B] Always join tens and ones
```diff
+++ euler17.py
@@ -0,0 +1,7 @@
+def words_under_100(n):
+    if n < 10:
+        return ones[n]
+    elif n < 20:
+        return teens[n - 10]
+    else:
+        return tens[n // 10] + "-" + ones[n % 10]
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** — guard the ones digit.

Option B would produce strings like "twenty-" when `n % 10` is 0, which would have a trailing hyphen. Even though we're going to strip hyphens out later anyway when we count letters, it feels cleaner to not generate invalid English in the first place. Option A checks if there's actually a ones digit to add, and only includes the hyphen if needed — so "20" becomes just "twenty", not "twenty-".

Plus, thinking ahead to when I'm debugging or spot-checking outputs, I'd rather see clean, correct English words in my intermediate strings.

Should I now write the main `number_to_words(n)` function that handles 1–1000 using this `words_under_100` helper?

---

## Turn 5

### Tutor

Tutor: Yes — but one important design question first. British English has a specific rule about "and" in hundreds. Which of these is right?

OPTIONS:
[A] Always include and
```diff
+++ euler17.py
@@ -0,0 +1,7 @@
+def number_to_words(n):
+    if n == 1000:
+        return 'one thousand'
+    elif n >= 100:
+        return ones[n // 100] + ' hundred and ' + words_under_100(n % 100)
+    else:
+        return words_under_100(n)
```

[B] Only and when remainder nonzero
```diff
+++ euler17.py
@@ -0,0 +1,9 @@
+def number_to_words(n):
+    if n == 1000:
+        return 'one thousand'
+    elif n >= 100:
+        h = ones[n // 100] + ' hundred'
+        r = n % 100
+        return h + ' and ' + words_under_100(r) if r else h
+    else:
+        return words_under_100(n)
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **B** — only include "and" when the remainder is nonzero.

In British English, you say "one hundred and twenty-three" but just "one hundred" (not "one hundred and"). Option A would produce "one hundred and" for numbers like 100, 200, 300, etc., which isn't correct English.

Option B guards against that by checking if there's actually a remainder — if `r` is 0 (meaning we have exactly 100, 200, etc.), we just return the hundreds part without the "and".

Okay, I think I have the structure now. Let me put it all together and test it on a few examples before running the full 1–1000 count. Should I write out the complete code?

---

## Turn 6

### Tutor

Tutor: Exactly right. Let's put it all together now.

[Write(euler17.py)]
ones  = ['', 'one', 'two', 'three', 'four', 'five',
          'six', 'seven', 'eight', 'nine']
teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
          'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
tens  = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
          'sixty', 'seventy', 'eighty', 'ninety']


def words_under_100(n):
    if n < 10:
        return ones[n]
    elif n < 20:
… (28 more lines)
  File created successfully at: euler17.py

[Bash(python euler17.py)]
  1 -> 'one'
    12 -> 'twelve'
    20 -> 'twenty'
    42 -> 'forty-two'
   100 -> 'one hundred'
   115 -> 'one hundred and fifteen'
   300 -> 'three hundred'
   342 -> 'three hundred and forty-two'
  1000 -> 'one thousand'
  
  Total letters (1–1000): 21124

Tutor: All the spot-checks look correct — including the tricky ones: `100` has no "and", `300` has no "and", but `115` and `342` do. The answer is **21124**.

A few things worth noticing in the final sum:
- The `replace` calls strip spaces and hyphens before `len()` — exactly as planned
- `range(1, 1001)` correctly includes 1000 and excludes 0

The structure paid off: each layer (`words_under_100` → `number_to_words` → final sum) was independently testable, and we never had to debug more than one thing at a time.

### Student

Perfect! That's exactly what I was hoping for. The spot-checks all match what I'd expect — especially seeing "one hundred" without "and" but "three hundred and forty-two" with it. And the final answer of **21124** feels right.

I really appreciated how we built this up in layers. Testing `words_under_100` first on a few examples gave me confidence that the core logic was sound before I layered on the hundreds/thousands handling. Then when I saw the spot-checks for 100, 115, 300, and 342 all correct, I knew the "and" logic was working too.

The string replacement approach (stripping spaces and hyphens before counting) was straightforward — no off-by-one errors, no tricky edge cases. Just build the English string, clean it up, count the letters.

Thanks for walking through those design choices upfront (the helper function, splitting teens from ones, guarding the ones digit). It made writing the actual code much clearer.

<done/>

---

**Run end:** done after 6 turn(s) in 133.3s
