import numpy as np
import os
import platform

# CHECKERS CODE ITSELF IS GENERATED THROUGH DEEPSEEK, AI I IMPLEMENTED ON MY OWN

class CheckersGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 1  # Player 1 starts (1 for black, 2 for white)
        self.game_over = False
        self.winner = None
        self.first_print = True
        
    def clear_screen(self):
        """Clears the terminal screen."""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def initialize_board(self):
        # 0: empty, 1: black, 2: white, 3: black king, 4: white king
        board = np.zeros((8, 8), dtype=int)
        
        # Set up black pieces (top)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 1
        
        # Set up white pieces (bottom)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 2
        
        return board
    
    def print_board(self):
        if not self.first_print:
            self.clear_screen()
        self.first_print = False
        
        print("\n   " + " ".join([str(i) for i in range(8)]))
        for row in range(8):
            print(f"{row} ", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece == 0:
                    print(" .", end="")
                elif piece == 1:
                    print(" b", end="")
                elif piece == 2:
                    print(" w", end="")
                elif piece == 3:
                    print(" B", end="")
                elif piece == 4:
                    print(" W", end="")
            print()
        print()
    
    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_valid_moves(self, player):
        moves = []
        captures = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (player == 1 and piece in (1, 3)) or (player == 2 and piece in (2, 4)):
                    piece_moves, piece_captures = self.get_piece_moves(row, col)
                    moves.extend([(row, col, *move) for move in piece_moves])
                    captures.extend([(row, col, *capture) for capture in piece_captures])
        
        # If captures are available, only return captures (must take)
        if captures:
            return captures
        return moves
    
    def get_piece_moves(self, row, col):
        piece = self.board[row][col]
        moves = []
        captures = []
        
        if piece in (1, 3, 4):  # Black or any king can move down
            # Down left
            new_row, new_col = row + 1, col - 1
            if self.is_valid_position(new_row, new_col):
                if self.board[new_row][new_col] == 0:
                    if piece == 1 and new_row == 7:  # Promotion
                        moves.append((new_row, new_col, True))
                    else:
                        moves.append((new_row, new_col, False))
                elif (piece == 1 or piece == 3) and self.board[new_row][new_col] in (2, 4):
                    # Check if jump is possible
                    jump_row, jump_col = new_row + 1, new_col - 1
                    if self.is_valid_position(jump_row, jump_col) and self.board[jump_row][jump_col] == 0:
                        if jump_row == 7:  # Promotion after capture
                            captures.append((jump_row, jump_col, True))
                        else:
                            captures.append((jump_row, jump_col, False))
            
            # Down right
            new_row, new_col = row + 1, col + 1
            if self.is_valid_position(new_row, new_col):
                if self.board[new_row][new_col] == 0:
                    if piece == 1 and new_row == 7:  # Promotion
                        moves.append((new_row, new_col, True))
                    else:
                        moves.append((new_row, new_col, False))
                elif (piece == 1 or piece == 3) and self.board[new_row][new_col] in (2, 4):
                    # Check if jump is possible
                    jump_row, jump_col = new_row + 1, new_col + 1
                    if self.is_valid_position(jump_row, jump_col) and self.board[jump_row][jump_col] == 0:
                        if jump_row == 7:  # Promotion after capture
                            captures.append((jump_row, jump_col, True))
                        else:
                            captures.append((jump_row, jump_col, False))
        
        if piece in (2, 3, 4):  # White or any king can move up
            # Up left
            new_row, new_col = row - 1, col - 1
            if self.is_valid_position(new_row, new_col):
                if self.board[new_row][new_col] == 0:
                    if piece == 2 and new_row == 0:  # Promotion
                        moves.append((new_row, new_col, True))
                    else:
                        moves.append((new_row, new_col, False))
                elif (piece == 2 or piece == 4) and self.board[new_row][new_col] in (1, 3):
                    # Check if jump is possible
                    jump_row, jump_col = new_row - 1, new_col - 1
                    if self.is_valid_position(jump_row, jump_col) and self.board[jump_row][jump_col] == 0:
                        if jump_row == 0:  # Promotion after capture
                            captures.append((jump_row, jump_col, True))
                        else:
                            captures.append((jump_row, jump_col, False))
            
            # Up right
            new_row, new_col = row - 1, col + 1
            if self.is_valid_position(new_row, new_col):
                if self.board[new_row][new_col] == 0:
                    if piece == 2 and new_row == 0:  # Promotion
                        moves.append((new_row, new_col, True))
                    else:
                        moves.append((new_row, new_col, False))
                elif (piece == 2 or piece == 4) and self.board[new_row][new_col] in (1, 3):
                    # Check if jump is possible
                    jump_row, jump_col = new_row - 1, new_col + 1
                    if self.is_valid_position(jump_row, jump_col) and self.board[jump_row][jump_col] == 0:
                        if jump_row == 0:  # Promotion after capture
                            captures.append((jump_row, jump_col, True))
                        else:
                            captures.append((jump_row, jump_col, False))
        
        return moves, captures
    
    def make_move(self, start_row, start_col, end_row, end_col, promotion):
        # Move the piece
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0
        
        if promotion:
            if piece == 1:  # Black becomes black king
                self.board[end_row][end_col] = 3
            elif piece == 2:  # White becomes white king
                self.board[end_row][end_col] = 4
            else:
                self.board[end_row][end_col] = piece  # Kings stay kings
        else:
            self.board[end_row][end_col] = piece
        
        # Check if it was a capture
        if abs(start_row - end_row) == 2:
            captured_row = (start_row + end_row) // 2
            captured_col = (start_col + end_col) // 2
            self.board[captured_row][captured_col] = 0
            
            # Check for additional captures with the same piece
            _, additional_captures = self.get_piece_moves(end_row, end_col)
            if additional_captures:
                print("Additional capture possible with the same piece!")
                self.print_board()
                print(f"Player {self.current_player}, you must continue capturing!")
                print(f"Current piece position: ({end_row}, {end_col})")
                print("Available captures:")
                for i, (_, _, new_row, new_col, promo) in enumerate(additional_captures):
                    print(f"{i}: ({new_row}, {new_col})")
                
                while True:
                    try:
                        choice = int(input("Select capture (0, 1, etc.): "))
                        if 0 <= choice < len(additional_captures):
                            _, _, new_row, new_col, promo = additional_captures[choice]
                            self.make_move(end_row, end_col, new_row, new_col, promo)
                            break
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
                return  # Don't switch turns yet
        
        # Switch players
        self.switch_player()
        
        # Check if game is over
        self.check_game_over()
    
    def switch_player(self):
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
    
    def check_game_over(self):
        # Check if either player has no pieces left
        black_exists = False
        white_exists = False
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece in (1, 3):
                    black_exists = True
                elif piece in (2, 4):
                    white_exists = True
        
        if not black_exists:
            self.game_over = True
            self.winner = 2
        elif not white_exists:
            self.game_over = True
            self.winner = 1
        
        # Check if current player has no valid moves
        valid_moves = self.get_valid_moves(self.current_player)
        if not valid_moves:
            self.game_over = True
            self.winner = 3 - self.current_player

    def make_temp_move(self, move):
        """Executes a move without game state checks or prints, returns undo info"""
        start_row, start_col, end_row, end_col, promotion = move
        
        # Save undo information
        undo_info = {
            'moved_piece': self.board[start_row][start_col],
            'start_pos': (start_row, start_col),
            'end_pos': (end_row, end_col),
            'promotion': promotion,
            'captured_piece': None,
            'captured_pos': None,
            'previous_player': self.current_player
        }
        
        # Execute the move
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0
        self.board[end_row][end_col] = piece
        
        # Handle promotion
        if promotion:
            self.board[end_row][end_col] = 3 if piece == 1 else 4
        
        # Handle capture
        if abs(start_row - end_row) == 2:
            captured_row = (start_row + end_row) // 2
            captured_col = (start_col + end_col) // 2
            undo_info['captured_piece'] = self.board[captured_row][captured_col]
            undo_info['captured_pos'] = (captured_row, captured_col)
            self.board[captured_row][captured_col] = 0
        
        # Switch player (without game over check)
        self.current_player = 3 - self.current_player
        
        return undo_info

    def undo_temp_move(self, undo_info):
        """Reverses a temporary move"""
        # Restore moved piece
        start_row, start_col = undo_info['start_pos']
        end_row, end_col = undo_info['end_pos']
        self.board[start_row][start_col] = undo_info['moved_piece']
        self.board[end_row][end_col] = 0
        
        # Restore promotion
        if undo_info['promotion']:
            self.board[start_row][start_col] = 1 if undo_info['moved_piece'] == 3 else 2 if undo_info['moved_piece'] == 4 else undo_info['moved_piece']
        
        # Restore captured piece
        if undo_info['captured_pos']:
            cap_row, cap_col = undo_info['captured_pos']
            self.board[cap_row][cap_col] = undo_info['captured_piece']
        
        # Restore player
        self.current_player = undo_info['previous_player']

    def get_ordered_moves(self, player):
        moves = self.get_valid_moves(player)
        
        # Score each move heuristically
        scored_moves = []
        for move in moves:
            score = 0
            start_row, start_col, end_row, end_col, _ = move
            
            # Prioritize captures
            if abs(start_row - end_row) == 2:  # It's a capture
                score += 10
                
            # Prioritize promotions
            piece = self.board[start_row][start_col]
            if (piece == 1 and end_row == 7) or (piece == 2 and end_row == 0):
                score += 5
                
            scored_moves.append((score, move))
        
        # Sort descending (best moves first)
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        return [move for (score, move) in scored_moves]

    def evaluate(self):
        king_weight = 1.5
        score = 0
        
        black_pieces = np.count_nonzero(self.board == 1)
        white_pieces = np.count_nonzero(self.board == 2)
        black_kings = np.count_nonzero(self.board == 3)
        white_kings = np.count_nonzero(self.board == 4)

        total_pieces = black_pieces + black_kings if self.current_player == 1 else white_pieces + white_kings

        if total_pieces > 12:
            center_cols = [2, 3, 4, 5]
            active_rows = [1, 2, 3, 4, 5, 6]
            
            for row in active_rows:
                for col in center_cols:
                    piece = self.board[row][col]
                    if piece == 1:  # Black piece in center
                        score += 0.2 if col in {3,4} else 0.1
                    elif piece == 2:  # White piece in center
                        score -= 0.2 if col in {3,4} else 0.1
        elif 6 <= total_pieces < 12:
            pass 
            
        
        if self.current_player == 1:  # Black
            return score + (black_pieces - white_pieces) + (black_kings * king_weight) - (white_kings * king_weight)
        else:  # White
            return -score + (white_pieces - black_pieces) + (white_kings * king_weight) - (black_kings * king_weight)
    
    def minimax(self, alpha, beta, depth, maximizing_player=True):
        if depth == 0:
            return self.evaluate(round), None

        if maximizing_player:
            best_score = -float('inf')
            best_move = None
            for move in self.get_ordered_moves(self.current_player):
                undo_info = self.make_temp_move(move)
                score, _ = self.minimax(alpha, beta, depth-1, not maximizing_player)
                self.undo_temp_move(undo_info)
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
            for move in self.get_valid_moves(self.current_player):
                undo_info = self.make_temp_move(move)
                score, _ = self.minimax(alpha, beta, depth-1, round, not maximizing_player)
                self.undo_temp_move(undo_info)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move

    def computer_player(self):
        self.minimax(-float('inf'), float('inf'), 3, True)
    
    def play(self):
        print("Welcome to Checkers!")
        print("AI: Black (b)")
        print("You: White (w)")
        print("Kings are represented as B and W")
        
        while not self.game_over:
            self.print_board()
            round += 1
            if self.current_player == 1:  # AI's turn (Black)
                print("AI is thinking...")
                _, best_move = self.minimax(-float('inf'), float('inf'), 3, True)
                if best_move:
                    start_row, start_col, end_row, end_col, promotion = best_move
                    self.make_move(start_row, start_col, end_row, end_col, promotion)
                continue
            else:  # Human's turn (White)
                print("Your turn (White)")
                valid_moves = self.get_valid_moves(self.current_player)
                if not valid_moves:
                    print("No valid moves available!")
                    break
                
                print("Available moves:")
                for i, (start_row, start_col, end_row, end_col, _) in enumerate(valid_moves):
                    print(f"{i}: ({start_row}, {start_col}) -> ({end_row}, {end_col})")
            
                while True:
                    try:
                        choice = input("Enter move number or coordinates (e.g., 2 1 3 0): ")
                        
                        if choice.isdigit():
                            # Move by index
                            choice = int(choice)
                            if 0 <= choice < len(valid_moves):
                                start_row, start_col, end_row, end_col, promotion = valid_moves[choice]
                                break
                            else:
                                print("Invalid move number. Try again.")
                        else:
                            # Move by coordinates
                            coords = list(map(int, choice.split()))
                            if len(coords) == 4:
                                start_row, start_col, end_row, end_col = coords
                                # Find if this matches any valid move
                                for move in valid_moves:
                                    if (move[0] == start_row and move[1] == start_col and 
                                        move[2] == end_row and move[3] == end_col):
                                        _, _, _, _, promotion = move
                                        break
                                else:
                                    print("Invalid coordinates. Try again.")
                                    continue
                                break
                            else:
                                print("Please enter 4 numbers separated by spaces.")
                    except ValueError:
                        print("Please enter valid numbers.")
                
                self.make_move(start_row, start_col, end_row, end_col, promotion)
        
        self.print_board()
        if self.winner:
            print(f"Game over! Player {self.winner} ({'Black' if self.winner == 1 else 'White'}) wins!")
        else:
            print("Game over! It's a draw.")

    def test_forced_capture(self):
        """AI must take available captures"""
        # Setup: AI (Black) can capture white piece
        self.board = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],  # Black piece at (2,3)
            [0, 0, 2, 0, 0, 0, 0, 0],  # White piece at (3,2)
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.current_player = 1  # Black's turn
        _, move = self.minimax(-float('inf'), float('inf'), 3, True)
        assert abs(move[0] - move[2]) == 2, "AI should perform capture (move 2 squares)"
        print("✓ Passed forced capture test")
    
    def test_promotion_priority(self):
        """AI should prioritize king promotions"""
        self.board = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],  # Black piece at (6,2)
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.current_player = 1
        _, move = self.minimax(-float('inf'), float('inf'), 3, True)
        assert move[2] == 7, "AI should move to promotion row"
        print("✓ Passed promotion priority test")

    def test_multi_capture(self):
        """AI should find capture sequences"""
        self.board = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],  # Black
            [0, 0, 2, 0, 2, 0, 0, 0],  # Two white pieces
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.current_player = 1
        _, move = self.minimax(-float('inf'), float('inf'), 3, True)
        # Should capture first white piece at (3,2)
        assert move == (2,3,4,1,False) or move == (2,3,4,5,False), "AI should initiate multi-capture"
        print("✓ Passed multi-capture test")

    def test_defensive_play(self):
        """AI should protect vulnerable pieces"""
        self.board = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],  # Black piece
            [0, 0, 2, 0, 0, 0, 0, 0],  # White threatening
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],  # Black defender
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.current_player = 1
        original_pos = (2,3)
        _, move = self.minimax(-float('inf'), float('inf'), 3, True)
        assert move[0:2] != original_pos, "AI should move threatened piece"
        print("✓ Passed defensive play test")

    def test_endgame(self):
        """AI should convert winning endgames"""
        self.board = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 0],  # Black king
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0],  # Lone white piece
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.current_player = 1
        _, move = self.minimax(-float('inf'), float('inf'), 5, True)  # Deeper search for endgame
        assert abs(move[0] - move[2]) == 2, "King should capture lone opponent"
        print("✓ Passed endgame test")
    
    def run_all_tests(self):
        self.test_forced_capture()
        self.test_promotion_priority()
        self.test_multi_capture()
        self.test_defensive_play()
        self.test_endgame()
        print("All fundamental tests completed!")
if __name__ == "__main__":
    game = CheckersGame()
    # game.play()
    game.run_all_tests()