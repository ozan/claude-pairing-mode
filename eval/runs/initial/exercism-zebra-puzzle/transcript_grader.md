# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:01:50

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

[Glob(zebra_puzzle*)]
  No files found

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good first design question before we write a line: the puzzle has 5 attributes × 5 values, so naïvely we'd iterate all 5!⁵ ≈ 25 billion combos. There's a smarter structure.

OPTIONS:
[A] Flat cross-product
Generate all five `permutations(range(5))` independently, zip them into one big loop, then check all 15 constraints at the end.
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,7 @@
+for nat, col, bev, smk, pet in product(
+        permutations(range(5)),  # nationality
+        permutations(range(5)),  # color
+        permutations(range(5)),  # beverage
+        permutations(range(5)),  # smoke
+        permutations(range(5))): # pet
+    if all_constraints_hold(...): ...
```

[B] Nested with early pruning
Nest the five `for … in permutations(…)` loops and check relevant constraints at each level, before entering the next loop.
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,10 @@
+for nat in permutations(range(5)):
+    if not nat_constraints_hold(nat): continue
+    for col in permutations(range(5)):
+        if not nat_col_constraints_hold(nat, col): continue
+        for bev in permutations(range(5)):
+            ...
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which structure do you want to go with?

### Student

I think I'd like to go with **B** — nested with early pruning.

Even though A is simpler to write, B makes more sense to me because it lets us throw away invalid branches early instead of wasting time on 5!^5 combos that fail halfway through. If we can rule out a nationality assignment before we even start testing colors, that saves us from checking 5!^4 useless color combinations.

Can we start by setting up the basic structure and defining what the constraints actually are? I want to make sure I understand which constraints depend on which attributes so I know where to check them in the nested loops.

---

## Turn 2

### Tutor

Tutor: Exactly right — that's the core insight. Before writing code, there's one more design choice that determines how clean every single constraint looks. How should each permutation represent its data?

OPTIONS:
[A] Position → value
`nat[2] == ENGLISH` means house 2 has the Englishman. Constraints need a lookup:
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,4 @@
+# "Englishman lives in red house"
+if nat.index(ENGLISH) != col.index(RED):
+    continue
+# "Green immediately right of ivory"
+if col.index(GREEN) != col.index(IVORY) + 1:
+    continue
```

[B] Value → position
`nat[ENGLISH] == 2` means the Englishman is in house 2. Constraints read directly:
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,4 @@
+# "Englishman lives in red house"
+if nat[ENGLISH] != col[RED]:
+    continue
+# "Green immediately right of ivory"
+if col[GREEN] != col[IVORY] + 1:
+    continue
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which representation do you prefer?

### Student

**B** — value → position, definitely.

In option A, every constraint needs `.index()` calls which feel clunky and harder to read. With B, the constraints are almost self-documenting: `nat[ENGLISH] != col[RED]` reads naturally as "the Englishman's house number doesn't match the red house's house number."

Plus, since we're iterating through permutations anyway, it's natural to build up the mapping as we go — each permutation already gives us the value-to-position relationship we need.

So I'm ready to start coding. Should I define constants for the attribute values first (like `ENGLISH = 0, SPANIARD = 1, ...`)? And do you want me to write out all 15 constraints from the puzzle, or should we tackle them incrementally as we build?

---

## Turn 3

### Tutor

Tutor: Yes — define all constants up front, write all constraints at once organized by loop level. The whole structure fits cleanly and you'll see exactly why each constraint lives where it does. Let me write the file:

