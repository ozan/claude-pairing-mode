# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:37

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

Thinking: The user wants to solve the classic Zebra Puzzle (also known as Einstein's Riddle). Let me think about this puzzle first.
  
  The Zebra Puzzle constraints are:
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
  
  The puzzle asks who drinks water and who owns the zebra. I'm considering two main approaches: a brute-force method using permutations to test all possible combinations, or a constraint satisfaction approach that prunes the search space more efficiently.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Let me propose two options for solving the Zebra Puzzle - one using brute-force with itertools.permutations and one using a constraint solver approach.

OPTIONS:
[A] Brute-force permutations
Generate all `5!` permutations for each of the 5 attributes (nationality, color, drink, smoke, pet), check every combination of those against all 15 constraints. Simple to read but evaluates up to `(5!)^5 ≈ 25 billion` tuples before pruning.

[B] Permutations with early pruning
Nest the attribute loops and apply constraints as early as possible — e.g. check color/nationality rules before iterating pets. Stays with `itertools.permutations` but cuts the search space by orders of magnitude in practice.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=The flat brute-force over all 5 attributes is conceptually O((5!)^5) which is ~25 billion combinations. Even with Python's speed at iteration this would be slow or need to be carefully structured. Early pruning by nesting loops and applying constraints incrementally reduces this massively in practice. Both use itertools.permutations (matching the user's request), but the pruning approach is the pragmatic choice for this puzzle.

Tutor: Both approaches use `itertools.permutations`, but they differ dramatically in how much work Python actually does.

**A — Brute-force permutations**
Generate all `5!` permutations for each of the 5 attributes (nationality, color, drink, smoke, pet), check every combination of those against all 15 constraints. Simple to read but evaluates up to `(5!)^5 ≈ 25 billion` tuples before pruning.

**B — Permutations with early pruning**
Nest the attribute loops and apply constraints as early as possible — e.g. check color/nationality rules before iterating pets. Stays with `itertools.permutations` but cuts the search space by orders of magnitude in practice.

Which do you prefer?

### Student

I think **B** makes more sense. 

Even though A is simpler to understand at first glance, checking 25 billion combinations seems wasteful when we can eliminate invalid partial assignments much earlier. If we know the Englishman lives in the red house, there's no point generating all the pet permutations for cases where that constraint is already violated.

