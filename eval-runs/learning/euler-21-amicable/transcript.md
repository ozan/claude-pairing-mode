# euler-21-amicable

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T20:00:19.075Z

---

## Turn 1

**User:**

Project Euler #21: find the sum of all amicable numbers below 10000. (a, b are amicable if d(a)=b and d(b)=a where d(n) is the sum of proper divisors of n, and a≠b.)

**Pair:**

Assistant: ## Strategy

For each number `a` below 10,000:
1. Compute `b = d(a)` (sum of proper divisors)
2. Compute `d(b)` — if it equals `a`, and `a ≠ b`, then `a` is amicable

**Key insight for `d(n)` efficiently:** loop up to √n, add both `i` and `n/i` each time a factor pair is found.

[Bash(python3 << 'EOF'
def d(n):
    """Sum of proper divisors of n (all divisors except n itself)."""
    if n <= 1:
        return 0
    total = 1                          # 1 is always a proper divisor (for n > 1)
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i                 # found factor i ...
            if i != n // i:
                total += n // i        # ... and its pair n/i (skip if perfect square)
        i += 1
    return total

# --- verify with the classic example ---
print(f"d(220) = {d(220)}")   # expect 284
print(f"d(284) = {d(284)}")   # expect 220
print()

# --- find all amicable numbers below 10000 ---
amicable = []
for a in range(2, 10_000):
    b = d(a)
    if b != a and d(b) == a:   # amicable pair, and not a perfect number
        amicable.append(a)

print("Amicable numbers found:")
# show them as pairs
seen = set()
for a in amicable:
    b = d(a)
    if (b, a) not in seen:
        print(f"  ({a}, {b})")
        seen.add((a, b))

print(f"\nSum = {sum(amicable)}")
EOF
)]
  d(220) = 284
  d(284) = 220
  
  Amicable numbers found:
    (220, 284)
    (1184, 1210)
    (2620, 2924)
    (5020, 5564)
    (6232, 6368)
  
  Sum = 31626

Assistant: ## Answer: **31626**

---

### How it works

**`d(n)` — sum of proper divisors**
```
d(220) → divisors: 1, 2, 4, 5, 10, 11, 20, 22, 44, 55, 110 → 284  ✓
d(284) → divisors: 1, 2, 4, 71, 142                         → 220  ✓
```
Loop up to `√n`, add factor pairs `(i, n/i)` — **O(√n)** instead of O(n).

**Amicable check:**
```
a → d(a)=b → d(b)=a?   and   a ≠ b   (rules out perfect numbers like 6)
```

**The 5 pairs below 10,000:**

| Pair | | |
|------|--|--|
| 220 | ↔ | 284 |
| 1184 | ↔ | 1210 |
| 2620 | ↔ | 2924 |
| 5020 | ↔ | 5564 |
| 6232 | ↔ | 6368 |

Both numbers in each pair are counted → **220 + 284 + 1184 + 1210 + 2620 + 2924 + 5020 + 5564 + 6232 + 6368 = 31626**.

---

## Turn 2 (final)

**User:**

Perfect! The solution is complete and verified. 

The algorithm efficiently computes the sum of proper divisors using a **√n loop** (factor pairs), then checks each number to see if it forms an amicable pair. The answer **31626** accounts for both members of each of the 5 pairs found below 10,000.

<done/>

---

**Run end**: done after 1 turn (28s)
