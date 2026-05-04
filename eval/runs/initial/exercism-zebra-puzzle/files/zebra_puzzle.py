from itertools import permutations

# Each constant is an index into its permutation tuple.
# perm[VALUE] = house position (0 = leftmost … 4 = rightmost)
ENGLISH, SPANISH, UKRAINIAN, NORWEGIAN, JAPANESE = range(5)
RED, GREEN, IVORY, YELLOW, BLUE = range(5)
COFFEE, TEA, MILK, OJ, WATER = range(5)
OLD_GOLD, KOOLS, CHESTERFIELDS, LUCKY_STRIKE, PARLIAMENTS = range(5)
DOG, SNAILS, FOX, HORSE, ZEBRA = range(5)

NAMES = ["Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese"]


def next_to(a, b):
    return abs(a - b) == 1


def solve():
    for nat in permutations(range(5)):
        # 10. Norwegian lives in house 1 (position 0)
        if nat[NORWEGIAN] != 0:
            continue
        for col in permutations(range(5)):
            # 2.  Englishman lives in the red house
            if nat[ENGLISH] != col[RED]:
                continue
            # 6.  Green house is immediately right of ivory house
            if col[GREEN] != col[IVORY] + 1:
                continue
            # 15. Norwegian lives next to the blue house
            if not next_to(nat[NORWEGIAN], col[BLUE]):
                continue
            for bev in permutations(range(5)):
                # 9.  Milk is drunk in the middle house
                if bev[MILK] != 2:
                    continue
                # 5.  Ukrainian drinks tea
                if nat[UKRAINIAN] != bev[TEA]:
                    continue
                # 4.  Coffee is drunk in the green house
                if col[GREEN] != bev[COFFEE]:
                    continue
                for smk in permutations(range(5)):
                    # 8.  Kools are smoked in the yellow house
                    if col[YELLOW] != smk[KOOLS]:
                        continue
                    # 14. Japanese smokes Parliaments
                    if nat[JAPANESE] != smk[PARLIAMENTS]:
                        continue
                    # 13. Lucky Strike smoker drinks OJ
                    if smk[LUCKY_STRIKE] != bev[OJ]:
                        continue
                    for pet in permutations(range(5)):
                        # 3.  Spaniard owns the dog
                        if nat[SPANISH] != pet[DOG]:
                            continue
                        # 7.  Old Gold smoker owns snails
                        if smk[OLD_GOLD] != pet[SNAILS]:
                            continue
                        # 11. Chesterfields smoker lives next to fox owner
                        if not next_to(smk[CHESTERFIELDS], pet[FOX]):
                            continue
                        # 12. Kools smoker lives next to horse owner
                        if not next_to(smk[KOOLS], pet[HORSE]):
                            continue
                        return nat, col, bev, smk, pet
    return None


_solution = solve()


def drinks_water():
    nat, col, bev, smk, pet = _solution
    return NAMES[nat.index(bev[WATER])]


def owns_zebra():
    nat, col, bev, smk, pet = _solution
    return NAMES[nat.index(pet[ZEBRA])]
