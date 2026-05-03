# euler-15-lattice-paths

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-02T23:32:50.647Z

---

## Turn 1

**User:**

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

**Pair:**

Assistant: ## Project Euler #15

### Framing the problem

A 20×20 **grid** has **21×21 lattice points**. You start at (0,0) and must reach (20,20). Every valid path is exactly 40 moves long: 20 rights (**R**) and 20 downs (**D**), in some order. Counting paths = counting distinct arrangements of those 40 moves.

---

### Closed-form answer

Choose which 20 of the 40 moves are **R** (the rest are forced to be **D**):

$$\binom{40}{20} = \frac{40!}{20!\;20!} = \mathbf{137{,}846{,}528{,}640}$$

---

### The DP path (and why it agrees)

Build a 21×21 table where `T[i][j]` = number of paths to lattice point *(i, j)*:

| | j=0 | j=1 | j=2 | … | j=20 |
|---|---|---|---|---|---|
| **i=0** | 1 | 1 | 1 | … | 1 |
| **i=1** | 1 | 2 | 3 | … | 21 |
| **i=2** | 1 | 3 | 6 | … | 231 |
| **⋮** | | | | | |
| **i=20** | 1 | 21 | 231 | … | **137,846,528,640** |

**Base cases** — only one way to travel along either border (no choice of direction):
```
T[0][j] = 1   for all j
T[i][0] = 1   for all i
```

**Recurrence** — you arrived from above *or* from the left:
```
T[i][j] = T[i-1][j] + T[i][j-1]
```

This is exactly Pascal's triangle rotated 45°. The closed form falls straight out of it:

$$T[i][j] = \binom{i+j}{i}$$

so `T[20][20] = C(40,20)` — the two approaches are the same identity viewed differently. DP is pedagogically cleaner (no factorial arithmetic, no overflow risk if you use integers); the binomial is O(1) once you see the structure.

---

### Quick Python check

```python
from math import comb
print(comb(40, 20))          # 137846528640

# DP confirmation
T = [[1]*(21) for _ in range(21)]
for i in range(1, 21):
    for j in range(1, 21):
        T[i][j] = T[i-1][j] + T[i][j-1]
print(T[20][20])             # 137846528640
```

**Answer: 137,846,528,640**

---

## Turn 2 (final)

**User:**

looks good — concise, complete, and covers both approaches. The binomial insight and the DP table make it clear they're the same structure viewed differently. The Python snippet is a nice touch for verification.

<done/>

---

**Run end**: done after 1 turn (42s)
