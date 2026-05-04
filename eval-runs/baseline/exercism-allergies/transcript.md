# exercism-allergies

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:30:11.009Z

---

## Turn 1

**User:**

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

**Pair:**

Assistant: Here's a clean Python implementation:

```python
ALLERGENS = [
    "eggs",        # 1   = 2^0
    "peanuts",     # 2   = 2^1
    "shellfish",   # 4   = 2^2
    "strawberries",# 8   = 2^3
    "tomatoes",    # 16  = 2^4
    "chocolate",   # 32  = 2^5
    "pollen",      # 64  = 2^6
    "cats",        # 128 = 2^7
]

def is_allergic_to(score: int, allergen: str) -> bool:
    """Return True if score has the allergen's bit set."""
    if allergen not in ALLERGENS:
        raise ValueError(f"Unknown allergen: {allergen!r}")
    bit = 1 << ALLERGENS.index(allergen)
    return bool(score & bit)

def allergies(score: int) -> list[str]:
    """Return every allergen whose bit is set in score."""
    return [a for i, a in enumerate(ALLERGENS) if score & (1 << i)]
```

---

### How it works

| Allergen      | Index | Bit (1 << i) |
|---------------|-------|--------------|
| eggs          | 0     | `0000_0001` = 1 |
| peanuts       | 1     | `0000_0010` = 2 |
| shellfish     | 2     | `0000_0100` = 4 |
| strawberries  | 3     | `0000_1000` = 8 |
| tomatoes      | 4     | `0001_0000` = 16 |
| chocolate     | 5     | `0010_0000` = 32 |
| pollen        | 6     | `0100_0000` = 64 |
| cats          | 7     | `1000_0000` = 128 |

**`is_allergic_to`** — computes the allergen's bitmask (`1 << index`) and ANDs it with `score`. Any non-zero result means the bit is set.

**`allergies`** — iterates all allergens and collects those whose bit is set. Because `score` can be > 255 (e.g. 257 = 256 + 1), the bitwise AND naturally ignores unknown high bits and still correctly reports `eggs`.

---

### Quick demo

```python
>>> allergies(0)
[]
>>> allergies(1)
['eggs']
>>> allergies(34)          # 32 (chocolate) + 2 (peanuts)
['peanuts', 'chocolate']
>>> allergies(255)
['eggs', 'peanuts', 'shellfish', 'strawberries', 'tomatoes', 'chocolate', 'pollen', 'cats']

>>> is_allergic_to(34, "peanuts")
True
>>> is_allergic_to(34, "eggs")
False
>>> is_allergic_to(257, "eggs")   # 257 = 256 + 1; high bit ignored
True
```

---

## Turn 2 (final)

**User:**

Perfect! The solution I provided covers the complete problem:

✅ **`is_allergic_to(score, allergen)`** — checks if a single allergen's bit is set  
✅ **`allergies(score)`** — returns the list of all allergens present  
✅ Handles the 8 standard allergens with correct bit values  
✅ Works with scores > 255 (ignores unknown high bits)  
✅ Includes error handling for unknown allergens  

The key insight is that each allergen maps to a power-of-2 bit position, so:
- **Check if set**: `score & (1 << allergen_index)` 
- **Collect all set**: iterate and check each bit

The code is ready to submit to Exercism!

<done/>

---

**Run end**: done after 1 turn (25s)
