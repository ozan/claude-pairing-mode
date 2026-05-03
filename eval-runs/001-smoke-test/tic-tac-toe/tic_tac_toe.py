def new_board():
    return [' '] * 9

LINES = [(0,1,2),(3,4,5),(6,7,8),
         (0,3,6),(1,4,7),(2,5,8),
         (0,4,8),(2,4,6)]

def render(b):
    cells = [c if c != ' ' else str(i + 1) for i, c in enumerate(b)]
    rows = [' | '.join(cells[i:i+3]) for i in (0, 3, 6)]
    return ('\n' + '-' * 9 + '\n').join(rows)

def winner(b):
    for i, j, k in LINES:
        if b[i] != ' ' and b[i] == b[j] == b[k]:
            return b[i]
    return None

def minimax(b, player, depth=0):
    w = winner(b)
    if w == 'O': return 10 - depth, None
    if w == 'X': return depth - 10, None
    if ' ' not in b: return 0, None
    best_score = -99 if player == 'O' else 99
    best_move = None
    for i in range(9):
        if b[i] == ' ':
            b[i] = player
            score, _ = minimax(b, 'X' if player == 'O' else 'O', depth + 1)
            b[i] = ' '
            if (player == 'O' and score > best_score) or (player == 'X' and score < best_score):
                best_score, best_move = score, i
    return best_score, best_move

def human_move(b):
    while True:
        try:
            i = int(input('Your move (1-9): ')) - 1
            if 0 <= i < 9 and b[i] == ' ':
                return i
        except ValueError:
            pass
        print('Invalid move, try again.')
