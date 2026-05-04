"""Zebra Puzzle — solved with itertools.permutations + early pruning.

Houses are numbered 1–5 (left to right).
Each attribute is a tuple where index 0 = value for house 1, etc.
We represent each attribute as the *house number* assigned to each person/thing.

Constraints:
  1.  Englishman lives in the red house.
  2.  Spaniard owns the dog.
  3.  Coffee is drunk in the green house.
  4.  Ukrainian drinks tea.
  5.  Green house is immediately to the right of the ivory house.
  6.  Old Gold smoker owns snails.
  7.  Kools are smoked in the yellow house.
  8.  Milk is drunk in the middle house (house 3).
  9.  Norwegian lives in house 1.
 10.  Chesterfield smoker lives next to the fox owner.
 11.  Kools smoker lives next to the horse owner.
 12.  Lucky Strike smoker drinks orange juice.
 13.  Japanese smokes Parliaments.
 14.  Norwegian lives next to the blue house.
"""

from itertools import permutations
from functools import lru_cache


def _solve():
    """Return (water_drinker, zebra_owner) as nationality strings."""
    houses = range(1, 6)
    nationalities = ('Englishman', 'Spaniard', 'Ukrainian', 'Norwegian', 'Japanese')

    for colors in permutations(houses):
        red, green, ivory, yellow, blue = colors
        # Constraint 5: green is immediately right of ivory
        if green - ivory != 1:
            continue

        for nats in permutations(houses):
            englishman, spaniard, ukrainian, norwegian, japanese = nats
            # Constraint 9: Norwegian in house 1
            if norwegian != 1:
                continue
            # Constraint 1: Englishman in red house
            if englishman != red:
                continue
            # Constraint 14: Norwegian next to blue house
            if abs(norwegian - blue) != 1:
                continue

            for beverages in permutations(houses):
                coffee, tea, milk, oj, water = beverages
                # Constraint 3: coffee in green house
                if coffee != green:
                    continue
                # Constraint 4: Ukrainian drinks tea
                if ukrainian != tea:
                    continue
                # Constraint 8: milk in middle house
                if milk != 3:
                    continue

                for smokes in permutations(houses):
                    kools, chesterfield, oldgold, luckystrike, parliament = smokes
                    # Constraint 7: Kools in yellow house
                    if kools != yellow:
                        continue
                    # Constraint 12: Lucky Strike -> OJ
                    if luckystrike != oj:
                        continue
                    # Constraint 13: Japanese smokes Parliament
                    if japanese != parliament:
                        continue

                    for pets in permutations(houses):
                        dog, snail, fox, horse, zebra = pets
                        # Constraint 2: Spaniard owns dog
                        if spaniard != dog:
                            continue
                        # Constraint 6: Old Gold smoker owns snails
                        if oldgold != snail:
                            continue
                        # Constraint 10: Chesterfield smoker next to fox owner
                        if abs(chesterfield - fox) != 1:
                            continue
                        # Constraint 11: Kools smoker next to horse owner
                        if abs(kools - horse) != 1:
                            continue

                        # All 14 constraints satisfied — extract answers
                        nat_by_house = {h: name for h, name in zip(nats, nationalities)}
                        return nat_by_house[water], nat_by_house[zebra]

    raise ValueError("No solution found — check the constraints.")


# Solve once and cache so both public functions are fast
_WATER_DRINKER, _ZEBRA_OWNER = _solve()


def drinks_water() -> str:
    return _WATER_DRINKER


def owns_zebra() -> str:
    return _ZEBRA_OWNER


if __name__ == "__main__":
    print(f"The {drinks_water()} drinks water.")
    print(f"The {owns_zebra()} owns the zebra.")
