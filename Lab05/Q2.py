def evaluate(cards):
    """Simple evaluation function - returns the difference in scores"""
    return sum(cards)  # Not used directly, but helps understand the game state

def alpha_beta(cards, depth, alpha, beta, is_max_turn):
    if not cards:
        return 0, None
    
    if is_max_turn:
        max_eval = -float('inf')
        best_move = None
        
        # Try left card
        left_eval, _ = alpha_beta(cards[1:], depth+1, alpha, beta, False)
        left_eval += cards[0]
        if left_eval > max_eval:
            max_eval = left_eval
            best_move = 'left'
        alpha = max(alpha, max_eval)
        if beta <= alpha:
            return max_eval, best_move
        
        # Try right card
        right_eval, _ = alpha_beta(cards[:-1], depth+1, alpha, beta, False)
        right_eval += cards[-1]
        if right_eval > max_eval:
            max_eval = right_eval
            best_move = 'right'
        
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        
        # Min always picks the minimum value card
        if cards[0] < cards[-1]:
            min_eval, _ = alpha_beta(cards[1:], depth+1, alpha, beta, True)
            best_move = 'left'
        else:
            min_eval, _ = alpha_beta(cards[:-1], depth+1, alpha, beta, True)
            best_move = 'right'
        
        return min_eval, best_move

def play_game(cards):
    max_score = 0
    min_score = 0
    current_player = "Max"
    
    print(f"Initial Cards: {cards}")
    
    while cards:
        if current_player == "Max":
            # Max's turn - use alpha-beta pruning
            _, move = alpha_beta(cards, 0, -float('inf'), float('inf'), True)
            if move == 'left':
                picked = cards.pop(0)
            else:
                picked = cards.pop()
            max_score += picked
            print(f"Max picks {picked}, Remaining Cards: {cards}")
            current_player = "Min"
        else:
            # Min's turn - always pick minimum
            if cards[0] < cards[-1]:
                picked = cards.pop(0)
            else:
                picked = cards.pop()
            min_score += picked
            print(f"Min picks {picked}, Remaining Cards: {cards}")
            current_player = "Max"
    
    print(f"\nFinal Scores - Max: {max_score}, Min: {min_score}")
    if max_score > min_score:
        print("Winner: Max")
    elif min_score > max_score:
        print("Winner: Min")
    else:
        print("It's a tie!")

# Sample game
cards = [4, 10, 6, 2, 9, 5]
play_game(cards)