import random

LINES = [(0,1,2),(3,4,5),(6,7,8),
         (0,3,6),(1,4,7),(2,5,8),
         (0,4,8),(2,4,6)]

def winner(board):
    for a, b, c in LINES:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def is_draw(board):
    return ' ' not in board and winner(board) is None

def best_move(board, ai='O', human='X'):
    def find_threat(mark):
        for a, b, c in LINES:
            cells = [board[a], board[b], board[c]]
            if cells.count(mark) == 2 and ' ' in cells:
                return (a, b, c)[cells.index(' ')]
        return None

    # 1. Win if possible
    move = find_threat(ai)
    if move is not None:
        return move
    # 2. Block human's win
    move = find_threat(human)
    if move is not None:
        return move
    # 3. Take center
    if board[4] == ' ':
        return 4
    # 4. Any open square
    # TODO: add fork detection here
    return random.choice([i for i, v in enumerate(board) if v == ' '])

def display(board):
    for i in range(0, 9, 3):
        row = [board[i+j] if board[i+j] != ' ' else str(i+j+1)
               for j in range(3)]
        print(' | '.join(row))
        if i < 6:
            print('---------')

def get_human_move(board):
    while True:
        raw = input("Your move (1-9): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 9 and board[int(raw)-1] == ' ':
            return int(raw) - 1
        print("Invalid move. Pick an empty square (1-9).")

def play():
    while True:
        board = [' '] * 9
        choice = input("Play as X (first) or O (second)? ").upper().strip()
        human = choice if choice in ('X', 'O') else 'X'
        ai = 'O' if human == 'X' else 'X'
        turn = 'X'

        while not winner(board) and not is_draw(board):
            display(board)
            if turn == human:
                move = get_human_move(board)
            else:
                move = best_move(board, ai=ai, human=human)
                print(f"Computer plays {ai} at position {move + 1}.")
            board[move] = turn
            turn = 'O' if turn == 'X' else 'X'

        display(board)
        w = winner(board)
        if w == human:
            print("You win!")
        elif w == ai:
            print("Computer wins!")
        else:
            print("It's a draw.")

        if input("Play again? (y/n): ").lower().strip() != 'y':
            break

if __name__ == '__main__':
    play()
