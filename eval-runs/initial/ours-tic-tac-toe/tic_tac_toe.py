import random

WINS = [(0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)]
def get_winner(board):
    for a, b, c in WINS:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def computer_move(board):
    for mark in ('O', 'X'):          # win, then block
        for line in WINS:
            vals = [board[i] for i in line]
            if vals.count(mark) == 2 and ' ' in vals:
                return line[vals.index(' ')]
    if board[4] == ' ': return 4     # centre
    corners = [i for i in (0,2,6,8) if board[i]==' ']
    if corners: return random.choice(corners)
    return random.choice([i for i,v in enumerate(board) if v==' '])

def display(board):
    def cell(i):
        return board[i] if board[i] != ' ' else str(i+1)
    for r in range(3):
        print(' | '.join(cell(r*3+c) for c in range(3)))
        if r < 2: print('--+---+--')

def play():
    board = [' '] * 9
    display(board)
    for turn in range(9):
        if turn % 2 == 0:
            while True:
                try:
                    move = int(input("Your move (1-9): ")) - 1
                    if 0 <= move <= 8 and board[move] == ' ':
                        break
                except ValueError:
                    pass
                print("Invalid move, try again.")
            board[move] = 'X'
        else:
            move = computer_move(board)
            print(f"Computer plays {move+1}")
            board[move] = 'O'
        display(board)
        winner = get_winner(board)
        if winner:
            print("You win!" if winner == 'X' else "Computer wins!")
            return
    print("Draw!")

if __name__ == '__main__':
    play()
