import time

def clear(): print('\033[2J\033[H', end='', flush=True)

def show(grid):
    cols = len(grid[0])
    print('┌' + '─' * cols + '┐')
    for row in grid:
        print('│' + ''.join('█' if cell else ' ' for cell in row) + '│')
    print('└' + '─' * cols + '┘')

def step(grid):
    rows, cols = len(grid), len(grid[0])
    next_g = [[0]*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = sum(
                grid[(r+dr) % rows][(c+dc) % cols]
                for dr in (-1,0,1) for dc in (-1,0,1)
                if (dr,dc) != (0,0))
            next_g[r][c] = int(neighbors==3 or (grid[r][c] and neighbors==2))
    return next_g

GLIDER = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0],
    [0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]

grid = [row[:] for row in GLIDER]
for gen in range(20):
    grid = step(grid)
    clear(); show(grid); print(f'gen {gen+1}')
    time.sleep(0.2)
