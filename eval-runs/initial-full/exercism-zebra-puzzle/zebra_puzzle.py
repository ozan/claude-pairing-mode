"""Zebra Puzzle — classic Einstein/5-houses constraint problem.

Each permutation maps an attribute variant → house index (0–4).
Constraints are checked as early as possible (outermost = tightest prune).
"""
from itertools import permutations


def solve():
    houses = range(5)

    for nat in permutations(houses):
        Eng, Spa, Ukr, Nor, Jap = nat
        if Nor != 0: continue                    # clue 10: Norwegian in house 1

        for col in permutations(houses):
            Red, Grn, Ivo, Yel, Blu = col
            if Eng != Red: continue              # clue 2
            if Grn != Ivo + 1: continue          # clue 6: green right of ivory
            if abs(Nor - Blu) != 1: continue     # clue 15: Norwegian next to blue

            for pet in permutations(houses):
                Dog, Snl, Fox, Hrs, Zeb = pet
                if Spa != Dog: continue          # clue 3

                for drk in permutations(houses):
                    Cof, Tea, Mlk, OJu, Wat = drk
                    if Cof != Grn: continue      # clue 4
                    if Ukr != Tea: continue      # clue 5
                    if Mlk != 2: continue        # clue 9: milk in middle house

                    for smk in permutations(houses):
                        OGd, Koo, Che, LuS, Par = smk
                        if OGd != Snl: continue           # clue 7
                        if Koo != Yel: continue           # clue 8
                        if LuS != OJu: continue           # clue 13
                        if Jap != Par: continue           # clue 14
                        if abs(Che - Fox) != 1: continue  # clue 11
                        if abs(Koo - Hrs) != 1: continue  # clue 12

                        names = ['Englishman', 'Spaniard', 'Ukrainian',
                                 'Norwegian', 'Japanese']
                        water_drinker = names[nat.index(Wat)]
                        zebra_owner   = names[nat.index(Zeb)]
                        return water_drinker, zebra_owner


def drinks_water():
    return solve()[0]


def owns_zebra():
    return solve()[1]


if __name__ == '__main__':
    water, zebra = solve()
    print(f"The {water} drinks water.")
    print(f"The {zebra} owns the zebra.")
