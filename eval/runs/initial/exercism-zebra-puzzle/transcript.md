# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:01:50

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

Thinking: The user wants to solve the classic Zebra Puzzle (also known as Einstein's Puzzle) from Exercism. Let me think about the best approach before proposing options.
  
  The Zebra Puzzle constraints:
  1. There are five houses.
  2. The Englishman lives in the red house.
  3. The Spaniard owns the dog.
  4. Coffee is drunk in the green house.
  5. The Ukrainian drinks tea.
  6. The green house is immediately to the right of the ivory house.
  7. The Old Gold smoker owns snails.
  8. Kools are smoked in the yellow house.
  9. Milk is drunk in the middle house.
  
  
  10. The Norwegian lives in the first house.
  11. The man who smokes Chesterfields lives in the house next to the man with the fox.
  12. Kools are smoked in the house next to the house where the horse is kept.
  13. The Lucky Strike smoker drinks orange juice.
  14. The Japanese smokes Parliaments.
  15. The Norwegian lives next to the blue house.
  
  I'm considering two main approaches: a brute force method using permutations to generate all possible combinations and check constraints, or a constraint satisfaction approach that prunes the search space more intelligently. The permutation method is simpler to implement but computationally expensive with billions of potential combinations to evaluate.
  
  The more efficient strategy would be to apply constraints progressively as I build up each attribute group, filtering out invalid combinations early rather than checking everything at the end. This dramatically reduces the search space compared to exhaustively testing all 5!^5 possibilities.

[Glob(zebra_puzzle*)]
  No files found

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Good, the tool is loaded. Let me think about the best approach for the Zebra Puzzle.
  
  The puzzle has 5 attributes × 5 values each. Brute force over all 5!^5 ≈ 24.8 billion combinations is way too slow. But if we apply constraints incrementally as we build up permutations, we can prune the search space dramatically.
  
  The key design question is: do we enumerate all 5 attribute permutations independently and then check all constraints, or do we enumerate one attribute at a time and filter constraints that only involve already-assigned attributes?
  
  
  I could go with a straightforward brute force approach that generates all permutations of each attribute and checks all 15 constraints at the end, but that means iterating through 24.8 billion combinations. The smarter approach is to build up house tuples incrementally, applying relevant constraints as we assign each attribute to prune the search space early. Let me go with the incremental filtering strategy using itertools.permutations. I'm recognizing that nested constraint checking with early pruning is significantly more efficient than checking everything at the end—this is a valuable lesson about constraint propagation and how early termination can dramatically reduce the search space.

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

PRIVATE: best=B
PRIVATE: rationale=Nested with early pruning is dramatically faster. Each constraint that involves only the attributes assigned so far can eliminate entire subtrees. For example, once we know nationalities don't satisfy "Norwegian lives in house 1", we skip all 120^4 ≈ 200M color/bev/smoke/pet combos for that nationality permutation. The flat approach must evaluate all 25B combos. The nested approach runs in milliseconds in practice. This is the core lesson about constraint propagation / branch-and-bound search.

Tutor: Which structure do you want to go with?

### Student

I think I'd like to go with **B** — nested with early pruning.

Even though A is simpler to write, B makes more sense to me because it lets us throw away invalid branches early instead of wasting time on 5!^5 combos that fail halfway through. If we can rule out a nationality assignment before we even start testing colors, that saves us from checking 5!^4 useless color combinations.

Can we start by setting up the basic structure and defining what the constraints actually are? I want to make sure I understand which constraints depend on which attributes so I know where to check them in the nested loops.

---

## Turn 2

### Tutor

Thinking: The user correctly identified the key insight about early pruning. Let me now write the initial structure of the file.
  
  The Zebra Puzzle constraints:
  1. The Englishman lives in the red house. (nationality + color)
  2. The Spaniard owns the dog. (nationality + pet)
  3. Coffee is drunk in the green house. (color + beverage)
  4. The Ukrainian drinks tea. (nationality + beverage)
  5. The green house is immediately to the right of the ivory house. (color + color - positional)
  6. The Old Gold smoker owns snails. (smoke + pet)
  
  
  7. Kools are smoked in the yellow house. (color + smoke)
  8. Milk is drunk in the middle house. (beverage - positional)
  9. The Norwegian lives in the first house. (nationality - positional)
  10. The man who smokes Chesterfields lives in the house next to the man with the fox. (smoke + pet - positional)
  11. Kools are smoked in the house next to the house where the horse is kept. (smoke + pet - positional)
  12. The Lucky Strike smoker drinks orange juice. (smoke + beverage)
  13. The Japanese smokes Parliaments. (nationality + smoke)
  14. The Norwegian lives next to the blue house. (nationality + color - positional)
  
  Now I'm organizing the constraints by which attributes they involve and planning my search strategy. I'll iterate through permutations in order—nationalities first, then colors, beverages, smokes, and pets—checking constraints as I go to prune the search space early.
  
  For the representation, I'm deciding between two approaches: indexing permutations by value to get position (so `nat[ENGLISH] = 2` means the Englishman is in house 2), or indexing by position to get value (so `nat[2] = ENGLISH`). The first option is cleaner for constraints like "Englishman lives in red house" since I can directly compare `nat[ENGLISH] == col[RED]` without needing to search for positions.
  
  Defining constants for the puzzle...
  
  Now I'm organizing the constraints by when they can be checked during the solving process. After assigning nationalities, I verify the Norwegian is in the first house. Once colors are assigned too, I can check that the Englishman lives in the red house, the green house is immediately right of the ivory one, and the Norwegian is adjacent to the blue house. Then after beverages are added, I verify milk is in the middle house, the Ukrainian drinks tea, and coffee is in the green house.
  
  For the remaining constraints, once I assign cigarette brands, I check that kools are in the yellow house, the Japanese person smokes parliaments, and the lucky strike smoker drinks orange juice. Finally, after assigning pets, I verify the Spaniard owns a dog, the old gold smoker owns snails, and that chesterfields and fox owners are neighbors, as are kools smokers and horse owners. Setting up the solver structure... Still writing constraint checks... Finishing the constraint checks for adjacency, then returning the solution once all clues are satisfied. After that, I'm extracting helper functions to identify which person drinks water and which owns the zebra by looking up their position in the final solution.
  
  Now I'm reconsidering how the data structure works—`nat` is a permutation tuple where each index represents a nationality and its value represents which house they're in. So `nat[ENGLISH]` gives the house position of the Englishman, and to reverse that lookup (finding which nationality is at a specific house), I use `nat.index()` to find which nationality has that house position. This approach correctly maps from house position back to nationality name.
  
  I'm thinking about whether to present this solution with some pedagogical framing around the representation choice—specifically whether to use "value → position" mapping like this or the alternative "position → value" approach, since the constraint structure differs between them. I'm going to write out the solution using the value-to-position mapping since it makes the constraints so much cleaner to express.

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

PRIVATE: best=B
PRIVATE: rationale=Value→position makes every constraint a direct index comparison or arithmetic expression, with no `.index()` lookups. Since we have 14 constraints and they all take the same form (attr[X] == attr[Y] or abs(attr[X]-attr[Y])==1), option B is consistently cleaner and faster — .index() is O(n) and called inside the innermost loops. Position→value requires a reverse lookup every time, which obscures the structure and adds unnecessary cost.

Tutor: Which representation do you prefer?

### Student

**B** — value → position, definitely.

In option A, every constraint needs `.index()` calls which feel clunky and harder to read. With B, the constraints are almost self-documenting: `nat[ENGLISH] != col[RED]` reads naturally as "the Englishman's house number doesn't match the red house's house number."

Plus, since we're iterating through permutations anyway, it's natural to build up the mapping as we go — each permutation already gives us the value-to-position relationship we need.

So I'm ready to start coding. Should I define constants for the attribute values first (like `ENGLISH = 0, SPANIARD = 1, ...`)? And do you want me to write out all 15 constraints from the puzzle, or should we tackle them incrementally as we build?

---

## Turn 3

### Tutor

Thinking: The user wants to start coding. Let me write the initial file with the constants, the solve() skeleton, and all 14 constraints organized by loop level. I'll also include the `drinks_water()` and `owns_zebra()` functions.
  
  Let me think about what to write. I'll create the full file since it doesn't exist yet.
  
  The user is asking whether to define constants first and whether to tackle constraints incrementally or all at once. I should just go ahead and write the full file - the structure is clear enough that we can lay it all out at once, organized by loop level, which will be educational.
  
  Let me think about the teaching moment here. One good question: should we define the constants as `range(5)` tuple unpacking, or as individual assignments? The `range(5)` approach is Pythonic and concise. Both work the same way.
  
  
  I'll go ahead and write out the complete file with all the constants defined and the constraint structure laid out clearly.
  
  Defining the constraint solver... Still checking constraints...
  
  Now I'm finishing up the helper functions that extract the answer from the solved puzzle. Both `drinks_water()` and `owns_zebra()` call `solve()` independently, which means I'm solving the entire puzzle twice. I could optimize this with caching, but for Exercism's purposes where these functions are called separately, it's probably acceptable as-is. I'm realizing the key insight here is how to map from a house position back to a person's name—we need to find which nationality index corresponds to that position in the permutation, then use that to look up the name. I'll write out the complete solution file and then focus the teaching question on the `solve()` caching pattern.

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

PRIVATE: best=A
PRIVATE: rationale=The puzzle takes a fixed (small) amount of work regardless of how many times it's called. While the solve is fast (~milliseconds), calling it twice is redundant when both answers come from the same unique solution. Module-level caching is idiomatic Python for this pattern and avoids the conceptual smell of running the same search twice. It also means adding a third query later (e.g. "who smokes Parliaments?") costs nothing. The counter-argument is that module-level state runs at import time, but for a pure computation with no side effects this is fine.

### Student

I'd go with **A** — cache at module level.

The puzzle is deterministic, so there's only ever one solution. Calling `solve()` twice and computing the exact same thing twice is wasteful, even if it's fast. Caching it makes the functions cleaner and the intent clearer: "here's the answer, use it."

Let me check the file you created — I want to see the actual constraint structure and the `solve()` function to understand how everything fits together before we test it.

---

## Turn 4

### Tutor

Thinking: The user wants to see the file and also wants to apply the caching change. Let me read the file and then apply the edit.

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
