def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    return sum(grid[r+dr][c+dc]
               for dr in (-1,0,1) for dc in (-1,0,1)
               if (dr,dc) != (0,0) and 0 <= r+dr < rows and 0 <= c+dc < cols)


def display(grid, gen):
    print(f"Generation {gen}:")
    for row in grid:
        print("".join("█" if c else "·" for c in row))
    print()


def step(grid):
    rows, cols = len(grid), len(grid[0])
    next_grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = count_neighbors(grid, r, c)
            alive = grid[r][c] == 1
            next_grid[r][c] = 1 if (alive and neighbors in (2, 3)) or (not alive and neighbors == 3) else 0
    return next_grid


if __name__ == "__main__":
    # Blinker smoke test
    blinker = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    print("=== Blinker (4 generations) ===\n")
    for gen in range(4):
        display(blinker, gen)
        blinker = step(blinker)

    # Glider on a 16x16 grid
    print("=== Glider (12 generations) ===\n")
    grid = [[0] * 16 for _ in range(16)]
    for (r, c) in [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
        grid[r][c] = 1
    for gen in range(12):
        display(grid, gen)
        grid = step(grid)
