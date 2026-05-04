board = [' '] * 9
LINES = [(0,1,2),(3,4,5),(6,7,8),
         (0,3,6),(1,4,7),(2,5,8),
         (0,4,8),(2,4,6)]

def display(board):
    r = lambda i: board[i] if board[i] != ' ' else str(i+1)
    print(f" {r(0)} | {r(1)} | {r(2)} ")
    print("---+---+---")
    print(f" {r(3)} | {r(4)} | {r(5)} ")
    print("---+---+---")
    print(f" {r(6)} | {r(7)} | {r(8)} ")

def winner(board):
    for a, b, c in LINES:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def minimax(board, is_max):
    w = winner(board)
    if w == 'X': return 1
    if w == 'O': return -1
    moves = [i for i, v in enumerate(board) if v == ' ']
    if not moves: return 0
    scores = []
    for m in moves:
        b = board[:]
        b[m] = 'X' if is_max else 'O'
        scores.append(minimax(b, not is_max))
    return max(scores) if is_max else min(scores)

def best_move(board):
    moves = [i for i, v in enumerate(board) if v == ' ']
    best_score = float('inf')
    best_idx = None
    for m in moves:
        b = board[:]
        b[m] = 'O'
        score = minimax(b, True)
        if score < best_score:
            best_score = score
            best_idx = m
    return best_idx

def human_move(board):
    while True:
        try:
            i = int(input("Your move (1-9): ")) - 1
            if 0 <= i <= 8 and board[i] == ' ':
                return i
            print("Invalid move. Try again.")
        except ValueError:
            print("Enter a number 1-9.")

def play():
    board = [' '] * 9
    print("You are X. Computer is O. Squares are numbered 1-9:")
    display(board)
    while True:
        # Human turn (X)
        board[human_move(board)] = 'X'
        display(board)
        w = winner(board)
        if w:
            print("You win!" if w == 'X' else "Computer wins!")
            break
        if ' ' not in board:
            print("Draw!")
            break

        # Computer turn (O)
        print("Computer is thinking...")
        board[best_move(board)] = 'O'
        display(board)
        w = winner(board)
        if w:
            print("You win!" if w == 'X' else "Computer wins!")
            break
        if ' ' not in board:
            print("Draw!")
            break

if __name__ == '__main__':
    play()
