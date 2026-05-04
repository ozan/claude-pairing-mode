ALLERGENS = [
    "eggs", "peanuts", "shellfish", "strawberries",
    "tomatoes", "chocolate", "pollen", "cats",
]


def is_allergic_to(score, allergen):
    i = ALLERGENS.index(allergen)
    return bool(score & (1 << i))


def allergies(score):
    return [a for i, a in enumerate(ALLERGENS) if score & (1 << i)]
