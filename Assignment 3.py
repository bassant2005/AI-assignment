"""
PROJECT OVERVIEW:
-----------------
This project implements a simplified version of the ancient
board game "Hnefatafl" (Viking Chess).

The final system is intended to support:
- Human vs Human gameplay
- Human vs AI gameplay

GAME RULES SUMMARY:
- Board size: 11x11 grid
- One King placed in the center (Throne)
- 12 Defenders protect the King
- 24 Attackers try to capture the King
- Pieces move like a Rook (horizontal/vertical sliding)
- No jumping over pieces

Winning conditions:
- Defenders win if King reaches any corner
- Attackers win if King is captured or fully blocked
"""

############################################################
"""
These constants define the entire game environment.
"""

EMPTY = '.'
KING = 'K'
DEFENDER = 'D'
ATTACKER = 'A'
BOARD_SIZE = 11
CORNERS = [(0,0), (0,10), (10,0), (10,10)]

############################################################
"""
Initializes the full 11x11 game board.
"""
def initial_state():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    center = BOARD_SIZE // 2

    # The King starts at the exact center of the board (Throne)
    board[center][center] = KING

    # Defenders are placed in a cross + diagonal formation
    # around the King to protect it from attackers.
    # This creates a symmetric defensive structure.
    defenders = [
        (center-1, center),
        (center+1, center),
        (center, center-1),
        (center, center+1),

        (center-2, center),
        (center+2, center),
        (center, center-2),
        (center, center+2),

        (center-1, center-1),
        (center-1, center+1),
        (center+1, center-1),
        (center+1, center+1),
    ]

    for r, c in defenders:
        board[r][c] = DEFENDER

    # Attackers are placed in a structured "arm formation"
    # around all four edges of the board.
    # This creates pressure from all directions toward the center.

    # TOP ARM
    for c in range(3, 8):
        board[0][c] = ATTACKER
    board[1][5] = ATTACKER

    # BOTTOM ARM
    for c in range(3, 8):
        board[10][c] = ATTACKER
    board[9][5] = ATTACKER

    # LEFT ARM
    for r in range(3, 8):
        board[r][0] = ATTACKER
    board[5][1] = ATTACKER

    # RIGHT ARM
    for r in range(3, 8):
        board[r][10] = ATTACKER
    board[5][9] = ATTACKER

    return board

