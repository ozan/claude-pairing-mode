# euler-14-collatz

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:31:20.959Z

---

## Turn 1

**User:**

Project Euler #14: which starting number under one million produces the longest Collatz sequence? Return the starting number.

**Pair:**

[Bash(python3 -c "
cache = {1: 1}

def collatz_len(n):
    if n in cache:
        return cache[n]
    if n % 2 == 0:
        result = 1 + collatz_len(n // 2)
    else:
        result = 1 + collatz_len(3 * n + 1)
    cache[n] = result
    return result

best_n, best_len = max(((n, collatz_len(n)) for n in range(1, 1_000_000)), key=lambda x: x[1])
print(f'Starting number: {best_n}, sequence length: {best_len}')
"
)]
  Starting number: 837799, sequence length: 525

Assistant: **837799**

Starting from 837799 produces the longest Collatz sequence under one million — **525 steps** before reaching 1. The solution uses memoization to cache already-computed sequence lengths, making it fast even for the full range up to 1,000,000.

---

## Turn 2 (final)

**User:**

Perfect! You've solved it cleanly. The memoization approach is the right move here — without caching, you'd be recalculating sequence lengths for numbers you've already seen, which would be slow. With the cache, it's efficient enough to scan the full million range in seconds.

The key insight is that many Collatz sequences overlap. Once you've computed the length from any intermediate number back to 1, you don't recompute it. That's what makes this tractable.

**837799** is indeed the answer.

<done/>

---

**Run end**: done after 1 turn (22s)
