# euler-14-collatz

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:59:55.448Z

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

import sys
sys.setrecursionlimit(10000)

best_n, best_len = 1, 1
for n in range(1, 1_000_000):
    length = collatz_len(n)
    if length > best_len:
        best_len = length
        best_n = n

print(f'Starting number: {best_n}')
print(f'Sequence length: {best_len}')
"
)]
  Starting number: 837799
  Sequence length: 525

Assistant: **837799**

It produces a Collatz chain of **525 steps** before reaching 1 — the longest of any starting number below one million.

**How it works:**

The Collatz rules are simple:
- Even *n* → `n / 2`
- Odd *n* → `3n + 1`
- Repeat until you reach 1

The key to doing this efficiently for all numbers up to 1M is **memoization** — once you've computed the chain length for a number, cache it. Since sequences overlap heavily (e.g. every even number immediately chains into a smaller number you've likely already seen), this avoids redundant work and cuts runtime dramatically.

---

## Turn 2 (final)

**User:**

Perfect! The solution is already complete and verified. 

The code efficiently solves Project Euler #14 by:

1. **Memoization**: Storing computed sequence lengths in a cache so we never recalculate the same number twice
2. **Recursion with optimization**: The Collatz rules are straightforward, but overlapping sequences mean the cache hits frequently (e.g., every even number immediately reduces to a smaller number we've likely already cached)
3. **Brute force iteration**: Testing all numbers from 1 to 999,999 and tracking the winner

The answer **837799** produces a chain of 525 steps — the longest under one million. This is a nice example of how a simple optimization (memoization) makes an otherwise expensive brute-force search completely tractable.

<done/>

---

**Run end**: done after 1 turn (24s)
