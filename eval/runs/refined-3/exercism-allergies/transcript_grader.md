# exercism-allergies

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:39

## Initial prompt

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good problem — let's start with the allergen data. Since each allergen maps to a power-of-2 value, how we store that mapping shapes everything else.

OPTIONS:
[A] Plain dict
```diff
+++ allergies.py
@@ -0,0 +1,12 @@
+ALLERGENS = {
+    "eggs":         1,
+    "peanuts":      2,
+    "shellfish":    4,
+    "strawberries": 8,
+    "tomatoes":    16,
+    "chocolate":   32,
+    "pollen":      64,
+    "cats":       128,
+}
```
String keys, integer values. Easy to look up by name.

[B] IntEnum
```diff
+++ allergies.py
@@ -0,0 +1,12 @@
+from enum import IntEnum
+
+class Allergen(IntEnum):
+    EGGS         =   1
+    PEANUTS      =   2
+    SHELLFISH    =   4
+    STRAWBERRIES =   8
+    TOMATOES     =  16
+    CHOCOLATE    =  32
+    POLLEN       =  64
+    CATS         = 128
```
Each member *is* an int — bitwise ops work directly on it, and the class is iterable.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you go with as the base?

### Student

I think I'd go with **B (IntEnum)**.

Here's my reasoning: since we're doing bitwise operations, having the allergen values *be* integers directly feels cleaner. And if we need to iterate over all allergens (which we probably do for the `allergies()` function to return the list), IntEnum lets us loop over `Allergen` members naturally.

With a plain dict, I'd have to iterate over `.keys()` or `.values()` and manage the mapping more manually. The IntEnum feels more purpose-built for this use case.

---

## Turn 2

### Tutor

Tutor: Exactly right on all counts — especially the iteration point, which pays off immediately in `allergies()`.

[Write(allergies.py)]
from enum import IntEnum

class Allergen(IntEnum):
    EGGS         =   1
    PEANUTS      =   2
    SHELLFISH    =   4
    STRAWBERRIES =   8
    TOMATOES     =  16
    CHOCOLATE    =  32
    POLLEN       =  64
    CATS         = 128

  File created successfully at: allergies.py

Tutor: Now for `is_allergic_to(score, allergen)` — `allergen` arrives as a lowercase string like `"eggs"`. Two ways to check the bit:

OPTIONS:
[A] Modulo arithmetic
```diff
+++ allergies.py
@@ -9,0 +10,3 @@
+def is_allergic_to(score, allergen):
+    val = Allergen[allergen.upper()]
+    return (score % (val * 2)) >= val
```
For any power-of-2 `val`, `score mod 2val ≥ val` iff that bit is set.

[B] Bitwise AND
```diff
+++ allergies.py
@@ -9,0 +10,3 @@
+def is_allergic_to(score, allergen):
+    val = Allergen[allergen.upper()]
+    return bool(score & val)
```
Mask the score with the allergen's flag; non-zero means the bit is set.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'd go with **B (Bitwise AND)**.

It's more direct and idiomatic for bitfield operations. When you're working with flags, `score & val` is the standard way to check if a bit is set — it's what bitfields are designed for. The modulo approach works mathematically, but it's less readable and feels like a workaround.

Also, `bool(score & val)` is clearer about intent: "is this bit present in the score?" versus "does the remainder fall in this range?" The bitwise version is what someone familiar with bit manipulation would immediately recognize.

---

## Turn 3

### Tutor

Tutor: Spot on. The modulo trick is a fun math curiosity but `&` is the right tool — and since `IntEnum` members *are* ints, it just works.

[Read(allergies.py)]
  1	from enum import IntEnum
  2	
  3	class Allergen(IntEnum):
  4	    EGGS         =   1
  5	    PEANUTS      =   2
  6	    SHELLFISH    =   4
  7	    STRAWBERRIES =   8
  8	    TOMATOES     =  16
  9	    CHOCOLATE    =  32
  10	    POLLEN       =  64
  11	    CATS         = 128
  12

[Edit(allergies.py)]
--- before
    CATS         = 128

--- after
    CATS         = 128

def is_allergic_to(score, allergen):
    val = Allergen[allergen.upper()]
    return bool(score & val)

  The file allergies.py has been updated successfully.

Tutor: Now `allergies(score)` — one decision worth thinking about:

OPTIONS:
[A] Reuse is_allergic_to
```diff
+++ allergies.py
@@ -14,0 +15,3 @@
+def allergies(score):
+    return [a.name.lower() for a in Allergen
+            if is_allergic_to(score, a.name.lower())]
```
DRY — delegates to the already-defined function.

[B] Direct bitwise check
```diff
+++ allergies.py
@@ -14,0 +15,3 @@
+def allergies(score):
+    return [a.name.lower() for a in Allergen
+            if score & a]
```
Iterates `Allergen` members directly; each member IS an int.

