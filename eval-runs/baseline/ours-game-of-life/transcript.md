# ours-game-of-life

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:33:29.974Z

---

## Turn 1

**User:**

Let's implement Conway's Game of Life in Python. Take a 2D grid (list of lists, 0/1), advance one generation, and pretty-print to the terminal. Run a few generations of a known pattern (glider or blinker).

**Pair:**

Assistant: I'll write a clean Python implementation with both patterns, then run it right away.

[Write(/tmp/life.py)]
"""Conway's Game of Life — 2D list-of-lists (0/1) implementation."""

import os
import time
import copy

# ── Core logic ────────────────────────────────────────────────────────────────

def count_neighbors(grid: list[list[int]], r: int, c: int) -> int:
    """Return the number of live neighbours for cell (r, c)."""
    rows, cols = len(grid), len(grid[0])
    total = 0
… (107 more lines)

[Bash(cd /tmp && python life.py)]
  error: Exit code 127

[Bash(cd /tmp && python3 life.py)]
  ==================================================
    BLINKER  (period-2 oscillator)
  ==================================================
   Generation 0  [blinker]
  ┌──────────┐
  │          │
  │    ██    │
  │    ██    │
  │    ██    │
  │          │
  └──────────┘
  
  … (247 more lines)

Assistant: Everything runs perfectly. Here's a walkthrough of the implementation:

---

## How it works

### Core engine (`next_generation`)
```
grid → count neighbours for every cell → apply rules → new grid
```
The four classic rules collapse into two simple checks:

| Cell state | Neighbours | Result |
|---|---|---|
| Alive | 2 or 3 | Survives |
| Alive | anything else | Dies |
| Dead | exactly 3 | Born |
| Dead | anything else | Stays dead |

`count_neighbors` walks the 3×3 Moore neighbourhood, skipping the cell itself and clamping to grid bounds — **no wrapping**, so cells at the edge simply have fewer neighbours.

### Key design choices
| Decision | Reason |
|---|---|
| **Returns a new grid** (no in-place mutation) | Applying rules simultaneously requires you to read from the old grid and write to a new one. Mutating in-place would corrupt neighbour counts mid-pass. |
| `copy.deepcopy` before the run loop | Keeps the original seed untouched so you can re-run it. |
| `██` (two block chars) for live cells | Terminal cells are ~2× taller than wide, so doubling the character width makes the grid look square. |
| `animate=False` by default | Leaves all generations on screen for easy scrolling; set `animate=True` to get a live animation with `os.system("clear")` between frames. |

### Patterns demonstrated
- **Blinker** — simplest oscillator (period 2): rotates between vertical ↕ and horizontal ↔ every generation.  
- **Glider** — simplest spaceship (period 4): the shape repeats itself shifted one cell diagonally every 4 generations — you can watch it crawl toward the bottom-right corner over the 12 frames above.

---

## Turn 2 (final)

**User:**

The implementation is complete and working! Here's what's happening in the output:

### **Blinker** (top section)
- Alternates between a vertical `██` column (gen 0, 2, 4...) and a horizontal `██` row (gen 1, 3, 5...)
- Classic period-2 oscillator — simplest non-trivial pattern

### **Glider** (bottom section)
- Watch the diagonal shape crawl toward the bottom-right over 12 generations
- Every 4 frames, it returns to its original shape but shifted — the archetypal "spaceship"

---

## Code highlights

**The rule engine:**
```python
def next_generation(grid):
    new = [[0] * cols for _ in rows]
    for r in range(rows):
        for c in range(cols):
            n = count_neighbors(grid, r, c)
            if grid[r][c] == 1 and n in (2, 3):
                new[r][c] = 1  # survives
            elif grid[r][c] == 0 and n == 3:
                new[r][c] = 1  # born
    return new
```

**Neighbor counting** clamps to grid bounds (no wrapping), so edge cells have naturally fewer neighbours.

**Key insight:** Must read from the old grid and write to a new one — applying all rules *simultaneously* is the entire point of Life. In-place mutation would corrupt mid-calculation.

<done/>

---

**Run end**: done after 1 turn (49s)
