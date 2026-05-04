ALLERGENS = {
    "eggs": 1, "peanuts": 2, "shellfish": 4,
    "strawberries": 8, "tomatoes": 16,
    "chocolate": 32, "pollen": 64, "cats": 128,
}


def is_allergic_to(score, allergen):
    return bool(score & ALLERGENS[allergen])


def allergies(score):
    return [a for a in ALLERGENS if is_allergic_to(score, a)]
