LINES = [(0,1,2),(3,4,5),(6,7,8),
         (0,3,6),(1,4,7),(2,5,8),
         (0,4,8),(2,4,6)]

def new_board():
    return [' '] * 9

def winner(b):
    for i,j,k in LINES:
        if b[i] != ' ' and b[i] == b[j] == b[k]:
            return b[i]
    return None

def render(b):
    cells = [b[i] if b[i] != ' ' else str(i+1) for i in range(9)]
    rows = [' | '.join(cells[r*3:r*3+3]) for r in range(3)]
    return ('\n---+---+---\n').join(rows)
