# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:42:00

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

Thinking: The user wants to solve the classic Zebra Puzzle (also known as Einstein's Riddle) for Exercism. Let me think about this puzzle and the best approach.
  
  The classic Zebra Puzzle constraints are:
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
  
  The puzzle asks who drinks water and who owns the zebra. For Exercism, I'll use `itertools.permutations` to generate all possible arrangements of the five attributes—nationality, color, pet, drink, and smoke—across the five houses, then filter them against all the constraints.
  
  A brute force approach checking all 120^5 combinations would be too slow, so I need to apply constraints progressively and prune early. I can generate permutations of each attribute and combine them while filtering out invalid combinations, or use a constraint solver approach. Let me build this by generating permutations with early pruning...
  
  Writing constraint solver... I'm setting up a cleaner approach using permutations to iterate through all possible arrangements of nationalities and colors, then checking constraints like the Norwegian being in the first house and the Englishman living in the red house.
  
  Adding more constraint checks... Finishing the constraint check, then extracting the solution by mapping the permutation indices back to the actual nationality names to identify who drinks water and who owns the zebra. I'm verifying the logic with a concrete example—if the Norwegian is at house 0, the Englishman at house 2, and water is drunk at house 3, then finding which nationality is at position 3 gives us the Ukrainian as the water drinker. For the implementation, I should present both the itertools approach with constraint pruning and a constraint solver option, since the user asked for either method.
  
  The itertools approach is self-contained and educational, while a constraint library like python-constraint is more declarative but adds a dependency. For Exercism, the itertools method is typically preferred since it doesn't require external packages. I'll outline both options and let the user decide which direction to take, then check the expected file structure for the exercise.

[Glob(zebra_puzzle*)]
  No files found

Tutor: No file yet. Before we write anything, here's the core design question:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me propose the two options for the main approach to solving the Zebra Puzzle.

OPTIONS:
[A] Nested permutations, prune early
Generate permutations of each attribute (nationality, color, drink, smoke, pet) in nested loops — but apply relevant constraints at each level before descending. 120⁵ worst-case collapses to a handful of paths in practice.

[B] Single flat permutation product
Use `itertools.product(permutations(range(5)), repeat=5)` to generate all attribute combos at once, then filter with one big predicate. Simpler structure, same `itertools` primitives.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Option A prunes the search space early — once nationalities+colors are fixed and violate a constraint, you never generate the ~14 million drink/smoke/pet combos for that branch. Option B evaluates all 120^5 ≈ 25 billion combinations and is effectively untestable without waiting minutes. The nested-with-pruning approach is both the practical choice and illustrates why constraint propagation matters.

Tutor: Which approach — **A** (nested loops, prune early) or **B** (flat product, filter at end)?

### Student

I think I'll go with **A** (nested loops, prune early).

My reasoning: the Zebra Puzzle has a lot of constraints, and if we can eliminate invalid partial assignments early, we'll avoid generating and testing tons of dead-end combinations. Option B would generate everything first and then filter, which seems wasteful. Plus, building it step-by-step might help me understand how the constraints actually work together.

Let me start by sketching out the structure — should I begin by listing all the constraints first, or jump straight into writing the nested loop skeleton?

---

## Turn 2

### Tutor

Thinking: Great, the user picked the right option and gave good reasoning. They're asking whether to list constraints first or jump into the skeleton. This is a good opportunity to propose options since there's a pedagogical consideration here - and I have a preference (list constraints first helps map them to the right pruning level).
  
  Actually, let me think about this... The user is asking a clarifying/workflow question. I could answer this directly or make it a propose_options moment. I think this is a good teaching moment - there's a real difference between the two approaches:
  
  1. List constraints first - lets you mentally assign each constraint to the right nesting level, which is the key insight for why pruning works
  
  
  2. Write the skeleton first - get the structure down, then slot in constraints
  
  I think option 1 is better because the pruning power comes from placing constraints at the *right* level. If you write the skeleton first you might not know where to put each constraint. The real pedagogical value here is understanding which constraints belong at which nesting depth, so I should propose both approaches and highlight why that mapping matters.

Tutor: Good instinct on the reasoning. One more structural question before we write anything:

OPTIONS:
[A] Skeleton first, fill in later
Write the 5 nested `for perm in permutations(...)` loops first, then slot constraints in wherever they seem to fit.

[B] Map constraints to depth first
List all 15 clues and tag each with the attributes it involves (e.g. "Englishman↔Red" needs nationality+color). That tells you exactly which loop level is the earliest you can check it — *before* writing any code.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=The pruning power comes entirely from checking constraints at the shallowest possible depth. If you write the skeleton first you tend to dump all constraints at the innermost loop "because all variables are available there" — which gives you no pruning benefit at all. Mapping constraints to attributes first makes the placement obvious and intentional, and illustrates the core idea of constraint propagation.

Tutor: **A** or **B** — does the order matter here?

### Student

I'll go with **B** (map constraints to depth first).

I think understanding *when* each constraint can be checked will make the code cleaner and help me avoid building constraints that depend on attributes I haven't permuted yet. Plus, it'll give me confidence that the early pruning will actually work before I start writing loops.

Can we list out the 15 clues and tag them? I want to see which attributes each constraint touches so I know at what nesting level I can start filtering.

---

## Turn 3

### Tutor

Thinking: The user wants to list all 15 clues and tag them with the attributes they involve. Let me do this systematically.
  
  The 5 attributes we're permuting, in order:
  1. Nationality: Norwegian, Englishman, Spaniard, Ukrainian, Japanese
  2. Color: Red, Green, Ivory, Yellow, Blue
  3. Drink: Coffee, Tea, Milk, OJ, Water
  4. Smoke: OldGold, Kools, Chesterfields, LuckyStrike, Parliaments
  5. Pet: Dog, Snails, Fox, Horse, Zebra
  
  
  Now I'm going through each clue and tagging which attributes it constrains. The Englishman in the red house links nationality to color, the Spaniard with the dog connects nationality to pet, coffee in the green house ties color to drink, and the Ukrainian drinking tea pairs nationality with drink. The green house being right of ivory is a positional constraint on colors, the Old Gold smoker owning snails links smoke to pet, and Kools in the yellow house connects smoke to color. Milk in the middle house and the Norwegian in the first house are position-based constraints. I need to continue through the remaining clues to complete the full list. Now I'm looking at the complete set of constraints for the zebra puzzle and organizing them by how many attributes they connect. I need to establish a nesting order for solving this systematically—starting with nationality as the outermost layer, then color, drink, smoke, and pet as the innermost. Some clues directly constrain single attributes like the Norwegian being in the first house, while others link multiple attributes together like the Englishman living in the red house, and I'll need to identify which constraints can be applied at each depth level to efficiently narrow down the possibilities. Let me organize these clues more systematically by what attributes they connect. I'm grouping them by the combination of attributes involved: some clues only constrain one attribute, while others link two or three together. I need to separate out the nationality-pet connections from the others—I see Clue 3 pairs Spaniard with Dog, which is different from what I was tracking before. Let me start fresh with a cleaner categorization.
  
  Now I'm mapping out the constraint structure for a backtracking solver. I'll nest the loops in order of nationality, then color, then drink, then smoke, then pet. For each depth, I'm identifying which clues can be checked immediately. At the nationality level, Clue 9 fixes the Norwegian to house 0. Once I add colors, I can check the Englishman-red pairing, the green-ivory adjacency, and the Norwegian-blue adjacency. Adding drinks lets me verify coffee in green, Ukrainian drinking tea, and milk in the middle house. The smoke level will handle the Old Gold-snails connection and other smoke-related constraints. Formatting the solution as a clean table for the user...

Tutor: Sure. Let's lay them all out. We'll permute in this order: **Nationality → Color → Drink → Smoke → Pet** — so the depth at which a constraint becomes checkable depends on which of those five it touches.

---

**Depth 1 — Nationality only**
| # | Clue | Attributes |
|---|------|-----------|
| 9 | Norwegian lives in house 1 (leftmost) | Nationality |

**Depth 2 — + Color**
| # | Clue | Attributes |
|---|------|-----------|
| 1 | Englishman lives in the red house | Nationality + Color |
| 5 | Green house is immediately right of ivory | Color |
| 14 | Norwegian lives next to the blue house | Nationality + Color |

**Depth 3 — + Drink**
| # | Clue | Attributes |
|---|------|-----------|
| 3 | Coffee is drunk in the green house | Color + Drink |
| 4 | Ukrainian drinks tea | Nationality + Drink |
| 8 | Milk is drunk in the middle house | Drink |

**Depth 4 — + Smoke**
| # | Clue | Attributes |
|---|------|-----------|
| 7 | Kools smoked in the yellow house | Color + Smoke |
| 12 | Lucky Strike smoker drinks OJ | Drink + Smoke |
| 13 | Japanese smokes Parliaments | Nationality + Smoke |

**Depth 5 — + Pet (innermost)**
| # | Clue | Attributes |
|---|------|-----------|
| 2 | Spaniard owns the dog | Nationality + Pet |
| 6 | Old Gold smoker owns snails | Smoke + Pet |
| 10 | Chesterfields smoker lives next to the fox owner | Smoke + Pet |
| 11 | Kools smoker lives next to the horse | Smoke + Pet |

---

That's all 14 structural clues placed. Clue 15 ("there is a zebra") just names the fifth pet — it's implicit in the permutation.

Notice that **4 constraints land at depth 5** vs. **3 at depth 2** — that's where most dead-ends are caught. The color-level pruning (depth 2) is especially powerful: clue 5 (`green = ivory + 1`) eliminates ~80% of color permutations before we ever touch drinks.

Ready to write the skeleton + constraints?

### Student

Yes, I'm ready. This breakdown is really helpful — I can see now that clue 5 (green immediately right of ivory) will do a ton of early pruning, and the depth-5 constraints are the real filters at the end.

Let me start writing the skeleton with the constraint checks slotted in at the right levels. I'll write the nested loops for nationality → color → drink → smoke → pet, and add the constraint checks as I go down.

Should I write this as a series of nested `for` loops with `if` conditions that skip ahead when a constraint fails, or would it be clearer to write helper functions for each constraint check? I'm thinking helper functions might make it easier to read, but I want to make sure that doesn't add overhead or make the early pruning less obvious.

---

## Turn 4

### Tutor

Thinking: The user is asking about whether to use inline `if` conditions vs. helper functions for the constraint checks. This is a good teaching moment. Let me think about the tradeoffs:
  
  **Inline `if` conditions:**
  - Pruning is explicit and visible at each level
  - Slightly faster (no function call overhead, though Python's overhead is minimal for 120^5 pruned to much less)
  - The structure makes it clear WHY each constraint is at that level
  - Can be harder to read with many conditions
  
  **Helper functions:**
  - Named functions like `right_of(a, b)` and `next_to(a, b)` make the constraint semantics clearer
  
  
  - But extracting entire clues as helpers obscures which depth level they're applied at
  - The sweet spot is keeping the nested `if` checks inline to preserve the depth-pruning structure, while extracting small predicate helpers for reusable comparisons like `next_to` and `right_of`
  
  Option A—inline checks with tiny predicate helpers—is better than Option B (helper functions for each constraint) because it maintains visibility of the depth structure where pruning happens.

OPTIONS:
[A] Per-clue helper functions
Wrap each constraint in its own function (`check_nationality`, `check_color`, etc.) and call them at the appropriate loop level. Reads like prose, each check is named.

[B] Inline checks, tiny predicate helpers
Keep the `if` guards inline in the loops, but extract only the two reusable spatial predicates:
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,4 @@
+def next_to(a, b):
+    return abs(a - b) == 1
+
+def right_of(a, b):
+    return a == b + 1
```
All constraint checks stay at their loop level — the depth structure stays visible.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=Per-clue helpers hide *when* pruning happens — the whole point of the design we just worked out. Inline checks make it obvious that depth-2 constraints fire before depth-5 ones. The only real repetition is the spatial relationships (next_to, right_of), which appear 3-4 times and warrant a one-liner each. Everything else is a single unique expression that doesn't benefit from wrapping.

Thinking: The user hasn't responded yet. The system reminder is about TodoWrite, but I shouldn't mention it. I'll wait for the user's response about option A or B.
  
  Actually, looking at the conversation again, the user hasn't responded to the last propose_options call. I should wait for them to respond.

Tutor: **A** or **B** — do the helper functions help or hurt readability here?

### Student

I'll go with **B** (inline checks, tiny predicate helpers).

I think keeping the constraint checks inline at their loop levels will make it crystal clear *where* each pruning happens — that's the whole point of the depth-first strategy we just mapped out. If I wrap everything in named helper functions, I lose that visual structure even if the code reads nicely in isolation.

The two spatial predicates (`next_to` and `right_of`) are genuinely reusable and worth extracting, so let's do that. Everything else stays inline so I can see the pruning happening at each nesting level.

Let me start writing the skeleton now — should I set up the basic 5 nested loops first, then add the constraints level by level?

---

## Turn 5

### Tutor

Thinking: The user picked the right option and wants to start writing the code. Let me write the full solution now. I'll create the `zebra_puzzle.py` file.
  
  Let me think about the structure:
  
  ```python
  from itertools import permutations
  
  def next_to(a, b):
      return abs(a - b) == 1
  
  def right_of(a, b):
      return a == b + 1
  
  def solution():
      houses = range(5)
      
      for nationalities in permutations(houses):
          Norwegian, Englishman, Spaniard, Ukrainian, Japanese = nationalities
          if Norwegian != 0:  # clue 9
  
  
  ```
  
  Still writing constraint checks...
  
  ```
  Finishing the constraint checks and returning the solution...
  ```
  
  Now I'm realizing that calling `solution()` twice would be inefficient, so I should cache the result or compute both answers from a single call to avoid redundant constraint checking. I'm settling on having both functions call a shared internal solver—since the puzzle runs in milliseconds, the performance hit from computing twice is negligible and keeps the code simple without needing caching overhead. I'll structure it so `drinks_water()` and `owns_zebra()` each extract their answer from the same solve function.
  
  Building the constraint solver... Now I'm extracting the solution by getting the water drinker and zebra owner from the solved configuration, then wrapping those in simple functions that call the solver and return the specific answers.

Tutor: Yes — let's just write the whole thing now. The design is fully mapped; building it level-by-level in conversation would just slow us down. I'll write it all at once with the constraints slotted in at exactly the depths we planned.

[Write(zebra_puzzle.py)]
from itertools import permutations


def next_to(a, b):
    return abs(a - b) == 1


def right_of(a, b):
    return a == b + 1


def _solve():
… (59 more lines)
  File created successfully at: zebra_puzzle.py

[Bash(cd /tmp && python -c "
import sys, time
sys.path.insert(0, '.')
import zebra_puzzle
t = time.time()
w = zebra_puzzle.drinks_water()
z = zebra_puzzle.owns_zebra()
print(f'Water drinker : {w}')
print(f'Zebra owner   : {z}')
print(f'Time          : {(time.time()-t)*1000:.1f} ms')
" 2>&1 || python3 -c "
import sys, time
sys.path.insert(0, '/tmp')
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location('zebra_puzzle', 'zebra_puzzle.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t = time.time()
w = m.drinks_water(); z = m.owns_zebra()
print(f'Water drinker : {w}')
print(f'Zebra owner   : {z}')
print(f'Time          : {(time.time()-t)*1000:.1f} ms')
"
)]
  error: Exit code 1

[Bash(python3 -c "
import sys, time, importlib.util
spec = importlib.util.spec_from_file_location('zebra_puzzle', 'zebra_puzzle.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t = time.time()
w = m.drinks_water(); z = m.owns_zebra()
print(f'Water drinker : {w}')
print(f'Zebra owner   : {z}')
print(f'Time          : {(time.time()-t)*1000:.1f} ms')
"
)]
  Water drinker : Norwegian
  Zebra owner   : Japanese
  Time          : 0.2 ms

Tutor: **Norwegian** drinks water. **Japanese** owns the zebra. Runs in 0.2 ms.

---

A few things worth noting about the final code:

**`nat.index(Water)`** — this is the key lookup. `nat` is a tuple of house positions indexed by person (position 0 = Norwegian, 1 = Englishman, …). `Water` is a house number 0–4. So `nat.index(Water)` finds *which person lives in the water house*, giving us the index into `people`. Clean one-liner that avoids any explicit loop.

**Why `_solve()` is called twice** (once for each public function) — for a puzzle that solves in 0.2 ms, that's fine. If you wanted to cache it, `@functools.lru_cache` on a zero-argument function is the idiomatic tool — but it'd be premature here.

**The depth 2 prune does the heavy lifting** — clues 1, 5, and 14 together reduce 120 color permutations down to just a few before we ever touch drinks or smokes. That's why the whole search completes in < 1 ms despite being written in pure Python.

### Student

That's really satisfying. The solution works cleanly and efficiently.

I want to understand the `nat.index(Water)` lookup better though — let me trace through it:

- `nat` is a permutation of `(0, 1, 2, 3, 4)` representing which house each nationality lives in, indexed by nationality (0=Norwegian, 1=Englishman, etc.)
- `Water` is a house number (0–4)
- `nat.index(Water)` finds the *position* in the `nat` tuple where `Water` appears, which tells us which nationality lives there
- Then we index into `people` to get the actual name

So if `nat = (0, 2, 4, 3, 1)` and `Water = 2`, then `nat.index(2) = 1`, and `people[1] = "Englishman"` — the Englishman lives in house 2 which is the water house.

Is that right?

Also, one last thing — I'm curious why the depth-2 constraint (green immediately right of ivory) was so powerful. Is it just that color adjacency is a hard constraint that eliminates most arrangements, or is there something else making it so effective?

---

## Turn 6

### Tutor

Thinking: The user has two questions:
  1. Is their trace of `nat.index(Water)` correct? Yes, it is.
  2. Why is the green/ivory adjacency constraint so powerful?
  
  Let me answer both clearly.
  
  For question 1: Yes, the trace is exactly right.
  
  For question 2: Let me think about this carefully.
  
  Clue 5 says green is immediately to the right of ivory. That means:
  - (ivory=0, green=1), (ivory=1, green=2), (ivory=2, green=3), (ivory=3, green=4)
  
  
  - So there are only 4 valid (ivory, green) pairs.
  
  Out of 120 total color permutations, only 24 satisfy this constraint—that's because for each of the 4 valid pairs, the remaining 3 colors can be arranged in 6 ways. This single clue cuts the search space down by a factor of 5. When combined with clue 1 (Englishman = Red), the constraints become even tighter.
  
  The real insight is that clue 5's power comes from being an ordering constraint—it doesn't just link two variables, it requires them to be adjacent in a specific sequence. That's why it eliminates 80% of possibilities on its own. Clue 1 is similarly powerful since it fixes a color to a specific position, also removing 4 out of 5 cases. but it depends on the nationality loop, while clue 5 is purely about colors.
  
  Actually the key thing about clue 5 is that it's a *relative ordering* constraint between two values: green must be exactly one position higher than ivory. In a 5-element permutation, only 4 out of the C(5,2)×2 = 20 ordered pairs of positions satisfy this, and since ivory and green are fixed values, only 4 out of 20 possible (ivory_pos, green_pos) pairs work. That constrains the arrangement to 4/20 = 1/5 of the possible position pairs for those two items.
  
  For 5! = 120 permutations of 5 colors, how many have green exactly one position to the right of ivory? There are only 4 valid pairs: (Green=1,Ivory=0), (Green=2,Ivory=1), (Green=3,Ivory=2), (Green=4,Ivory=3). For each pair, the remaining three colors can be arranged in 3! = 6 ways, giving us 4 × 6 = 24 permutations that satisfy this constraint.
  
  So clue 5 eliminates 96 out of 120 permutations, leaving only 24 valid ones. That's an 80% elimination rate, which explains why it's so powerful as a pruning constraint early in the search.

Tutor: Your trace is exactly right. Nicely done.

---

On why clue 5 is so powerful — let's count. Out of 5! = 120 color permutations, how many have `Green == Ivory + 1`?

The valid (Ivory, Green) position pairs are only: `(0,1) (1,2) (2,3) (3,4)` — just **4** pairs. The remaining 3 colors fill the leftover positions in 3! = 6 ways each:

```
4 pairs × 6 arrangements = 24 survivors out of 120
```

Clue 5 alone eliminates **80%** of color permutations before any other constraint fires. That's why it's so effective — it's not just an adjacency check, it's a *directional* ordering constraint on two specific values, and 5 houses don't leave many slots for that.

Compare it to a plain equality constraint like clue 1 (`Englishman == Red`): once `Englishman`'s position is fixed from the outer loop, that also eliminates 4/5 of color permutations — but it *depends* on the nationality loop to do so. Clue 5 is self-contained within the color loop and fires unconditionally, making it a pure structural filter.

The general principle: **the tightest constraints are ones that impose a relative order between two variables** (adjacency + direction), because those reduce `n!` arrangements to roughly `(n-1) × (n-2)!` — a factor-of-n reduction by themselves.

### Student

That makes complete sense now. The directional adjacency constraint is so powerful because it's not just saying "these two must be adjacent" — it's saying "this one must be immediately to the right of that one," which cuts the search space by a fixed factor regardless of what else permutes around it.

I can see how that principle generalizes: any constraint that imposes a strict relative ordering between two specific values in a sequence will give you those kinds of dramatic early prunings, especially in smaller spaces like 5 houses.

This was a really solid walkthrough. The problem is solved, the code works efficiently, and I understand both *how* it works and *why* the depth-first constraint mapping strategy was worth doing upfront. 

Thanks for breaking down the design before jumping into code — that made the whole thing much clearer than if we'd just started writing nested loops and bolted constraints on afterward.

<done/>

---

**Run end:** done after 6 turn(s) in 204.1s
