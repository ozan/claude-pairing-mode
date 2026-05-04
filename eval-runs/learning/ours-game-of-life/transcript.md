# ours-game-of-life

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T20:01:54.447Z

---

## Turn 1

**User:**

Let's implement Conway's Game of Life in Python. Take a 2D grid (list of lists, 0/1), advance one generation, and pretty-print to the terminal. Run a few generations of a known pattern (glider or blinker).

**Pair:**

[Write(/tmp/game_of_life.py)]
"""Conway's Game of Life — step through generations of a glider pattern."""

import time
import os


# ── Rules ────────────────────────────────────────────────────────────────────
# 1. Live cell with 2 or 3 live neighbours → survives
# 2. Dead cell with exactly 3 live neighbours → becomes alive
# 3. Every other cell → dies / stays dead


… (88 more lines)

[Bash(cat /tmp/game_of_life.py 2>/dev/null || echo "FILE_NOT_FOUND")]
  """
  Conway's Game of Life
  - Grid: list of lists of 0/1 (dead/alive)
  - Advances one generation per step
  - Pretty-prints each generation to the terminal
  """
  
  import time
  import os
  from typing import List
  
  Grid = List[List[int]]
  … (133 more lines)

Assistant: There's already a file there. Let me read it properly, then overwrite it with the clean version.

[Read(/tmp/game_of_life.py)]
  1	"""
  2	Conway's Game of Life
  3	- Grid: list of lists of 0/1 (dead/alive)
  4	- Advances one generation per step
  5	- Pretty-prints each generation to the terminal
  6	"""
  7	
  8	import time
  9	import os
  10	from typing import List
  11	
  12	Grid = List[List[int]]
  … (134 more lines)

Assistant: The file already exists with a good structure. Let me rewrite it with improvements — cleaner type hints, a non-clearing scroll mode so all generations stay visible, and a better demo:

[Write(/tmp/game_of_life.py)]
"""
Conway's Game of Life
─────────────────────
Grid: list[list[int]]  (0 = dead, 1 = alive)

Rules applied each generation:
  1. Live cell with 2 or 3 live neighbours → survives
  2. Dead cell with exactly 3 live neighbours → born
  3. All other cells → die / stay dead
"""

import time
… (145 more lines)

[Bash(cd /tmp && python game_of_life.py 2>&1)]
  error: Exit code 127

[Bash(cd /tmp && python3 game_of_life.py 2>&1)]
  ══════════════════════════════
    Blinker demo  (6 generations)
  ══════════════════════════════
  
    Generation 0  [Blinker  (period-2 oscillator)]
    ┌──────────┐
    │          │
    │          │
    │  ██████  │
    │          │
    │          │
    └──────────┘
  … (332 more lines)

Assistant: Works perfectly. Here's a walkthrough of every key idea:

---

## How it works

### The grid
A plain `list[list[int]]` — `0` is dead, `1` is alive. No libraries needed.

```python
Grid = list[list[int]]

def make_empty(rows: int, cols: int) -> Grid:
    return [[0] * cols for _ in range(rows)]
```

---

### Counting neighbours
Every cell has up to 8 neighbours. We iterate over all 9 offsets `(-1, 0, +1) × (-1, 0, +1)` and skip `(0, 0)` (the cell itself). Boundary checks keep us in-bounds without wrapping.

```python
for dr in (-1, 0, 1):
    for dc in (-1, 0, 1):
        if dr == 0 and dc == 0:   # skip self
            continue
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            total += grid[r][c]
```

---

### Advancing one generation — `step()`
Three rules collapse into **one expression**:

```python
new[r][c] = 1 if (alive and n in (2, 3)) or (not alive and n == 3) else 0
#                 ^─── survival ───────^    ^─── birth ───────────^
```

Critically, `step()` **always writes a fresh grid** — mutating in place would let already-updated cells influence their own neighbours.

---

### Pretty printer
Two-wide `██` blocks make cells look square in most terminal fonts. Box-drawing characters give it a clean border.

```python
LIVE = "██"
DEAD = "  "
```

---

### The two patterns you saw

| Pattern | What it does |
|---|---|
| **Blinker** | 3 horizontal cells ↔ 3 vertical cells, forever (period 2) |
| **Glider** | Reproduces itself shifted one cell diagonally every 4 generations |

---

### Live animation mode
Set `ANIMATE = True` at the bottom to get a proper in-place animation — `os.system("clear")` redraws the same screen position each frame instead of scrolling.

---

## Turn 2 (final)

**User:**

Perfect! The implementation is complete and working. Here's what we've built:

## Summary

✅ **Conway's Game of Life in Python** — fully functional with:

- **Grid representation**: Plain `list[list[int]]` with 0 (dead) and 1 (alive)
- **Core rules**: Implemented in a single-line conditional in the `step()` function
  - Live cell with 2–3 neighbours survives
  - Dead cell with exactly 3 neighbours born
  - All others die
- **Pretty-printing**: Box-drawing characters `┌─┐│└─┘` with `██` for live cells
- **Two demo patterns**:
  - **Blinker** (period-2): horizontal ↔ vertical oscillator running 6 generations
  - **Glider** (period-4): diagonal self-replicating pattern (commented; swap `PATTERN = "blinker"` to `"glider"`)

## Key learnings

1. **Boundary checks** — no wrapping; cells outside the grid don't have neighbours
2. **Fresh grid per generation** — `step()` writes to a new grid to avoid cells affecting their own updates
3. **Neighbour counting** — all 8 directions in a simple nested loop, skipping the cell itself
4. **Visual polish** — two-wide blocks make cells look square; box borders frame the action

The code is at `/tmp/game_of_life.py`, runs with `python3 game_of_life.py`, and produces stable, correct output. You can toggle `ANIMATE = True` for in-place terminal animation instead of scroll-down mode.

<done/>

---

**Run end**: done after 1 turn (96s)
