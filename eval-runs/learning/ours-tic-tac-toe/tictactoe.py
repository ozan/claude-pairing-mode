"""
Tic-Tac-Toe: Human vs Computer
The computer plays optimally using the minimax algorithm.
"""

# The board is a list of 9 cells, indexed 1-9:
#
#   1 | 2 | 3
#  ---+---+---
#   4 | 5 | 6
#  ---+---+---
#   7 | 8 | 9

WINNING_LINES = [
    (1, 2, 3), (4, 5, 6), (7, 8, 9),  # rows
    (1, 4, 7), (2, 5, 8), (3, 6, 9),  # columns
    (1, 5, 9), (3, 5, 7),              # diagonals
]


def new_board():
    """Return a fresh board: keys 1-9, all empty."""
    return {i: " " for i in range(1, 10)}


def display(board):
    """Print the board with grid lines."""
    r = board
    print(f"\n {r[1]} | {r[2]} | {r[3]} ")
    print("---+---+---")
    print(f" {r[4]} | {r[5]} | {r[6]} ")
    print("---+---+---")
    print(f" {r[7]} | {r[8]} | {r[9]} ")
    print()


def winner(board):
    """Return 'X', 'O', or None."""
    for a, b, c in WINNING_LINES:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None


def is_full(board):
    return all(v != " " for v in board.values())


def free_cells(board):
    return [k for k, v in board.items() if v == " "]


# ── Minimax ────────────────────────────────────────────────────────────────────
# Returns a score from the computer's ('O') perspective:
#   +1  computer wins
#   -1  human wins
#    0  draw

def minimax(board, is_computer_turn):
    w = winner(board)
    if w == "O":
        return 1
    if w == "X":
        return -1
    if is_full(board):
        return 0

    scores = []
    for cell in free_cells(board):
        board[cell] = "O" if is_computer_turn else "X"
        scores.append(minimax(board, not is_computer_turn))
        board[cell] = " "

    return max(scores) if is_computer_turn else min(scores)


def best_move(board):
    """Return the cell index that gives the computer the best outcome."""
    best_score = float("-inf")
    choice = None
    for cell in free_cells(board):
        board[cell] = "O"
        score = minimax(board, is_computer_turn=False)
        board[cell] = " "
        if score > best_score:
            best_score, choice = score, cell
    return choice


# ── I/O helpers ────────────────────────────────────────────────────────────────

def human_move(board):
    """Ask the human for a valid cell and apply it."""
    while True:
        raw = input("Your move (1-9): ").strip()
        if not raw.isdigit() or int(raw) not in range(1, 10):
            print("  Please enter a number from 1 to 9.")
            continue
        cell = int(raw)
        if board[cell] != " ":
            print("  That cell is already taken.")
            continue
        board[cell] = "X"
        return


# ── Game loop ──────────────────────────────────────────────────────────────────

def play():
    print("=== Tic-Tac-Toe ===")
    print("You are X. Computer is O.")
    print("Cells are numbered 1-9, left-to-right, top-to-bottom.\n")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 \n")

    board = new_board()

    while True:
        # ── Human's turn ──
        display(board)
        human_move(board)

        w = winner(board)
        if w:
            display(board)
            print("You win! 🎉")
            break
        if is_full(board):
            display(board)
            print("It's a draw.")
            break

        # ── Computer's turn ──
        print("Computer is thinking...")
        cell = best_move(board)
        board[cell] = "O"
        print(f"Computer plays {cell}.")

        w = winner(board)
        if w:
            display(board)
            print("Computer wins.")
            break
        if is_full(board):
            display(board)
            print("It's a draw.")
            break

    again = input("\nPlay again? (y/n): ").strip().lower()
    if again == "y":
        play()


if __name__ == "__main__":
    play()
