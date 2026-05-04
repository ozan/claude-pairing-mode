# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:24:52

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

Thinking: The user wants to solve the classic Zebra Puzzle (also known as Einstein's Puzzle or the Logic Puzzle). Let me think about the best approach before diving in.
  
  The puzzle has 5 houses, each with 5 attributes:
  - Nationality: Englishman, Spaniard, Ukrainian, Norwegian, Japanese
  - Color: Red, Green, Ivory, Yellow, Blue
  - Beverage: Coffee, Tea, Milk, Orange Juice, Water
  - Cigarette: Old Gold, Kools, Chesterfields, Lucky Strike, Parliaments
  - Pet: Dog, Snail, Fox, Horse, Zebra
  
  
  Now I'm going through the constraints that define the puzzle. There are 12 clues that establish relationships between the attributes—like the Englishman living in the red house, the Norwegian in the first house, and various adjacency and ownership rules that narrow down the possibilities.
  
  For solving this, I'm weighing two main approaches: a brute force method that generates all possible permutations and checks them against the constraints, versus a smarter constraint-based approach using backtracking or a CSP library. The brute force approach with permutations is straightforward and commonly used for this puzzle. The key insight is that instead of checking all 24.8 billion combinations blindly, I can nest the loops strategically and apply constraints early to eliminate invalid branches before they expand further.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me propose the first key design decision - the search strategy. The naive approach of generating all (5!)^5 combinations is computationally infeasible (~24.8 billion), while the smart approach nests loops and applies constraints early to prune the search space.

Tutor: Before writing any code, let's nail the search strategy. The puzzle has 5 attributes × 5 houses — that's 5 values each. Which approach do we take?

OPTIONS:
[A] Flat brute force
Generate all `(5!)^5` combinations upfront, then filter by all 14 clues at the end.

```diff
+++ zebra_puzzle.py
@@ -0,0 +1,7 @@
+from itertools import permutations, product
+
+def solve():
+    attrs = [permutations(range(5)) for _ in range(5)]
+    for combo in product(*attrs):
+        nat, color, drink, smoke, pet = combo
+        if check_all_clues(nat, color, drink, smoke, pet):
+            return answer(nat, drink, pet)
```

[B] Nested loops, prune early
Nest `permutations` loops and apply relevant clues *inside* each loop level before going deeper.

```diff
+++ zebra_puzzle.py
@@ -0,0 +1,8 @@
+from itertools import permutations
+
+def solve():
+    for color in permutations(range(5)):
+        if not color_clues(color): continue
+        for nat in permutations(range(5)):
+            if not nat_clues(nat, color): continue
+            # ... drink, smoke, pet loops
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=Option A (flat brute force) generates 5!^5 = ~24.8 billion combinations, which is completely infeasible. Option B prunes the search space at each level - after pruning color (24 permutations), only a handful pass; then nat pruning on those handful, etc. The actual search tree explored is tiny. This is the standard approach for constraint satisfaction and a great lesson in early termination vs. generate-then-filter.

Tutor: `5! = 120` permutations per attribute — how many total combinations does option A actually need to check?

### Student

Let me think through this...

Option A generates all permutations independently for each of the 5 attributes. That's `(5!)^5` total combinations to check before filtering.

So that's `120^5` = `24,883,200,000` combinations to check upfront before we even apply a single clue. That's a lot of wasted work if we can eliminate invalid branches earlier.

Option B sounds much smarter — we'd apply clues as we build up each attribute, so we never explore branches that are already known to be invalid. We'd prune the search space dramatically before we get to the later attributes.

I think I should go with **B**. Early pruning seems way more efficient for this constraint problem.

---

## Turn 2

### Tutor

Thinking: The user correctly analyzed the problem and chose option B, which is my preferred option. They understood the combinatorial explosion problem with option A and the benefit of early pruning in option B. I should affirm their choice and then proceed to build the solution, potentially offering more design decisions along the way.
  
  Now let me think about the next design decision. With the nested loop approach, there are a few interesting choices:
  1. What order to nest the loops? (Which attribute first?)
  2. How to represent houses - as indices 0-4 where the index = house position, and the value = which variant is at that position?
  
  
  3. Whether to use named constants or raw integers for the attribute values
  
  I'm leaning toward starting with loop ordering as the teaching moment—specifically, which attribute should go in the outermost loop. Color has that constraining clue about green being immediately right of ivory, so it should probably come first to prune the search space early. Let me start building out the solution and pose this as a question to guide the user's thinking. an interesting optimization question.
  
  Let me think about what's most instructive here. The key insight about the nested loop approach is that you want the most constrained attribute in the outer loop so each failed iteration prunes all inner iterations. Color is highly constrained by clue 5 (green immediately right of ivory), which eliminates 116 of 120 permutations, leaving only 4 valid ones. So the real question becomes: should I put color outermost since it's so tightly constrained, or would nationality make more sense as the primary loop structure?
  
  I think I should present both options to the user and let them guide the next design decision.

Tutor: Exactly right — 24.8 billion vs. a few thousand. Good reasoning.

Now, within the nested approach, loop order matters. Which attribute should be the **outermost** loop?

OPTIONS:
[A] Color outermost
Put `color` in the outermost loop. Clue 5 says the green house is *immediately right* of the ivory house — only 4 of 120 color permutations satisfy this.

[B] Nationality outermost
Put `nationality` in the outermost loop. It feels natural as the "main" attribute, and clue 9 (Norwegian in house 1) does constrain it significantly.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Color is the most constrained attribute: clue 5 (green immediately right of ivory) reduces 120 permutations down to just 4 (positions 1-2, 2-3, 3-4, or 4-5 for ivory-green pair). Nationality with clue 9 (Norwegian in house 1) reduces to 24. Putting the most constrained attribute outermost means all inner loops only run 4 times instead of 24, dramatically reducing total work. This is a key insight in constraint satisfaction: order variables by most-constrained first (MRV heuristic).

Tutor: How many valid permutations does each clue leave for its attribute?

### Student

Good question. Let me think about the pruning power of each:

**Color (Clue 5):** "Green house is immediately right of ivory house"
- Out of 120 permutations, only 4 satisfy this (ivory at position 0 with green at 1, ivory at 1 with green at 2, etc.)
- That's massive pruning — we'd eliminate 116 invalid permutations right away.

**Nationality (Clue 9):** "Norwegian in house 1"
- This constrains the Norwegian to a specific position, but doesn't fully order the nationality permutation.
- We'd still have `4! = 24` valid permutations (the remaining 4 nationalities in the remaining 4 positions).
- Much less pruning than color.

So **A** is the way to go. Starting with color as the outermost loop gives us the tightest initial filter — we only keep 4 out of 120 permutations before moving deeper into the nested loops. That eliminates way more branches early on.

---

## Turn 3

### Tutor

Thinking: The user correctly analyzed the pruning power and chose A (color outermost). They got the right answer - only 4 valid color permutations pass clue 5, vs 24 for nationality with clue 9.
  
  Now let me start building the solution. I'll create the file with the basic structure, and then ask one more design question - perhaps about how to represent the attributes (named constants vs. raw integers, or maybe about how to express the adjacency clues).
  
  Actually, let me think about a good next question. Once we have the structure down, a good question would be about how to write adjacency clue helpers. The clues like "next to" and "immediately right of" come up multiple times. Should we:
  
  
  - Write them inline as simple comparisons, or define helper functions for readability?
  - Use index-based access where each attribute maps to houses, or the reverse?
  
  I think the representation question is more fundamental - whether to use named constants for clarity or rely on positional ordering with raw integers. Let me just sketch out the skeleton and ask about the adjacency helpers, since that's a concrete design choice that affects readability.
  
  Actually, the key insight is how to structure the permutation representation itself. If I use `color = (RED, GREEN, IVORY, YELLOW, BLUE)` where position represents the house, then clue 5 (the green house owner drinks coffee) becomes finding the index where `color[i] == GREEN`. This feels like the natural way to handle permutations.
  
  Now I'm ready to start implementing—I'll set up the attribute tuples with house indices, use named constants for clarity, and write helper functions to express constraints like "immediately to the right of" cleanly.
  
  Writing the solver code... Writing constraint checks... I see the issue now—I need to handle clues that mix different attribute types, like comparing the Norwegian's house position to the blue house's position. I'm defining helper functions to check if two houses are adjacent or if one is directly to the right of the other, then applying these to validate constraints across different attributes.
  
  Writing constraint checks... I'm deciding between two approaches for the helper functions: either separate `next_to` and `right_of` helpers that work directly with house indices, or a single `next_to` helper that takes attribute values and the permutation. The first option feels cleaner and more reusable, while the second mixes concerns even though it reads more naturally. I'll code this up and present both options.

Tutor: Nailed it — the MRV (Most Restricted Variable) heuristic. Color's 4/120 vs Nationality's 24/120 means color as the outer loop cuts inner work by 6×.

Now let's write the actual code. One small but real design question before we do — how should the adjacency helpers work?

OPTIONS:
[A] Helpers take house indices
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+def next_to(h1, h2):
+    return abs(h1 - h2) == 1
+
+def right_of(h1, h2):
+    return h1 - h2 == 1
+# usage: next_to(nat.index(Norwegian), color.index(Blue))
```

[B] Helpers take values + perm
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+def next_to(a, b, perm):
+    return abs(perm.index(a) - perm.index(b)) == 1
+
+def right_of(a, b, perm):
+    return perm.index(a) - perm.index(b) == 1
+# usage: next_to(Norwegian, Blue, ???)
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Option B breaks down when the two values come from *different* permutations (e.g., clue 14: Norwegian from nat perm, Blue from color perm). There's no single perm to pass. You'd have to call nat.index() and color.index() anyway to get house numbers before calling the helper — so the helper adds nothing. Option A operates on house indices, which are the common currency across all attributes, and works correctly for cross-attribute clues.

Tutor: Consider clue 14: *"The Norwegian lives next to the blue house."* Norwegian comes from `nat`, blue from `color` — which helper signature handles that?

### Student

Ah, that's the key insight. Clue 14 involves two *different* attributes — Norwegian is a value in the `nat` permutation, and Blue is a value in the `color` permutation.

With option A, I'd need to do:
```python
next_to(nat.index(Norwegian), color.index(Blue))
```

This works because I'm converting both values to their house positions (indices in their respective permutations), then comparing those positions.

With option B, I'd need to pass the permutation(s), but which one? Norwegian is in `nat` and Blue is in `color` — I'd need both permutations, not just one. The signature breaks down.

So **A** is the right design. The helpers work on house indices (positions), which are universal across all attributes. I can mix and match values from different permutations by looking up their indices.

That makes sense — the constraint is about *positions in the house lineup*, not about which attribute a value belongs to.

---

## Turn 4

### Tutor

Thinking: The user correctly identified the issue with option B and chose A. Now let me write the full solution. I'll create the file with everything.
  
  The full solution:
  
  ```python
  from itertools import permutations
  
  # House positions: 0 = leftmost, 4 = rightmost
  # Each permutation tuple: perm[house] = attribute_value
  
  Red, Green, Ivory, Yellow, Blue = range(5)
  Englishman, Spaniard, Ukrainian, Norwegian, Japanese = range(5)
  Coffee, Tea, Milk, OrangeJuice, Water = range(5)
  
  
  ```
  
  Setting up the constraint solver...
  
  ```
  
  Now I'm checking the constraint that green must be immediately to the right of ivory, then iterating through nationality permutations to verify the Englishman lives in red, the Norwegian is in the first house, and the Norwegian is next to blue. Then I'm working through drink permutations to ensure coffee is in the green house and the Ukrainian drinks tea.
  
  ```
  
  Continuing with the beverage constraints...
  
  Now I'm checking the remaining clues about pet ownership and adjacency rules. The old gold smoker must own snails, chesterfields need to be next to the fox, and kools next to the horse. Once all constraints are satisfied, I extract the water drinker and zebra owner from the solution.
  
  ```
  Actually, let me reconsider the Exercism interface. The puzzle expects two separate functions: `drinks_water()` and `owns_zebra()`, each returning the nationality of the person who satisfies that condition. I should write both functions along with a shared solver that checks all the clues systematically.
  
  Let me verify my constraint logic is correct for each clue before implementing.
  ```
  ) == drink.index(OJ)` ✓
  13. Japanese smokes Parliaments: `nat.index(Japanese) == smoke.index(Parliaments)` ✓
  14. Norwegian next to blue house: `next_to(nat.index(Norwegian), color.index(Blue))` ✓
  ```
  
  All 14 clues are accounted for. Now I'll write the solver...
  
  Actually, let me double-check clue 11 — Kools are in the yellow house from clue 7, so the constraint simplifies to the yellow house being next to the horse owner. I can express this either way, but using `smoke.index(Kools)` works fine.
  
  Let me verify against the known solution: Norwegian in house 1 drinks water, Japanese in house 5 smokes Parliaments and owns the zebra...
  
  Running through the solution mentally: House 1 has the Norwegian with yellow house, water, Kools, and fox. House 2 is the Ukrainian with blue house, tea, Chesterfields, and horse. House 3 is the Englishman with red house, milk, Old Gold, and snails. House 4 is the Spaniard with ivory house, orange juice, Lucky Strike, and dog. House 5 is the Japanese with green house, coffee, Parliaments, and zebra. Checking the constraints: Englishman in red ✓, Spaniard owns dog ✓, coffee in green ✓, Ukrainian drinks tea ✓, green immediately right of ivory ✓...
  
  continuing through all fourteen clues and they all check out. So the Norwegian drinks water and the Japanese owns the zebra. Now I'll write the code to solve this.
  
  Before I do though, I should think about the implementation approach — specifically whether to solve the puzzle once and cache the result, or have each function independently call the solver. Caching is clearly the better approach since it avoids redundant computation, so I'll structure it that way.

