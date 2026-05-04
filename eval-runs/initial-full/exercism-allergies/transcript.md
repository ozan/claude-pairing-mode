# exercism-allergies

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:58:12.757Z

---

## Turn 1

**User:**

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

**Pair:**

Assistant: Good problem — the bitfield encoding is the key insight. Let me start with a foundational design question before we write anything.

Assistant: How should we store the allergen registry? Both approaches work, but one is more elegant:

Assistant: The `propose_options` tool isn't available in this session, so I'll ask directly — it's still worth thinking through.

**How should we store the allergen registry?**

**Option A — ordered list** (bit value derived from index):
```python
ALLERGENS = [
    "eggs", "peanuts", "shellfish", "strawberries",
    "tomatoes", "chocolate", "pollen", "cats",
]
# bit value for allergen at index i  →  1 << i
```

**Option B — dict with explicit values:**
```python
ALLERGENS = {
    "eggs": 1, "peanuts": 2, "shellfish": 4,
    "strawberries": 8, "tomatoes": 16,
    "chocolate": 32, "pollen": 64, "cats": 128,
}
```

Which would you go with, and why? (A or B)

---

## Turn 2

**User:**

I'd go with **B** — the dict with explicit values.

Here's my thinking: Option A is clever and DRY, but it hides the bit-position requirement inside the list index. If someone (including future me) accidentally reorders the list, the whole bitfield breaks silently. With Option B, each allergen's bit value is explicit and tied to it directly. For a bitfield problem where position *is* the semantics, that explicitness feels right.

Also, when you're reading code and see `ALLERGENS["eggs"] == 1`, it's immediately obvious what's happening. With Option A, you'd have to remember that index 0 means 2^0, etc.

Go with B.

**Pair:**

Assistant: Solid reasoning — the "silent reorder bug" is real, and for a fixed spec where the values *are* the semantics, explicitness wins. I'd have gone with the list for DRY reasons, but your argument holds up.

Let me write the foundation with the dict, then we'll tackle the two functions:

[Glob(allergies.py)]
  No files found

[Write(allergies.py)]
ALLERGENS = {
    "eggs": 1, "peanuts": 2, "shellfish": 4,
    "strawberries": 8, "tomatoes": 16,
    "chocolate": 32, "pollen": 64, "cats": 128,
}


def is_allergic_to(score, allergen):
    pass


def allergies(score):
… (2 more lines)

Assistant: Now, `is_allergic_to`. The bit-check is the core of this whole problem. Two ways to write it — which is correct, and why?

**Option A:**
```python
def is_allergic_to(score, allergen):
    return score & ALLERGENS[allergen] == 1
```

**Option B:**
```python
def is_allergic_to(score, allergen):
    return bool(score & ALLERGENS[allergen])
```

---

## Turn 3

**User:**

**B** — `bool(score & ALLERGENS[allergen])`

Option A is a trap. It checks if the result equals exactly 1, but that only works for eggs (value 1). For any other allergen like strawberries (value 8), if the bit is set, `score & 8` returns 8, not 1, so `8 == 1` is False — incorrectly saying you're not allergic.

Option B checks if the AND result is non-zero, which works for *all* bit positions. If the bit is set, we get a non-zero result (truthy); if not, we get 0 (falsy).

The `bool()` wrapping makes the intent explicit too — "convert the bit-check to a boolean result."

**Pair:**

Assistant: Spot on — `score & 128` gives `128`, not `1`, so `== 1` silently fails for everything but eggs. The non-zero check is the right pattern for any bitfield test.

[Edit(allergies.py)]
--- before
def is_allergic_to(score, allergen):
    pass
--- after
def is_allergic_to(score, allergen):
    return bool(score & ALLERGENS[allergen])

Assistant: Now `allergies()`. Two reasonable implementations — which would you pick?

**Option A:**
```python
def allergies(score):
    return [a for a, val in ALLERGENS.items() if score & val]
```

**Option B:**
```python
def allergies(score):
    return [a for a in ALLERGENS if is_allergic_to(score, a)]
```

---

## Turn 4

**User:**

**B** — `return [a for a in ALLERGENS if is_allergic_to(score, a)]`

Here's why:

1. **DRY**: We already wrote the bit-check logic in `is_allergic_to()`. Option A duplicates it (`score & val`).

2. **Single source of truth**: If the bit-checking semantics ever need to change, you fix it in one place, not two.

3. **Clarity**: Reading `is_allergic_to(score, a)` immediately says "list the allergens I'm allergic to." Option A requires you to re-understand `score & val` in a different context.

4. **Confidence**: We already validated that `is_allergic_to()` works. Reusing it here means we're testing the same logic we know is correct.

Option A is fine — more direct, slightly faster — but for 8 items the performance difference is nothing, and Option B is clearer and more maintainable.

**Pair:**

Assistant: All four points are solid. "Slightly faster for 8 items" is a non-argument — readability and correctness of composition win here.

[Edit(allergies.py)]
--- before
def allergies(score):
    pass
--- after
def allergies(score):
    return [a for a in ALLERGENS if is_allergic_to(score, a)]

[Read(allergies.py)]
  1	ALLERGENS = {
  2	    "eggs": 1, "peanuts": 2, "shellfish": 4,
  3	    "strawberries": 8, "tomatoes": 16,
  4	    "chocolate": 32, "pollen": 64, "cats": 128,
  5	}
  6	
  7	
  8	def is_allergic_to(score, allergen):
  9	    return bool(score & ALLERGENS[allergen])
  10	
  11	
  12	def allergies(score):
  … (2 more lines)

Assistant: Done. Clean and complete.

One thing worth knowing: scores above 255 work correctly here without any extra handling. A score of `257` (= 256 + 1) still returns `["eggs"]` because we only ever test the 8 known bits — the higher bits are simply never `&`-ed against. No `score % 256` guard needed.

---

## Turn 5 (final)

**User:**

Looks good. The logic is sound, and I like how you walked through the edge case (scores > 255). The code is clean and correct.

<done/>

---

**Run end**: done after 4 turns (168s)
