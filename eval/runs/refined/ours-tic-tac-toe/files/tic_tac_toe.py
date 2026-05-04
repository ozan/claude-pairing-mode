WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

import random

def get_winner(board):
    for a, b, c in WINNING_LINES:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]

def display(board):
    row = lambda i: [board[i+j] if board[i+j] != ' ' else str(i+j+1)
                     for j in range(3)]
    for i in (0, 3, 6):
        print('|'.join(row(i)))

def player_move(board):
    while True:
        s = input("Your move (1-9): ")
        if s.isdigit() and 1 <= int(s) <= 9 and board[int(s)-1] == ' ':
            return int(s) - 1
        print("Invalid move, try again.")

def computer_move(board):
    return random.choice([i for i, v in enumerate(board) if v == ' '])

def main():
    board = [' '] * 9
    current = 'X'
    print("You are X. Computer is O.")
    print()

    while True:
        display(board)
        print()

        if current == 'X':
            board[player_move(board)] = current
        else:
            print("Computer is thinking...")
            board[computer_move(board)] = current

        winner = get_winner(board)
        if winner:
            display(board)
            print()
            print("You win!" if winner == 'X' else "Computer wins!")
            break
        if ' ' not in board:
            display(board)
            print()
            print("It's a draw!")
            break

        current = 'O' if current == 'X' else 'X'

if __name__ == '__main__':
    main()
