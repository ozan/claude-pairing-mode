import time


def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    total = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr, dc) != (0, 0) and 0 <= r + dr < rows and 0 <= c + dc < cols:
                total += grid[r + dr][c + dc]
    return total


def next_generation(grid):
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = count_neighbors(grid, r, c)
            alive = grid[r][c]
            new_grid[r][c] = int(
                alive and neighbors in (2, 3) or not alive and neighbors == 3
            )
    return new_grid


def clear():
    print('\033[H\033[2J', end='', flush=True)


def pretty_print(grid, gen):
    print(f"Generation {gen}")
    for row in grid:
        print(' '.join('█' if cell else '·' for cell in row))
    print()


# fmt: off
GLIDER = [
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# fmt: on


if __name__ == '__main__':
    grid = [row[:] for row in GLIDER]
    for gen in range(20):
        clear()
        pretty_print(grid, gen)
        time.sleep(0.3)
        grid = next_generation(grid)
