# exercism-zebra-puzzle

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:53:42.163Z

---

## Turn 1

**User:**

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

**Pair:**

Thinking: The user wants to solve the classic Zebra Puzzle (also known as Einstein's Riddle) using Python. Let me think about the puzzle first.
  
  The classic Zebra Puzzle has these clues:
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
  
  The puzzle asks who drinks water and who owns the zebra. For the Exercism version, I need to implement a `ZebraPuzzle` class with methods that return these answers. I'm considering the best approach to solve this—likely using constraint satisfaction or brute force to test all possible house configurations against the clues.
  
  I'm thinking through the structure: each of the 5 houses needs a nationality, color, drink, cigarette brand, and pet. The brute force approach would generate permutations of these attributes and test them against all the constraints, though that's computationally intensive with millions of combinations to check.
  
  Writing the solver function... Writing constraint checks... Still writing constraint checks...
  
  Actually, I'm realizing the indexing approach is getting messy. Let me restructure this to use house dictionaries or a cleaner data model instead, and then implement the ZebraPuzzle class with the required methods for finding who drinks water and who owns the zebra.
  
  Building the solver class... Still writing constraint checks... I need to verify that the mapping is correct—`nats` contains the house numbers for each nation, so zipping them with the nation names gives me the right lookup table. Now I'm thinking about whether to present just the brute force approach with pruning or also show a constraint solver alternative, since both have merit depending on the use case.
  
  The permutations approach is simpler and doesn't require external dependencies, making it ideal for Exercism, though a constraint solver would be more declarative. I'll go with the permutations strategy and focus the teaching moment on how to structure the search effectively—either with nested loops and early pruning or by generating all combinations upfront and filtering them.
  
  The brute force approach of generating all possible permutations and then filtering would create an astronomical number of iterations, so early pruning through nested loops is clearly the way to go.

Assistant: Good puzzle — it's a classic constraint-satisfaction problem. Before I write any code, let me ask about the core approach:

OPTIONS:
[A] Flat product + filter
Generate all 5-attribute combinations with `itertools.product(permutations(houses), repeat=5)`, then filter by all constraints at once.

[B] Nested loops + prune early
5 nested `for perm in permutations(houses)` loops, applying each attribute's constraints *before* entering the next loop.

(Reply with A or B, or ask a follow-up question.)

Assistant: **A**: Flat product + filter — generate all 5-attribute combinations with `itertools.product(permutations(houses), repeat=5)`, then filter by all constraints at once.

**B**: Nested loops + prune early — 5 nested `for perm in permutations(houses)` loops, applying each attribute's constraints *before* entering the next loop.

Which approach do you prefer?

---

## Turn 2

**User:**

I think **B** makes more sense here. 

Option A would generate millions of combinations upfront (120^5 is huge!), and most of them would fail the constraints. It feels wasteful to generate everything and *then* filter.

With option B, we can check constraints like "the Norwegian is in house 1" or "green is right of ivory" as soon as we assign attributes to a house. That should cut down the search space dramatically before we even get to later attributes.

Should we start by setting up the data structure and then writing the constraint checks?

**Pair:**

Thinking: The user correctly identified why B is better. They understand the pruning benefit. Let me agree and proceed to write the code. 
  
  Let me start with creating the file. I should check if it exists first.
  
  The Exercism exercise expects a file called `zebra_puzzle.py` (or similar). Let me check the current directory.
  
  Actually, let me just start writing the code. I'll use the Write tool to create the file after checking if it exists.
  
  Let me think about how to structure this. The Exercism zebra puzzle exercise expects:
  - A class `ZebraPuzzle` with methods `drinks_water()` and `owns_zebra()`
  
  
  - I need to decide on the data representation: should I use a dict mapping houses to attributes, or separate permutation arrays for each attribute type?
  
  Writing the solution... to represent the permutations. This is a subtle but important design decision:
  
  Option A: permutations of house numbers (1-5), where index = attribute value index
  - `nats = (3, 1, 2, 5, 4)` means Englishman=house3, Spaniard=house1, etc.
  
  Option B: permutations of attribute indices (0-4), where index = house number
  - `nats = (2, 0, 1, 4, 3)` means house1=Ukrainian, house2=Englishman, etc.
  
  Both work, but Option A (value → house) makes constraint checking like `if eng != red` more readable (both are house numbers). Option B (house → value) makes reverse lookup easier.
  
  Actually Option A is cleaner for constraint checking. I'll go ahead and implement this approach using permutations of house positions for each attribute, then check if there's already a file in the directory.

Assistant: Exactly right — you nailed the asymmetry. Pruning after "Norwegian = house 1" alone eliminates 96% of nation permutations before touching colors at all.

Let me check for any existing file first:

[Glob(zebra_puzzle.py)]
  No files found

Assistant: Clean slate. Before I write anything, one design question — it shapes every constraint check:

OPTIONS:
[A] Perm = house → attribute
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,5 @@
+# nats[house_index] = which nation lives there
+# e.g. nats = ('Norwegian','Englishman',...)
+for nats in permutations(NATIONS):
+    english_house = nats.index('Englishman') + 1
+    red_house     = cols.index('Red') + 1
```

[B] Perm = attribute → house
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,5 @@
+# nats = (eng_house, spa_house, ukr_house, nor_house, jap_house)
+# e.g. nats = (3, 1, 2, 5, 4)
+for nats in permutations(range(1, 6)):
+    eng, spa, ukr, nor, jap = nats
+    if eng == red:  # both are house numbers — direct compare
```

(Reply with A or B, or ask a follow-up question.)

Assistant: **A**: Perm = house → attribute — `nats[house_index]` gives the nation; look up with `.index()` when you need the house number.

**B**: Perm = attribute → house — unpack directly as `eng, spa, ukr, nor, jap = nats`; every value *is* a house number, so constraints become `if eng == red`.

Which feels cleaner to you?

---

## Turn 3

**User:**

I think **B** is cleaner. 

In option A, every constraint check needs a `.index()` lookup — like "find which house the Englishman is in" — which feels roundabout. With option B, the constraint check is just `if eng == red`, which is immediate and reads like the actual puzzle clue. Both are house numbers, so the comparison is direct.

Plus option B avoids the string lookups entirely, which should be faster when we're iterating through thousands of permutations.

Ready to start writing the nested loops with constraint checks?

**Pair:**

Thinking: The user correctly identified why B is better. Now let me write the full solution. Let me create the `zebra_puzzle.py` file.
  
  The structure will be:
  1. Import `itertools.permutations`
  2. Create a `ZebraPuzzle` class with `drinks_water()` and `owns_zebra()` methods
  3. Solve in `__init__` using nested permutations with early pruning
  
  Let me think through all the constraints:
  1. There are 5 houses (numbered 1-5, left to right)
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
  
  Now I'm setting up the constraint satisfaction problem with the attribute categories and their possible values, then starting to assign constraints in order of maximum pruning efficiency—beginning with the Norwegian's position in house one. ue 10) — eliminates 96% immediately
  2. Colors: eng == red (clue 2), grn == ivo + 1 (clue 6), nor next to blu (clue 15)
  3. Drinks: cof == grn (clue 4), ukr == tea (clue 5), mlk == 3 (clue 9)
  4. Smokes: koo == yel (clue 8), luc == ojc (clue 13), jap == par (clue 14)
  5. Pets: spa == dog (clue 3), old == sna (clue 7), |che - fox| == 1 (clue 11), |koo - hor| == 1 (clue 12)
  
  Now I need to set up the reverse lookup to find which nation occupies the water and zebra houses — I'll create a nations tuple with the house positions for each nationality, then search through it to match against the target houses and return the corresponding nation name.

