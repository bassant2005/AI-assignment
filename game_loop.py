from Assignment3 import *

def print_board_with_coords(board):
    """Print board with coordinate labels"""
    print("   " + " ".join([str(i).rjust(2) for i in range(BOARD_SIZE)]))
    for i, row in enumerate(board):
        print(f"{i:2} " + " ".join([piece.rjust(2) for piece in row]))
    print()

def get_human_move(board, player):
    """Get move input from human player"""
    print(f"\n{player}'s turn. Enter your move:")
    print("Format: from_row from_col to_row to_col (e.g., 0 5 1 5)")
    
    while True:
        try:
            move_input = input("Your move: ").strip().split()
            if len(move_input) != 4:
                print("Please enter 4 coordinates: from_row from_col to_row to_col")
                continue
                
            r1, c1, r2, c2 = map(int, move_input)
            
            if not is_valid_move(board, r1, c1, r2, c2, player):
                print("Invalid move! Try again.")
                continue
                
            return (r1, c1, r2, c2)
            
        except ValueError:
            print("Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\nGame aborted.")
            return None

def print_move(move, player):
    """Print a move in readable format"""
    if move:
        r1, c1, r2, c2 = move
        print(f"{player} moves: ({r1},{c1}) → ({r2},{c2})")

def game_loop():
    """Main game loop - text based"""
    print("=" * 60)
    print("HNEFATAFL - TEXT BASED GAME")
    print("=" * 60)
    
    # Game setup
    board = initial_state()
    current_player = ATTACKER  # Attackers move first
    
    # Game mode selection - Human vs Computer only
    print("\nSelect your side:")
    print("1. Play as Attackers (you move first)")
    print("2. Play as Defenders (AI moves first)")
    
    while True:
        try:
            side = int(input("Choose side (1-2): "))
            if side == 1:
                human_player = ATTACKER
                ai_player = DEFENDER
                break
            elif side == 2:
                human_player = DEFENDER
                ai_player = ATTACKER
                break
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter a number.")
    
    # AI difficulty selection
    print("\nSelect AI difficulty:")
    print("1. Easy")
    print("2. Medium") 
    print("3. Hard")
    
    while True:
        try:
            diff = int(input("Enter difficulty (1-3): "))
            if diff == 1:
                ai_difficulty = "easy"
                break
            elif diff == 2:
                ai_difficulty = "medium"
                break
            elif diff == 3:
                ai_difficulty = "hard"
                break
            else:
                print("Please enter 1-3.")
        except ValueError:
            print("Please enter a number.")
    
    print(f"\nStarting game - {ai_difficulty} difficulty")
    print_board_with_coords(board)
    
    # Main game loop
    turn_count = 0
    while True:
        turn_count += 1
        print(f"\n--- Turn {turn_count} ---")
        print(f"Current player: {current_player}")
        
        # Check for winner before move
        winner = is_winner(board)
        if winner:
            print(f"\n🎮 GAME OVER! {winner} wins!")
            print_board_with_coords(board)
            break
        
        # Get move - Human vs Computer only
        move = None
        
        if current_player == human_player:
            move = get_human_move(board, current_player)
        else:
            print(f"AI ({current_player}) is thinking...")
            move = get_ai_move(board, current_player, ai_difficulty)
        
        # Handle game abort or no moves
        if move is None:
            break
        if move == []:
            print(f"No valid moves for {current_player}!")
            break
        
        # Execute move
        print_move(move, current_player)
        board = apply_move(board, move)
        board = apply_capture(board, move[2], move[3], current_player)
        
        print("Board after move:")
        print_board_with_coords(board)
        
        # Switch player
        current_player = DEFENDER if current_player == ATTACKER else ATTACKER
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    game_loop()
