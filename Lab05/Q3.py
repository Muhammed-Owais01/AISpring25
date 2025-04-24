import random
import numpy as np
from os import system

class BattleshipGame:
    def __init__(self):
        self.board_size = 10
        self.ships = {
            'Carrier': 5,
            'Battleship': 4,
            'Cruiser': 3,
            'Submarine': 3,
            'Destroyer': 2
        }
        self.player_board = self.create_board()
        self.ai_board = self.create_board()
        self.player_target = self.create_board()
        self.ai_target = self.create_board()
        self.ai_probability = np.zeros((self.board_size, self.board_size))
        self.ai_hits = []
        self.setup_game()

    def create_board(self):
        return [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def print_board(self, board, hide_ships=False):
        print("   " + " ".join([chr(65+i) for i in range(self.board_size)]))
        for i in range(self.board_size):
            print(f"{i+1:2} " + " ".join([cell if not hide_ships or cell not in ['C','B','S','D'] else ' ' for cell in board[i]]))

    def place_ship(self, board, ship, size):
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, self.board_size-1)
                col = random.randint(0, self.board_size-size)
                if all(board[row][col+i] == ' ' for i in range(size)):
                    for i in range(size):
                        board[row][col+i] = ship[0]
                    break
            else:
                row = random.randint(0, self.board_size-size)
                col = random.randint(0, self.board_size-1)
                if all(board[row+i][col] == ' ' for i in range(size)):
                    for i in range(size):
                        board[row+i][col] = ship[0]
                    break

    def setup_game(self):
        # Place player ships
        for ship, size in self.ships.items():
            self.place_ship(self.player_board, ship, size)
        
        # Place AI ships
        for ship, size in self.ships.items():
            self.place_ship(self.ai_board, ship, size)
        
        # Initialize AI probability
        self.update_ai_probability()

    def update_ai_probability(self):
        self.ai_probability = np.zeros((self.board_size, self.board_size))
        
        # If we have hits, focus on adjacent squares
        if self.ai_hits:
            for (row, col) in self.ai_hits:
                for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                    r, c = row + dr, col + dc
                    if 0 <= r < self.board_size and 0 <= c < self.board_size:
                        if self.player_target[r][c] == ' ':
                            self.ai_probability[r][c] += 10
        
        # Otherwise use probability density
        else:
            for ship_size in self.ships.values():
                for row in range(self.board_size):
                    for col in range(self.board_size):
                        # Check horizontal placement
                        if col + ship_size <= self.board_size:
                            if all(self.player_target[row][col+i] == ' ' for i in range(ship_size)):
                                for i in range(ship_size):
                                    self.ai_probability[row][col+i] += 1
                        # Check vertical placement
                        if row + ship_size <= self.board_size:
                            if all(self.player_target[row+i][col] == ' ' for i in range(ship_size)):
                                for i in range(ship_size):
                                    self.ai_probability[row+i][col] += 1

    def player_attack(self):
        while True:
            try:
                coord = input("Enter attack coordinates (e.g., B4): ").upper()
                col = ord(coord[0]) - ord('A')
                row = int(coord[1:]) - 1
                
                if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                    raise ValueError
                
                if self.ai_board[row][col] in ['X', 'O']:
                    print("You already attacked there!")
                    continue
                    
                if self.ai_board[row][col] != ' ':
                    ship_char = self.ai_board[row][col]
                    self.ai_board[row][col] = 'X'
                    self.player_target[row][col] = 'X'
                    print(f"Player attacks: {coord} → Hit!")
                    
                    # Check if ship is sunk
                    ship_sunk = True
                    for r in range(self.board_size):
                        for c in range(self.board_size):
                            if self.ai_board[r][c] == ship_char:
                                ship_sunk = False
                                break
                    
                    if ship_sunk:
                        print(f"You sunk the {self.get_ship_name(ship_char)}!")
                    return True
                else:
                    self.ai_board[row][col] = 'O'
                    self.player_target[row][col] = 'O'
                    print(f"Player attacks: {coord} → Miss")
                    return False
            except (ValueError, IndexError):
                print("Invalid input. Please enter coordinates like 'B4'")

    def get_ship_name(self, char):
        for name in self.ships:
            if name[0] == char:
                return name
        return "Unknown"

    def ai_attack(self):
        # Find highest probability cell
        max_prob = np.max(self.ai_probability)
        candidates = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.player_target[row][col] == ' ' and self.ai_probability[row][col] == max_prob:
                    candidates.append((row, col))
        
        row, col = random.choice(candidates)
        coord = f"{chr(65+col)}{row+1}"
        
        if self.player_board[row][col] != ' ':
            ship_char = self.player_board[row][col]
            self.player_board[row][col] = 'X'
            self.ai_target[row][col] = 'X'
            self.ai_hits.append((row, col))
            print(f"AI attacks: {coord} → Hit!")
            
            # Check if ship is sunk
            ship_sunk = True
            for r in range(self.board_size):
                for c in range(self.board_size):
                    if self.player_board[r][c] == ship_char:
                        ship_sunk = False
                        break
            
            if ship_sunk:
                print(f"AI sunk your {self.get_ship_name(ship_char)}!")
                # Remove hits from this ship
                self.ai_hits = [hit for hit in self.ai_hits if self.player_board[hit[0]][hit[1]] != 'X']
        else:
            self.player_board[row][col] = 'O'
            self.ai_target[row][col] = 'O'
            print(f"AI attacks: {coord} → Miss")
        
        self.update_ai_probability()

    def check_win(self, board):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] not in [' ', 'X', 'O']:
                    return False
        return True

    def play(self):
        print("Welcome to Battleship!")
        print("Your ships have been placed randomly.")
        
        while True:
            system('cls')
            print("\nYour Target Board:")
            self.print_board(self.player_target)
            print("\nYour Ships:")
            self.print_board(self.player_board, hide_ships=True)
            
            # Player's turn
            hit = self.player_attack()
            if self.check_win(self.ai_board):
                print("Congratulations! You sunk all enemy ships!")
                break
            
            if not hit:
                # AI's turn
                self.ai_attack()
                if self.check_win(self.player_board):
                    print("Game over! The AI sunk all your ships!")
                    break
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    game = BattleshipGame()
    game.play()