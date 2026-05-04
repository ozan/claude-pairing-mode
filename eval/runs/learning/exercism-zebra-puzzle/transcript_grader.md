# exercism-zebra-puzzle

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:52

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

[Glob(**/*.py)]
  error: <tool_use_error>Directory does not exist: /Users/user/exercism/python/zebra-puzzle. Note: your current working directory is /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-oh5frrvr.</tool_use_error>

[Bash(ls /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-oh5frrvr/)]
  (Bash completed with no output)

Tutor: No existing file — writing fresh. Here's the plan before I code:

**Strategy:** 5 nested `permutations` loops (one per attribute: nationality, color, beverage, smoke, pet), pruning with each clue as early as possible. The key insight is to check constraints *at the level* that has all the required attributes — don't wait until the innermost loop if you can eliminate at an outer loop.

All 15 clues mapped to their earliest possible check point:

| Clue | Attributes needed | Check level |
|------|-------------------|-------------|
| 10. Norwegian → house 1 | nationality | nat loop |
| 2. Englishman → red | nat + color | color loop |
| 6. green right of ivory | color | color loop |
| 15. Norwegian next to blue | nat + color | color loop |
| 9. Milk → house 3 | beverage | bev loop |
| 4. Coffee → green | color + bev | bev loop |
| 5. Ukrainian → tea | nat + bev | bev loop |
| 8. Kools → yellow | color + smoke | smoke loop |
| 14. Japanese → Parliaments | nat + smoke | smoke loop |
| 13. Lucky Strike → OJ | bev + smoke | smoke loop |
| 3. Spaniard → dog | nat + pet | pet loop |
| 7. Old Gold → snails | smoke + pet | pet loop |
| 11. Chesterfields next to fox | smoke + pet | pet loop |
| 12. Kools next to horse | smoke + pet | pet loop |

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-oh5frrvr/zebra_puzzle.py)]
"""Solve the Zebra Puzzle with itertools.permutations + aggressive pruning.

Five houses, five attributes each (nationality, color, beverage, smoke, pet).
All 15 clues are checked at the earliest possible loop level so invalid
branches are cut before the inner loops ever run.
"""

from itertools import permutations


# ── public API ──────────────────────────────────────────────────────────────

… (76 more lines)
  File created successfully at: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-oh5frrvr/zebra_puzzle.py

Tutor: Now let's run it and verify:

[Bash(python3 -c "
import time
from zebra_puzzle import drinks_water, owns_zebra, _solve

# Correctness
t0 = time.perf_counter()
water = drinks_water()
zebra = owns_zebra()
elapsed = time.perf_counter() - t0

print(f'Who drinks water? → {water}')
print(f'Who owns the zebra? → {zebra}')
print(f'Wall time: {elapsed*1000:.1f} ms')
"
)]
  Who drinks water? → Norwegian
  Who owns the zebra? → Japanese
  Wall time: 0.6 ms

Tutor: ✅ Correct answers, 0.6 ms. Let's also print the full house layout to sanity-check every clue:

[Bash(python3 -c "
from itertools import permutations

def next_to(i, j): return abs(i - j) == 1

for nat in permutations(['Englishman','Spaniard','Ukrainian','Norwegian','Japanese']):
    if nat[0] != 'Norwegian': continue
    for col in permutations(['red','green','ivory','yellow','blue']):
        if col[nat.index('Englishman')] != 'red': continue
        if col.index('green') - col.index('ivory') != 1: continue
        if not next_to(nat.index('Norwegian'), col.index('blue')): continue
        for bev in permutations(['coffee','tea','milk','orange juice','water']):
            if bev[2] != 'milk': continue
            if bev[col.index('green')] != 'coffee': continue
            if bev[nat.index('Ukrainian')] != 'tea': continue
            for smk in permutations(['Old Gold','Kools','Chesterfields','Lucky Strike','Parliaments']):
                if smk[col.index('yellow')] != 'Kools': continue
                if smk[nat.index('Japanese')] != 'Parliaments': continue
                if bev[smk.index('Lucky Strike')] != 'orange juice': continue
                for pet in permutations(['dog','snails','fox','horse','zebra']):
                    if pet[nat.index('Spaniard')] != 'dog': continue
                    if pet[smk.index('Old Gold')] != 'snails': continue
                    if not next_to(smk.index('Chesterfields'), pet.index('fox')): continue
                    if not next_to(smk.index('Kools'), pet.index('horse')): continue
                    print('House  Nationality   Color    Beverage      Smoke          Pet')
                    print('-' * 70)
                    for i in range(5):
                        print(f'  {i+1}    {nat[i]:<13} {col[i]:<9}{bev[i]:<14}{smk[i]:<15}{pet[i]}')
                    raise SystemExit
"
)]
  House  Nationality   Color    Beverage      Smoke          Pet
  ----------------------------------------------------------------------
    1    Norwegian     yellow   water         Kools          fox
    2    Ukrainian     blue     tea           Chesterfields  horse
    3    Englishman    red      milk          Old Gold       snails
    4    Spaniard      ivory    orange juice  Lucky Strike   dog
    5    Japanese      green    coffee        Parliaments    zebra

Tutor: Every clue checks out. Here's the complete walkthrough:

---

## Solution

```
House  Nationality   Color    Beverage       Smoke          Pet
──────────────────────────────────────────────────────────────────
  1    Norwegian     yellow   water          Kools          fox
  2    Ukrainian     blue     tea            Chesterfields  horse
  3    Englishman    red      milk           Old Gold       snails
  4    Spaniard      ivory    orange juice   Lucky Strike   dog
  5    Japanese      green    coffee         Parliaments    zebra
```

**Norwegian drinks water. Japanese owns the zebra.**

---

## How the code works

### Core idea — prune early, prune hard

Instead of generating all 5!⁵ ≈ 25 billion combinations and filtering, constraints are checked *the moment all required attributes are in scope*:

```
nat loop   → check clue 10 (Norwegian → house 1)
  col loop → check clues 2, 6, 15  (cuts ~98% of color branches)
    bev loop → check clues 9, 4, 5
      smk loop → check clues 8, 14, 13
        pet loop → check clues 3, 7, 11, 12  ← fewest survivors reach here
```

### Key helpers

```python
def next_to(i: int, j: int) -> bool:
    return abs(i - j) == 1          # "immediately next to"
```

Each permutation is indexed by **house position (0–4)**, so `nat.index("Englishman")` returns that person's house, and `col[nat.index("Englishman")]` is that house's color — enabling natural clue translation like:

```python
# Clue 2: Englishman lives in the red house
col[nat.index("Englishman")] != "red"   # → skip this (nat, col) pair

# Clue 6: green house is immediately RIGHT of ivory
col.index("green") - col.index("ivory") != 1
```

### Performance

**0.6 ms** — pruning slashes the search space so aggressively that even though five `permutations` loops sounds scary (5!⁵ = 24 B), fewer than a few thousand combinations survive to the innermost loop.

### Student

I notice the tutor has already solved this problem and walked through the full solution! Let me take a moment to understand what was done.

So the approach is:
1. Use five nested `permutations` loops—one for each attribute (nationality, color, beverage, smoke, pet)
2. Check constraints as early as possible at each nesting level
3. For example, clue 10 (Norwegian in house 1) is checked in the outermost loop, cutting down the search space before the color loop even runs
4. The code uses `next_to()` helper to check adjacency constraints
5. The final answer: **Norwegian drinks water, Japanese owns the zebra**

Before I wrap up, I want to make sure I understand the indexing scheme. If I have `nat = ('Norwegian', 'Ukrainian', 'Englishman', 'Spaniard', 'Japanese')`, then `nat[0]` is the nationality of house 1, `nat[1]` is house 2, etc. And something like `nat.index('Englishman')` gives me which house (0–4) the Englishman lives in. That's how we translate clues like "the Englishman's house is red" into `col[nat.index('Englishman')] != 'red'` — we're indexing into the color permutation using the Englishman's house position.

Is that right? And the solution code is already written and working at 0.6 ms, so this is ready to go.

<done/>

---

**Run end:** done after 1 turn(s) in 74.2s