############################################################
"""
Checks whether a given position is inside the board.
This function ensures we never access invalid grid indexes.
"""
def within_bounds(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

############################################################
"""
Generates all possible legal moves for a player.

MOVEMENT RULES:
- rook-like movement (horizontal / vertical only)
- can move multiple empty cells
- cannot jump over pieces
"""
def get_all_moves(board, player):
    moves = []

    # 4 directions: down, up, right, left
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            # skip cells that do NOT belong to current player
            if board[r][c] != player:
                continue

            # try moving in all 4 directions
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # keep moving while:
                # - inside board
                # - cell is empty (no blocking piece)
                while within_bounds(nr, nc) and board[nr][nc] == EMPTY:

                    # add move: (start_row, start_col, end_row, end_col)
                    moves.append((r, c, nr, nc))

                    # continue sliding further in same direction
                    nr += dr
                    nc += dc

    return moves

############################################################
"""
Checks if a move is legal according to basic rules.
"""
def is_valid_move(board, r1, c1, r2, c2):
    # 1. check if destination is inside board boundaries
    if not within_bounds(r2, c2):
        return False

    # 2. ensure movement is straight line only
    if r1 != r2 and c1 != c2:
        return False

    # 3. destination must be empty (no overlapping pieces)
    if board[r2][c2] != EMPTY:
        return False

    return True

############################################################
"""
Applies a move and returns a NEW board state.

IMPORTANT DESIGN IDEA:
- we DO NOT modify original board
- we create a copy (important for AI search like alpha-beta)
"""
def apply_move(board, move):
    r1, c1, r2, c2 = move

    # deep copy of board (row by row copy)
    new_board = [row[:] for row in board]

    # move piece from source to destination
    new_board[r2][c2] = new_board[r1][c1]

    # clear old position
    new_board[r1][c1] = EMPTY

    return new_board

############################################################
"""
Prints board in readable
"""
def print_board(board):
    for row in board:
        print(" ".join(row))

    print("\n")

############################################################
"""
Search for where is the king now 
"""
def find_king(board):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == KING:
                return r,c
    return None

############################################################
def is_corner(r,c):
    return (r,c) in CORNERS

############################################################
"""
This function checks if the game has ended and determines which side has won.
"""
def is_winner(board):
    king_pos = find_king(board)

    # If king is gone → attackers win
    if not king_pos:
        return "ATTACKER"

    kr, kc = king_pos

    # 1. KING REACHES CORNER → DEFENDER WINS
    if is_corner(kr, kc):
        return "DEFENDER"

    # 2. CHECK KING CAPTURE CONDITIONS
    surrounded = 0

    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = kr + dr, kc + dc

        # Wall counts as blocked
        if not within_bounds(nr, nc):
            surrounded += 1

        # Attacker blocks the king
        elif board[nr][nc] == ATTACKER:
            surrounded += 1

    # CASE 1: Fully surrounded (middle board)
    if surrounded == 4:
        return "ATTACKER"

    # CASE 2: King on edge (wall reduces escape sides)
    if (kr == 0 or kr == BOARD_SIZE-1 or kc == 0 or kc == BOARD_SIZE-1):
        if surrounded >= 3:
            return "ATTACKER"

    # CASE 3: King in corner-adjacent situation (more strict rule)
    if is_corner(kr, kc):
        if surrounded >= 2:
            return "ATTACKER"

    return None

############################################################
"""
A piece is captured if it is trapped between TWO enemy pieces
in a straight line (horizontal or vertical).

Example:
    A - D - A   → Defender captured
    D - A - D   → Attacker captured
"""
def apply_capture(board, r2, c2, current_player):
    new_board = [row[:] for row in board]

    # Identify who the 'enemy' is based on who just moved
    if current_player == ATTACKER:
        enemies = [DEFENDER, KING]
        friendlies = [ATTACKER]
    else:
        # Note: King is 'unarmed' per rules, but Defenders can use the King
        # as an anchor to capture an Attacker.
        enemies = [ATTACKER]
        friendlies = [DEFENDER, KING]

    center = BOARD_SIZE // 2
    throne = (center, center)

    # Check all 4 cardinal directions around the piece that just landed
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        enemy_r, enemy_c = r2 + dr, c2 + dc
        anchor_r, anchor_c = r2 + (dr * 2), c2 + (dc * 2)

        # 1. Ensure the 'enemy' and the 'anchor' positions are on the board
        if within_bounds(enemy_r, enemy_c) and within_bounds(anchor_r, anchor_c):
            target_piece = new_board[enemy_r][enemy_c]
            anchor_piece = new_board[anchor_r][anchor_c]

            # 2. Check if the adjacent piece is actually an enemy
            if target_piece in enemies:

                # Per rules: The King is captured differently (surrounded on 4 sides),
                # so we skip him here and let is_winner handle his capture.
                if target_piece == KING:
                    continue

                # 3. Check for valid 'Anchor' (Sandwich side)
                # An anchor can be a friendly piece, a corner, or the empty throne
                is_friendly_anchor = anchor_piece in friendlies
                is_corner_anchor = is_corner(anchor_r, anchor_c)
                is_throne_anchor = (anchor_r, anchor_c) == throne and anchor_piece == EMPTY

                if is_friendly_anchor or is_corner_anchor or is_throne_anchor:
                    new_board[enemy_r][enemy_c] = EMPTY

    return new_board



############################################################
"""
================================================================================
MEMBER 1: THE RULE MASTER (Logic, Evaluation & Rules)
================================================================================
1. PATH VALIDATION (`is_valid_move`):
   - Implement the "No Jumping" rule. Use a loop to check all squares between 
     (r1, c1) and (r2, c2). Return False if any square is not EMPTY.

2. UTILITY FUNCTION (`evaluate_board`):
   - Create a scoring system for Alpha-Beta:
     - Material: +10 per Defender, -10 per Attacker.
     - King Safety: +500 for King on Corner, -50 per adjacent Attacker.
     - King Mobility: +5 per available move for the King.

3. WIN CONDITION REFINEMENT (`is_winner`):
   - Update King capture logic: 4 attackers needed in the center, 3 on the edge, 
     and 2 if the King is against a corner.

================================================================================
MEMBER 2: THE STRATEGIST (AI Engine & Alpha-Beta)
================================================================================
1. CORE ENGINE (`alpha_beta`):
   - Implement the recursive Alpha-Beta function.
   - Must return a tuple of (best_score, best_move).

2. MOVE SIMULATION:
   - Ensure the AI uses `apply_move` (which creates board copies) to test future 
     scenarios without corrupting the live game state.

3. DIFFICULTY CONTROLLER:
   - Create a function to handle search depth based on user selection:
     - Easy (Depth 1), Medium (Depth 3), Hard (Depth 5).

================================================================================
MEMBER 3: THE ARCHITECT (GUI & Game Controller)
================================================================================
1. PYGAME VISUALS:
   - Build the 11x11 grid. Color the Throne (center) and 4 Corners differently.
   - Load/Draw pieces: Use gold for King, white for Defenders, black for Attackers.

2. TURN MANAGEMENT:
   - Create the loop that handles "Human (A) -> AI (D)" or "AI (A) -> Human (D)".
   - Note: Per rules, Attackers MUST move first.

3. EVENT HANDLING:
   - Map mouse clicks to board coordinates.
   - Trigger Member 1's `apply_capture` after every move and check for `is_winner`.
================================================================================
"""
############################################################