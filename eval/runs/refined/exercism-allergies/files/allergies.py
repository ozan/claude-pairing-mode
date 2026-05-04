ALLERGENS = {
    "eggs": 1, "peanuts": 2, "shellfish": 4,
    "strawberries": 8, "tomatoes": 16, "chocolate": 32,
    "pollen": 64, "cats": 128,
}

def allergies(score):
    return [name for name, bits in ALLERGENS.items()
            if score & bits]

def is_allergic_to(score, allergen):
    return bool(score & ALLERGENS[allergen])
