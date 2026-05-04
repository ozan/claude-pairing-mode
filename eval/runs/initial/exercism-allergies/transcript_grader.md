# exercism-allergies

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:02:04

## Initial prompt

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

---

## Turn 1

### Tutor

Tutor: Nice bite-sized problem with a real design decision hiding inside it. Let me check the directory first, then we'll make one key call before writing any code.

[Glob(allergies.py)]
  No files found

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

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

Tutor: Which do you prefer?

### Student

I think I'd go with **B** — the list in bit order.

Here's my reasoning: since we're working with bitfield flags, the position in the list directly corresponds to the bit position, which feels natural. If allergen at index `i` has value `2^i`, then checking whether someone is allergic becomes a simple bit operation. With option A, I'd still need to look up the value, which adds an extra step.

Plus, for the `allergies(score)` function that returns a list, iterating through the list and checking bits seems cleaner than iterating through a dict and checking values.

Does that make sense, or am I missing something about option A?

---

## Turn 2

### Tutor

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

Tutor: Which do you prefer?

### Student

I'd stick with **A** — the direct bit check.

Option B feels like it could be a premature optimization in reverse. We'd be building the *entire* list of allergens just to check membership for one, when a single bitwise operation is O(1) and crystal clear. If someone calls `is_allergic_to` a lot (which is plausible), option B wastes cycles rebuilding that list every time.

Plus, the direct bit check is the whole point of using bitfields in the first place — it's efficient and explicit about what we're doing. Option A keeps that contract front and center.

Should I fill in the last two lines of `allergies(score)` now?

---

## Turn 3

### Tutor

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
