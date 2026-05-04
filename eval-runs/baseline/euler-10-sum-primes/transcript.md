# euler-10-sum-primes

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:30:53.513Z

---

## Turn 1

**User:**

Project Euler #10: find the sum of all primes below two million. (Naive trial-division will be slow — consider a sieve.)

**Pair:**

[Bash(python3 - <<'EOF'
def sum_primes_below(limit):
    # Sieve of Eratosthenes
    sieve = bytearray([1]) * limit   # 1 = prime candidate, bytearray is memory-efficient
    sieve[0] = sieve[1] = 0          # 0 and 1 are not prime

    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            # Mark all multiples of i starting from i² as composite
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))

    return sum(i for i, is_prime in enumerate(sieve) if is_prime)

import time
start = time.perf_counter()
result = sum_primes_below(2_000_000)
elapsed = time.perf_counter() - start

print(f"Sum of all primes below 2,000,000: {result:,}")
print(f"Computed in {elapsed*1000:.1f} ms")
EOF
)]
  Sum of all primes below 2,000,000: 142,913,828,922
  Computed in 33.1 ms

Assistant: **Answer: 142,913,828,922** — computed in ~33 ms.

---

### How it works: Sieve of Eratosthenes

```
sieve = [1, 1, 1, 1, 1, 1, ...]   ← indices 0..1,999,999, 1 = "prime candidate"
         ↑  ↑
         0  1  → immediately cleared (not prime)

For i = 2: mark 4, 6, 8, 10, ...  as composite
For i = 3: mark 9, 12, 15, 18, ... as composite
For i = 5: mark 25, 30, 35, ...    as composite
...only need to go up to √2,000,000 ≈ 1,414
```

Key optimisations used:

| Trick | Why it helps |
|---|---|
| `bytearray` instead of a list | ~8× less memory than a Python `list` of bools |
| Start marking at **i²** | Everything below i² was already crossed off by smaller primes |
| **Slice assignment** `sieve[i*i::i] = bytearray(n)` | Batch-zeros the whole stride in one C-level operation — much faster than a Python loop |
| Only iterate to **√limit** | Any composite ≤ limit must have a prime factor ≤ √limit |

This runs in **O(n log log n)** time — essentially linear — versus the **O(n√n)** of trial division, which would be ~1,000× slower here.

---

## Turn 2 (final)

**User:**

Perfect! You've nailed it. The Sieve of Eratosthenes is the classic approach for "sum all primes below N" problems, and your implementation hits all the right notes:

- **Memory efficiency** with `bytearray` 
- **Smart skipping** by starting the mark-as-composite loop at i²
- **Vectorized slice assignment** for the actual marking step
- **Early loop termination** at √limit

The result **142,913,828,922** is correct, and running in 33 ms on a modern machine is exactly what you'd expect from the O(n log log n) time complexity.

If you were curious to push it further, you *could* optimize the sieve even more (segmented sieve for very tight memory, wheel factorization to skip multiples of 2/3/5), but for limit=2M, you've hit the sweet spot—fast enough that optimization would just add complexity for negligible gain.

<done/>

---

**Run end**: done after 1 turn (27s)
