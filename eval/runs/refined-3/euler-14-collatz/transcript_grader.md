# euler-14-collatz

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:53:20

## Initial prompt

Project Euler #14: which starting number under one million produces the longest Collatz sequence? Return the starting number.

---

## Turn 1

### Tutor

Tutor: Good classic DP/memoization problem. Let me start with the most consequential design decision.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Brute force each number
For each n from 1 to 999,999, walk the full Collatz chain from scratch and count steps. Simple, no extra memory.

[B] Memoize chain lengths
Cache the chain length for every number we compute. Many starting numbers share suffixes — e.g. any n that reaches 13 can reuse `cache[13]` instead of recomputing from there.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to use?

### Student

I think B makes sense here. Since we're computing chain lengths for up to a million starting numbers, and the Collatz sequences overlap a lot, memoization should save us a ton of repeated work.

Let me start coding it up and see if I run into any issues. Should I use a dictionary to store the cache, or is there a better data structure?

---

## Turn 2

### Tutor

OPTIONS:
[A] Pre-allocated list
```diff
+++ collatz.py
@@ -0,0 +1,4 @@
+LIMIT = 1_000_000
+cache = [0] * LIMIT  # cache[n] = chain length, 0 = unknown
+
+# store result: if n < LIMIT: cache[n] = length
```
Direct index access, better memory locality. But Collatz intermediates can exceed 1M — what happens then?

[B] Dictionary cache
```diff
+++ collatz.py
@@ -0,0 +1,3 @@
+LIMIT = 1_000_000
+cache = {1: 1}
+
+# store result: cache[n] = length, works for any n
```
Handles all intermediate values naturally — no bounds check needed. Slightly higher per-lookup cost due to hashing.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which cache structure do you prefer?

### Student

I'll go with B — the dictionary. Even though list indexing is faster, I don't want to deal with the bounds checking every time an intermediate value exceeds 1M. That feels like it'll make the code messier and error-prone. The dictionary is cleaner and handles all cases naturally.

Let me write out the main function that computes the chain length with memoization:

```python
LIMIT = 1_000_000
cache = {1: 1}

def chain_length(n):
    if n in cache:
        return cache[n]
    
    if n % 2 == 0:
        next_n = n // 2
    else:
        next_n = 3 * n + 1
    
    length = 1 + chain_length(next_n)
    cache[n] = length
    return length

max_length = 0
max_start = 0

for start in range(1, LIMIT):
    length = chain_length(start)
    if length > max_length:
        max_length = length
        max_start = start

print(max_start)
```

Does this look right to you? I'm computing the chain length recursively and caching as I go.

---

## Turn 3

### Tutor

Tutor: The logic is correct. One thing worth thinking about before we finalize it — what happens with this line:

```python
length = 1 + chain_length(next_n)
```

when the chain hasn't been seen before and runs long?

OPTIONS:
[A] Keep recursive approach
Add `sys.setrecursionlimit(10_000)` at the top. Python's default is 1000 — a few Collatz chains (especially early when the cache is cold) can exceed that.

[B] Rewrite as iterative
Build the chain as a list until hitting a cached value, then walk backwards to fill the cache for every new node visited.
```diff
+++ collatz.py
@@ -4,10 +4,12 @@
-def chain_length(n):
-    if n in cache:
-        return cache[n]
-    if n % 2 == 0:
-        next_n = n // 2
-    else:
-        next_n = 3 * n + 1
-    length = 1 + chain_length(next_n)
-    cache[n] = length
-    return length
+def chain_length(n):
+    path = []
+    while n not in cache:
+        path.append(n)
+        n = n // 2 if n % 2 == 0 else 3 * n + 1
+    length = cache[n]
+    for node in reversed(path):
+        length += 1
+        cache[node] = length
+    return cache[path[0]] if path else cache[n]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'll go with B — the iterative approach. I'd rather avoid tweaking recursion limits if I can help it, and the iterative version is more predictable. Plus, it's actually more efficient since we cache every node in the path, not just the final result.

Let me trace through the logic to make sure I understand it:

1. We walk the chain forward, collecting nodes in `path`, until we hit something already in the cache
2. Then we walk backwards through `path`, incrementing the length each time and caching each node
3. That way every intermediate value we compute gets cached for future lookups

One thing I want to double-check though — at the end when we return, if `path` is empty (meaning `n` was already cached), we should just return `cache[n]`, right? And if `path` isn't empty, we return `cache[path[0]]` which is the cached length for our original starting number?

Actually, looking at it again, I think there might be a subtle bug. After the loop, `length` holds the final chain length, but we're returning `cache[path[0]]` which we just set in the loop. Should we just return `length` instead? Or am I missing something?

---

## Turn 4

### Tutor

Tutor: You're exactly right. After the backwards loop finishes, `length` already holds the chain length for `path[0]` — the last iteration sets `cache[path[0]] = length`, so they're equivalent. And in the empty-path case, `length = cache[n]` was set before the loop and never changes. So `return length` works cleanly in both cases.

Let me write the final version:

[Bash(ls collatz.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(collatz.py)]
LIMIT = 1_000_000
cache = {1: 1}

def chain_length(n):
    path = []
    while n not in cache:
        path.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    length = cache[n]
    for node in reversed(path):
        length += 1
        cache[node] = length
… (13 more lines)
  File created successfully at: collatz.py

[Bash(python3 collatz.py)]
  837799

Tutor: **837799** — chain length of 525 steps.

The return simplification you spotted is a nice example of a broader principle: when you're building up a value incrementally in a loop, you often don't need to re-derive it from a data structure at the end — the accumulator already has it. The conditional return was doing extra work to look up something you already knew.

### Student

That's a really helpful insight. I was overthinking the return — the accumulator pattern is cleaner and more direct. Thanks for catching that and showing me the final version.

So just to solidify my understanding: the key wins here were:
1. Using a dictionary cache to handle intermediates that exceed 1M
2. Going iterative instead of recursive to avoid stack limits
3. Caching every node in the path, not just endpoints, so future chains reuse that work

And the answer is **837799**. I feel good about this solution.

<done/>

---

**Run end:** done after 4 turn(s) in 117.3s
