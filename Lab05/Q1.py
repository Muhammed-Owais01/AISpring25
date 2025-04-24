import sys
from os import system
import random

# Constants
BOARD_SIZE = 8
WHITE = 'W'
BLACK = 'B'
WHITE_KING = 'WK'
BLACK_KING = 'BK'
EMPTY = ' '
DIRECTIONS = {
    WHITE: [(-1, -1), (-1, 1)],
    BLACK: [(1, -1), (1, 1)],
    WHITE_KING: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    BLACK_KING: [(-1, -1), (-1, 1), (1, -1), (1, 1)]
}

def print_board(board):
    system('cls')
    print("   " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i in range(BOARD_SIZE):
        print(f"{i} |" + "|".join(board[i][j].center(3) for j in range(BOARD_SIZE)) + "|")

def initialize_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # Place white pieces
    for i in range(3):
        for j in range(BOARD_SIZE):
            if (i + j) % 2 == 1:
                board[i][j] = WHITE
    # Place black pieces
    for i in range(5, 8):
        for j in range(BOARD_SIZE):
            if (i + j) % 2 == 1:
                board[i][j] = BLACK
    return board

def get_valid_moves(board, player):
    moves = []
    captures = []
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            piece = board[i][j]
            if piece.startswith(player):
                # Check normal moves
                for di, dj in DIRECTIONS[piece]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
                        if board[ni][nj] == EMPTY:
                            moves.append(((i, j), (ni, nj)))
                
                # Check captures
                for di, dj in DIRECTIONS[piece]:
                    ni, nj = i + di, j + dj
                    nni, nnj = i + 2*di, j + 2*dj
                    if (0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and 
                        0 <= nni < BOARD_SIZE and 0 <= nnj < BOARD_SIZE):
                        opponent = BLACK if player == WHITE else WHITE
                        if (board[ni][nj].startswith(opponent) and 
                            board[nni][nnj] == EMPTY):
                            captures.append(((i, j), (nni, nnj)))
    
    return captures if captures else moves

def make_move(board, start, end, player):
    i, j = start
    ni, nj = end
    piece = board[i][j]
    board[i][j] = EMPTY
    
    # Check if it's a capture
    if abs(ni - i) == 2:
        captured_i = (i + ni) // 2
        captured_j = (j + nj) // 2
        board[captured_i][captured_j] = EMPTY
    
    # Check for promotion to king
    if (player == WHITE and ni == BOARD_SIZE-1) or (player == BLACK and ni == 0):
        piece = WHITE_KING if player == WHITE else BLACK_KING
    
    board[ni][nj] = piece
    return board

def evaluate_board(board, player):
    score = 0
    
    # Piece count evaluation
    white_pieces = 0
    black_pieces = 0
    white_kings = 0
    black_kings = 0
    
    for row in board:
        for piece in row:
            if piece == WHITE:
                white_pieces += 1
            elif piece == BLACK:
                black_pieces += 1
            elif piece == WHITE_KING:
                white_kings += 1
            elif piece == BLACK_KING:
                black_kings += 1
    
    # Material advantage
    if player == WHITE:
        score = (white_pieces + 2*white_kings) - (black_pieces + 2*black_kings)
    else:
        score = (black_pieces + 2*black_kings) - (white_pieces + 2*white_kings)
    
    # Positional advantage (center control)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            piece = board[i][j]
            if piece.startswith(player):
                # Bonus for being in the center
                if 2 <= i <= 5 and 2 <= j <= 5:
                    score += 0.5
                # Bonus for kings
                if piece.endswith('K'):
                    score += 1
    
    return score

def minimax(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0:
        return evaluate_board(board, player), None
    
    valid_moves = get_valid_moves(board, player if maximizing_player else (BLACK if player == WHITE else WHITE))
    
    if not valid_moves:
        # No valid moves means loss
        return (-100 if maximizing_player else 100), None
    
    best_move = None
    
    if maximizing_player:
        max_eval = -float('inf')
        for move in valid_moves:
            new_board = [row[:] for row in board]
            make_move(new_board, move[0], move[1], player)
            eval, _ = minimax(new_board, depth-1, alpha, beta, False, player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_board = [row[:] for row in board]
            make_move(new_board, move[0], move[1], BLACK if player == WHITE else WHITE)
            eval, _ = minimax(new_board, depth-1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def ai_move(board, player, depth=3):
    _, best_move = minimax(board, depth, -float('inf'), float('inf'), True, player)
    return best_move

def human_move(board, player):
    while True:
        try:
            print(f"Your pieces: {WHITE if player == WHITE else BLACK}")
            start = input("Enter start position (row,col): ").split(',')
            end = input("Enter end position (row,col): ").split(',')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            
            valid_moves = get_valid_moves(board, player)
            if (start, end) in valid_moves:
                return start, end
            else:
                print("Invalid move. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Format: row,col (e.g., 2,3)")

def is_game_over(board, player):
    opponent = BLACK if player == WHITE else WHITE
    return (not get_valid_moves(board, player) or 
            not any(piece.startswith(opponent) for row in board for piece in row))

def play_checkers():
    board = initialize_board()
    current_player = WHITE  # Human starts first
    
    while True:
        print_board(board)
        
        if is_game_over(board, current_player):
            opponent = BLACK if current_player == WHITE else WHITE
            print(f"{opponent} wins!")
            break
        
        if current_player == WHITE:
            print("Your turn (White)")
            start, end = human_move(board, current_player)
            print(f"Player moves: {start} → {end}")
        else:
            print("AI's turn (Black)")
            start, end = ai_move(board, current_player)
            print(f"AI moves: {start} → {end}")
        
        make_move(board, start, end, current_player)
        
        # Check for additional captures
        while abs(end[0] - start[0]) == 2 and get_valid_moves(board, current_player):
            print_board(board)
            if current_player == WHITE:
                print("Additional capture available!")
                start, end = human_move(board, current_player)
                print(f"Player moves: {start} → {end}")
            else:
                start, end = ai_move(board, current_player)
                print(f"AI moves: {start} → {end}")
            make_move(board, start, end, current_player)
        
        current_player = BLACK if current_player == WHITE else WHITE

if __name__ == '__main__':
    play_checkers()