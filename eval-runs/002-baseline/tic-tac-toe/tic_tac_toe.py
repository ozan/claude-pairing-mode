LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def new_board():
    return [' '] * 9


def render(board):
    cells = [c if c != ' ' else str(i) for i, c in enumerate(board)]
    rows = []
    for r in range(3):
        rows.append(' ' + ' | '.join(cells[r*3:r*3+3]) + ' ')
    print(('\n' + '-' * 11 + '\n').join(rows))


def status(board):
    """Return 'X', 'O', 'draw', or None (game ongoing)."""
    for i, j, k in LINES:
        if board[i] == board[j] == board[k] != ' ':
            return board[i]
    if ' ' not in board:
        return 'draw'
    return None


def human_move(board):
    while True:
        raw = input('Your move (0-8): ').strip()
        if not raw.isdigit():
            print('Enter a digit 0-8.')
            continue
        i = int(raw)
        if not 0 <= i <= 8 or board[i] != ' ':
            print('Cell unavailable.')
            continue
        return i


def minimax(board, player, me='O', you='X'):
    s = status(board)
    if s == me:     return 1, None
    if s == you:    return -1, None
    if s == 'draw': return 0, None
    best_score = -2 if player == me else 2
    best_move = None
    for i in range(9):
        if board[i] != ' ':
            continue
        board[i] = player
        score, _ = minimax(board, you if player == me else me, me, you)
        board[i] = ' '
        if player == me and score > best_score:
            best_score, best_move = score, i
        elif player == you and score < best_score:
            best_score, best_move = score, i
    return best_score, best_move


def computer_move(board, me='O', you='X'):
    return minimax(board, me, me, you)[1]


def play_one():
    board = new_board()
    turn = 'X'  # human is X and goes first
    while status(board) is None:
        render(board)
        if turn == 'X':
            board[human_move(board)] = 'X'
        else:
            print('Computer thinking...')
            board[computer_move(board)] = 'O'
        turn = 'O' if turn == 'X' else 'X'
    render(board)
    s = status(board)
    print('Draw.' if s == 'draw' else f'{s} wins.')


def main():
    while True:
        play_one()
        if input('Play again? (y/n): ').strip().lower() != 'y':
            break


if __name__ == '__main__':
    main()

# cells indexed 0..8, laid out like a numpad:
#   0 | 1 | 2
#   3 | 4 | 5
#   6 | 7 | 8
