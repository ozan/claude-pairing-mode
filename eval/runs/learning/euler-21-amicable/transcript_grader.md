# euler-21-amicable

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:58

## Initial prompt

Project Euler #21: find the sum of all amicable numbers below 10000. (a, b are amicable if d(a)=b and d(b)=a where d(n) is the sum of proper divisors of n, and a≠b.)

---

## Turn 1

### Tutor

Tutor: ## Approach

For each `a` below 10,000:
1. Compute `b = d(a)` (sum of proper divisors of `a`)
2. Check that `d(b) = a` **and** `a ≠ b`
3. If so, `a` is amicable — add it to the running sum

**Key helper:** to find proper divisors of `n`, iterate `i` up to `√n`, adding both `i` and `n//i` when `i` divides `n`.

---

```python
def d(n):
    """Sum of proper divisors of n."""
    if n < 2:
        return 0
    total = 1                    # 1 is always a proper divisor (n > 1)
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:      # avoid double-counting perfect squares
                total += n // i
        i += 1
    return total

total = 0
for a in range(2, 10_000):
    b = d(a)
    if b != a and d(b) == a:     # amicable pair, a ≠ b
        total += a

print(total)  # → 31626
```

---

## Amicable pairs found

| Pair | d(a) | d(b) |
|------|------|------|
| **(220, 284)** | 284 ✓ | 220 ✓ |
| (1184, 1210) | 1210 ✓ | 1184 ✓ |
| (2620, 2924) | 2924 ✓ | 2620 ✓ |
| (5020, 5564) | 5564 ✓ | 5020 ✓ |
| (6232, 6368) | 6368 ✓ | 6232 ✓ |

Sum: `220 + 284 + 1184 + 1210 + 2620 + 2924 + 5020 + 5564 + 6232 + 6368`

## **Answer: 31626**

---

### Why `i` only goes to `√n`

Every divisor pair `(i, n/i)` straddles the square root — so iterating to `√n` is sufficient and cuts the work from **O(n)** to **O(√n)** per number, making the whole search fast despite checking 10,000 numbers.

### Student

Thanks for walking me through this! I want to make sure I understand the solution before I finalize it.

Let me trace through the `d()` function with a concrete example to verify the logic. Let's use **n = 220**:

- Start with `total = 1` (since 1 is always a proper divisor for n > 1)
- `i = 2`: 220 % 2 == 0, so add 2. Also 220 // 2 = 110, and 2 ≠ 110, so add 110. `total = 1 + 2 + 110 = 113`
- `i = 3`: 220 % 3 ≠ 0, skip
- `i = 4`: 220 % 4 == 0, so add 4. Also 220 // 4 = 55, and 4 ≠ 55, so add 55. `total = 113 + 4 + 55 = 172`
- `i = 5`: 220 % 5 == 0, so add 5. Also 220 // 5 = 44, and 5 ≠ 44, so add 44. `total = 172 + 5 + 44 = 221`
- `i = 6, 7, ..., 14`: none divide 220
- `i = 15`: 15 × 15 = 225 > 220, so we stop

So `d(220) = 221`... but the table says it should be 284. Let me recount the proper divisors of 220 manually: 1, 2, 4, 5, 10, 11, 20, 22, 44, 55, 110. That sums to 284.

I think I missed a few factors—let me check `i = 10`: 220 % 10 == 0, so add 10. And 220 // 10 = 22, and 10 ≠ 22, so add 22. And `i = 11`: 220 % 11 == 0, so add 11. And 220 // 11 = 20, and 11 ≠ 20, so add 20.

So the full sum is: 1 + 2 + 110 + 4 + 55 + 5 + 44 + 10 + 22 + 11 + 20 = 284 ✓

Great! That confirms the function works. Can you clarify one more thing: in the main loop, why do we only count each amicable number once (by iterating `a` from 2 to 9999) instead of accidentally double-counting both members of a pair?

---

## Turn 2

### Tutor

Tutor: Great trace-through — and this is a really worthwhile thing to nail down!

## There's no double-counting — and that's intentional

The loop adds `a` to the total, never `b`. So when two amicable numbers are both in range, **each one earns its own addition independently**:

```
a = 220 → b = d(220) = 284,  d(284) = 220 ✓  →  add 220
a = 284 → b = d(284) = 220,  d(220) = 284 ✓  →  add 284
```

That's not a bug — it's exactly right, because the problem says *"sum of all amicable numbers"*, meaning every qualifying number in the range, **both** members of each pair included.

## The real guard: `b != a`

The only "don't count twice" check in the code is actually protecting against a different case — **perfect numbers** like 6 (where d(6) = 6). Those would satisfy `d(b) == a` trivially, but they're *not* amicable by definition:

```
a = 6 → b = d(6) = 6 → b == a  →  skip  ✗
```

## Summary

| Concern | What actually happens |
|---|---|
| Adding both 220 and 284 | ✅ Correct — both are amicable numbers to be summed |
| Adding the same number twice | 🚫 Impossible — each `a` appears once in `range(2, 10_000)` |
| Counting perfect numbers (d(n) = n) | 🚫 Blocked by `b != a` guard |

The elegance here is that the loop naturally treats every number as a **candidate**, not as part of a pair. Each number proves its own amicability and contributes its own value to the sum.

### Student

Ah, that makes perfect sense! So the loop structure itself prevents double-counting (each number appears once as `a`), and the `b != a` check filters out perfect numbers. I was worried we'd somehow count 220 twice or something, but that's impossible given how the iteration works.

Let me just verify the code runs and gives the right answer:

```python
def d(n):
    """Sum of proper divisors of n."""
    if n < 2:
        return 0
    total = 1                    # 1 is always a proper divisor (n > 1)
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:      # avoid double-counting perfect squares
                total += n // i
        i += 1
    return total

total = 0
for a in range(2, 10_000):
    b = d(a)
    if b != a and d(b) == a:     # amicable pair, a ≠ b
        total += a

print(total)  # Should be 31626
```

I'm confident this is correct now. The logic is:
1. For each candidate number `a`, compute its divisor sum `b`
2. Check if `b ≠ a` (to exclude perfect numbers) AND `d(b) = a` (to confirm the amicable relationship)
3. If both conditions hold, `a` is amicable, so add it to the total
4. The answer is 31626

<done/>

---

**Run end:** done after 2 turn(s) in 41.8s