[Bash(ls zebra_puzzle.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(zebra_puzzle.py)]
from itertools import permutations

# Each constant is an index into its permutation tuple.
# perm[VALUE] = house position (0 = leftmost … 4 = rightmost)
ENGLISH, SPANISH, UKRAINIAN, NORWEGIAN, JAPANESE = range(5)
RED, GREEN, IVORY, YELLOW, BLUE = range(5)
COFFEE, TEA, MILK, OJ, WATER = range(5)
OLD_GOLD, KOOLS, CHESTERFIELDS, LUCKY_STRIKE, PARLIAMENTS = range(5)
DOG, SNAILS, FOX, HORSE, ZEBRA = range(5)

NAMES = ["Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese"]

… (66 more lines)
  File created successfully at: zebra_puzzle.py

Tutor: Now — notice `drinks_water()` and `owns_zebra()` each call `solve()` independently. Quick question:

OPTIONS:
[A] Cache at module level
Compute once when the module loads and reuse:
```diff
+++ zebra_puzzle.py
@@ -54,8 +54,8 @@
-def drinks_water():
-    nat, col, bev, smk, pet = solve()
-    return NAMES[nat.index(bev[WATER])]
-
-def owns_zebra():
-    nat, col, bev, smk, pet = solve()
-    return NAMES[nat.index(pet[ZEBRA])]
+_solution = solve()
+
+def drinks_water():
+    nat, col, bev, smk, pet = _solution
+    return NAMES[nat.index(bev[WATER])]
+
+def owns_zebra():
+    nat, col, bev, smk, pet = _solution
+    return NAMES[nat.index(pet[ZEBRA])]
```

[B] Leave as two solve() calls
Each function is self-contained; the puzzle solves fast enough that repeating it doesn't matter in practice. Simpler, no shared state.

(Reply with A or B, or ask a follow-up question.)

### Student

I'd go with **A** — cache at module level.

The puzzle is deterministic, so there's only ever one solution. Calling `solve()` twice and computing the exact same thing twice is wasteful, even if it's fast. Caching it makes the functions cleaner and the intent clearer: "here's the answer, use it."

Let me check the file you created — I want to see the actual constraint structure and the `solve()` function to understand how everything fits together before we test it.

---

## Turn 4

### Tutor

[Read(zebra_puzzle.py)]
  1	from itertools import permutations
  2	
  3	# Each constant is an index into its permutation tuple.
  4	# perm[VALUE] = house position (0 = leftmost … 4 = rightmost)
  5	ENGLISH, SPANISH, UKRAINIAN, NORWEGIAN, JAPANESE = range(5)
  6	RED, GREEN, IVORY, YELLOW, BLUE = range(5)
  7	COFFEE, TEA, MILK, OJ, WATER = range(5)
  8	OLD_GOLD, KOOLS, CHESTERFIELDS, LUCKY_STRIKE, PARLIAMENTS = range(5)
  9	DOG, SNAILS, FOX, HORSE, ZEBRA = range(5)
  10	
  11	NAMES = ["Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese"]
  12	
  … (66 more lines)

Tutor: Good — the structure is exactly what we designed. Now applying the cache:

[Edit(zebra_puzzle.py)]
--- before
def drinks_water():
    nat, col, bev, smk, pet = solve()
    return NAMES[nat.index(bev[WATER])]


def owns_zebra():
    nat, col, bev, smk, pet = solve()
    return NAMES[nat.index(pet[ZEBRA])]
--- after
_solution = solve()


def drinks_water():
    nat, col, bev, smk, pet = _solution
    return NAMES[nat.index(bev[WATER])]


def owns_zebra():
    nat, col, bev, smk, pet = _solution
    return NAMES[nat.index(pet[ZEBRA])]
  The file zebra_puzzle.py has been updated successfully.

Tutor: Here's a quick tour of the structure:

**Constants** (lines 5–9): `ENGLISH = 0`, `SPANISH = 1`, etc. — these are just indices. Same numbering reused per group, which is fine since they index different tuples.

**`next_to(a, b)`** — the only helper needed; two houses are adjacent when their positions differ by exactly 1.

**`solve()` — constraint placement by level:**
| Loop | Constraints checked before going deeper |
|------|----------------------------------------|
| `nat` | Norwegian at pos 0 *(1 clue, purely positional)* |
| `col` | Englishman=red, green right of ivory, Norwegian next to blue *(3 clues)* |
| `bev` | Milk in middle, Ukrainian=tea, coffee=green *(3 clues)* |
| `smk` | Kools=yellow, Japanese=Parliaments, LuckyStrike=OJ *(3 clues)* |
| `pet` | Spaniard=dog, OldGold=snails, Chesterfields↔fox, Kools↔horse *(4 clues)* |

**`nat.index(bev[WATER])`** — this is the reverse lookup: `bev[WATER]` is the house position of water; `.index()` on the `nat` tuple finds *which* nationality index occupies that position.

Let's run it:

[Bash(python3 -c "import zebra_puzzle; print('Drinks water:', zebra_puzzle.drinks_water()); print('Owns zebra:', zebra_puzzle.owns_zebra())")]
  Drinks water: Norwegian
  Owns zebra: Japanese

Tutor: **Norwegian drinks water, Japanese owns the zebra** — the canonical answers. 

One thing worth noting: `_solution` is computed at *import time*. That's fine here since `solve()` is a pure, fast computation — but it's a pattern to be careful with for expensive or side-effectful module-level code. Want to run the Exercism test suite against it, or is there anything in the solution you'd like to dig into further?

### Student

Perfect! The solution works and the answers match the expected result. 

I'm satisfied with how it came together. The nested structure with early pruning was a great design choice, and the value→position representation made the constraints read naturally. I also appreciate how the constraint placement by loop level is so clear — each level only checks what it needs before going deeper.

The caching at module level makes sense too, since the puzzle is deterministic and fast.

I think this is ready. I don't need to dig deeper into the solution or run additional tests — the core problem is solved cleanly.

<done/>

---

**Run end:** done after 4 turn(s) in 158.9s
