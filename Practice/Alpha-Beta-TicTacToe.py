from os import system
import random

def print_board(board):
    system('cls')
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def print_board_nums():
    number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
    for row in number_board:
        print('| ' + ' | '.join(row) + ' |')

def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

def empty_squares(board):
    return ' ' in board

def num_empty_squares(board):
    return board.count(' ')

def make_move(board, square, letter):
    if board[square] == ' ':
        board[square] = letter
        if check_winner(board, square, letter):  # Now using the passed letter
            return True, letter
        return True, None
    return False, None

def check_winner(board, square, letter):
    # Check row
    row_ind = square // 3
    row = board[row_ind*3 : (row_ind + 1)*3]
    if all([spot == letter for spot in row]):
        return True
    
    # Check column
    col_ind = square % 3
    column = [board[col_ind+i*3] for i in range(3)]
    if all([spot == letter for spot in column]):
        return True
    
    # Check diagonals
    if square % 2 == 0:
        diagonal1 = [board[i] for i in [0, 4, 8]]
        if all([spot == letter for spot in diagonal1]):
            return True
        diagonal2 = [board[i] for i in [2, 4, 6]]
        if all([spot == letter for spot in diagonal2]):
            return True
    return False

def evaluate_board(board, CLetter, PLetter, depth=0):
    """Evaluate the board state using player letters"""
    winning_combos = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    
    for combo in winning_combos:
        a, b, c = combo
        if board[a] == board[b] == board[c] == CLetter:
            return 10 - depth  # Computer wins
        if board[a] == board[b] == board[c] == PLetter:
            return -10 + depth  # Player wins
    
    return 0 if ' ' not in board else None

def check_draw(board):
    return not empty_squares(board)

def human_player(board, CLetter, PLetter):
    valid_square = False
    val = None
    while not valid_square:
        square = input('Enter your move (0-8): ')
        try:
            val = int(square)
            if val not in available_moves(board):
                raise ValueError
            valid_square = True
        except ValueError:
            print('Invalid square. Try again.')
    return val

def minimax(board, alpha, beta, CLetter, PLetter, maximizing_player=True):
    result = evaluate_board(board, CLetter, PLetter)
    if result is not None: 
        return result, None  

    if maximizing_player:
        best_score = -float('inf')
        best_move = None
        for move in available_moves(board):
            board[move] = CLetter
            score, _ = minimax(board, alpha, beta, CLetter, PLetter, False)
            board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for move in available_moves(board):
            board[move] = PLetter
            score, _ = minimax(board, alpha, beta, CLetter, PLetter, True)
            board[move] = ' '
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move

def computer_player(board, CLetter, PLetter):
    _, best_move = minimax(board, -float('inf'), float('inf'), CLetter, PLetter, True)
    return best_move

def play(x_player, o_player, print_game=True):
    board = [' ' for _ in range(9)]
    
    if print_game:
        print_board_nums()

    current_letter = 'X'  # X always goes first
    while empty_squares(board):
        if current_letter == 'X':
            square = x_player(board, 'X', 'O')
        else:
            square = o_player(board, 'O', 'X')

        move_success, winner = make_move(board, square, current_letter)
        if move_success:
            if print_game:
                print(current_letter + f' makes a move to square {square}')
                print_board(board)
                print('')

            if winner:
                if print_game:
                    print(current_letter + ' wins!')
                return current_letter

            current_letter = 'O' if current_letter == 'X' else 'X'  # Switch player

    if print_game:
        print('It\'s a tie!')
    return None

if __name__ == '__main__':
    # Human plays as 'O', Computer plays as 'X' (computer goes first)
    if random.randint(0, 1):
        play(computer_player, human_player) 
    # OR Human plays as 'X', Computer plays as 'O' (human goes first)
    else: play(human_player, computer_player)
