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


# ── helpers ──────────────────────────────────────────────────────────────────

def _next_to(a: int, b: int) -> bool:
    """True when positions a and b are adjacent."""
    return abs(a - b) == 1


def _solve():
    """
    Return a list of 5 dicts, one per house (left → right), each containing:
        nationality, color, pet, drink, smoke
    """
    NATIONALITIES = ("Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese")
    COLORS        = ("red", "green", "ivory", "yellow", "blue")
    PETS          = ("dog", "snails", "fox", "horse", "zebra")
    DRINKS        = ("coffee", "tea", "milk", "oj", "water")
    SMOKES        = ("Old Gold", "Kools", "Chesterfields", "Lucky Strike", "Parliaments")

    for nat in permutations(range(5)):
        # nat[i] = nationality index living in house i
        # Equivalently: house of nationality k  →  nat.index(k)
        # We'll use a lookup array instead:
        # house_of_nat[k] = position of nationality k
        hn = [0] * 5
        for pos, k in enumerate(nat):
            hn[k] = pos
        # indices: Englishman=0, Spaniard=1, Ukrainian=2, Norwegian=3, Japanese=4

        # Clue 10 — Norwegian lives in house 1 (index 0)
        if hn[3] != 0:
            continue

        for col in permutations(range(5)):
            # col[i] = color index of house i
            # house_of_color[k] = position of color k
            # indices: red=0, green=1, ivory=2, yellow=3, blue=4
            hc = [0] * 5
            for pos, k in enumerate(col):
                hc[k] = pos

            # Clue 2  — Englishman lives in the red house
            if hn[0] != hc[0]:
                continue
            # Clue 6  — green house is immediately right of ivory house
            if hc[1] != hc[2] + 1:
                continue
            # Clue 15 — Norwegian lives next to the blue house
            if not _next_to(hn[3], hc[4]):
                continue

            for pet in permutations(range(5)):
                # pet[i] = pet index in house i
                # house_of_pet[k] = position of pet k
                # indices: dog=0, snails=1, fox=2, horse=3, zebra=4
                hp = [0] * 5
                for pos, k in enumerate(pet):
                    hp[k] = pos

                # Clue 3  — Spaniard owns the dog
                if hn[1] != hp[0]:
                    continue

                for drink in permutations(range(5)):
                    # drink[i] = drink index in house i
                    # house_of_drink[k] = position of drink k
                    # indices: coffee=0, tea=1, milk=2, oj=3, water=4
                    hd = [0] * 5
                    for pos, k in enumerate(drink):
                        hd[k] = pos

                    # Clue 9  — Milk is drunk in the middle house (index 2)
                    if hd[2] != 2:
                        continue
                    # Clue 4  — Coffee is drunk in the green house
                    if hd[0] != hc[1]:
                        continue
                    # Clue 5  — Ukrainian drinks tea
                    if hn[2] != hd[1]:
                        continue

                    for smoke in permutations(range(5)):
                        # smoke[i] = smoke index in house i
                        # house_of_smoke[k] = position of smoke k
                        # indices: Old Gold=0, Kools=1, Chesterfields=2,
                        #          Lucky Strike=3, Parliaments=4
                        hs = [0] * 5
                        for pos, k in enumerate(smoke):
                            hs[k] = pos

                        # Clue 8  — Kools smoked in the yellow house
                        if hs[1] != hc[3]:
                            continue
                        # Clue 13 — Lucky Strike smoker drinks orange juice
                        if hs[3] != hd[3]:
                            continue
                        # Clue 14 — Japanese smokes Parliaments
                        if hn[4] != hs[4]:
                            continue
                        # Clue 7  — Old Gold smoker owns snails
                        if hs[0] != hp[1]:
                            continue
                        # Clue 11 — Chesterfields smoker is next to fox owner
                        if not _next_to(hs[2], hp[2]):
                            continue
                        # Clue 12 — Kools smoker is next to horse owner
                        if not _next_to(hs[1], hp[3]):
                            continue

                        # ── solution found ───────────────────────────────
                        houses = []
                        for i in range(5):
                            houses.append({
                                "position":    i + 1,
                                "nationality": NATIONALITIES[nat[i]],
                                "color":       COLORS[col[i]],
                                "pet":         PETS[pet[i]],
                                "drink":       DRINKS[drink[i]],
                                "smoke":       SMOKES[smoke[i]],
                            })
                        return houses

    raise RuntimeError("No solution found — check the constraints!")


# Cache the solution so both public functions pay the search cost only once.
_SOLUTION = None

def _get_solution():
    global _SOLUTION
    if _SOLUTION is None:
        _SOLUTION = _solve()
    return _SOLUTION


# ── public API (Exercism contract) ────────────────────────────────────────────

def drinks_water() -> str:
    """Return the nationality of the person who drinks water."""
    for house in _get_solution():
        if house["drink"] == "water":
            return house["nationality"]


def owns_zebra() -> str:
    """Return the nationality of the person who owns the zebra."""
    for house in _get_solution():
        if house["pet"] == "zebra":
            return house["nationality"]


# ── pretty-print when run directly ───────────────────────────────────────────

if __name__ == "__main__":
    solution = _get_solution()

    header = f"{'#':<4} {'Nationality':<13} {'Color':<8} {'Pet':<8} {'Drink':<14} {'Smoke'}"
    print(header)
    print("-" * len(header))
    for h in solution:
        print(
            f"{h['position']:<4} {h['nationality']:<13} {h['color']:<8} "
            f"{h['pet']:<8} {h['drink']:<14} {h['smoke']}"
        )
    print()
    print(f"💧  Drinks water : {drinks_water()}")
    print(f"🦓  Owns the zebra: {owns_zebra()}")
