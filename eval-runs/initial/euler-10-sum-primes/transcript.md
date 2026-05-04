# euler-10-sum-primes

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:41:25.055Z

---

## Turn 1

**User:**

Project Euler #10: find the sum of all primes below two million. (Naive trial-division will be slow — consider a sieve.)

**Pair:**

Assistant: Good classic problem. The sieve is the right call — let's build it in Python. Before I write anything, here's the key inner-loop decision:

Assistant: Hmm, the tool isn't loading — I'll just pose the question directly.

**Key sieve question:** for each prime `p`, where should we start crossing off multiples?

| | Option A | Option B |
|---|---|---|
| **Start at** | `2*p` | `p*p` |
| **Reasoning** | "First composite multiple of p" | "Earlier multiples already handled" |

Which would you pick, and why? Think about what's already been marked by the time we process prime `p`.

---

## Turn 2

**User:**

Great question! You're right that **Option B (start at `p*p`)** is the solid choice here.

By the time we process prime `p`, all smaller primes have already done their work. Their multiples — including `2*p`, `3*p`, etc. — are already marked. So `p*p` is the first unmarked multiple of `p`. Starting there cuts iterations roughly in half and is the textbook Sieve of Eratosthenes optimization.

**Option A** (start at `2*p`) works, but it wastes cycles re-marking composites that smaller primes already handled.

So: **I'd go with Option B**. Should I write the sieve now? Here's what I'm thinking:

```python
def sum_of_primes_below(n):
    """Sieve of Eratosthenes, summing primes below n."""
    if n <= 2:
        return 0
    
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p*p, n, p):  # ← start at p*p
                is_prime[i] = False
    
    return sum(i for i in range(n) if is_prime[i])

print(sum_of_primes_below(2_000_000))
```

The key points:
- `is_prime` bool array (memory efficient)
- Only iterate up to √n for the outer loop (primes above √n don't produce unmarked composites below n)
- Inner loop starts at `p*p`, stepping by `p`

Ready for me to test this?

**Pair:**

Assistant: Exactly right — clean analysis. Let me write this and then flag one more optimization worth knowing about.

[Glob(euler10.py)]
  No files found

[Write(euler10.py)]
def sum_of_primes_below(n):
    """Sieve of Eratosthenes, summing primes below n."""
    if n <= 2:
        return 0

    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p*p, n, p):  # start at p*p
                is_prime[i] = False
… (5 more lines)

[Bash(time python euler10.py)]
  error: Exit code 127

[Bash(time python3 euler10.py)]
  142913828922
  
  real	0m0.134s
  user	0m0.120s
  sys	0m0.010s

Assistant: Answer is **142913828922** ✓, runs in ~130ms. Correct and fast enough.

Worth knowing though: the Python inner `for` loop is the bottleneck here. There's a way to replace it with a single C-level operation. Which of these inner-loop approaches do you think is faster?

**Option A — slice assignment:**
```diff
+++ euler10.py
@@ -8,8 +8,7 @@
     for p in range(2, int(n**0.5) + 1):
         if is_prime[p]:
-            for i in range(p*p, n, p):
-                is_prime[i] = False
+            is_prime[p*p::p] = [False] * len(is_prime[p*p::p])
```

**Option B — bytearray + slice assignment:**
```diff
+++ euler10.py
@@ -5,10 +5,9 @@
-    is_prime = [True] * n
-    is_prime[0] = is_prime[1] = False
+    is_prime = bytearray([1]) * n
+    is_prime[0] = is_prime[1] = 0

     for p in range(2, int(n**0.5) + 1):
         if is_prime[p]:
-            for i in range(p*p, n, p):
-                is_prime[i] = False
+            is_prime[p*p::p] = b'\x00' * len(is_prime[p*p::p])

-    return sum(i for i in range(n) if is_prime[i])
+    return sum(i for i, v in enumerate(is_prime) if v)
```

Both replace the Python for-loop with a slice. Which is faster, and why?

---

## Turn 3

**User:**

Great question — this is about C-level slice assignment vs. Python object overhead.

**I'd pick Option B** (bytearray). Here's why:

1. **Memory efficiency**: A bytearray stores raw bytes (1 byte per element), not Python bool objects. A list of bools in CPython has much more per-element overhead (pointer indirection, refcount, etc.). For 2 million elements, that's a *huge* difference in memory pressure.

2. **Cache locality**: Smaller memory footprint → better CPU cache behavior. The sieve is memory-bound; cache misses hurt more than algorithm complexity here.

