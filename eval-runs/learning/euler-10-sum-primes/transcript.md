# euler-10-sum-primes

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:59:31.702Z

---

## Turn 1

**User:**

Project Euler #10: find the sum of all primes below two million. (Naive trial-division will be slow — consider a sieve.)

**Pair:**

Assistant: ## Project Euler #10 — Sum of Primes Below 2,000,000

### The Tool: Sieve of Eratosthenes

The key insight is to flip the problem. Instead of asking *"is this number prime?"* for each candidate, we ask *"which numbers can I eliminate?"*

**How the sieve works:**
1. Start with a boolean array of size *N*, all `True` ("assumed prime")
2. Begin at `p = 2`. Mark every multiple of `p` (i.e. `4, 6, 8…`) as `False`
3. Move to the next `True` entry, repeat
4. You only need to sieve up to `√N` — any composite ≤ N must have a factor ≤ √N
5. Whatever remains `True` is prime

This is **O(N log log N)** — vastly faster than trial-division's **O(N√N)**.

[Bash(python3 - <<'EOF'
import math, time

def sum_primes_sieve(limit):
    # Boolean array: sieve[i] means "i is prime"
    sieve = bytearray([1]) * limit   # bytearray is faster than list of bools
    sieve[0] = sieve[1] = 0          # 0 and 1 are not prime

    # Only need to eliminate composites up to √limit
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            # Mark multiples of p, starting at p² (smaller ones already marked)
            sieve[p*p :: p] = bytearray(len(sieve[p*p :: p]))

    return sum(i for i, is_prime in enumerate(sieve) if is_prime)

t0 = time.perf_counter()
answer = sum_primes_sieve(2_000_000)
elapsed = time.perf_counter() - t0

print(f"Answer : {answer:,}")
print(f"Runtime: {elapsed*1000:.1f} ms")
EOF
)]
  Answer : 142,913,828,922
  Runtime: 32.8 ms

Assistant: ### Answer: **142,913,828,922**

---

### Code walkthrough

```python
sieve = bytearray([1]) * limit   # ① all numbers presumed prime
sieve[0] = sieve[1] = 0          # ② 0 and 1 are not prime

for p in range(2, math.isqrt(limit) + 1):   # ③ only up to √N
    if sieve[p]:
        sieve[p*p :: p] = bytearray(...)     # ④ cross off composites
```

| Step | Why |
|---|---|
| `bytearray` not `list` | 8× less memory; Python can zero a slice in one C call |
| Start crossing off at `p²` | `2p, 3p, … (p-1)p` were already eliminated by smaller primes |
| Loop only to `√N` | A composite ≤ N always has a prime factor ≤ √N |
| `sum(i … if is_prime)` | One pass at the end; no list allocation |

### Why trial division loses

For each of ~150,000 primes below 2M, trial division checks ~1,414 divisors → **~210 million checks**.  
The sieve does at most `N/2 + N/3 + N/5 + …` ≈ **N log log N ≈ 6M** operations. The sieve wins by ~35×.

---

## Turn 2 (final)

**User:**

I see you've already got a complete, elegant solution here! Let me verify what's presented:

✅ **Algorithm**: Sieve of Eratosthenes — correct choice for this problem
✅ **Implementation**: 
  - Uses `bytearray` for memory efficiency (8× smaller than list)
  - Only sieves up to √N (smart optimization)
  - Starts crossing off at p² (no redundant work)
  - Single final pass to sum primes

✅ **Answer**: 142,913,828,922 — matches the official Project Euler solution
✅ **Performance**: 32.8 ms is excellent for 2 million numbers

The explanation is also solid:
- Clearly explains *why* sieve beats trial division (O(N log log N) vs O(N√N))
- Quantifies the difference: ~35× speedup
- Points out the key optimizations

The code is production-ready and educational. There's nothing broken or left unfinished here.

<done/>

---

**Run end**: done after 1 turn (30s)
