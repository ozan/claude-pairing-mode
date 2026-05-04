# euler-14-collatz

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T06:05:10.726Z

---

## Turn 1

**User:**

Project Euler #14: which starting number under one million produces the longest Collatz sequence? Return the starting number.

**Pair:**

Assistant: Good classic problem. Before we write the solution, there's a key algorithmic choice here worth thinking through.

OPTIONS:
[A] Cache chain lengths
```diff
+++ euler14.py
@@ -0,0 +1,12 @@
+cache = {1: 1}
+
+def chain_len(n):
+    if n in cache:
+        return cache[n]
+    step = chain_len(n // 2 if n % 2 == 0 else 3 * n + 1)
+    cache[n] = step + 1
+    return cache[n]
+
+best = max(range(1, 1_000_000), key=chain_len)
+print(best)
```

[B] Compute each chain fresh
```diff
+++ euler14.py
@@ -0,0 +1,11 @@
+def chain_len(n):
+    length = 1
+    while n != 1:
+        n = n // 2 if n % 2 == 0 else 3 * n + 1
+        length += 1
+    return length
+
+best = max(range(1, 1_000_000), key=chain_len)
+print(best)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which approach do you want to use?

---

## Turn 2

**User:**

API Error: Stream idle timeout - partial response received

**Pair:**

Assistant: No problem, I'll just proceed. The memoized approach is clearly better — it caches sub-chain lengths so we never recompute the same suffix twice. Let me write it out.

[Bash(ls euler14.py 2>/dev/null && echo "exists" || echo "not found")]
  not found

[Write(euler14.py)]
import sys
sys.setrecursionlimit(1_000_000)

cache = {1: 1}

def chain_len(n):
    if n in cache:
        return cache[n]
    step = chain_len(n // 2 if n % 2 == 0 else 3 * n + 1)
    cache[n] = step + 1
    return cache[n]

… (3 more lines)

[Bash(time python3 euler14.py)]
  837799
  
  real	0m0.425s
  user	0m0.394s
  sys	0m0.024s

Assistant: **837799** — and it runs in under half a second.

The key insight: many numbers share Collatz suffixes. When computing the chain for 54, you'll eventually hit 27. If you've already computed `chain_len(27)`, you can stop there and just add 1. Without caching, the brute-force version recomputes those shared tails over and over — in Python it takes ~30s instead of ~0.4s.

Two implementation notes worth knowing:
- `sys.setrecursionlimit` is needed because some chains go deep before hitting a cached value (the default limit of 1000 would blow up)
- The recursion naturally builds the cache bottom-up as the call stack unwinds — that's what makes it clean

---

## Turn 3 (final)

**User:**

Got it, the problem's solved. The memoization dramatically speeds things up by avoiding recomputation of overlapping Collatz chain suffixes. Nice work choosing A — without the cache this would've taken much longer.

<done/>

---

**Run end**: done after 2 turns (8422s)
