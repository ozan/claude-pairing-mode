# exercism-zebra-puzzle

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:51:49

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

Thinking: The user wants me to solve the classic Zebra Puzzle (also known as Einstein's Puzzle). Let me write a Python solution for the Exercism Zebra Puzzle exercise.
  
  The classic puzzle constraints are:
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
  
  I need to find who drinks water and who owns the zebra. I'll use itertools.permutations to generate all possible house configurations and filter them against these constraints.
  
  Writing the solver functions... Still writing constraint checks... Finishing the constraint check for the Lucky Strike drinker, then validating the Japanese nationality constraint. Once all constraints pass, I'm constructing the solution by building a list of house objects with all their attributes and returning it. Now I need to think about the Exercism file structure and make sure I'm implementing just the required functions with clean, well-commented code.

[Glob(*zebra*)]
  No files found

[Bash(pwd)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-hvjwltel

Tutor: No existing file — I'll create the solution from scratch.

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-hvjwltel/zebra_puzzle.py)]
"""
Zebra Puzzle (Einstein's Riddle) — Exercism solution
=====================================================
Fifteen clues, five houses, five attributes each.
We iterate permutations from largest fan-out to smallest, pruning as early
as possible so the inner loops rarely get a chance to run.

Attribute order in every tuple:   (house 1, house 2, house 3, house 4, house 5)
Position index 0 = leftmost house, index 4 = rightmost house.
"""

from itertools import permutations
… (169 more lines)
  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-hvjwltel/zebra_puzzle.py

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-hvjwltel && python zebra_puzzle.py)]
  #    Nationality   Color    Pet      Drink          Smoke
  ---------------------------------------------------------
  1    Norwegian     yellow   fox      water          Kools
  2    Ukrainian     blue     horse    tea            Chesterfields
  3    Englishman    red      snails   milk           Old Gold
  4    Spaniard      ivory    dog      oj             Lucky Strike
  5    Japanese      green    zebra    coffee         Parliaments
  
  💧  Drinks water : Norwegian
  🦓  Owns the zebra: Japanese

Tutor: Works perfectly. Here's a full breakdown of the solution and how the code works.

---

## Answers

| Question | Answer |
|---|---|
| 💧 Who drinks water? | **Norwegian** |
| 🦓 Who owns the zebra? | **Japanese** |

---

## Full Solution Table

| House | Nationality | Color | Pet | Drink | Smoke |
|---|---|---|---|---|---|
| 1 | Norwegian | Yellow | Fox | Water | Kools |
| 2 | Ukrainian | Blue | Horse | Tea | Chesterfields |
| 3 | Englishman | Red | Snails | Milk | Old Gold |
| 4 | Spaniard | Ivory | Dog | OJ | Lucky Strike |
| 5 | Japanese | Green | Zebra | Coffee | Parliaments |

---

## How the Code Works

**Strategy: pruned nested `itertools.permutations`**

Each of the five attributes (nationality, color, pet, drink, smoke) has 5! = 120 permutations. Naïve brute-force would check 120⁵ ≈ 25 billion combos. Heavy early pruning keeps it instant.

**Key design decisions:**

1. **Lookup arrays for O(1) "house of X"** — instead of calling `.index()` in a hot loop, we pre-build `hn[nationality] → position`, `hc[color] → position`, etc. from each permutation tuple.

2. **Prune at the earliest layer possible** — constraints are checked as soon as all the attributes they reference are in scope:
   - Clues 10, 6, 15 (`Norwegian`, ivory/green adjacency, blue neighbor) are checked in the **nationality / color** loops — killing most combos before pets/drinks/smokes are ever tried.
   - Clue 9 (milk in middle) and clues 4 & 5 (coffee/green, Ukrainian/tea) prune the drink loop early.
   - All remaining smoke clues (7, 8, 11–14) prune the innermost loop.

3. **Result cache** — `_get_solution()` stores the result in a module-level global so `drinks_water()` and `owns_zebra()` both get the answer without paying the search cost twice.

4. **Exercism public API** — exactly the two functions `drinks_water() → str` and `owns_zebra() → str` that Exercism's test suite expects.

### Student

Thanks for walking me through the solution! I can see how the code is structured and that it's working correctly—the output shows Norwegian drinks water and Japanese owns the zebra.

I'd like to understand the constraint checking a bit better though. When you say constraints are "pruned at the earliest layer," I want to make sure I understand how that actually works in the code. 

Looking at the output, the solution is found and the two functions return the correct answers. Before we wrap up, could you show me one or two specific examples of how a constraint (like "clue 10: Norwegian is in house 1") actually prevents the code from exploring a branch? Like, what does that early-exit logic look like in the actual code?

I want to see the real constraint checks so I can understand *why* this approach is so much faster than checking all 25 billion combinations.

---

## Turn 2

### Tutor