That said, I'm curious — when you say "nest the attribute loops and apply constraints as early as possible," does that mean we'd build up the solution house-by-house (like, fix house 1's nationality, then check what colors/drinks are compatible, then move to house 2)? Or are we still working with permutations but just filtering after each attribute layer?

I want to make sure I understand the structure before we start coding.

---

## Turn 2

### Tutor

Thinking: The user wants to understand the structure of the approach. Let me clarify: we're still working with permutations of entire attributes (not building house-by-house), but we apply constraints as we add each attribute layer. So it's more like:
  
  1. Generate all permutations of colors
  2. For each color permutation, generate all permutations of nationalities
  3. Check nationality+color constraints (Englishman=red, etc.)
  4. Only if those pass, generate all permutations of drinks
  5. Check drink+color+nationality constraints
  
  
  6. Continue this pattern through the remaining attributes, filtering at each step
  
  This layered filtering approach differs fundamentally from a house-by-house backtracking search, which would use constraint propagation more dynamically. I should clarify which structure we're actually implementing here.

Tutor: Good question — let me clarify with a concrete choice, because these really are two different structures:

OPTIONS:
[A] Attribute-layer nesting
Loop over full permutations of one attribute at a time — colors, then nationalities (checking color+nat constraints), then drinks (checking those constraints), etc. Each inner loop only runs if the outer layers already pass. Still `5! × 5! × …` in the worst case per layer, but bad layers are skipped early.

[B] House-by-house backtracking
Assign all 5 attributes to house 1, then house 2, etc., pruning whenever any partial assignment violates a constraint. Tighter pruning per step, but the code is more involved — essentially reimplementing backtracking search by hand.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Attribute-layer nesting with itertools.permutations is the idiomatic Python approach for this puzzle. It's easy to write, read, and reason about, and it runs in well under a second for a 5-house puzzle. House-by-house backtracking gives tighter pruning in theory but the code is significantly more complex and the performance gain is irrelevant at this scale. The user also specifically asked about permutations, so this directly answers their question.

Tutor: **A — Attribute-layer nesting**
Loop over full permutations of one attribute at a time — colors, then nationalities (checking color+nat constraints), then drinks (checking those constraints), etc. Each inner loop only runs if the outer layers already pass. Still `5! × 5! × …` in the worst case per layer, but bad layers are skipped early.

**B — House-by-house backtracking**
Assign all 5 attributes to house 1, then house 2, etc., pruning whenever any partial assignment violates a constraint. Tighter pruning per step, but the code is more involved — essentially reimplementing backtracking search by hand.

Which structure do you want?

### Student

I'll go with **A — Attribute-layer nesting**.

It feels like a good balance: it's still built around `itertools.permutations` (which the problem suggests), but we get meaningful pruning by checking constraints between layers. And the code should be more readable than hand-rolled backtracking.

Let's start coding and see how it goes. Should I begin by setting up the houses, defining the valid values for each attribute, and then sketching out the nested loop structure?

---

## Turn 3

### Tutor

Thinking: The user wants to start coding. Let me create the file. I'll start with the foundational structure and then propose the first key decision - how to represent a house/solution.
  
  Let me think about what the first decision should be. A good first decision would be about how to represent the data - as indices (tuples of positions) vs. as named constants. Let me think about what's most instructive here.
  
  Actually, the first foundational decision I want to propose is how to represent the houses/attributes. We could use:
  - Integer indices (0-4 for houses, and permutations as tuples of positions)
  - Named constants/enums
  
  Let me propose this as an option. Actually, let me think about what's most instructive...
  
  
  I'm circling back on the core design choice here - whether to use string literals directly for readability or integer indices with named constants for the attribute values. The real foundational decision though is probably how we structure the constraint helpers and the overall file layout, so let me start by proposing that initial structure first.
  
  For the Exercism puzzle, the function needs to return a tuple of the water drinker and zebra owner. The most fundamental question is how we represent a solution internally as we pass it around - either as a named tuple or dict for each house, or as separate tuples for each attribute.
  
  I'm leaning toward separate tuples since that works naturally with a permutations-based approach. With that structure, finding "who lives in the red house" becomes a simple index lookup. Now I need to decide on the overall skeleton - whether to put all constraints in one validation function or split them across multiple checks.
  
  Actually, the more important first decision is how to express directional constraints like "immediately to the right." I could use `abs(a - b) == 1` for general adjacency, or `a + 1 == b` to be explicit about direction. That distinction matters for constraint 6, so let me propose both options and see which feels clearer for the puzzle. The key decision here is how to represent the constraint checks themselves—I can either write clean helper functions like `right_of()` and `next_to()` that make the logic readable, or inline the index arithmetic directly in each constraint. I'll present both approaches after setting up the initial file skeleton.

Tutor: Yes, let's go. First foundational decision — how we structure the solution:

OPTIONS:
[A] One tuple per attribute
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,12 @@
+from itertools import permutations
+
+COLORS      = ("red", "green", "ivory", "yellow", "blue")
+NATIONS     = ("Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese")
+DRINKS      = ("coffee", "tea", "milk", "oj", "water")
+SMOKES      = ("OldGold", "Kools", "Chesterfields", "LuckyStrike", "Parliaments")
+PETS        = ("dog", "snails", "fox", "horse", "zebra")
+
+def solution():
+    for colors in permutations(range(5)):
+        for nations in permutations(range(5)):
+            # check color+nation constraints, then continue...
+            pass
```
Each permutation is a tuple of house indices (0–4). `colors[i]` = which house gets color `i`.

[B] Dict of dicts per house
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,10 @@
+from itertools import permutations
+
+def solution():
+    attrs = ["color","nation","drink","smoke","pet"]
+    values = [("red","green","ivory","yellow","blue"),
+              ("Englishman","Spaniard","Ukrainian","Norwegian","Japanese"),
+              ("coffee","tea","milk","oj","water"),
+              ("OldGold","Kools","Chesterfields","LuckyStrike","Parliaments"),
+              ("dog","snails","fox","horse","zebra")]
+    for combo in product(*[permutations(v) for v in values]):
```
Bundles all attributes together; each combo is a 5-tuple of 5-tuples indexed by house.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Option A (one tuple per attribute) is the right structure for attribute-layer nesting with early pruning. It lets us loop over colors first, check color constraints, then loop over nations and check, etc. Option B bundles all permutations together, which loses the early-pruning benefit — it's essentially the flat brute-force approach we already ruled out, just with different syntax.

Tutor: **A — One tuple per attribute**
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,12 @@
+from itertools import permutations
+
+COLORS      = ("red", "green", "ivory", "yellow", "blue")
+NATIONS     = ("Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese")
+DRINKS      = ("coffee", "tea", "milk", "oj", "water")
+SMOKES      = ("OldGold", "Kools", "Chesterfields", "LuckyStrike", "Parliaments")
+PETS        = ("dog", "snails", "fox", "horse", "zebra")
+
+def solution():
+    for colors in permutations(range(5)):
+        for nations in permutations(range(5)):
+            # check color+nation constraints, then continue...
+            pass
```
Each permutation is a tuple of house indices (0–4). `colors[i]` = which house gets color `i`.

**B — Dict of dicts per house**
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,10 @@
+from itertools import permutations
+
+def solution():
+    attrs = ["color","nation","drink","smoke","pet"]
+    values = [("red","green","ivory","yellow","blue"),
+              ("Englishman","Spaniard","Ukrainian","Norwegian","Japanese"),
+              ("coffee","tea","milk","oj","water"),
+              ("OldGold","Kools","Chesterfields","LuckyStrike","Parliaments"),
+              ("dog","snails","fox","horse","zebra")]
+    for combo in product(*[permutations(v) for v in values]):
```
Bundles all attributes together; each combo is a 5-tuple of 5-tuples indexed by house.

Which structure?

### Student

I'll go with **A — One tuple per attribute**.

It's clearer to me: `colors[i]` tells me which house gets color `i`, and I can build up the constraints layer by layer. Option B feels a bit harder to reason about when I'm writing the constraint checks — I'd have to keep track of which tuple is which attribute.

Let me start writing the skeleton with the constants and the nested loops. Then I'll need to implement the constraint-checking functions.

---

## Turn 4

### Tutor

Thinking: The user wants to start writing the skeleton. Let me create the initial file and then propose the constraint-checking approach.
  
  First, let me write the initial file with the constants and skeleton structure. Then I'll propose how to write the constraint helper functions.
  
  The key thing to note about the encoding: `colors[i]` = house index for color `i`. So `colors[0]` is the house index of "red" (first in COLORS tuple). To check "Englishman lives in red house": `nations[0] == colors[0]` (Englishman is index 0 in NATIONS, red is index 0 in COLORS).
  
  
  Now I'm thinking through how to express the spatial constraints—"immediately to the right" becomes checking if green's house index is one more than ivory's, and adjacency is just checking if their house indices differ by exactly one. The real question is whether to define named helper functions like `right_of()` and `next_to()` for readability, or inline the comparisons directly.
  
  But the more fundamental choice is about the encoding itself: should I map each color to its house position, or map each house to its color? The first approach means `colors[0]` tells me which house has red, while the second means `colors[0]` tells me what color house 1 has. Both work with permutations, but they flip how I'd answer different types of queries—one makes "what house has this color?" fast, while the other makes "what color is in this house?" fast. same house). For "green is immediately to the right of ivory," that translates to `colors[1] == colors[2] + 1`, and "Norwegian lives in first house" becomes `nations[3] == 0`. This encoding works well for expressing the constraints. I'm thinking about whether to create helper functions like `right_of` and `next_to` for readability, but I'll set up the file with the constants and basic structure first, then decide on the helpers based on what makes sense pedagogically.

Tutor: Let's write the file, then tackle the constraint helpers as the next decision.

[Glob(zebra_puzzle.py)]
  No files found

[Write(zebra_puzzle.py)]
from itertools import permutations

# Indices into each permutation tuple
# e.g. colors[i] = house number (0–4) assigned to the i-th color
COLORS  = ("red", "green", "ivory", "yellow", "blue")
NATIONS = ("Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese")
DRINKS  = ("coffee", "tea", "milk", "oj", "water")
SMOKES  = ("OldGold", "Kools", "Chesterfields", "LuckyStrike", "Parliaments")
PETS    = ("dog", "snails", "fox", "horse", "zebra")


def solution():
… (12 more lines)
  File created successfully at: zebra_puzzle.py

Tutor: Good — skeleton is in place. Now the key question before filling in the constraints: there are two kinds of spatial relationship in this puzzle. How should we express them?

OPTIONS:
[A] Named helper functions
```diff
+++ zebra_puzzle.py
@@ -12,0 +13,6 @@
+def next_to(a, b):
+    return abs(a - b) == 1
+
+def right_of(a, b):
+    return a == b + 1
+
```
Constraint 6 becomes `right_of(colors[1], colors[2])`. Constraint 11 becomes `next_to(smokes[2], pets[2])`.

[B] Inline arithmetic everywhere
```diff
+++ zebra_puzzle.py
@@ -16,2 +16,2 @@
-            # color+nation constraints go here
+            if nations[0] == colors[0] and nations[3] == 0:  # Englishman/red, Norwegian/first
```
Write `abs(a - b) == 1` and `a == b + 1` directly at each constraint site. No helpers needed.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Named helpers are better here. The puzzle has 5 adjacency/directional constraints and the distinction between "next to" (symmetric, abs difference) and "immediately to the right" (directional, +1) is easy to confuse. Named functions make the intent explicit and prevent subtle bugs like using abs() where directionality matters (constraint 6: green is specifically to the RIGHT of ivory, not just adjacent). The helpers also make the final constraint block read almost like the original puzzle description.

Tutor: **A — Named helper functions**
```diff
+++ zebra_puzzle.py
@@ -12,0 +13,6 @@
+def next_to(a, b):
+    return abs(a - b) == 1
+
+def right_of(a, b):
+    return a == b + 1
+
```
Constraint 6 becomes `right_of(colors[1], colors[2])`. Constraint 11 becomes `next_to(smokes[2], pets[2])`.

**B — Inline arithmetic everywhere**
```diff
+++ zebra_puzzle.py
@@ -16,2 +16,2 @@
-            # color+nation constraints go here
+            if nations[0] == colors[0] and nations[3] == 0:  # Englishman/red, Norwegian/first
```
Write `abs(a - b) == 1` and `a == b + 1` directly at each constraint site. No helpers needed.

Which do you prefer?

### Student

**A — Named helper functions**.

With 15 constraints to check, having `next_to()` and `right_of()` will make the code much more readable. It's easier to scan through the logic and see what each constraint is doing without parsing the arithmetic each time. Plus if I need to debug a constraint later, the helper name gives me context.

Let me add those helpers and then start writing out the constraint checks in the nested loops.

---

## Turn 5

### Tutor

Thinking: The user chose A. Let me add the helper functions to the file and then propose how to fill in the constraints. The next interesting decision would be about the constraint placement - where exactly to put each constraint check in the nested loop structure.
  
  Let me add the helpers and then propose the constraint organization.

[Edit(zebra_puzzle.py)]
--- before
def solution():
--- after
def next_to(a, b):
    return abs(a - b) == 1

def right_of(a, b):
    return a == b + 1

def solution():
  The file zebra_puzzle.py has been updated successfully.

Tutor: Now the interesting decision: where to place the 15 constraints across the 5 loop layers. Here's a representative sample — how would you distribute them?

OPTIONS:
[A] Check at earliest possible layer
```diff
+++ zebra_puzzle.py
@@ -17,6 +17,10 @@
     for colors in permutations(range(5)):
+        if not right_of(colors[1], colors[2]):   # green right of ivory
+            continue
         for nations in permutations(range(5)):
+            if nations[0] != colors[0]: continue  # Englishman/red
+            if nations[3] != 0: continue          # Norwegian first
             for drinks in permutations(range(5)):
+                if drinks[0] != colors[1]: continue  # coffee/green
```
Each constraint fires as soon as all the attributes it references are in scope.

[B] All constraints at innermost loop
```diff
+++ zebra_puzzle.py
@@ -22,3 +22,18 @@
                     for pets in permutations(range(5)):
+                        if (right_of(colors[1], colors[2])
+                            and nations[0] == colors[0]
+                            and nations[3] == 0
+                            and drinks[0] == colors[1]
+                            # ... all 15 constraints ...
+                            ):
+                            return answer
```
One big `if` block at the bottom. Simpler structure, every constraint checked for every combination of all 5 attributes.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Checking at the earliest possible layer is the whole point of attribute-layer nesting — it's what makes this approach fast. Option B is essentially the brute-force approach we rejected earlier, just with a nested loop structure on the outside. With early checking, a bad color permutation is rejected immediately before any of the 5!^4 = 207M iterations of the inner loops run. Option B checks all 25B combinations regardless. This is the core pruning insight.

Tutor: **A — Check at earliest possible layer**
```diff
+++ zebra_puzzle.py
@@ -17,6 +17,10 @@
     for colors in permutations(range(5)):
+        if not right_of(colors[1], colors[2]):   # green right of ivory
+            continue
         for nations in permutations(range(5)):
+            if nations[0] != colors[0]: continue  # Englishman/red
+            if nations[3] != 0: continue          # Norwegian first
             for drinks in permutations(range(5)):
+                if drinks[0] != colors[1]: continue  # coffee/green
```
Each constraint fires as soon as all the attributes it references are in scope.

**B — All constraints at innermost loop**
```diff
+++ zebra_puzzle.py
@@ -22,3 +22,18 @@
                     for pets in permutations(range(5)):
+                        if (right_of(colors[1], colors[2])
+                            and nations[0] == colors[0]
+                            and nations[3] == 0
+                            and drinks[0] == colors[1]
+                            # ... all 15 constraints ...
+                            ):
+                            return answer
```
One big `if` block at the bottom. Simpler structure, every constraint checked for every combination of all 5 attributes.

Which approach?

### Student

**A — Check at earliest possible layer**.

This is the whole point of attribute-layer nesting, right? If I check constraints as soon as I have the attributes they need, I skip generating permutations in deeper loops that are already doomed to fail. Option B defeats that purpose — it generates all `(5!)^5` combinations and only then filters.

Let me start mapping out which constraints apply at each layer so I can implement them correctly.

---

## Turn 6

### Tutor

Thinking: The user correctly identified why A is better. Now let me help them implement the full solution. Let me think about which constraints belong at which layer:
  
  **Layer 1: colors only**
  - Constraint 6: green is immediately to the right of ivory → `right_of(colors[1], colors[2])`
  
  **Layer 2: colors + nations**
  - Constraint 2: Englishman lives in red house → `nations[0] == colors[0]`
  - Constraint 10: Norwegian lives in first house → `nations[3] == 0`
  - Constraint 15: Norwegian lives next to blue house → `next_to(nations[3], colors[4])`
  
  
  - Constraint 4: Coffee is drunk in green house → `drinks[0] == colors[1]`
  - Constraint 5: Ukrainian drinks tea → `drinks[1] == nations[2]`
  - Constraint 9: Milk is drunk in middle house → `drinks[2] == 2`
  - Constraint 8: Kools are smoked in yellow house → `smokes[1] == colors[3]`
  - Constraint 13: Lucky Strike smoker drinks OJ → `smokes[3] == drinks[3]`
  - Constraint 14: Japanese smokes Parliaments → `smokes[4] == nations[4]`
  - Constraint 3: Spaniard owns dog → `pets[0] == nations[1]`
  - Constraint 7: Old Gold smoker owns snails → `pets[1] == smokes[0]`
  - Constraint 11: Chesterfields smoker lives next to fox owner → `next_to(smokes[2], pets[2])`
  - Constraint 12: Kools smoker next to horse owner → `next_to(smokes[1], pets[3])`
  
  Now I need to figure out who drinks water and who owns the zebra by solving these constraints together. Let me reconsider how I'm encoding this problem.
  
  Each attribute array is a permutation where the index represents the attribute type and the value represents which house it's in. So `colors[0]` tells me which house has red, `nations[0]` tells me which house has the Englishman, and so on. This means I can directly compare indices to enforce constraints like the Englishman living in the red house.
  
  Now I'm mapping out the remaining constraints using this same indexing scheme—checking that coffee is in the green house, the Ukrainian drinks tea, green is positioned right of ivory, and working through the adjacency and positioning rules for the cigarette brands and pets.
  
  To solve for who drinks water, I need to find which house contains water, then identify the nationality of whoever lives there.
  
  I can use `nations.index(drinks[4])` to find the position where the nationality tuple matches the water house, then look up that nationality from the NATIONS list. The same approach works for finding the zebra owner.
  
  Finalizing the solution... I'm debating whether to present the constraint assignments as a decision point or just implement the full solution directly. Let me work through all the constraints systematically across each layer—starting with the color constraints, then adding nations, then drinks—to make sure I have them all correct before writing the complete code. I'm verifying the constraint count against the original puzzle statement. Let me list out all 15 constraints and make sure I've captured each one correctly in my formulation.

Tutor: Exactly right. Now let's map all 14 constraints to their layers and write the full solution. I'll lay out the assignment — you can verify it makes sense before we code it up:

| Layer | Variables available | Constraints |
|---|---|---|
| `colors` | colors | C6: green right of ivory |
| `nations` | colors, nations | C2: Englishman/red · C10: Norwegian/first · C15: Norwegian next to blue |
| `drinks` | + drinks | C4: coffee/green · C5: Ukrainian/tea · C9: milk/middle |
| `smokes` | + smokes | C8: Kools/yellow · C13: LuckyStrike/OJ · C14: Japanese/Parliaments |
| `pets` | all | C3: Spaniard/dog · C7: OldGold/snails · C11: Chesterfields↔fox · C12: Kools↔horse |

Each constraint lands at the earliest layer where all its referenced attributes exist. Let's write it out:

[Read(zebra_puzzle.py)]
  1	from itertools import permutations
  2	
  3	# Indices into each permutation tuple
  4	# e.g. colors[i] = house number (0–4) assigned to the i-th color
  5	COLORS  = ("red", "green", "ivory", "yellow", "blue")
  6	NATIONS = ("Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese")
  7	DRINKS  = ("coffee", "tea", "milk", "oj", "water")
  8	SMOKES  = ("OldGold", "Kools", "Chesterfields", "LuckyStrike", "Parliaments")
  9	PETS    = ("dog", "snails", "fox", "horse", "zebra")
  10	
  11	
  12	def next_to(a, b):
  … (18 more lines)

[Edit(zebra_puzzle.py)]
--- before
def solution():
    for colors in permutations(range(5)):
        # color-only constraints go here
        for nations in permutations(range(5)):
            # color+nation constraints go here
            for drinks in permutations(range(5)):
                # color+nation+drink constraints go here
                for smokes in permutations(range(5)):
                    # +smoke constraints go here
                    for pets in permutations(range(5)):
                        # final constraints + return answer
                        pass
--- after
def solution():
    for colors in permutations(range(5)):
        if not right_of(colors[1], colors[2]):          # C6:  green right of ivory
            continue
        for nations in permutations(range(5)):
            if nations[0] != colors[0]: continue        # C2:  Englishman/red
            if nations[3] != 0: continue                # C10: Norwegian/first house
            if not next_to(nations[3], colors[4]): continue  # C15: Norwegian next to blue
            for drinks in permutations(range(5)):
                if drinks[0] != colors[1]: continue     # C4:  coffee/green
                if nations[2] != drinks[1]: continue    # C5:  Ukrainian/tea
                if drinks[2] != 2: continue             # C9:  milk in middle house
                for smokes in permutations(range(5)):
                    if smokes[1] != colors[3]: continue # C8:  Kools/yellow
                    if smokes[3] != drinks[3]: continue # C13: LuckyStrike/OJ
                    if nations[4] != smokes[4]: continue# C14: Japanese/Parliaments
                    for pets in permutations(range(5)):
                        if nations[1] != pets[0]: continue   # C3:  Spaniard/dog
                        if smokes[0] != pets[1]: continue    # C7:  OldGold/snails
                        if not next_to(smokes[2], pets[2]): continue  # C11: Chesterfields↔fox
                        if not next_to(smokes[1], pets[3]): continue  # C12: Kools↔horse
                        water_drinker = NATIONS[nations.index(drinks[4])]
                        zebra_owner   = NATIONS[nations.index(pets[4])]
                        return (water_drinker, zebra_owner)
  The file zebra_puzzle.py has been updated successfully.

[Bash(cd /Users/xxxxxxxx && python -c "from zebra_puzzle import solution; print(solution())")]
  error: Exit code 1

[Bash(python zebra_puzzle.py 2>/dev/null; python -c "from zebra_puzzle import solution; print(solution())")]
  ('Norwegian', 'Japanese')

Tutor: Works. **The Norwegian drinks water, the Japanese owns the zebra.**

One thing worth noticing before we call it done — the final two lines:

```python
water_drinker = NATIONS[nations.index(drinks[4])]
zebra_owner   = NATIONS[nations.index(pets[4])]
```

`drinks[4]` is the house number where water is served. `nations.index(drinks[4])` finds *which nationality index* lives in that house — and then we look up the name. Quick question: what's the time complexity of `nations.index(...)` here, and does it matter?

### Student

`nations.index(...)` is O(n), and since `nations` is a permutation of 5 elements, it's O(5) = O(1) in practice. So it doesn't matter at all — we're doing this lookup only once at the very end, not in a loop.

That said, I realize there's a cleaner way to think about it: `nations` is a permutation where `nations[i]` tells us which house the i-th nationality lives in. So `nations.index(drinks[4])` reverses that — it finds which nationality index corresponds to the house that drinks water. Then we grab the name from `NATIONS[that_index]`.

It works, but I could also just index directly into `NATIONS` after finding the right index. Either way, the logic is sound.

The solution runs and gives us the right answer. I think we're done!

<done/>

---

**Run end:** done after 6 turn(s) in 187.4s
