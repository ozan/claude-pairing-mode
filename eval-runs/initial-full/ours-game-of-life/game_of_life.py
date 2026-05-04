import time

# ── core logic ────────────────────────────────────────────────────────────────

def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    return sum(
        grid[r + dr][c + dc]
        for dr in (-1, 0, 1) for dc in (-1, 0, 1)
        if (dr, dc) != (0, 0)
        and 0 <= r + dr < rows and 0 <= c + dc < cols
    )

def next_gen(grid):
    rows, cols = len(grid), len(grid[0])
    new = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            n = count_neighbors(grid, r, c)
            new[r][c] = 1 if (grid[r][c] and n in (2, 3)) or (not grid[r][c] and n == 3) else 0
    return new

# ── display ───────────────────────────────────────────────────────────────────

def clear():
    print('\033[H', end='', flush=True)

def pretty_print(grid, gen):
    rows, cols = len(grid), len(grid[0])
    border = '┼' + '─' * cols + '┼'
    lines = [border]
    for row in grid:
        lines.append('│' + ''.join('█' if cell else ' ' for cell in row) + '│')
    lines.append(border)
    lines.append(f'  generation {gen}')
    print('\n'.join(lines), flush=True)

# ── seeds ─────────────────────────────────────────────────────────────────────

def make_grid(rows, cols, live_cells):
    """Return a rows×cols zero grid with the given (r, c) cells set to 1."""
    grid = [[0] * cols for _ in range(rows)]
    for r, c in live_cells:
        grid[r][c] = 1
    return grid

GLIDER = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]   # classic SE-moving glider

BLINKER = [(5, 4), (5, 5), (5, 6)]                    # period-2 oscillator

# ── main ──────────────────────────────────────────────────────────────────────

def run(seed, rows=20, cols=40, generations=40, delay=0.15):
    grid = make_grid(rows, cols, seed)
    # Reserve screen space on first print (no cursor-home yet)
    pretty_print(grid, gen=0)
    for gen in range(1, generations + 1):
        time.sleep(delay)
        grid = next_gen(grid)
        clear()
        pretty_print(grid, gen)

if __name__ == '__main__':
    run(GLIDER)
