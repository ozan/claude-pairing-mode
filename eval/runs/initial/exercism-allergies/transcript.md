# exercism-allergies

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:02:04

## Initial prompt

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

---

## Turn 1

### Tutor

Thinking: Let me start building this Exercism 'Allergies' problem. First, let me think about the design.
  
  The allergens are encoded as bitfield flags:
  - eggs = 1 (bit 0)
  - peanuts = 2 (bit 1)
  - shellfish = 4 (bit 2)
  - strawberries = 8 (bit 3)
  - tomatoes = 16 (bit 4)
  - chocolate = 32 (bit 5)
  - pollen = 64 (bit 6)
  - cats = 128 (bit 7)
  
  There's a good teaching moment here about how to represent the allergens. 
  
  I'm weighing two approaches: storing allergens as a list where the index determines the bit position, or using a dictionary with explicit values. The list approach feels cleaner for iterating through allergens and checking which ones are present, since I can just enumerate with the index and calculate the bit value on the fly. I need to check if there's already a file before proceeding.

Tutor: Nice bite-sized problem with a real design decision hiding inside it. Let me check the directory first, then we'll make one key call before writing any code.

[Glob(allergies.py)]
  No files found

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: No existing file. Let me ask the first key design question: how to represent the allergen-to-bit mapping. I'll present two options:
  
  Option A: A list in bit order (DRY, derive bit value from index)
  Option B: A dict with explicit bit values (verbose, error-prone)
  
  I'll randomize which is "best" — let me put the list approach as option B and the dict as option A.

Tutor: No existing file. First design call — how do we store the allergen data?

OPTIONS:
[A] Dict with explicit values
```diff
+++ allergies.py
@@ -0,0 +1,5 @@
+ALLERGENS = {
+    "eggs": 1, "peanuts": 2, "shellfish": 4,
+    "strawberries": 8, "tomatoes": 16, "chocolate": 32,
+    "pollen": 64, "cats": 128,
+}
```

[B] List in bit order
```diff
+++ allergies.py
@@ -0,0 +1,4 @@
+ALLERGENS = [
+    "eggs", "peanuts", "shellfish", "strawberries",
+    "tomatoes", "chocolate", "pollen", "cats",
+]
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=The list approach is DRY: bit values are implicit from index position (1 << i), so there's no risk of a typo like assigning the wrong power of 2. Both allergies() and is_allergic_to() are clean with enumerate(). The dict approach requires manually maintaining the correct power-of-2 values, which is redundant and error-prone if the list ever changes order or gains new entries.

Tutor: Which do you prefer?

### Student

I think I'd go with **B** — the list in bit order.

Here's my reasoning: since we're working with bitfield flags, the position in the list directly corresponds to the bit position, which feels natural. If allergen at index `i` has value `2^i`, then checking whether someone is allergic becomes a simple bit operation. With option A, I'd still need to look up the value, which adds an extra step.

Plus, for the `allergies(score)` function that returns a list, iterating through the list and checking bits seems cleaner than iterating through a dict and checking values.

Does that make sense, or am I missing something about option A?

---

## Turn 2

### Tutor

Thinking: The user picked the right option (B) and gave excellent reasoning. I should affirm their choice, briefly add any extra insight, and then move forward to write the file and implement the functions.
  
  Let me write the file with the list approach, then implement both functions.

Tutor: Spot on — that's exactly right. The list is the *source of truth* for ordering, and `1 << i` derives the rest. No redundancy, no way to fat-finger a value.

One small bonus: if Exercism ever adds a 9th allergen, you just append a string — no mental arithmetic required.

Let's write it:

[Write(allergies.py)]
ALLERGENS = [
    "eggs", "peanuts", "shellfish", "strawberries",
    "tomatoes", "chocolate", "pollen", "cats",
]


def is_allergic_to(score, allergen):
    i = ALLERGENS.index(allergen)
    return bool(score & (1 << i))


def allergies(score):
… (2 more lines)
  File created successfully at: allergies.py

Thinking: Now let me ask a didactic question. There's an interesting subtlety here: the score can be any integer, including values > 255 (i.e., beyond the 8 defined allergens). The Exercism spec says scores above 255 should just ignore the higher bits — which our implementation already handles correctly because we only ever check bits 0-7.
  
  Actually, let me think about what else to ask. One interesting question: in `is_allergic_to`, I used `ALLERGENS.index(allergen)` which is O(n) and raises `ValueError` if not found. Should I handle invalid allergens? Or maybe ask about the `bool()` call vs just using the bitwise result directly?
   
  I'm noticing there's a choice between two equivalent bit extraction approaches: `score & (1 << i)` versus `(score >> i) & 1`. The first shifts the mask left, the second shifts the score right — both give the same result, but the latter is arguably more idiomatic for isolating a specific bit position. the result is always 0 or 1.
  
  Actually, the `bool()` question is interesting: `score & (1 << i)` without `bool()` would return 0 or `1 << i` (not always 0 or 1). So if someone does `is_allergic_to(score, "cats") == True`, it would fail without `bool()` since `128 != True`... wait, actually `128 == True` is False in Python, but `bool(128) == True` is True. And `if is_allergic_to(...)` would work fine without bool() due to truthiness.
  
  But actually the function is meant to return a boolean. Let me think about what's more interesting to explore here. Edge cases with scores above 255 could be worth examining, since the `allergies()` function only checks the 8 known bits. Or I could ask about whether `is_allergic_to` should reuse `allergies()` by checking if the allergen is in that list, versus doing a direct bit check. The list approach follows DRY principles but requires building the full list each time, while the bit check is O(1) and more efficient. That feels like a more useful teaching moment about tradeoffs between code reuse and performance.

Tutor: Quick question before we call it done — there's a tempting refactor for `is_allergic_to`:

OPTIONS:
[A] Direct bit check
```diff
+++ allergies.py
@@ -6,3 +6,3 @@
 def is_allergic_to(score, allergen):
