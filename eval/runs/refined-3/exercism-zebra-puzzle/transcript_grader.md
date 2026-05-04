# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:37

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Brute-force permutations
Generate all `5!` permutations for each of the 5 attributes (nationality, color, drink, smoke, pet), check every combination of those against all 15 constraints. Simple to read but evaluates up to `(5!)^5 ≈ 25 billion` tuples before pruning.

[B] Permutations with early pruning
Nest the attribute loops and apply constraints as early as possible — e.g. check color/nationality rules before iterating pets. Stays with `itertools.permutations` but cuts the search space by orders of magnitude in practice.

(Reply with A or B, or ask a follow-up question.)

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

Tutor: Good question — let me clarify with a concrete choice, because these really are two different structures:

OPTIONS:
[A] Attribute-layer nesting
Loop over full permutations of one attribute at a time — colors, then nationalities (checking color+nat constraints), then drinks (checking those constraints), etc. Each inner loop only runs if the outer layers already pass. Still `5! × 5! × …` in the worst case per layer, but bad layers are skipped early.

[B] House-by-house backtracking
Assign all 5 attributes to house 1, then house 2, etc., pruning whenever any partial assignment violates a constraint. Tighter pruning per step, but the code is more involved — essentially reimplementing backtracking search by hand.

(Reply with A or B, or ask a follow-up question.)

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
