import random

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def make_board():
    return [' '] * 9

def winner(board):
    for a, b, c in LINES:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def minimax(board, is_max):
    w = winner(board)
    if w == 'O': return 1
    if w == 'X': return -1
    moves = [i for i, v in enumerate(board) if v == ' ']
    if not moves: return 0
    results = []
    for i in moves:
        board[i] = 'O' if is_max else 'X'
        results.append(minimax(board, not is_max))
        board[i] = ' '
    return max(results) if is_max else min(results)

def computer_move(board):
    moves = [i for i, v in enumerate(board) if v == ' ']
    best_score = max(_score_move(board, i) for i in moves)
    best_moves = [i for i in moves if _score_move(board, i) == best_score]
    return random.choice(best_moves)

def _score_move(board, i):
    board[i] = 'O'
    s = minimax(board, False)
    board[i] = ' '
    return s

def print_board(board):
    def cell(i):
        return board[i] if board[i] != ' ' else str(i + 1)
    for row in range(3):
        r = row * 3
        print(f" {cell(r)} | {cell(r+1)} | {cell(r+2)} ")
        if row < 2:
            print("---+---+---")

def get_human_move(board):
    while True:
        try:
            i = int(input("Your move (1-9): ")) - 1
            if 0 <= i <= 8 and board[i] == ' ':
                return i
        except ValueError:
            pass
        print("Invalid move, try again.")

def play():
    board = make_board()
    print("You are X, computer is O. X goes first.")
    print_board(board)

    for turn in range(9):
        if turn % 2 == 0:
            board[get_human_move(board)] = 'X'
        else:
            move = computer_move(board)
            print(f"Computer plays {move + 1}.")
            board[move] = 'O'

        print_board(board)
        w = winner(board)
        if w:
            print(f"{'You win!' if w == 'X' else 'Computer wins!'}")
            return

    print("It's a draw.")

if __name__ == '__main__':
    play()
