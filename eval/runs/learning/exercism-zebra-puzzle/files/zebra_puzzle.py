"""Solve the Zebra Puzzle with itertools.permutations + aggressive pruning.

Five houses, five attributes each (nationality, color, beverage, smoke, pet).
All 15 clues are checked at the earliest possible loop level so invalid
branches are cut before the inner loops ever run.
"""

from itertools import permutations


# ── public API ──────────────────────────────────────────────────────────────

def drinks_water() -> str:
    water_drinker, _ = _solve()
    return water_drinker


def owns_zebra() -> str:
    _, zebra_owner = _solve()
    return zebra_owner


# ── solver ───────────────────────────────────────────────────────────────────

def _solve() -> tuple[str, str]:
    """Return (water_drinker, zebra_owner) by brute-force with pruning."""

    def next_to(i: int, j: int) -> bool:
        return abs(i - j) == 1

    # Each permutation is a tuple of length 5 where index = house position (0–4).
    for nat in permutations(["Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese"]):
        # Clue 10: Norwegian lives in house 1 (index 0).
        if nat[0] != "Norwegian":
            continue

        for col in permutations(["red", "green", "ivory", "yellow", "blue"]):
            # Clue 2:  Englishman lives in the red house.
            if col[nat.index("Englishman")] != "red":
                continue
            # Clue 6:  Green house is immediately to the right of the ivory house.
            if col.index("green") - col.index("ivory") != 1:
                continue
            # Clue 15: Norwegian lives next to the blue house.
            if not next_to(nat.index("Norwegian"), col.index("blue")):
                continue

            for bev in permutations(["coffee", "tea", "milk", "orange juice", "water"]):
                # Clue 9:  Milk is drunk in the middle (3rd) house.
                if bev[2] != "milk":
                    continue
                # Clue 4:  Coffee is drunk in the green house.
                if bev[col.index("green")] != "coffee":
                    continue
                # Clue 5:  Ukrainian drinks tea.
                if bev[nat.index("Ukrainian")] != "tea":
                    continue

                for smk in permutations(["Old Gold", "Kools", "Chesterfields", "Lucky Strike", "Parliaments"]):
                    # Clue 8:  Kools are smoked in the yellow house.
                    if smk[col.index("yellow")] != "Kools":
                        continue
                    # Clue 14: Japanese smokes Parliaments.
                    if smk[nat.index("Japanese")] != "Parliaments":
                        continue
                    # Clue 13: Lucky Strike smoker drinks orange juice.
                    if bev[smk.index("Lucky Strike")] != "orange juice":
                        continue

                    for pet in permutations(["dog", "snails", "fox", "horse", "zebra"]):
                        # Clue 3:  Spaniard owns the dog.
                        if pet[nat.index("Spaniard")] != "dog":
                            continue
                        # Clue 7:  Old Gold smoker owns snails.
                        if pet[smk.index("Old Gold")] != "snails":
                            continue
                        # Clue 11: Chesterfields smoker lives next to the fox owner.
                        if not next_to(smk.index("Chesterfields"), pet.index("fox")):
                            continue
                        # Clue 12: Kools smoker lives next to the horse owner.
                        if not next_to(smk.index("Kools"), pet.index("horse")):
                            continue

                        # All 15 clues satisfied — unique solution found.
                        return nat[bev.index("water")], nat[pet.index("zebra")]

    raise ValueError("No solution found — check the clues.")
