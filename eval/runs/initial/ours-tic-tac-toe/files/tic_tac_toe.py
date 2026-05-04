board = [' '] * 9
WINS = [(0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)]

def display(board):
    for i in range(0, 9, 3):
        row = [board[i+j] if board[i+j] != ' ' else str(i+j+1)
               for j in range(3)]
        print(' | '.join(row))
        if i < 6: print('---------')

def check_winner(board):
    for a,b,c in WINS:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return 'D' if ' ' not in board else None

def computer_move(board):
    # 1. Win if possible; 2. Block opponent win
    for player in ('O', 'X'):
        for a,b,c in WINS:
            line = [board[a],board[b],board[c]]
            if line.count(player)==2 and ' ' in line:
                return [a,b,c][line.index(' ')]
    # 3. Center, 4. Corner, 5. Any open
    for sq in [4, 0,2,6,8, 1,3,5,7]:
        if board[sq] == ' ':
            return sq

def player_move(board):
    while True:
        try:
            sq = int(input('Your move (1-9): ')) - 1
            if 0 <= sq <= 8 and board[sq] == ' ':
                return sq
        except ValueError:
            pass
        print('Invalid — try again.')

def main():
    board = [' '] * 9
    print('You are X, computer is O.')
    display(board)
    while True:
        # Player turn
        sq = player_move(board)
        board[sq] = 'X'
        display(board)
        result = check_winner(board)
        if result:
            print('You win!' if result == 'X' else "It's a draw!")
            break
        # Computer turn
        sq = computer_move(board)
        print(f'Computer plays {sq+1}.')
        board[sq] = 'O'
        display(board)
        result = check_winner(board)
        if result:
            print('Computer wins!' if result == 'O' else "It's a draw!")
            break

if __name__ == '__main__':
    main()