(Reply with A or B, or ask a follow-up question.)

### Student

I'd go with **B (Direct bitwise check)**.

Since we're already iterating over `Allergen` members and they're `IntEnum` values (meaning they *are* integers), we can use the bitwise AND directly without the extra function call. It's simpler and more efficient — we don't need to convert back to a string and then look it up again.

Option A works fine, but it's doing unnecessary work: converting `a.name` to lowercase, looking it up in the enum by string key, and then doing the bitwise check. Option B is more direct and leverages the fact that `IntEnum` members are already the integer values we need.

---

## Turn 4

### Tutor

Tutor: Exactly — the round-trip in option A is a code smell that reveals `is_allergic_to` was designed for *external* string callers, not internal iteration. Good call.

[Read(allergies.py)]
  1	from enum import IntEnum
  2	
  3	class Allergen(IntEnum):
  4	    EGGS         =   1
  5	    PEANUTS      =   2
  6	    SHELLFISH    =   4
  7	    STRAWBERRIES =   8
  8	    TOMATOES     =  16
  9	    CHOCOLATE    =  32
  10	    POLLEN       =  64
  11	    CATS         = 128
  12	
  … (4 more lines)

[Edit(allergies.py)]
--- before
def is_allergic_to(score, allergen):
    val = Allergen[allergen.upper()]
    return bool(score & val)

--- after
def is_allergic_to(score, allergen):
    val = Allergen[allergen.upper()]
    return bool(score & val)

def allergies(score):
    return [a.name.lower() for a in Allergen if score & a]

  The file allergies.py has been updated successfully.

Tutor: The solution is functionally complete. One last thing worth thinking about — the Exercism tests include scores **above 255** (e.g. `score=509`). How should `allergies()` behave?

OPTIONS:
[A] Normalize score first
```diff
+++ allergies.py
@@ -18,2 +18,3 @@
 def allergies(score):
-    return [a.name.lower() for a in Allergen if score & a]
+    score %= 256
+    return [a.name.lower() for a in Allergen if score & a]
```
Clamp to 8 bits before checking, making the intent explicit.

[B] Leave it as-is
```diff
+++ allergies.py
@@ -18,1 +18,1 @@
 def allergies(score):
     return [a.name.lower() for a in Allergen if score & a]
```
No change needed — iteration only visits the 8 defined allergen bits regardless of what's in the upper bits.

(Reply with A or B, or ask a follow-up question.)

### Student

I'd go with **B (Leave it as-is)**.

The bitwise AND operation naturally handles this — when we check `score & a` for each allergen, we're only checking the specific bits that correspond to the defined allergens (1 through 128). Any bits above 128 don't matter because none of our `Allergen` enum members have those bits set. So `509 & 1` still correctly identifies the eggs bit, `509 & 2` checks peanuts, etc.

Adding `score %= 256` would work, but it's unnecessary noise. The code already does the right thing without it — we're not losing anything by leaving higher bits alone, and the iteration implicitly handles the constraint.

---

## Turn 5

### Tutor

Tutor: Nailed it. The iteration *is* the constraint — you can't accidentally check a bit that no allergen occupies. `% 256` would be defensive programming against a problem that the data model already prevents.

Here's the finished solution:

[Read(allergies.py)]
  1	from enum import IntEnum
  2	
  3	class Allergen(IntEnum):
  4	    EGGS         =   1
  5	    PEANUTS      =   2
  6	    SHELLFISH    =   4
  7	    STRAWBERRIES =   8
  8	    TOMATOES     =  16
  9	    CHOCOLATE    =  32
  10	    POLLEN       =  64
  11	    CATS         = 128
  12	
  … (7 more lines)

Tutor: Clean and complete. The decisions all reinforce each other:

- **`IntEnum`** — members are ints, so `score & a` just works, and the class is iterable so `allergies()` is a one-liner
- **`score & val`** — canonical bitmask test, expresses intent directly
- **No `% 256`** — the enum's domain already constrains which bits get checked

One thing to keep in mind if you extend this: `Allergen["BAD_STRING"]` raises a `KeyError`. For a kata that's fine, but in production you'd want to decide whether `is_allergic_to` should fail loudly (let it raise) or return `False` for unknown allergens — those are meaningfully different contracts.

### Student

That's a really helpful note. I appreciate the distinction — in the kata context, letting it raise is probably fine since the tests will only pass valid allergen names. But I can see how in production code, that choice matters a lot depending on the caller's expectations.

This was a great walkthrough. I learned a lot about how `IntEnum` makes bitfield operations natural, how to recognize when reusing a function adds unnecessary work, and how the data model itself can enforce constraints without explicit normalization. The whole solution is elegant precisely because each piece supports the others.

Thanks for the learning!

<done/>

---

**Run end:** done after 5 turn(s) in 157.8s
