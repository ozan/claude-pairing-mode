EMPTY = ' '
HUMAN = 'X'
CPU   = 'O'

WINS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def make_board():
    return [EMPTY] * 9

def print_board(board):
    def cell(i):
        return board[i] if board[i] != EMPTY else str(i + 1)
    print(f"\n {cell(0)} | {cell(1)} | {cell(2)}")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)}")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)}\n")

def winner(board):
    for a, b, c in WINS:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    return None

def is_full(board):
    return EMPTY not in board

def human_move(board):
    while True:
        try:
            choice = int(input("Your move (1-9): ")) - 1
            if 0 <= choice <= 8 and board[choice] == EMPTY:
                return choice
            print("Invalid move. Try again.")
        except ValueError:
            print("Enter a number 1-9.")

def cpu_move(board):
    # Win if possible
    for a, b, c in WINS:
        for x, y, z in [(a,b,c),(b,a,c),(c,a,b)]:
            if board[x] == board[y] == CPU and board[z] == EMPTY:
                return z
    # Block human win
    for a, b, c in WINS:
        for x, y, z in [(a,b,c),(b,a,c),(c,a,b)]:
            if board[x] == board[y] == HUMAN and board[z] == EMPTY:
                return z
    # Prefer center, then corners, then edges
    for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if board[i] == EMPTY:
            return i

def play():
    board = make_board()
    print("Tic-Tac-Toe — you are X, computer is O.")
    print("Squares are numbered 1-9, left to right, top to bottom.")
    print_board(board)

    turn = HUMAN  # human goes first

    while True:
        if turn == HUMAN:
            move = human_move(board)
        else:
            move = cpu_move(board)
            print(f"Computer plays {move + 1}.")

        board[move] = turn
        print_board(board)

        w = winner(board)
        if w:
            print("You win!" if w == HUMAN else "Computer wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        turn = CPU if turn == HUMAN else HUMAN

if __name__ == "__main__":
    play()
