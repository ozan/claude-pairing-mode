from itertools import permutations

# Indices into each permutation tuple
# e.g. colors[i] = house number (0–4) assigned to the i-th color
COLORS  = ("red", "green", "ivory", "yellow", "blue")
NATIONS = ("Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese")
DRINKS  = ("coffee", "tea", "milk", "oj", "water")
SMOKES  = ("OldGold", "Kools", "Chesterfields", "LuckyStrike", "Parliaments")
PETS    = ("dog", "snails", "fox", "horse", "zebra")


def next_to(a, b):
    return abs(a - b) == 1

def right_of(a, b):
    return a == b + 1

def solution():
    for colors in permutations(range(5)):
        if not right_of(colors[1], colors[2]):          # C6:  green right of ivory
            continue
        for nations in permutations(range(5)):
            if nations[0] != colors[0]: continue        # C2:  Englishman/red
            if nations[3] != 0: continue                # C10: Norwegian/first house
            if not next_to(nations[3], colors[4]): continue  # C15: Norwegian next to blue
            for drinks in permutations(range(5)):
                if drinks[0] != colors[1]: continue     # C4:  coffee/green
                if nations[2] != drinks[1]: continue    # C5:  Ukrainian/tea
                if drinks[2] != 2: continue             # C9:  milk in middle house
                for smokes in permutations(range(5)):
                    if smokes[1] != colors[3]: continue # C8:  Kools/yellow
                    if smokes[3] != drinks[3]: continue # C13: LuckyStrike/OJ
                    if nations[4] != smokes[4]: continue# C14: Japanese/Parliaments
                    for pets in permutations(range(5)):
                        if nations[1] != pets[0]: continue   # C3:  Spaniard/dog
                        if smokes[0] != pets[1]: continue    # C7:  OldGold/snails
                        if not next_to(smokes[2], pets[2]): continue  # C11: Chesterfields↔fox
                        if not next_to(smokes[1], pets[3]): continue  # C12: Kools↔horse
                        water_drinker = NATIONS[nations.index(drinks[4])]
                        zebra_owner   = NATIONS[nations.index(pets[4])]
                        return (water_drinker, zebra_owner)
