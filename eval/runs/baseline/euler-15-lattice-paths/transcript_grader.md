# euler-15-lattice-paths

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:53:09

## Initial prompt

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

---

## Turn 1

### Tutor

Tutor: ## Project Euler #15: Lattice Paths

### Framing the Problem

A 20×20 **grid** has **21×21 lattice points**. A route from top-left `(0,0)` to bottom-right `(20,20)` consists of exactly **40 steps**: 20 right (R) and 20 down (D), in any order.

---

### Closed-Form Solution

Every route is uniquely described by choosing *which 20 of the 40 steps* are "right":

$$\text{Answer} = \binom{40}{20} = \frac{40!}{20!\;20!} = \boxed{137{,}846{,}528{,}640}$$

---

### Dynamic Programming Path

Define `dp[i][j]` = number of distinct routes from `(0,0)` to `(i,j)`.

**Base cases** — only one way to travel along an edge:
```
dp[0][j] = 1   for all j   (only move right)
dp[i][0] = 1   for all i   (only move down)
```

**Recurrence** — you arrived from either the cell above or the cell to the left:
```
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

**Why this works:** this recurrence is Pascal's triangle rotated 45°. Every interior cell sums its two "parents," exactly mirroring how binomial coefficients are built. In fact `dp[i][j] = C(i+j, i)` — the closed form is just the DP closed up.

```
     j=0  j=1  j=2  j=3  ...  j=20
i=0:   1    1    1    1         1
i=1:   1    2    3    4    ...
i=2:   1    3    6   10    ...
i=3:   1    4   10   20    ...
...
i=20:  1   ...              137846528640
```

Quick Python to verify both approaches:

```python
from math import comb
from functools import lru_cache

N = 20

# --- Closed form ---
print(comb(2*N, N))   # 137846528640

# --- DP (bottom-up) ---
dp = [[1]*(N+1) for _ in range(N+1)]   # edges = 1
for i in range(1, N+1):
    for j in range(1, N+1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]
print(dp[N][N])        # 137846528640

# --- DP (top-down memoisation) ---
@lru_cache(maxsize=None)
def routes(i, j):
    if i == 0 or j == 0: return 1
    return routes(i-1, j) + routes(i, j-1)

print(routes(N, N))    # 137846528640
```

---

### Summary

| Approach | Time | Space | Key idea |
|---|---|---|---|
| Closed form `C(40,20)` | O(N) | O(1) | Count sequences of 20 R's in 40 steps |
| Bottom-up DP | O(N²) | O(N²) or O(N) with rolling array | Pascal's triangle on a grid |
| Top-down memoisation | O(N²) | O(N²) call stack + cache | Same recurrence, lazy |

The DP approach generalises naturally to grids with **obstacles** (set `dp[i][j] = 0` for blocked cells) or **weighted paths**, where the closed form breaks down.

### Student

Thanks for walking me through this! I really appreciate seeing both the closed-form and DP approaches laid out together.

I want to make sure I understand the recurrence correctly. When we say `dp[i][j] = dp[i-1][j] + dp[i][j-1]`, we're saying that to reach cell `(i,j)`, we could have come from the cell directly above it `(i-1,j)` or directly to the left `(i,j-1)`, right? And each of those cells already "knows" how many ways there are to reach *them* from the start, so we just add those up?

Also, I'm curious — when you mention that this is "Pascal's triangle rotated 45°," do you mean that if I look at the diagonals of the DP table, I'd see the rows of Pascal's triangle? Let me think through the table you showed:

```
     j=0  j=1  j=2  j=3
i=0:   1    1    1    1
i=1:   1    2    3    4
i=2:   1    3    6   10
i=3:   1    4   10   20
```

So the diagonal with `[1, 2, 6, 20]`... hmm, that doesn't look like a Pascal row. Is it the *other* direction diagonals that match Pascal's triangle, or am I misunderstanding?

One more quick thing — in the bottom-up DP code, initialising `dp = [[1]*(N+1) for _ in range(N+1)]` sets *everything* to 1 at first, but then we only update interior cells. Is that intentional, or should we explicitly only initialize the edges to 1?

---

## Turn 2

### Tutor

Tutor: All three questions are sharp — let me take them in order.

---

### 1. The recurrence — yes, exactly right

Your description is precisely the argument. The key property that makes it valid is **optimal substructure**: the number of ways to reach `(i,j)` depends *only* on the counts already stored in its two possible predecessors, and those are always computed before `(i,j)` in the row-major fill order. You're not double-counting because the two predecessor cells are distinct — every route arrives from exactly one of them.

---

### 2. Pascal's triangle — you looked at the wrong diagonal

You spotted the main diagonal `dp[0][0], dp[1][1], dp[2][2], dp[3][3]` = `1, 2, 6, 20`. Those are the **central binomial coefficients** `C(0,0), C(2,1), C(4,2), C(6,3)` — they *appear* in Pascal's triangle, but they're plucked from the *centres* of different rows, not from a single row.

The rows of Pascal's triangle live on the **anti-diagonals**, where `i + j = k`:

```
     j=0  j=1  j=2  j=3  j=4
