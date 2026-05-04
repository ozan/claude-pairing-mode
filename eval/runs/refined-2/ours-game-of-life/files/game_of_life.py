DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),
        (0,1),(1,-1),(1,0),(1,1)]


def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    return sum(grid[r+dr][c+dc] for dr, dc in DIRS
               if 0 <= r+dr < rows and 0 <= c+dc < cols)


def next_gen(grid):
    rows, cols = len(grid), len(grid[0])
    new = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            n = count_neighbors(grid, r, c)
            if grid[r][c] and n in (2, 3):
                new[r][c] = 1
            elif not grid[r][c] and n == 3:
                new[r][c] = 1
    return new


def pretty_print(grid):
    for row in grid:
        print(' '.join('#' if cell else '.' for cell in row))


def run(grid, generations=5):
    for i in range(generations):
        print(f"--- gen {i} ---")
        pretty_print(grid)
        print()
        grid = next_gen(grid)


# --- Blinker: period-2 oscillator ---
#   . . . . .        . . . . .
#   . . . . .        . . # . .
#   . # # # .  <-->  . . # . .
#   . . . . .        . . # . .
#   . . . . .        . . . . .
BLINKER = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

# --- Glider: travels diagonally every 4 generations ---
GLIDER = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

if __name__ == "__main__":
    print("======= BLINKER (6 generations) =======")
    run(BLINKER, generations=6)

    print("======= GLIDER (9 generations) =======")
    run(GLIDER, generations=9)
