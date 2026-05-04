def clear_screen():
    print("\033[H\033[2J", end="")

DIRS = [(-1,-1), (-1, 0), (-1, 1),
        ( 0,-1),          ( 0, 1),
        ( 1,-1), ( 1, 0), ( 1, 1)]

def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    return sum(grid[r+dr][c+dc] for dr, dc in DIRS
               if 0 <= r+dr < rows and 0 <= c+dc < cols)

def render(grid, gen):
    header = f"Generation {gen}\n"
    frame = "\n".join("".join("█" if c else "·" for c in row)
                      for row in grid)
    print(header + frame)

def step(grid):
    rows, cols = len(grid), len(grid[0])
    next_grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            n = count_neighbors(grid, r, c)
            if (grid[r][c] == 1 and n in (2, 3)) or n == 3:
                next_grid[r][c] = 1
    return next_grid

GLIDER = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
]

def make_grid(rows, cols, pattern, offset_r=1, offset_c=1):
    grid = [[0] * cols for _ in range(rows)]
    for r, row in enumerate(pattern):
        for c, val in enumerate(row):
            grid[offset_r + r][offset_c + c] = val
    return grid

if __name__ == "__main__":
    import time
    grid = make_grid(20, 40, GLIDER)
    for gen in range(60):
        clear_screen()
        render(grid, gen)
        time.sleep(0.12)
        grid = step(grid)