i=0:  [1]   1    1    1    1      ← anti-diag k=0: [1]
i=1:   1   [2]   3    4    5      ← anti-diag k=2: [1, 2, 1]
i=2:   1    3   [6]  10   15      ← anti-diag k=4: [1, 4, 6, 4, 1]
i=3:   1    4   10  [20]  35
i=4:   1    5   15   35  [70]
```

Tracing anti-diagonal `k = i + j`:

| k | cells (top→bottom) | values | Pascal row k |
|---|---|---|---|
| 0 | `(0,0)` | `1` | `1` |
| 1 | `(0,1)`, `(1,0)` | `1, 1` | `1 1` |
| 2 | `(0,2)`, `(1,1)`, `(2,0)` | `1, 2, 1` | `1 2 1` |
| 3 | `(0,3)`, `(1,2)`, `(2,1)`, `(3,0)` | `1, 3, 3, 1` | `1 3 3 1` |
| 4 | `(0,4)`, `(1,3)`, `(2,2)`, `(3,1)`, `(4,0)` | `1, 4, 6, 4, 1` | `1 4 6 4 1` ✓ |

This is what "rotated 45°" means: **tilt the DP table so the anti-diagonals become horizontal rows** and you're looking at Pascal's triangle. The recurrence `dp[i][j] = dp[i-1][j] + dp[i][j-1]` is structurally identical to Pascal's `C(n,k) = C(n-1,k-1) + C(n-1,k)` — they're the same addition rule, just laid out on different coordinate axes.

---

### 3. The `[[1]*...]` initialisation — intentional, but worth being precise about

```python
dp = [[1]*(N+1) for _ in range(N+1)]   # every cell starts as 1
for i in range(1, N+1):
    for j in range(1, N+1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

It's intentional as a **shortcut**, but the reasoning is subtle:

- The loop starts at `i=1, j=1`, so it **never touches row 0 or column 0**.
- Those edge cells keep their initialised value of `1` — which is exactly correct (one route along any edge).
- Every interior cell `(i≥1, j≥1)` is **unconditionally overwritten** by the recurrence, so their initial `1` is irrelevant — it's never read before being replaced.

A more explicit version that makes intent clearer:

```python
dp = [[0]*(N+1) for _ in range(N+1)]
for i in range(N+1): dp[i][0] = 1   # left edge
for j in range(N+1): dp[0][j] = 1   # top edge
for i in range(1, N+1):
    for j in range(1, N+1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

Both are correct. The `[[1]*...]` version works because the loop structure and the correct values happen to align perfectly — but if you ever changed the loop bounds accidentally (say, `range(0, N+1)`), the shortcut would silently produce wrong answers, while the explicit version would catch it immediately.

### Student

Ah, that makes so much sense now! Thank you for clarifying — especially the anti-diagonals explanation. I was looking at the main diagonal and got confused, but now I can see how tilting the table 45° reveals Pascal's triangle exactly. That's a really elegant way to see why the recurrence works.

And I appreciate you spelling out both the shortcut and the explicit initialization approaches. The explicit version is definitely clearer for intent and more robust — I'll remember that as a defensive coding habit when dealing with DP tables.

Let me just code this up quickly to make sure I can write it myself:

```python
from math import comb

# Closed form
N = 20
answer_closed = comb(2*N, N)
print(f"Closed form: {answer_closed}")

# DP bottom-up (explicit init)
dp = [[0]*(N+1) for _ in range(N+1)]
for i in range(N+1):
    dp[i][0] = 1
for j in range(N+1):
    dp[0][j] = 1
for i in range(1, N+1):
    for j in range(1, N+1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]

answer_dp = dp[N][N]
print(f"DP bottom-up: {answer_dp}")

assert answer_closed == answer_dp == 137846528640
print("✓ Both methods agree!")
```

Running through this in my head, the closed form hits the answer immediately with `C(40, 20)`, and the DP builds up from the edges, adding each cell from its neighbors. Both should give `137846528640`.

I feel like I've got a solid understanding now — the recurrence, the Pascal's triangle connection via anti-diagonals, and when to be explicit with initialization. For the actual problem submission, I'd probably go with the closed form since it's so clean, but knowing the DP path is really useful for extending to grids with obstacles or weights later.

<done/>

---

**Run end:** done after 2 turn(s) in 79.9s
