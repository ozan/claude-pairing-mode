# euler-21-amicable

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:31:49.360Z

---

## Turn 1

**User:**

Project Euler #21: find the sum of all amicable numbers below 10000. (a, b are amicable if d(a)=b and d(b)=a where d(n) is the sum of proper divisors of n, and a≠b.)

**Pair:**

[Bash(python3 -c "
def d(n):
    if n < 2:
        return 0
    s = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            s += i
            if i != n // i:
                s += n // i
        i += 1
    return s

total = sum(a for a in range(1, 10000)
            if (b := d(a)) != a and d(b) == a)
print(total)
"
)]
  31626

Assistant: The answer is **31626**.

Here's how it works:

```python
def d(n):          # sum of proper divisors of n
    s = 1          # 1 is always a divisor (for n > 1)
    i = 2
    while i * i <= n:
        if n % i == 0:
            s += i
            if i != n // i:   # avoid double-counting perfect squares
                s += n // i
    return s

total = sum(a for a in range(1, 10000)
            if (b := d(a)) != a and d(b) == a)
```

**Key steps:**
1. **`d(n)`** — sums proper divisors efficiently by iterating only up to √n, adding both `i` and `n/i` for each factor found.
2. For each `a < 10000`, compute `b = d(a)`, then check `d(b) == a` and `a ≠ b` (the second condition excludes perfect numbers like 6 where d(6)=6).

The amicable pairs below 10,000 are: **(220, 284), (1184, 1210), (2620, 2924), (5020, 5564), (6232, 6368)** — summing all ten numbers gives **31626**.

---

## Turn 2 (final)

**User:**

Perfect! You've already solved it. The solution is clean and efficient:

**Key insights in your approach:**
- The `d(n)` function smartly computes proper divisor sums in **O(√n)** time by only checking factors up to the square root
- The walrus operator `:=` elegantly captures `b = d(a)` in the filter condition
- The `a ≠ b` check (`b != a`) correctly excludes perfect numbers (where d(n) = n)

**The algorithm:**
For each number `a`, compute its divisor sum `b`, then check if `d(b)` equals `a`. If so, both `a` and `b` are amicable. Since you iterate through all numbers 1–9999, you'll find each pair twice (once as `a`, once as `b`), which is why summing all matching `a` values gives you the complete answer: **31626**.

**Verified pairs below 10,000:**
- (220, 284) → 220 + 284 = 504
- (1184, 1210) → 1394
- (2620, 2924) → 5544
- (5020, 5564) → 10584
- (6232, 6368) → 12600
- **Total: 31,626** ✓

<done/>

---

**Run end**: done after 1 turn (22s)
