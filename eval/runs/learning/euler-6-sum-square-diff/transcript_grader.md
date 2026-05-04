# euler-6-sum-square-diff

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:26

## Initial prompt

Project Euler #6: find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.

---

## Turn 1

### Tutor

Tutor: ## Project Euler #6

### The Two Formulas

**Sum of first *n* natural numbers:**

$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

**Sum of squares of first *n* natural numbers:**

$$\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$$

---

### Step-by-step for n = 100

**① Sum of the first 100 naturals:**
$$\frac{100 \times 101}{2} = 5{,}050$$

**② Square of that sum:**
$$5{,}050^2 = 25{,}502{,}500$$

**③ Sum of squares:**
$$\frac{100 \times 101 \times 201}{6} = \frac{2{,}030{,}100}{6} = 338{,}350$$

**④ The difference:**
$$25{,}502{,}500 - 338{,}350 = \boxed{25{,}164{,}150}$$

---

### Why the gap is so large

The square of the sum captures all the **cross-product terms** (2×i×j for every pair i≠j) that the sum of squares completely ignores. With 100 numbers, there are 4,950 such pairs, each contributing a positive amount — so the difference grows roughly as O(n⁴).

### Student

Thanks for walking through this! That really helps me see the structure of the problem.

So if I'm understanding correctly:
- The **square of the sum** includes all those cross-product terms (like 2×1×2, 2×1×3, etc.) that naturally appear when you expand (1+2+3+...+100)²
- The **sum of squares** only captures the diagonal terms (1², 2², 3², etc.)
- That's why the difference is so huge — we're essentially adding up all those 2×i×j products

Before I code this up, I want to make sure I have the right approach. Should I:
1. Use the formulas directly (which is efficient), or
2. Implement it with loops to verify the answer, or
3. Just go straight to the formula since we have it?

For a production solution I'd use the formulas, but for learning should I also code the loop version to double-check my understanding?

---

## Turn 2

### Tutor

Tutor: Your cross-product intuition is exactly right! And yes — **do both**, in this order:

### Why loops first, then formulas

The loop version forces you to translate the *math definition* directly into code, with no shortcuts. Once it runs and gives you 25,164,150, the formula version becomes a *verified optimization*, not just something you're trusting blindly.

```python
# --- Loop version (builds intuition) ---
total_sum = sum(range(1, 101))
square_of_sum = total_sum ** 2
sum_of_squares = sum(i**2 for i in range(1, 101))
difference_loop = square_of_sum - sum_of_squares

# --- Formula version (O(1), no iteration needed) ---
n = 100
square_of_sum_f  = (n * (n + 1) // 2) ** 2
sum_of_squares_f = n * (n + 1) * (2*n + 1) // 6
difference_formula = square_of_sum_f - sum_of_squares_f

# --- Verify they agree ---
assert difference_loop == difference_formula == 25_164_150
print(difference_formula)  # 25164150
```

---

### The learning payoff from doing both

| | Loop version | Formula version |
|---|---|---|
| **Teaches** | How the definition maps to code | Why closed-form math matters |
| **Scales to n=10⁹?** | ❌ Too slow | ✅ Instant |
| **Risk** | None — it's self-evident | Transcription error (the assert catches it) |

The `assert` on the last line is the key habit — it turns the loop into a **free unit test** for your formula, and you can delete the loop version once you're confident.

### Student

Perfect, that makes total sense. Let me code this up now.

```python
# --- Loop version (builds intuition) ---
total_sum = sum(range(1, 101))
square_of_sum = total_sum ** 2
sum_of_squares = sum(i**2 for i in range(1, 101))
difference_loop = square_of_sum - sum_of_squares

print(f"Loop version: {difference_loop}")

# --- Formula version (O(1), no iteration needed) ---
n = 100
square_of_sum_f = (n * (n + 1) // 2) ** 2
sum_of_squares_f = n * (n + 1) * (2*n + 1) // 6
difference_formula = square_of_sum_f - sum_of_squares_f

print(f"Formula version: {difference_formula}")

# --- Verify they agree ---
assert difference_loop == difference_formula == 25_164_150
print(f"✓ Both methods agree: {difference_formula}")
```

Running this in my head:
- `total_sum = 5050`
- `square_of_sum = 25502500`
- `sum_of_squares = 338350`
- `difference_loop = 25164150`

And the formula version should give the same. Let me verify the formula arithmetic once more:
- `(100 * 101 // 2)² = 5050² = 25502500` ✓
- `100 * 101 * 201 // 6 = 2030100 // 6 = 338350` ✓
- `25502500 - 338350 = 25164150` ✓

Great! Both should pass the assert. The code is clean and the assert gives me confidence that my formula transcription is correct.

<done/>

---

**Run end:** done after 2 turn(s) in 25.9s
