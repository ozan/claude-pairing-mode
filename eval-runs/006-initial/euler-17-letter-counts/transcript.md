# euler-17-letter-counts

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:55:08.823Z

---

## Turn 1

**User:**

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

**Pair:**

Thinking: Let me think about this problem. We need to count the letters in all numbers from 1 to 1000 written in British English.
  
  Let me start building this step by step. I'll propose some key implementation decisions to the user as we go.
  
  Let me think about the structure:
  - 1-19: unique words
  - 20-99: tens + ones
  - 100-999: X hundred [and Y] where Y is 1-99
  - 1000: one thousand
  
  The key decision here is how to structure the code. Let me think about what would make a good teaching moment.
  
  One good question: how to handle the "hundred and" part - specifically, do we count the "and" only when the remainder is non-zero? (British English uses "and" for numbers like 342 = "three hundred and forty-two", but 300 = "three hundred")
   
  Now I'm weighing whether to use a recursive approach that breaks numbers down hierarchically, or explicit lookup tables for each range. The recursive method is more elegant and scales to larger numbers, but the lookup table approach is more straightforward for this specific problem. I think I'll lean toward the lookup table method since it's clearer for this particular task.
  
  Let me work through an example to verify my logic: "three hundred and forty-two" becomes "threehundredandfortytwo" when you remove spaces and hyphens, which gives me 23 letters total. I'll structure the solution with word mappings for 1-19, tens (20, 30, etc.), and then build up from there.
  
  The key decision is whether to use recursion or explicit conditionals for handling different ranges. A recursive approach where a function breaks down numbers into their components feels cleaner, but I could also go with straightforward if/elif chains for each magnitude. The trickier part is handling the "and" in British English—I need to decide whether to count letter lengths as I build each word or tally them at the end. I'm comparing the two approaches more carefully now. Both handle the "and" correctly for British English—it appears after hundreds when there's a remainder, and both implementations capture that. But looking at the recursive version, when we spell out the hundreds digit, we're concatenating it directly with "hundred," which works fine since `spell(3)` returns "three" and we get "threehundred" as intended.
  
  After checking the edge cases—zero remainders, multiples of ten, round hundreds—the recursive approach feels cleaner and more elegant. I'll go with Option A and frame this as a teaching moment about recursion versus iteration.

Assistant: Fun one. Before writing any code, let me ask about the core structure:

OPTIONS:
[A] Recursive breakdown
```diff
+++ euler17.py
@@ -0,0 +1,12 @@
+ones = ['','one','two','three','four','five','six','seven',
+        'eight','nine','ten','eleven','twelve','thirteen',
+        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
+tens = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
+
+def spell(n):
+    if n == 1000: return 'onethousand'
+    if n < 20:    return ones[n]
+    if n < 100:   return tens[n//10] + spell(n % 10)
+    rest = spell(n % 100)
+    return spell(n//100) + 'hundred' + ('and' + rest if rest else '')
```

