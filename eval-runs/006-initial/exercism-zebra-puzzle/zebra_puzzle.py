from itertools import permutations

# Attribute order within each permutation tuple:
NATIONS = ('Englishman', 'Spaniard', 'Ukrainian', 'Norwegian', 'Japanese')
DRINKS  = ('Coffee', 'Tea', 'Milk', 'OJ', 'Water')
PETS    = ('Dog', 'Snails', 'Fox', 'Horse', 'Zebra')


class ZebraPuzzle:
    def __init__(self):
        self._water_drinker, self._zebra_owner = self._solve()

    def drinks_water(self):
        return self._water_drinker

    def owns_zebra(self):
        return self._zebra_owner

    @staticmethod
    def _solve():
        houses = range(1, 6)

        def next_to(a, b):
            return abs(a - b) == 1

        for nats in permutations(houses):
            eng, spa, ukr, nor, jap = nats
            if nor != 1:                         # clue 10
                continue

            for cols in permutations(houses):
                red, grn, ivo, yel, blu = cols
                if eng != red:                   # clue 2
                    continue
                if grn - ivo != 1:               # clue 6: green immediately right of ivory
                    continue
                if not next_to(nor, blu):        # clue 15
                    continue

                for drnks in permutations(houses):
                    cof, tea, mlk, ojc, wat = drnks
                    if cof != grn:               # clue 4
                        continue
                    if ukr != tea:               # clue 5
                        continue
                    if mlk != 3:                 # clue 9: milk in middle house
                        continue

                    for smks in permutations(houses):
                        old, koo, che, luc, par = smks
                        if koo != yel:           # clue 8
                            continue
                        if luc != ojc:           # clue 13
                            continue
                        if jap != par:           # clue 14
                            continue

                        for ptz in permutations(houses):
                            dog, sna, fox, hor, zeb = ptz
                            if spa != dog:               # clue 3
                                continue
                            if old != sna:               # clue 7
                                continue
                            if not next_to(che, fox):    # clue 11
                                continue
                            if not next_to(koo, hor):    # clue 12
                                continue

                            # All constraints satisfied — map house → nation
                            house_to_nation = dict(zip(nats, NATIONS))
                            return house_to_nation[wat], house_to_nation[zeb]