Assistant: Perfect reasoning on both counts. Let's build it now.

[Write(zebra_puzzle.py)]
from itertools import permutations

# Attribute order within each permutation tuple:
NATIONS = ('Englishman', 'Spaniard', 'Ukrainian', 'Norwegian', 'Japanese')
DRINKS  = ('Coffee', 'Tea', 'Milk', 'OJ', 'Water')
PETS    = ('Dog', 'Snails', 'Fox', 'Horse', 'Zebra')


class ZebraPuzzle:
    def __init__(self):
        self._water_drinker, self._zebra_owner = self._solve()

… (60 more lines)

Assistant: Let's verify it actually runs and gives the right answers:

[Bash(cd /Users/ozan/exercism/python/zebra-puzzle && python -c "
from zebra_puzzle import ZebraPuzzle
import time
start = time.perf_counter()
p = ZebraPuzzle()
elapsed = time.perf_counter() - start
print(f'Drinks water: {p.drinks_water()}')
print(f'Owns zebra:   {p.owns_zebra()}')
print(f'Solved in:    {elapsed*1000:.1f} ms')
"
)]
  error: Exit code 1

[Bash(python zebra_puzzle.py 2>/dev/null; python -c "
from zebra_puzzle import ZebraPuzzle
import time
start = time.perf_counter()
p = ZebraPuzzle()
elapsed = time.perf_counter() - start
print(f'Drinks water: {p.drinks_water()}')
print(f'Owns zebra:   {p.owns_zebra()}')
print(f'Solved in:    {elapsed*1000:.1f} ms')
")]
  error: Exit code 127

[Bash(python3 -c "
from zebra_puzzle import ZebraPuzzle
import time
start = time.perf_counter()
p = ZebraPuzzle()
elapsed = time.perf_counter() - start
print(f'Drinks water: {p.drinks_water()}')
print(f'Owns zebra:   {p.owns_zebra()}')
print(f'Solved in:    {elapsed*1000:.1f} ms')
")]
  Drinks water: Norwegian
  Owns zebra:   Japanese
  Solved in:    0.2 ms

Assistant: **Norwegian** drinks water, **Japanese** owns the zebra — and it solves in 0.2 ms.

---

A few things worth noting in the implementation:

**Constraint ordering is the whole ballgame.** We apply the cheapest, most-selective checks first:
- `nor != 1` immediately drops 96% of nation permutations (only 24 out of 120 pass)
- `mlk != 3` then `cof != grn` collapse the drink space fast
- The "next to" checks on `che/fox` and `koo/hor` are left last since they need values from two different attribute groups

**`house_to_nation = dict(zip(nats, NATIONS))`** — this works because `nats` is the tuple of house numbers in the same order as `NATIONS` (Englishman, Spaniard, …). So `dict(zip(nats, NATIONS))` maps `house_number → nation_name`, and `house_to_nation[wat]` gives you whoever lives where water is drunk.

**`grn - ivo != 1`** instead of `next_to` — clue 6 is *directional* ("immediately to the right"), so we check `grn - ivo == 1` specifically, not `abs(grn - ivo) == 1`. Using `next_to` here would be a subtle bug that would still find a solution — just potentially the wrong one if there were multiple valid arrangements with ivory-green swapped.

---

## Turn 4 (final)

**User:**

Ah, that's really insightful — especially the constraint ordering point. I was thinking of them as all equally important, but it makes total sense that `nor != 1` ruling out 96% of nation permutations upfront means we avoid exploring billions of invalid combinations in the later attribute loops. It's like early failure detection compounding through the nested loops.

And the `grn - ivo == 1` vs `abs(grn - ivo) == 1` distinction is exactly the kind of subtle bug I'd have missed — the puzzle says "immediately to the right," which is directional, not just "adjacent." Good catch flagging that.

The solution is working cleanly and I understand the core strategy: pick the right data representation (option B), order constraints by selectivity to prune early, and handle directional constraints carefully. This gives me a solid template for other constraint problems too.

<done/>

---

**Run end**: done after 3 turns (154s)
