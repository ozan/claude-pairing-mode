from itertools import permutations


def next_to(a, b):
    return abs(a - b) == 1


def right_of(a, b):
    return a == b + 1


def _solve():
    houses = range(5)
    people = ("Norwegian", "Englishman", "Spaniard", "Ukrainian", "Japanese")

    for nat in permutations(houses):
        Norwegian, Englishman, Spaniard, Ukrainian, Japanese = nat
        if Norwegian != 0:                          # clue 9
            continue

        for col in permutations(houses):
            Red, Green, Ivory, Yellow, Blue = col
            if Englishman != Red:                   # clue 1
                continue
            if not right_of(Green, Ivory):          # clue 5
                continue
            if not next_to(Norwegian, Blue):        # clue 14
                continue

            for drink in permutations(houses):
                Coffee, Tea, Milk, OJ, Water = drink
                if Coffee != Green:                 # clue 3
                    continue
                if Ukrainian != Tea:                # clue 4
                    continue
                if Milk != 2:                       # clue 8
                    continue

                for smoke in permutations(houses):
                    OldGold, Kools, Chesterfields, LuckyStrike, Parliaments = smoke
                    if Kools != Yellow:             # clue 7
                        continue
                    if LuckyStrike != OJ:           # clue 12
                        continue
                    if Japanese != Parliaments:     # clue 13
                        continue

                    for pet in permutations(houses):
                        Dog, Snails, Fox, Horse, Zebra = pet
                        if Spaniard != Dog:                     # clue 2
                            continue
                        if OldGold != Snails:                   # clue 6
                            continue
                        if not next_to(Chesterfields, Fox):     # clue 10
                            continue
                        if not next_to(Kools, Horse):           # clue 11
                            continue

                        return (
                            people[nat.index(Water)],
                            people[nat.index(Zebra)],
                        )


def drinks_water():
    return _solve()[0]


def owns_zebra():
    return _solve()[1]
