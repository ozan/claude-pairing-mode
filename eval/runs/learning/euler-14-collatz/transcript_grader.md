# euler-14-collatz

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:42

## Initial prompt

Project Euler #14: which starting number under one million produces the longest Collatz sequence? Return the starting number.

---

## Turn 1

### Tutor

[Bash(python3 -c "
def collatz_len(n, cache={}):
    if n in cache:
        return cache[n]
    if n == 1:
        return 1
    if n % 2 == 0:
        result = 1 + collatz_len(n // 2, cache)
    else:
        result = 1 + collatz_len(3 * n + 1, cache)
    cache[n] = result
    return result

import sys
sys.setrecursionlimit(10000)

best_n, best_len = max(
    ((n, collatz_len(n)) for n in range(1, 1_000_000)),
    key=lambda x: x[1]
)
print(f'Starting number: {best_n}, sequence length: {best_len}')
"
)]
  Starting number: 837799, sequence length: 525

Tutor: ## Answer: **837,799**

That starting number produces a Collatz chain of **525 steps** — the longest of any number below 1,000,000.

### How it works

The **Collatz conjecture** says every positive integer eventually reaches 1 via this rule:

| n is… | next step |
|-------|-----------|
| even  | n / 2     |
| odd   | 3n + 1    |

### Key optimization: memoization

Naively computing each chain from scratch would be slow. Instead, we **cache lengths already computed**, so any time a chain passes through a number we've seen before, we immediately know the remaining length.

```python
def collatz_len(n, cache={}):
    if n in cache: return cache[n]       # already know this tail
    if n == 1:     return 1
    nxt = n // 2 if n % 2 == 0 else 3*n + 1
    result = 1 + collatz_len(nxt, cache)
    cache[n] = result                    # store for future callers
    return result
```

This turns what could be tens of millions of redundant steps into a single pass over all 999,999 starting numbers — each interior node computed only **once**.

### Student

Thanks for walking me through this! I can see how the memoization makes this so much faster. A couple quick questions to make sure I understand:

1. When we use `cache={}` as a default argument, that cache persists across all calls to `collatz_len`, right? So every time we call `collatz_len(n)` for a new starting number, we're building on the same cache?

2. I notice we set `sys.setrecursionlimit(10000)` — is that because some of the Collatz sequences get pretty deep, and we'd hit Python's default limit otherwise? How did you know 10,000 was enough?

3. One thing I'm wondering: could we have done this iteratively instead of recursively? I'm asking because iteration usually avoids recursion limit issues altogether, and I'm curious if it would be faster or just more verbose.

<done/>

---

**Run end:** done after 1 turn(s) in 16.7s