Tutor: Exactly — positions are the common currency. House indices let you join across attributes cleanly.

One more design question before we write the full solution. The Exercism interface wants two separate functions: `drinks_water()` and `owns_zebra()`. How should they share the work?

OPTIONS:
[A] Solve once, cache result
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+from functools import lru_cache
+
+@lru_cache(maxsize=None)
+def _solution():
+    ...  # nested permutation search
+    return water_drinker, zebra_owner
```
`drinks_water()` and `owns_zebra()` each call `_solution()` and unpack.

[B] Each function solves independently
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+def drinks_water():
+    for color in permutations(...):
+        ...  # full search
+
+def owns_zebra():
+    for color in permutations(...):
+        ...  # full search again
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Option B duplicates the entire search and runs it twice. Even if it's fast enough, it's a DRY violation and doubles runtime. Option A with lru_cache is the idiomatic Python way to memoize a no-argument function — the result is computed once and reused. The private _solution() naming also clearly signals it's an implementation detail.

### Student

This is straightforward — **A** is the way to go.

Option B would solve the entire puzzle *twice*, doing all that constraint checking and permutation work from scratch each time. That's wasteful.

Option A solves it once, caches the result, and both `drinks_water()` and `owns_zebra()` just call the cached `_solution()` function and extract what they need. The second call gets the cached result instantly.

Since the puzzle has a unique solution and it's deterministic, caching makes perfect sense. We do the hard work once and reuse it.

---

## Turn 5

### Tutor

Thinking: The user chose option A (solve once, cache with lru_cache). Now let me write the complete solution. I have all the design decisions made:
  
  1. Nested loops with early pruning ✓
  2. Color outermost (most constrained, only 4 valid permutations) ✓
  3. Helper functions take house indices ✓
  4. `lru_cache` on `_solution()` ✓
  
  Let me write the complete file now.
  
  The Exercism zebra puzzle exercise expects:
  - `drinks_water()` returns nationality string
  
  
  - `owns_zebra()` returns nationality string
  
  Writing the complete solution... I'm continuing to build out the constraint checking for the puzzle solver, validating that the Norwegian is in the first house, the Englishman lives in the red house, and the Norwegian is next to the blue house. Then I'm iterating through drink assignments to ensure milk is in the middle house, coffee is in the green house, and the Ukrainian drinks tea. Now I'm moving into smoke assignments and checking that Kools cigarettes are in the yellow house.
  
  Checking more constraints... Checking the constraint ordering to maximize early pruning — the nationality loop with the Norwegian at position 0 constraint eliminates most invalid permutations immediately, leaving just 24 to check, then the drink loop's milk at position 2 similarly filters down to 24 valid combinations before hitting the more complex adjacency checks in the smoke and pet loops.

Tutor: Right. Now let's build the whole thing. All decisions are locked in:

- Color outermost (4 valid perms), prune inside each level
- `next_to`/`right_of` on house indices
- `lru_cache` on a private `_solution()`

[Glob(zebra_puzzle.py)]
  No files found

[Write(zebra_puzzle.py)]
from itertools import permutations
from functools import lru_cache

# Each permutation is indexed by house (0 = leftmost).
# perm[house] = attribute_value   →   perm.index(value) = house number

Red, Green, Ivory, Yellow, Blue = range(5)
Englishman, Spaniard, Ukrainian, Norwegian, Japanese = range(5)
Coffee, Tea, Milk, OrangeJuice, Water = range(5)
OldGold, Kools, Chesterfields, LuckyStrike, Parliaments = range(5)
Dog, Snail, Fox, Horse, Zebra = range(5)

… (80 more lines)
  File created successfully at: zebra_puzzle.py

[Bash(cd /root && python -c "
from zebra_puzzle import drinks_water, owns_zebra
print('Drinks water:', drinks_water())
print('Owns zebra:  ', owns_zebra())
")]
  error: Exit code 1

[Bash(python -c "
from zebra_puzzle import drinks_water, owns_zebra
print('Drinks water:', drinks_water())
print('Owns zebra:  ', owns_zebra())
")]
  Drinks water: Norwegian
  Owns zebra:   Japanese

Tutor: It works. Here's the final structure:

```
color loop      →  4 pass  (clue 5: green right of ivory)
  nat loop      →  ~2 pass (clues 9, 1, 14)
    drink loop  →  ~2 pass (clues 8, 3, 4)
      smoke loop→  ~2 pass (clues 7, 13, 12)
        pet loop→  1 pass  (clues 2, 6, 10, 11)
