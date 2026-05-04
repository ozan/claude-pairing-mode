# exercism-allergies

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:40:03.033Z

---

## Turn 1

**User:**

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

**Pair:**

Assistant: Good exercise — clean bitfield problem. I'll use Python. First decision: how to store the allergen data.

[Glob(allergies.py)]
  No files found

Assistant: How should we store the allergen→value mapping?

**A — dict**
```diff
+++ allergies.py
@@ -0,0 +1,5 @@
+ALLERGENS = {
+    "eggs": 1, "peanuts": 2, "shellfish": 4,
+    "strawberries": 8, "tomatoes": 16, "chocolate": 32,
+    "pollen": 64, "cats": 128,
+}
```

**B — list**
```diff
+++ allergies.py
@@ -0,0 +1,4 @@
+ALLERGENS = [
+    "eggs", "peanuts", "shellfish", "strawberries",
+    "tomatoes", "chocolate", "pollen", "cats",
+]
```

Which structure do you prefer?

---

## Turn 2

**User:**

I'd pick **A — dict**.

Here's my reasoning:

**A (dict)** makes the bit values explicit and self-documenting. When you (or someone reading the code later) sees `ALLERGENS["eggs"]`, you immediately know it's `1`. For `is_allergic_to()`, you do a direct lookup: `score & ALLERGENS[allergen]`. No mental math.

**B (list)** is elegant and compact — it relies on the insight that allergens are powers of 2 in order, so you can use `2 ** index`. But that requires calculating the bit value each time, and it's less obvious to someone reading the code that the order matters and encodes the bit position.

For a learning exercise, **A** is clearer because the mapping is literal, not derived. Let's go with the dict.

**Pair:**

Assistant: Good reasoning, but B was actually my preference — here's the crux: the dict introduces redundancy. The values `1, 2, 4, 8…` aren't independent facts, they're *derived* from position. That means a typo like `"peanuts": 3` is silently wrong and nothing catches it. With the list, position **is** the data — there's a single source of truth, and `1 << index` is idiomatic bitfield code.

The readability concern is real, but it cuts the other way: a reader who knows bitfields sees the list and immediately understands the encoding. A reader who *doesn't* know bitfields might not realize the dict values must be a strict power-of-2 sequence.

That said, your argument stands for a learning context. Want to switch to B, or stick with A?

---

## Turn 3

**User:**

You're raising a fair point — and I see Claude's counterargument has merit too. Let me dig into the real tradeoff:

**Your argument (clarity)**: The dict is literal and obvious. Someone unfamiliar with bitfields doesn't have to decode `1 << 0` → 1, `1 << 1` → 2, etc.

**Claude's argument (integrity)**: The list is the source of truth. With a dict, `ALLERGENS["peanuts"] = 3` silently breaks the invariant (must be powers of 2), and there's no guard. With a list, the bit value is *derived*—can't get it wrong.

Both are true. But here's the thing: in a learning context, **explicitness beats cleverness**. You're learning bitfields, not optimizing for brevity. If you see `1, 2, 4, 8…` spelled out, you might not *realize* they're powers of 2, and miss the pattern. If you see the dict with explicit values, you see the pattern immediately *and* you can verify each value is correct.

Claude's right that the list is elegant. But your intuition—that the dict is better for *learning*—is solid.

**Final call**: stay with **A (dict)**, or switch to **B (list)** for the data-integrity win?

I'll implement whichever you pick and we'll get to `is_allergic_to()` and `allergies()` next.

**Pair:**

Assistant: I'll call it: **B (list)**. Data integrity beats explicitness here — and `1 << i` is worth learning once.

[Write(allergies.py)]
ALLERGENS = [
    "eggs", "peanuts", "shellfish", "strawberries",
    "tomatoes", "chocolate", "pollen", "cats",
]


Assistant: Now, `is_allergic_to`. Two ways to check if a bit is set:

Assistant: **A**
```diff
+++ allergies.py
@@ -4,3 +4,4 @@
     "tomatoes", "chocolate", "pollen", "cats",
 ]
+
+def is_allergic_to(score, allergen):
+    i = ALLERGENS.index(allergen)
+    return score & (1 << i) != 0
```

**B**
```diff
+++ allergies.py
@@ -4,3 +4,4 @@
     "tomatoes", "chocolate", "pollen", "cats",
 ]
+
+def is_allergic_to(score, allergen):
+    i = ALLERGENS.index(allergen)
+    return (score >> i) % 2 == 1
```

Both produce the same result — which would you pick, and why?

---

## Turn 4

**User:**

**A — mask and test**. Here's why:

**A** (`score & (1 << i) != 0`) is the idiomatic bitfield pattern:
- `1 << i` builds a mask with only the i-th bit set
- `score & mask` isolates that bit
- `!= 0` tests it
- **Intent is obvious**: "mask and check."