[B] Iterative with mutation
```diff
+++ euler17.py
@@ -0,0 +1,12 @@
+ones = ['','one','two','three','four','five','six','seven',
+        'eight','nine','ten','eleven','twelve','thirteen',
+        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
+tens = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
+
+def spell(n):
+    if n == 1000: return 'onethousand'
+    w = ''
+    if n >= 100:
+        w += ones[n//100] + 'hundred'; n %= 100
+        if n: w += 'and'
+    if n >= 20:  w += tens[n//10]; n %= 10
+    if n:        w += ones[n]
+    return w
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just solve the problem directly and present two options in text form, then ask the user to choose.
  
  Actually, let me just proceed with building the solution and ask the question as text. I'll present two options clearly.

Assistant: Before I write any code — quick design question. Which structure would you use for `spell(n)`?

**Option A — recursive breakdown:**
```python
def spell(n):
    if n == 1000: return 'onethousand'
    if n < 20:    return ones[n]
    if n < 100:   return tens[n//10] + spell(n % 10)
    rest = spell(n % 100)
    return spell(n//100) + 'hundred' + ('and' + rest if rest else '')
```

**Option B — iterative with mutation:**
```python
def spell(n):
    if n == 1000: return 'onethousand'
    w = ''
    if n >= 100:
        w += ones[n//100] + 'hundred'; n %= 100
        if n: w += 'and'
    if n >= 20:  w += tens[n//10]; n %= 10
    if n:        w += ones[n]
    return w
```

Both use the same lookup tables at the top. Which do you prefer?

---

## Turn 2

**User:**

I'd go with **Option A** — the recursive breakdown. I like that each digit magnitude (ones, tens, hundreds) gets its own case, and I can trace through how a number like 342 would decompose step by step. 

With Option B, I'm a bit lost by the mutation of `n` — it feels like I have to track both what gets added to `w` *and* remember that `n` has changed. Recursion feels less error-prone to me.

So I'm picking A. Should I go ahead and write the full solution now, or is there something else you want me to think through first?

**Pair:**

Thinking: The user picked option A (the recursive approach), which is my preference. I should express brief agreement and then proceed to build the solution. Let me write the full solution.
  
  Let me think about whether there's another good teaching moment here before writing the full solution. One thing worth pointing out is the "and" handling - in British English, "and" appears in numbers like:
  - 342 = "three hundred and forty-two" 
  - 100 = "one hundred" (no "and")
  - 101 = "one hundred and one"
  
  The spell function already handles this correctly with `('and' + rest if rest else '')`.
  
  
  Now I'm writing out the complete recursive solution with the lookup tables for ones and tens, then building the spell function that handles the base cases and recursively constructs the number words...
  
  Finishing the recursive logic...
  
  Let me verify this works by tracing through a few examples like single digits, teens, and larger numbers like 342 to make sure the concatenation and 'and' placement are correct...

Assistant: Good instinct — the mutation in B is exactly why it's harder to reason about. Your mental model is right: recursion makes the *decomposition structure* explicit.

Let me write the full solution:

[Bash(ls euler17.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(euler17.py)]
ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
        'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
        'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
        'sixty', 'seventy', 'eighty', 'ninety']

def spell(n):
    if n == 1000: return 'onethousand'
    if n < 20:    return ones[n]
    if n < 100:   return tens[n // 10] + spell(n % 10)
    rest = spell(n % 100)
    return spell(n // 100) + 'hundred' + ('and' + rest if rest else '')
… (13 more lines)

[Bash(python euler17.py)]
  error: Exit code 127

[Bash(python3 euler17.py)]
  21124

Assistant: **21124** — correct answer for PE #17.

A few things worth noting about the implementation:

- `ones[0] = ''` is the key trick — `spell(20)` calls `tens[2] + spell(0)` = `'twenty' + ''`, so the empty string acts as a natural base case for "no remainder"
- The `'and' + rest if rest else ''` handles British English: `spell(300)` → `'threehundred'` (no "and"), `spell(342)` → `'threehundredandfortytwo'` (with "and")
- The assertions double as documentation — you can trace `spell(342)` step by step right there

One small thing to notice: `spell(0)` is never called from the final sum (we start at 1), but it returns `ones[0] = ''` which is exactly what we want internally. That's the kind of happy accident you want to make *intentional* with a comment or assertion if this were production code.

---

## Turn 3 (final)

**User:**

That makes total sense. I was confused about the empty string at index 0 before, but now I see it — that's clever. `spell(20)` just naturally becomes `'twenty' + ''` without needing an extra conditional.

And thanks for pointing out the "and" logic — I was worried that might be the tricky part, but the way you wrote it (`'and' + rest if rest else ''`) is actually really clean. You only add "and" if there's something left after the hundreds place.

I noticed you mentioned assertions in the explanation but the diff shows "… (13 more lines)" — was the full code including those assertions, or were you just saying that would be a good practice? Either way, I feel like I understand the solution now: the recursive structure maps directly onto English number grammar.

<done/>

---

**Run end**: done after 2 turns (106s)
