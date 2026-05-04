from itertools import permutations
from functools import lru_cache

# Each permutation is indexed by house (0 = leftmost).
# perm[house] = attribute_value   →   perm.index(value) = house number

Red, Green, Ivory, Yellow, Blue = range(5)
Englishman, Spaniard, Ukrainian, Norwegian, Japanese = range(5)
Coffee, Tea, Milk, OrangeJuice, Water = range(5)
OldGold, Kools, Chesterfields, LuckyStrike, Parliaments = range(5)
Dog, Snail, Fox, Horse, Zebra = range(5)

NATIONALITIES = ["Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese"]


def next_to(h1, h2):
    return abs(h1 - h2) == 1


def right_of(h1, h2):
    """h1 is immediately to the right of h2."""
    return h1 - h2 == 1


@lru_cache(maxsize=None)
def _solution():
    for color in permutations(range(5)):
        # Clue 5: green immediately right of ivory  [4/120 pass]
        if not right_of(color.index(Green), color.index(Ivory)):
            continue

        for nat in permutations(range(5)):
            # Clue 9: Norwegian in first house
            if nat[0] != Norwegian:
                continue
            # Clue 1: Englishman in red house
            if nat.index(Englishman) != color.index(Red):
                continue
            # Clue 14: Norwegian next to blue house (Norwegian is always house 0)
            if not next_to(0, color.index(Blue)):
                continue

            for drink in permutations(range(5)):
                # Clue 8: milk in the middle house
                if drink[2] != Milk:
                    continue
                # Clue 3: coffee drunk in the green house
                if drink.index(Coffee) != color.index(Green):
                    continue
                # Clue 4: Ukrainian drinks tea
                if drink.index(Tea) != nat.index(Ukrainian):
                    continue

                for smoke in permutations(range(5)):
                    # Clue 7: Kools smoked in the yellow house
                    if smoke.index(Kools) != color.index(Yellow):
                        continue
                    # Clue 13: Japanese smokes Parliaments
                    if smoke.index(Parliaments) != nat.index(Japanese):
                        continue
                    # Clue 12: Lucky Strike smoker drinks OJ
                    if drink.index(OrangeJuice) != smoke.index(LuckyStrike):
                        continue

                    for pet in permutations(range(5)):
                        # Clue 2: Spaniard owns the dog
                        if pet.index(Dog) != nat.index(Spaniard):
                            continue
                        # Clue 6: Old Gold smoker owns snails
                        if pet.index(Snail) != smoke.index(OldGold):
                            continue
                        # Clue 10: Chesterfields smoker next to fox owner
                        if not next_to(smoke.index(Chesterfields), pet.index(Fox)):
                            continue
                        # Clue 11: Kools smoker next to horse owner
                        if not next_to(smoke.index(Kools), pet.index(Horse)):
                            continue

                        # All 14 clues satisfied — unique solution found
                        return (
                            NATIONALITIES[nat[drink.index(Water)]],
                            NATIONALITIES[nat[pet.index(Zebra)]],
                        )


def drinks_water():
    return _solution()[0]


def owns_zebra():
    return _solution()[1]