**B** (`(score >> i) % 2 == 1`) works, but it's roundabout:
- Shifts the bits right, then checks if the result is odd
- `% 2 == 1` is awkward — you're checking divisibility when a direct bit test is clearer
- (Also, `& 1` would be more idiomatic than `% 2 == 1` if you *were* going this route)

For a learning exercise, **A** teaches the right mental model: bitfield operations are about masks and isolation, not arithmetic tricks.

Let's go with **A**.

**Pair:**

Assistant: Exactly right — and the `% 2` vs `& 1` point is sharp. B isn't just roundabout, it's inconsistent: you already shifted, so why not `& 1`? The arithmetic framing doesn't earn its keep.

[Edit(allergies.py)]
--- before
ALLERGENS = [
    "eggs", "peanuts", "shellfish", "strawberries",
    "tomatoes", "chocolate", "pollen", "cats",
]
--- after
ALLERGENS = [
    "eggs", "peanuts", "shellfish", "strawberries",
    "tomatoes", "chocolate", "pollen", "cats",
]

def is_allergic_to(score, allergen):
    i = ALLERGENS.index(allergen)
    return score & (1 << i) != 0

Assistant: Now `allergies(score)` — return the list of all allergens the person reacts to. Two approaches:

**A**
```diff
+++ allergies.py
@@ -8,3 +8,4 @@
     return score & (1 << i) != 0
+
+def allergies(score):
+    return [a for a, i in zip(ALLERGENS, range(8)) if score & (1 << i)]
```

**B**
```diff
+++ allergies.py
@@ -8,3 +8,4 @@
     return score & (1 << i) != 0
+
+def allergies(score):
+    return [a for a in ALLERGENS if is_allergic_to(score, a)]
```

Which do you prefer?

---

## Turn 5

**User:**

**B — reuse `is_allergic_to()`**. Here's the reasoning:

**A** duplicates the bit-checking logic. You already wrote and tested `is_allergic_to()` — repeating `score & (1 << i)` in a new function violates DRY. If you later change how allergen checking works, you update one place, not two.

**B** is also more readable. A reader sees `allergies()` returns "all allergens we're allergic to" — the *intent* is clear without decoding the bitfield pattern again. The pattern lives in `is_allergic_to()`, which is where it belongs.

**A**'s only advantage is that it avoids a function call per allergen. But with 8 allergens, that cost is truly negligible.

For a learning exercise, **B** teaches a better habit: reuse tested functions, keep logic centralized. That's worth more than saving a few function-call cycles.

Go with **B**?

**Pair:**

Assistant: Agreed on all counts. Apply it:

[Edit(allergies.py)]
--- before
def is_allergic_to(score, allergen):
    i = ALLERGENS.index(allergen)
    return score & (1 << i) != 0
--- after
def is_allergic_to(score, allergen):
    i = ALLERGENS.index(allergen)
    return score & (1 << i) != 0

def allergies(score):
    return [a for a in ALLERGENS if is_allergic_to(score, a)]

[Read(allergies.py)]
  1	ALLERGENS = [
  2	    "eggs", "peanuts", "shellfish", "strawberries",
  3	    "tomatoes", "chocolate", "pollen", "cats",
  4	]
  5	
  6	def is_allergic_to(score, allergen):
  7	    i = ALLERGENS.index(allergen)
  8	    return score & (1 << i) != 0
  9	
  10	def allergies(score):
  11	    return [a for a in ALLERGENS if is_allergic_to(score, a)]
  12

Assistant: Clean and done. One edge case worth knowing: scores above 255 work fine — extra high bits are just ignored since we only iterate over 8 known allergens. Exercism actually tests this (score=256 → no allergies, score=257 → eggs only), and the implementation handles it for free.

---

## Turn 6 (final)

**User:**

Spot on. Let me verify it works with a quick test:

```python
# Test: score=248 (shellfish=4, strawberries=8, tomatoes=16, chocolate=32, pollen=64, cats=128)
# Binary: 11111000
# Expected: ["shellfish", "strawberries", "tomatoes", "chocolate", "pollen", "cats"]

assert is_allergic_to(248, "eggs") == False
assert is_allergic_to(248, "shellfish") == True
assert allergies(248) == ["shellfish", "strawberries", "tomatoes", "chocolate", "pollen", "cats"]

# Edge case: score=0 (no allergies)
assert allergies(0) == []

# Edge case: score=255 (all allergens)
assert allergies(255) == ALLERGENS

# Edge case: score=256 (beyond allergen bits)
assert allergies(256) == []
```

The solution is complete, idiomatic, and teaches the right concepts:

✓ **Bitfield encoding** — position → power of 2 (no magic numbers in code)  
✓ **Mask-and-test** — the standard pattern for bit checking  
✓ **DRY principle** — `allergies()` reuses `is_allergic_to()` rather than duplicating logic  
✓ **Edge cases** — scores > 255 naturally work because we only iterate over 8 allergens  

<done/>

---

**Run end**: done after 5 turns (122s)
