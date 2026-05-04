# exercism-roman-numerals

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:39

## Initial prompt

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

---

## Turn 1

### Tutor

Tutor: ## Roman Numerals — Greedy Subtraction

**Key insight:** include all 13 subtractive pairs in the lookup table, largest-first, then greedily peel them off.

```python
def to_roman(n: int) -> str:
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        ( 100, "C"), ( 90, "XC"), ( 50, "L"), ( 40, "XL"),
        (  10, "X"), (  9, "IX"), (  5, "V"), (  4, "IV"),
        (   1, "I"),
    ]

    result = []
    for value, symbol in values:
        while n >= value:
            result.append(symbol)
            n -= value

    return "".join(result)
```

### How it works — a walkthrough

**`to_roman(1994)`**

| Remaining `n` | Symbol appended | Why |
|---|---|---|
| 1994 | `M` | 1994 ≥ 1000 → subtract → 994 |
| 994 | `CM` | 994 ≥ 900 → subtract → 94 |
| 94 | `XC` | 94 ≥ 90 → subtract → 4 |
| 4 | `IV` | 4 ≥ 4 → subtract → 0 |

Result → **`MCMXCIV`** ✓

### Why this design

| Choice | Reason |
|---|---|
| Subtractive pairs in the table | Eliminates all special-casing; `IV`, `IX`, etc. are just regular entries |
| Largest-first ordering | Greedy works correctly because the table is a *complete* set of "atomic" symbols |
| `while` not `if` | Handles repeated symbols (`III`, `MMM`) naturally in one pass |

### Edge cases verified

```python
assert to_roman(1)    == "I"
assert to_roman(4)    == "IV"
assert to_roman(9)    == "IX"
assert to_roman(40)   == "XL"
assert to_roman(90)   == "XC"
assert to_roman(400)  == "CD"
assert to_roman(900)  == "CM"
assert to_roman(3999) == "MMMCMXCIX"
```

### Student

Thanks for walking me through that! This is really clear. Let me make sure I understand the core idea before I code it myself.

So the key is that by including all 13 value-symbol pairs (including the subtractive ones like 900→"CM"), I don't have to write special logic to decide when to use IV vs IIII. The greedy algorithm just naturally picks them because they're in the table, largest first.

The `while` loop handles repetition—if I have 3000, it'll append "M" three times as it subtracts 1000 three times.

Let me code this up myself and test it:

```python
def to_roman(n: int) -> str:
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I"),
    ]
    
    result = []
    for value, symbol in values:
        while n >= value:
            result.append(symbol)
            n -= value
    
    return "".join(result)

# Test
print(to_roman(1994))  # Should be MCMXCIV
print(to_roman(4))     # Should be IV
print(to_roman(9))     # Should be IX
print(to_roman(3999))  # Should be MMMCMXCIX
```

This works great! I can see why the greedy approach is safe here—because the table includes all the "atomic" pieces we need, we'll never get stuck in a situation where we miss a subtractive pair.

<done/>

---

**Run end:** done after 1 turn(s) in 16.4s
