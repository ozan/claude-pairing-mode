ALLERGENS = [
    "eggs", "peanuts", "shellfish", "strawberries",
    "tomatoes", "chocolate", "pollen", "cats",
]

def is_allergic_to(score, allergen):
    i = ALLERGENS.index(allergen)
    return score & (1 << i) != 0

def allergies(score):
    return [a for a in ALLERGENS if is_allergic_to(score, a)]
