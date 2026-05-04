"""Zebra Puzzle — Einstein's classic 5-houses constraint problem.

Strategy: nested permutation search with aggressive early pruning.
Each attribute (nationality, color, drink, smoke, pet) is assigned a house
number 1-5.  We iterate over permutations of {1,2,3,4,5} for each attribute
and short-circuit as soon as any constraint is violated, keeping the search
tractable without an external solver.

The 15 clues
------------
 1.  There are five houses.                               (implicit)
 2.  The Englishman lives in the red house.
 3.  The Spaniard owns the dog.
 4.  Coffee is drunk in the green house.
 5.  The Ukrainian drinks tea.
 6.  The green house is immediately to the right of the ivory house.
 7.  The Old Gold smoker owns snails.
 8.  Kools are smoked in the yellow house.
 9.  Milk is drunk in the middle house.
10.  The Norwegian lives in the first house.
11.  The man who smokes Chesterfields lives next to the man with the fox.
12.  Kools are smoked next to the house where the horse is kept.
13.  The Lucky Strike smoker drinks orange juice.
14.  The Japanese smokes Parliaments.
15.  The Norwegian lives next to the blue house.
"""

from itertools import permutations


class ZebraPuzzle:
    def __init__(self):
        self._water_drinker, self._zebra_owner = self._solve()

    # ------------------------------------------------------------------ #
    # Public API expected by Exercism                                      #
    # ------------------------------------------------------------------ #

    def drinks_water(self) -> str:
        return self._water_drinker

    def owns_zebra(self) -> str:
        return self._zebra_owner

    # ------------------------------------------------------------------ #
    # Solver                                                               #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _solve() -> tuple[str, str]:
        houses = range(1, 6)  # house positions: 1 (left) … 5 (right)

        def next_to(a: int, b: int) -> bool:
            return abs(a - b) == 1

        def right_of(a: int, b: int) -> bool:
            """a is immediately to the right of b."""
            return a == b + 1

        # ---- nationality loop (pruned first — two cheap clues) ----------
        for nat in permutations(houses):
            Englishman, Spaniard, Ukrainian, Norwegian, Japanese = nat

            if Norwegian != 1:              # clue 10 — kills 96 % straight away
                continue

            # ---- color loop --------------------------------------------
            for col in permutations(houses):
                Red, Green, Ivory, Yellow, Blue = col

                if Englishman != Red:           # clue 2
                    continue
                if not right_of(Green, Ivory):  # clue 6
                    continue
                if not next_to(Norwegian, Blue):# clue 15
                    continue

                # ---- drink loop ----------------------------------------
                for drk in permutations(houses):
                    Coffee, Tea, Milk, OJ, Water = drk

                    if Coffee != Green:          # clue 4
                        continue
                    if Ukrainian != Tea:         # clue 5
                        continue
                    if Milk != 3:               # clue 9
                        continue

                    # ---- smoke loop ------------------------------------
                    for smk in permutations(houses):
                        OldGold, Kools, Chesterfields, LuckyStrike, Parliaments = smk

                        if Kools != Yellow:          # clue 8
                            continue
                        if LuckyStrike != OJ:        # clue 13
                            continue
                        if Japanese != Parliaments:  # clue 14
                            continue

                        # ---- pet loop ----------------------------------
                        for pet in permutations(houses):
                            Dog, Snails, Fox, Horse, Zebra = pet

                            if Spaniard != Dog:              # clue 3
                                continue
                            if OldGold != Snails:            # clue 7
                                continue
                            if not next_to(Chesterfields, Fox):  # clue 11
                                continue
                            if not next_to(Kools, Horse):    # clue 12
                                continue

                            # All 15 clues satisfied — build answer map
                            house_to_nat = {
                                Englishman: "Englishman",
                                Spaniard:   "Spaniard",
                                Ukrainian:  "Ukrainian",
                                Norwegian:  "Norwegian",
                                Japanese:   "Japanese",
                            }
                            return (
                                house_to_nat[Water],
                                house_to_nat[Zebra],
                            )

        raise RuntimeError("No solution found — check the clues!")  # should never happen