```

Instead of 24.8 billion candidates, we explore a few thousand at most.

**The answer:** The **Norwegian** drinks water, the **Japanese** owns the zebra.

One thing worth noting: `nat[0] != Norwegian` (clue 9) lets us replace `nat.index(Norwegian)` with the literal `0` in clue 14 — a small but clean simplification since Norwegian's house is always known to be `0` by the time we check it.

### Student

That's a great point about the simplification. Since clue 9 locks Norwegian into house 0, we could hardcode that constraint and skip the index lookup in clue 14. That's a nice optimization that makes the code slightly faster and clearer — we're leveraging what we've already established rather than redundantly looking it up.

The pruning structure is really satisfying to see laid out:
- Start with 4 valid color permutations
- Nest nationality checks (down to ~2 per color)
- Nest drink checks (down to ~2 per nationality)
- And so on...

Going from 24.8 *billion* candidates down to a few thousand by applying constraints incrementally is exactly why the nested-loop approach with early pruning beats flat brute force.

I feel like I've got a solid understanding of the strategy now:
1. Identify the most constrained attribute first (color, via the adjacency clue)
2. Use house indices as the universal currency for joining constraints across attributes
3. Nest loops and prune at each level
4. Cache the result so both output functions reuse it

The solution is correct — Norwegian drinks water, Japanese owns the zebra. Thanks for walking through the design decisions before jumping into code; it made the actual implementation much clearer.

<done/>

---

**Run end:** done after 5 turn(s) in 177.6s