Thinking: The user wants to understand how the pruning/early-exit logic works in the code. They want concrete examples of how specific constraints prevent the code from exploring branches. Let me read the code and explain this clearly.
  
  Let me re-read the relevant parts of the code to give a precise, accurate explanation.

Tutor: Great question — let me show you the exact lines and trace through the logic concretely.

[Read(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-hvjwltel/zebra_puzzle.py)]
  55	            # Clue 2  — Englishman lives in the red house
  56	            if hn[0] != hc[0]:
  57	                continue
  58	            # Clue 6  — green house is immediately right of ivory house
  59	            if hc[1] != hc[2] + 1:
  60	                continue
  61	            # Clue 15 — Norwegian lives next to the blue house
  62	            if not _next_to(hn[3], hc[4]):
  63	                continue
  64	
  65	            for pet in permutations(range(5)):
  66	                # pet[i] = pet index in house i
  … (43 more lines)

Tutor: Perfect. Here are two concrete examples, traced step by step.

---

### Example 1 — Clue 10: "Norwegian lives in house 1"

This is the very first check, at the top of the **outermost** loop:

```python
for nat in permutations(range(5)):   # 120 iterations of (0,1,2,3,4) in every order
    hn = [0]*5
    for pos, k in enumerate(nat):
        hn[k] = pos                  # hn[3] = position of the Norwegian (index 3)

    if hn[3] != 0:                   # ← Clue 10: Norwegian must be in house 0
        continue                     # skip the entire nat combo immediately
```

**What gets pruned:** `permutations` of 5 nationalities produces 120 orderings. The Norwegian appears in position 0 in only **1/5** of them (i.e., 24 out of 120). So 96 of the 120 nationality combos are rejected *before a single color, pet, drink, or smoke is ever tried.* Those 96 dead-ends would each have spawned up to 120⁴ ≈ 207 million further iterations — all avoided with one `if`.

---

### Example 2 — Clue 9: "Milk is drunk in the middle house"

This sits at the top of the **drink** loop, after nationality, color, and pet have already been committed:

```python
for drink in permutations(range(5)):   # 120 drink orderings
    hd = [0]*5
    for pos, k in enumerate(drink):
        hd[k] = pos                    # hd[2] = position of milk (index 2)

    if hd[2] != 2:                     # ← Clue 9: milk must be in house index 2
        continue
```

**What gets pruned:** Again, milk occupies position 2 in only 1/5 of the 120 orderings (24 of them). So for every (nat, color, pet) triple that survived the earlier checks, 96 out of 120 drink combos are killed *before the 120-iteration smoke loop even starts.* The smoke loop is the most expensive because it runs last and has the most checks — Clue 9 prevents it from running ~80% of the time.

---

### The compounding effect — why it's so much faster

Think of the five loops as a tree. Each level multiplies the branching factor:

```
nat (120 total)
 └─ only 24 pass Clue 10  (1/5 survive)
     └─ col (120 each) → only ~8 pass Clues 2, 6, 15
         └─ pet (120 each) → only ~24 pass Clue 3
             └─ drink (120 each) → only ~24 pass Clues 9, 4, 5
                 └─ smoke (120 each) → checked fully

Naïve:   120⁵  =  24,883,200,000
Pruned:   24 × 8 × 24 × 24 × 120  ≈  165,000   (~150,000× fewer)
```

Each `continue` doesn't just skip **one** iteration — it skips **all the inner loops** that would have been nested inside it. That's the key insight: pruning high in the tree has exponential leverage over everything below it.

### Student

Ah, that makes it crystal clear now! I see the compounding effect — rejecting a nationality permutation early saves you from running through 120⁴ combinations of everything else. And doing the same at the color, pet, and drink levels just multiplies the savings.

So the strategy is really: "Put the most restrictive clues at the outermost loops, so you kill entire branches of the search tree as soon as possible."

Let me just verify I'm understanding the actual implementation correctly. In the code you showed, when we do:

```python
if hn[3] != 0:
    continue
```

We're checking: "Is the Norwegian (index 3 in the nationalities list) at position 0?" And if not, we skip that entire permutation and move to the next one.

And then later, when we get to drinks:

```python
if hd[2] != 2:
    continue
```

We're checking: "Is milk (index 2 in the drinks list) at position 2 (the middle house)?" And if not, we skip that drink permutation — but only after we've already filtered down to the nationality/color/pet combos that passed their checks.

So the `hn`, `hc`, `hp`, `hd`, `hs` arrays are just reverse-lookup maps: given an attribute *value* (like "Norwegian" or "milk"), they tell us which *house position* it's in. That's brilliant for fast constraint checking.

Does that sound right? And just to close out — the solution found works correctly, so I think we're done here. The Norwegian drinks water and the Japanese owns the zebra. Perfect!

<done/>

---

**Run end:** done after 2 turn(s) in 84.2s
