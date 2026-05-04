ALLERGENS = {
    "eggs": 1,
    "peanuts": 2,
    "shellfish": 4,
    "strawberries": 8,
    "tomatoes": 16,
    "chocolate": 32,
    "pollen": 64,
    "cats": 128,
}


def is_allergic_to(score, allergen):
    return score & ALLERGENS[allergen] != 0


def allergies(score):
    return [allergen for allergen, value in ALLERGENS.items() if score & value]
