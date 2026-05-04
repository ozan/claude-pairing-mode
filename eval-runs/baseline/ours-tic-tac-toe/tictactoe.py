import random

def make_board():
    return [" "] * 9

def print_board(board):
    rows = [board[i*3:(i+1)*3] for i in range(3)]
    print()
    for i, row in enumerate(rows):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("---+---+---")
    print()

def print_board_with_hints(board):
    """Print the board with position numbers for empty squares."""
    display = [str(i+1) if board[i] == " " else board[i] for i in range(9)]
    rows = [display[i*3:(i+1)*3] for i in range(3)]
    print()
    for i, row in enumerate(rows):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("---+---+---")
    print()

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def check_winner(board):
    for a, b, c in WINNING_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board):
    return " " not in board

def minimax(board, is_maximizing, alpha=-float("inf"), beta=float("inf")):
    winner = check_winner(board)
    if winner == "O":   return 10
    if winner == "X":   return -10
    if is_full(board):  return 0

    if is_maximizing:
        best = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                best = max(best, minimax(board, False, alpha, beta))
                board[i] = " "
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                best = min(best, minimax(board, True, alpha, beta))
                board[i] = " "
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

def computer_move(board):
    empty = [i for i in range(9) if board[i] == " "]
    # On the first move, pick randomly for variety
    if len(empty) == 9:
        return random.choice(empty)
    best_score = -float("inf")
    best_move = empty[0]
    for i in empty:
        board[i] = "O"
        score = minimax(board, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            best_move = i
    return best_move

def get_human_move(board):
    while True:
        try:
            move = int(input("Your move (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] == " ":
                return move
            else:
                print("That square is taken or out of range. Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")

def play_game():
    board = make_board()
    print("\n  Tic-Tac-Toe  ")
    print("  You are X, computer is O")
    print("  Squares are numbered 1-9:")
    print_board_with_hints(board)

    human_first = input("Do you want to go first? (y/n): ").strip().lower() != "n"
    human_turn = human_first

    while True:
        print_board(board)

        if human_turn:
            print("Your turn (X):")
            move = get_human_move(board)
            board[move] = "X"
        else:
            print("Computer is thinking...")
            move = computer_move(board)
            board[move] = "O"
            print(f"Computer plays {move + 1}")

        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "X":
                print("You win! Congratulations!")
            else:
                print("Computer wins! Better luck next time.")
            return

        if is_full(board):
            print_board(board)
            print("It's a draw!")
            return

        human_turn = not human_turn

def main():
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
