# exercism-allergies

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:25:00

## Initial prompt

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

---

## Turn 1

### Tutor

Tutor: Good problem — the bitfield encoding is the whole puzzle. Let me start with the most consequential design choice.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Plain dict of names→values
```diff
+++ allergies.py
@@ -0,0 +1,6 @@
+ALLERGENS = {
+    "eggs": 1, "peanuts": 2, "shellfish": 4,
+    "strawberries": 8, "tomatoes": 16, "chocolate": 32,
+    "pollen": 64, "cats": 128,
+}
```
Simple, readable. Lookup is O(1) by name.

[B] IntEnum flags
```diff
+++ allergies.py
@@ -0,0 +1,8 @@
+from enum import IntEnum
+
+class Allergen(IntEnum):
+    eggs = 1; peanuts = 2; shellfish = 4
+    strawberries = 8; tomatoes = 16; chocolate = 32
+    pollen = 64; cats = 128
```
Each member *is* its bitmask value. You can write `score & Allergen.cats` directly.

(Reply with A or B, or ask a follow-up question.)

Tutor: How do you want to represent the allergen data?

### Student

I think I'd go with **A** — the plain dict.

My reasoning: the problem asks me to return a list of allergen *names* from the `allergies()` function, so I'll be iterating over the dict keys anyway. And for `is_allergic_to()`, I just need to look up the name and check if `score & allergen_value`, which is straightforward with a dict.

IntEnum feels like it might be overkill here since I'm not doing anything fancy with the enum itself — I'm just checking bits and returning strings. The dict is simpler and more readable.

Should I go ahead and set up that dict now, then write the two functions?

---

## Turn 2

### Tutor

Tutor: Your reasoning is sound — the dict works well and your instinct about simplicity is good. One thing worth noting: `IntEnum` members are directly iterable and carry their name as `.name`, so `allergies()` would be `[a.name for a in Allergen if score & a]` — no `.items()` needed. But that's a marginal win, and the dict is totally fine.

The bigger point: because the allergens are a *power-of-two* set, any representation that pairs a name with an integer value works. The dict is honest and clear.

Let's build it. Now, the core of both functions is the same bit operation. Which of these would you use for `is_allergic_to`?

OPTIONS:
[A] Mask and compare zero
```diff
+++ allergies.py
@@ -0,0 +1,3 @@
+def is_allergic_to(score, allergen):
+    return score & ALLERGENS[allergen] != 0
```

[B] Double-mask the score first
```diff
+++ allergies.py
@@ -0,0 +1,3 @@
+def is_allergic_to(score, allergen):
+    return (score % 256) & ALLERGENS[allergen] != 0
```
Clamps score to 8 bits before checking, since only 8 allergens are defined.

(Reply with A or B, or ask a follow-up question.)

### Student

I'd go with **A** — mask and compare zero.

Here's my thinking: the problem doesn't say anything about the score being out of range or needing to clamp it. If someone passes in a huge number like 1000, the bitwise AND will still work correctly — it'll just check if that specific bit is set, which is what we want.

Option B feels like it's solving a problem that doesn't exist yet. And if the problem *did* specify that scores should be clamped to 8 bits, I'd rather see that requirement explicitly in the tests first before adding that logic.

The simpler approach (A) is cleaner and correct for the problem as stated. Should I write out both functions now with the dict and this approach?

---

## Turn 3

### Tutor

Tutor: Exactly right. `score & 4` isolates bit 2 regardless of what the other bits are — no normalization needed. Let's write it out.

[Glob(allergies.py)]
  No files found

[Write(allergies.py)]
ALLERGENS = {
    "eggs": 1,
    "peanuts": 2,
    "shellfish": 4,
    "strawberries": 8,
    "tomatoes": 16,
    "chocolate": 32,
    "pollen": 64,
    "cats": 128,
}


… (7 more lines)
  File created successfully at: allergies.py

Tutor: Done. One last question before we call it finished — think about what the Exercism tests might throw at `allergies()`:

OPTIONS:
[A] Output order matches dict
Return allergens in whatever order the dict iterates (insertion order in Python 3.7+). The dict is already defined lowest-bit-first, so the output is naturally `["eggs", "peanuts", ...]` order.

[B] Sort the output list
Add `.sort()` or wrap in `sorted()` to guarantee alphabetical order, since test assertions might not account for ordering.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you go with?

### Student

I'd go with **A** — output order matches dict.

My reasoning: the dict is already defined in bit-order (lowest to highest), which happens to be a sensible natural order. More importantly, Exercism tests are usually pretty well-designed, and if they care about output order, they'll either accept any order or the test will fail and tell me exactly what's wrong.

Adding `.sort()` preemptively feels like guessing. If the test expects bit-order and I sort alphabetically instead, I've just made the problem worse. Better to run the test first, see if order matters, and adjust only if needed.

Let me see what the full `allergies()` function looks like with the dict iteration:

```python
def allergies(score):
    return [allergen for allergen, value in ALLERGENS.items() if score & value]
```

Does that look right? Should I test it out to make sure it works?

---

## Turn 4

### Tutor

Tutor: Exactly right — and I'd actually prefer your variable name `allergen` over `name` in the loop; it's more descriptive. Let me update the file to match:

[Edit(allergies.py)]
--- before
    return [name for name, value in ALLERGENS.items() if score & value]
--- after
    return [allergen for allergen, value in ALLERGENS.items() if score & value]
  The file allergies.py has been updated successfully.

Tutor: Let's spot-check a few cases quickly:

[Bash(python3 -c "
from allergies import is_allergic_to, allergies

# score=0: no allergies
print(allergies(0))

# score=1: just eggs
print(allergies(1))

# score=5 = 1+4: eggs + shellfish
print(allergies(5))

# score=255: all allergens
print(allergies(255))

# score=257 = 256+1: unknown high bit + eggs — should still return just eggs
print(allergies(257))

# is_allergic_to spot checks
print(is_allergic_to(5, 'eggs'))      # True
print(is_allergic_to(5, 'peanuts'))   # False
print(is_allergic_to(5, 'shellfish')) # True
"
)]
  []
  ['eggs']
  ['eggs', 'shellfish']
  ['eggs', 'peanuts', 'shellfish', 'strawberries', 'tomatoes', 'chocolate', 'pollen', 'cats']
  ['eggs']
  True
  False
  True

Tutor: All correct — including the `score=257` case, which confirms that the stray high bit is silently ignored with no extra logic needed. The final file:

[Read(allergies.py)]
  1	ALLERGENS = {
  2	    "eggs": 1,
  3	    "peanuts": 2,
  4	    "shellfish": 4,
  5	    "strawberries": 8,
  6	    "tomatoes": 16,
  7	    "chocolate": 32,
  8	    "pollen": 64,
  9	    "cats": 128,
  10	}
  11	
  12	
  … (7 more lines)

Tutor: Clean and done. The whole solution hinges on one insight: `score & power_of_two` is nonzero iff that bit is set — everything else is just bookkeeping around that operation.

### Student

Perfect. That was really helpful — I can see how the bitfield logic is the heart of the problem, and everything else naturally falls out from that one operation.

The key takeaway for me: when you're working with bitmasks and powers of two, the AND operation is your friend, and you don't need to overthink edge cases like score normalization or output ordering unless the tests tell you otherwise.

Thanks for walking through the design choices too — it's good to see how to think through "plain dict vs. IntEnum" and "clamp vs. don't clamp" in a practical way rather than just picking the fanciest tool.

<done/>

---

**Run end:** done after 4 turn(s) in 87.0s