3. **Slice assignment is equally fast in both**: Both `is_prime[p*p::p] = [False] * ...` and `is_prime[p*p::p] = b'\x00' * ...` are C-level operations. But Option B avoids the overhead of creating a list of Python bool objects in the first place.

4. **The real win**: bytearray was specifically designed for this — in-place modification of large mutable sequences. It's the right data structure for a sieve.

Option A *works* and is faster than the original for-loop, but Option B removes Python's object-boxing overhead entirely. For a 2-million-element sieve, that translates to noticeable wall-clock time.

Should I test both and show you the speedup?

**Pair:**

Assistant: Spot on — let's apply it and measure all three so you can see the actual numbers.

[Read(euler10.py)]
  1	def sum_of_primes_below(n):
  2	    """Sieve of Eratosthenes, summing primes below n."""
  3	    if n <= 2:
  4	        return 0
  5	
  6	    is_prime = [True] * n
  7	    is_prime[0] = is_prime[1] = False
  8	
  9	    for p in range(2, int(n**0.5) + 1):
  10	        if is_prime[p]:
  11	            for i in range(p*p, n, p):  # start at p*p
  12	                is_prime[i] = False
  … (5 more lines)

[Edit(euler10.py)]
--- before
def sum_of_primes_below(n):
    """Sieve of Eratosthenes, summing primes below n."""
    if n <= 2:
        return 0

    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p*p, n, p):  # start at p*p
                is_prime[i] = False

    return sum(i for i in range(n) if is_prime[i])

print(sum_of_primes_below(2_000_000))
--- after
import timeit

def sieve_python_loop(n):
    """Original: list[bool] + Python for-loop."""
    if n <= 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p*p, n, p):
                is_prime[i] = False
    return sum(i for i in range(n) if is_prime[i])

def sieve_list_slice(n):
    """list[bool] + C-level slice assignment."""
    if n <= 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = [False] * len(is_prime[p*p::p])
    return sum(i for i in range(n) if is_prime[i])

def sieve_bytearray(n):
    """bytearray + C-level slice assignment."""
    if n <= 2:
        return 0
    is_prime = bytearray([1]) * n
    is_prime[0] = is_prime[1] = 0
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = b'\x00' * len(is_prime[p*p::p])
    return sum(i for i, v in enumerate(is_prime) if v)

N = 2_000_000
assert sieve_python_loop(N) == sieve_list_slice(N) == sieve_bytearray(N) == 142913828922

for name, fn in [("python loop ", sieve_python_loop),
                 ("list + slice", sieve_list_slice),
                 ("bytearray   ", sieve_bytearray)]:
    t = timeit.timeit(lambda f=fn: f(N), number=5) / 5
    print(f"{name}  {t*1000:.1f} ms")

[Bash(python3 euler10.py)]
  python loop   92.0 ms
  list + slice  55.7 ms
  bytearray     32.3 ms

Assistant: There it is:

| Approach | Time | vs. original |
|---|---|---|
| Python for-loop | 92 ms | 1× |
| `list[bool]` + slice | 56 ms | 1.6× faster |
| `bytearray` + slice | **32 ms** | **2.8× faster** |

The two speedups are independent and stack:
1. **Slice assignment** (`list` → `list` version): eliminates Python bytecode dispatch for each `is_prime[i] = False` — that alone is ~40% faster.
2. **`bytearray`** (the extra jump): no Python bool objects to allocate, no pointer indirection to dereference. The crossing-off loop is operating on a flat array of raw bytes, and the CPU's prefetcher loves it.

Your cache locality intuition was exactly right — this is a memory-bound algorithm, and shrinking from 8 bytes/element (list of pointers) to 1 byte/element (bytearray) dramatically reduces cache pressure on a 2M-element structure.

The final answer: **142913828922**.

---

## Turn 4 (final)

**User:**

Perfect — we've nailed it. You traced through the design decisions beautifully:

1. **Sieve optimization**: Start crossing-off at `p*p` because all smaller multiples are already marked.
2. **Data structure**: `bytearray` beats `list[bool]` because it eliminates Python's per-object overhead — 1 byte vs ~8 bytes per element.
3. **Slice assignment**: C-level batch operations crush Python for-loops on memory-bound work.

The final solution is **2.8× faster** than the naive approach, runs in ~32ms, and returns the correct answer: **142913828922**.

Key lesson here: when benchmarking, always measure — your intuitions about memory pressure and cache locality were dead-on, but the actual numbers (`92ms → 56ms → 32ms`) make it concrete. That's the real power of learning this way: you see *why* the tradeoff matters, not just that it does.

<done/>

---

**Run end**: done after 3 turns (124s)