-    i = ALLERGENS.index(allergen)
-    return bool(score & (1 << i))
+    i = ALLERGENS.index(allergen)
+    return bool(score & (1 << i))
```
No change — check the one relevant bit directly.

[B] Reuse allergies()
```diff
+++ allergies.py
@@ -6,3 +6,2 @@
 def is_allergic_to(score, allergen):
-    i = ALLERGENS.index(allergen)
-    return bool(score & (1 << i))
+    return allergen in allergies(score)
```
DRY: delegate to `allergies()` and use `in`.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=The `allergen in allergies(score)` version looks clean but always builds the full list of all matching allergens just to answer a yes/no question — O(n) work and an allocation for what should be O(1). The direct bit check is both faster and clearer about what's actually happening. DRY is valuable, but not when the "reuse" forces unnecessary work. The list-building should be reserved for when you actually need the list.

Thinking: The user hasn't responded yet - I should wait for their response to the options question.

Tutor: Which do you prefer?

### Student

I'd stick with **A** — the direct bit check.

Option B feels like it could be a premature optimization in reverse. We'd be building the *entire* list of allergens just to check membership for one, when a single bitwise operation is O(1) and crystal clear. If someone calls `is_allergic_to` a lot (which is plausible), option B wastes cycles rebuilding that list every time.

Plus, the direct bit check is the whole point of using bitfields in the first place — it's efficient and explicit about what we're doing. Option A keeps that contract front and center.

Should I fill in the last two lines of `allergies(score)` now?

---

## Turn 3

### Tutor

Thinking: The user picked correctly and gave great reasoning. They're asking about `allergies(score)` but it's already implemented! The file already has the complete implementation. Let me point that out and maybe show them the final state.

Tutor: Exactly right — great instinct. "Premature abstraction" is just as real a trap as premature optimization.

Good news: `allergies()` is already done — we wrote the whole thing up front. Here's the final file:

[Read(allergies.py)]
  1	ALLERGENS = [
  2	    "eggs", "peanuts", "shellfish", "strawberries",
  3	    "tomatoes", "chocolate", "pollen", "cats",
  4	]
  5	
  6	
  7	def is_allergic_to(score, allergen):
  8	    i = ALLERGENS.index(allergen)
  9	    return bool(score & (1 << i))
  10	
  11	
  12	def allergies(score):
  … (2 more lines)

Tutor: That's it — 13 lines. A few things worth noting:

- **`enumerate(ALLERGENS)`** gives `(i, name)` pairs, so `1 << i` is the bit mask for each allergen — same logic as `is_allergic_to`, just applied across all 8.
- **Scores > 255** are handled for free: we only ever test bits 0–7, so extra high bits are silently ignored (which is what Exercism expects).
- **`bool()`** in `is_allergic_to` matters: `score & (1 << i)` returns `0` or the bit value (e.g. `128` for cats), not `True`/`False`. Without `bool()`, a caller doing `== True` would get surprising results.

Want to run some quick manual tests, or move on to another exercise?

### Student

I'd like to run a quick manual test to make sure I understand it all correctly.

Let me trace through an example in my head: say `score = 248` (which should be binary `11111000`). That's bits 3–7 set, so strawberries, tomatoes, chocolate, pollen, and cats.

For `is_allergic_to(248, "cats")`:
- `i = 7` (cats is at index 7)
- `1 << 7 = 128`
- `248 & 128 = 128` (non-zero, truthy)
- `bool(128) = True` ✓

For `is_allergic_to(248, "eggs")`:
- `i = 0`
- `1 << 0 = 1`
- `248 & 1 = 0`
- `bool(0) = False` ✓

And `allergies(248)` would iterate through all 8 allergens, collecting only those where `248 & (1 << i)` is non-zero — so `["strawberries", "tomatoes", "chocolate", "pollen", "cats"]`.

Does that match what the code does?

---

## Turn 4

### Tutor

Tutor: Perfect trace — that's exactly what the code does. You've got the mental model down.

Let's verify it live:

[Bash(cd /Users/llorenc/dev/cc && python3 -c "
from allergies import is_allergic_to, allergies

print(bin(248))
print(is_allergic_to(248, 'cats'))   # True
print(is_allergic_to(248, 'eggs'))   # False
print(allergies(248))
")]
  error: Exit code 1

[Bash(python3 -c "
from allergies import is_allergic_to, allergies

print(bin(248))
print(is_allergic_to(248, 'cats'))   # True
print(is_allergic_to(248, 'eggs'))   # False
print(allergies(248))
")]
  0b11111000
  True
  False
  ['strawberries', 'tomatoes', 'chocolate', 'pollen', 'cats']

Tutor: Matches your trace exactly. `0b11111000` confirms bits 3–7 set, and the list comes back in the same order as `ALLERGENS` — which is a nice side effect of iterating the list rather than a set.

You're good to submit this one.

### Student

Excellent! That's really satisfying to see the output match my mental trace exactly. I appreciate how you walked me through the design decision upfront — choosing the list as the source of truth made everything else fall into place naturally.

One thing I'll take away: when you're dealing with bitfields, keep your allergen ordering explicit and in one place, and let bit positions flow from that. And the reminder about premature abstraction was helpful too — sometimes the straightforward solution *is* the right one.

Thanks for the pairing session. I'm ready to move on.

<done/>

---

**Run end:** done after 4 turn(s) in 80.7s
