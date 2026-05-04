import time
import os

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

OFFSETS = [(-1,-1),(-1,0),(-1,1),
           ( 0,-1),        ( 0,1),
           ( 1,-1),( 1,0),( 1,1)]

def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    return sum(
        grid[r + dr][c + dc]
        for dr, dc in OFFSETS
        if 0 <= r + dr < rows and 0 <= c + dc < cols
    )

def step(grid):
    """Advance one generation. Builds a NEW grid so all cells are
    evaluated against the same snapshot — mutating in place would
    corrupt neighbor counts mid-scan."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            n = count_neighbors(grid, r, c)
            alive = grid[r][c]
            new_grid[r][c] = 1 if (alive and n in (2, 3)) or (not alive and n == 3) else 0
    return new_grid

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

CELL_ALIVE = "██"
CELL_DEAD  = "  "

def render(grid, generation):
    border = "+" + "--" * len(grid[0]) + "+"
    lines = [f"Generation {generation}", border]
    for row in grid:
        lines.append("|" + "".join(CELL_ALIVE if c else CELL_DEAD for c in row) + "|")
    lines.append(border)
    return "\n".join(lines)

def run(grid, generations=10, delay=0.2):
    for gen in range(generations):
        os.system("clear" if os.name != "nt" else "cls")
        print(render(grid, gen))
        time.sleep(delay)
        grid = step(grid)
    os.system("clear" if os.name != "nt" else "cls")
    print(render(grid, generations))

# ---------------------------------------------------------------------------
# Known patterns
# ---------------------------------------------------------------------------

def make_empty(rows, cols):
    return [[0] * cols for _ in range(rows)]

def place(grid, pattern, row_offset, col_offset):
    """Place a pattern (list of (r,c) live-cell coords) onto grid."""
    for r, c in pattern:
        grid[r + row_offset][c + col_offset] = 1
    return grid

# Glider — travels diagonally, period 4
GLIDER = [(0,1),(1,2),(2,0),(2,1),(2,2)]

# Blinker — oscillates period 2
BLINKER = [(1,0),(1,1),(1,2)]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    pattern_name = sys.argv[1] if len(sys.argv) > 1 else "glider"

    if pattern_name == "blinker":
        grid = make_empty(7, 9)
        place(grid, BLINKER, 3, 3)
        run(grid, generations=6, delay=0.4)
    else:
        grid = make_empty(16, 32)
        place(grid, GLIDER, 1, 1)
        run(grid, generations=40, delay=0.1)
