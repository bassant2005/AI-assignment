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
THRONE = (BOARD_SIZE // 2, BOARD_SIZE // 2)

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
Helper: returns True if the piece belongs to the given player.
Defenders 'own' both DEFENDER pieces AND the KING.
This is used everywhere we need to check piece ownership.
"""
def belongs_to(piece, player):
    if player == ATTACKER:
        return piece == ATTACKER
    return piece in (DEFENDER, KING)   # DEFENDER side owns the King too

############################################################
"""
Helper: returns True if (r, c) is the central Throne square.
Used by is_valid_move (restricted landing) and apply_capture (anchor rule).
"""
def is_throne(r, c):
    return (r, c) == THRONE

############################################################
"""
Generates all possible legal moves for a player.

MOVEMENT RULES:
- rook-like movement (horizontal / vertical only)
- can move multiple empty cells
- cannot jump over pieces

FIXED by Person 1:
- uses belongs_to() so the King is included for the DEFENDER player
- calls is_valid_move() (with player) to respect all refined rules
"""
def get_all_moves(board, player):
    moves = []

    # 4 directions: down, up, right, left
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            # skip cells that do NOT belong to current player
            if not belongs_to(board[r][c], player):   # ← FIXED: King included for DEFENDER
                continue

            # try moving in all 4 directions
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # keep moving while inside board and cell is empty
                while within_bounds(nr, nc) and board[nr][nc] == EMPTY:

                    # validate before adding (catches throne/corner restriction)
                    if is_valid_move(board, r, c, nr, nc, player):
                        moves.append((r, c, nr, nc))

                    # Non-king pieces cannot pass through restricted squares
                    if board[r][c] != KING and (is_throne(nr, nc) or is_corner(nr, nc)):
                        break

                    # continue sliding further in same direction
                    nr += dr
                    nc += dc

    return moves

############################################################
"""
Returns all legal destination squares (r2, c2) for the piece at (r, c).
Used by the GUI to highlight valid moves when a piece is selected.
Returns a list of (row, col) tuples, or [] if wrong player.
"""
def get_piece_moves(board, r, c, player):
    piece = board[r][c]
    if not belongs_to(piece, player):
        return []   # wrong player clicked this piece

    destinations = []
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        while within_bounds(nr, nc) and board[nr][nc] == EMPTY:
            if is_valid_move(board, r, c, nr, nc, player):
                destinations.append((nr, nc))
            # Non-king pieces stop sliding at restricted squares
            if piece != KING and (is_throne(nr, nc) or is_corner(nr, nc)):
                break
            nr += dr
            nc += dc
    return destinations

############################################################
"""
Checks if a move is legal according to basic rules.

REFINED by Person 1:
  - Added current_player parameter: piece must belong to the current player.
  - Only the KING may land on the Throne or a Corner square.
"""
def is_valid_move(board, r1, c1, r2, c2, current_player):

    # correct player must own the piece
    piece = board[r1][c1]
    if not belongs_to(piece, current_player):
        return False

    # 1. check if destination is inside board boundaries
    if not within_bounds(r2, c2):
        return False

    # 2. ensure movement is straight line only
    if r1 != r2 and c1 != c2:
        return False

    # 3. destination must be empty (no overlapping pieces)
    if board[r2][c2] != EMPTY:
        return False

    # 4. NO JUMPING: check every square between source and destination
    #    Determine step direction (+1 or -1) for row and column
    dr = 0 if r1 == r2 else (1 if r2 > r1 else -1)
    dc = 0 if c1 == c2 else (1 if c2 > c1 else -1)

    nr, nc = r1 + dr, c1 + dc
    while (nr, nc) != (r2, c2):
        if board[nr][nc] != EMPTY:
            return False  # piece is blocking the path
        nr += dr
        nc += dc

    # only the King may stop on the Throne or a Corner
    if piece != KING:
        if is_throne(r2, c2) or is_corner(r2, c2):
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

REFINED by Person 3:
  - Added Case 4: King adjacent (1 step) to a corner only needs
    2 attacker-sides blocked (2 walls already box it in).
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

    # A corner square adjacent to the King acts as an extra blocker
    for cr, cc in CORNERS:
        if abs(kr - cr) + abs(kc - cc) == 1:
            surrounded += 1
            break  # at most one corner can be adjacent at a time

    # Single unified check — walls + adjacent corner + attackers all count
    if surrounded >= 4:
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

    if current_player == ATTACKER:
        enemies   = [DEFENDER, KING]
        friendlies = [ATTACKER]
    else:
        enemies   = [ATTACKER]
        friendlies = [DEFENDER]

    throne = THRONE
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    for dr, dc in directions:
        enemy_r, enemy_c   = r2 + dr,     c2 + dc
        anchor_r, anchor_c = r2 + dr*2,   c2 + dc*2

        if not within_bounds(enemy_r, enemy_c):
            continue

        target_piece = new_board[enemy_r][enemy_c]
        if target_piece not in enemies or target_piece == KING:
            continue

        # anchor = friendly piece, corner, empty throne, OR a wall
        if not within_bounds(anchor_r, anchor_c):
            is_wall_anchor     = True
            is_friendly_anchor = False
            is_corner_anchor   = False
            is_throne_anchor   = False
        else:
            anchor_piece       = new_board[anchor_r][anchor_c]
            is_wall_anchor     = False
            is_friendly_anchor = anchor_piece in friendlies
            is_corner_anchor   = is_corner(anchor_r, anchor_c)
            is_throne_anchor   = (anchor_r, anchor_c) == throne and anchor_piece == EMPTY

        if is_wall_anchor or is_friendly_anchor or is_corner_anchor or is_throne_anchor:
            new_board[enemy_r][enemy_c] = EMPTY

    return new_board

############################################################
"""
    Utility / heuristic function for Alpha-Beta search.
    Returns a score from the DEFENDER's perspective:
      positive  → good for Defender
      negative  → good for Attacker

    Scoring breakdown:
      Material     : +10 per Defender alive,   -10 per Attacker alive
      King Safety  : +500 if King is on corner (defenders win)
                     -50  for each Attacker adjacent to the King
      King Mobility: +5   for each legal move the King can make
      Corner Prox  : +30 / +10 bonus if King is close to a corner  ← ADDED
      Cohesion     : +3  per Defender within 3 steps of the King    ← ADDED
    """
def evaluate_board(board):
    score = 0
    king_pos = find_king(board)

    # If King is gone → Attacker has won → very bad for Defender
    if king_pos is None:
        return -9999

    kr, kc = king_pos

    # ── MATERIAL ──
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == DEFENDER:
                score += 10
            elif board[r][c] == ATTACKER:
                score -= 10

    # ── KING SAFETY ──
    # Big bonus if King has already reached a corner
    if is_corner(kr, kc):
        return 9999   # return immediately (terminal win state)

    # Penalty for each Attacker directly adjacent to the King
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = kr + dr, kc + dc
        if within_bounds(nr, nc) and board[nr][nc] == ATTACKER:
            score -= 50

    # ── KING MOBILITY ──
    # Count how many squares the King can legally slide to
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = kr + dr, kc + dc
        while within_bounds(nr, nc) and board[nr][nc] == EMPTY:
            score += 5
            nr += dr
            nc += dc

    # ── ADDED: CORNER PROXIMITY ──
    # Reward Defender when King is close to an escape corner
    min_corner_dist = min(abs(kr - cr) + abs(kc - cc) for cr, cc in CORNERS)
    if min_corner_dist <= 2:
        score += 30
    elif min_corner_dist <= 4:
        score += 10

    # ── ADDED: DEFENDER COHESION ──
    # Small bonus for keeping Defenders near the King (protective formation)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == DEFENDER:
                dist = abs(r - kr) + abs(c - kc)
                if dist <= 3:
                    score += 3

    return score

############################################################
"""
Alpha-Beta Pruning Algorithm
Returns: (best_score, best_move)
- best_score: evaluation score from current player's perspective
- best_move: tuple (r1, c1, r2, c2) representing the best move
"""
def alpha_beta(board, depth, alpha, beta, maximizing_player, current_player):
    # Check for terminal states or depth limit
    winner = is_winner(board)
    if winner is not None or depth == 0:
        return evaluate_board(board), None
    
    # Get all legal moves for the current player
    moves = get_all_moves(board, current_player)
    
    # If no moves available, evaluate current position
    if not moves:
        return evaluate_board(board), None
    
    best_move = None
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            # Apply move and capture
            new_board = apply_move(board, move)
            new_board = apply_capture(new_board, move[2], move[3], current_player)
            
            # Switch player for next turn
            next_player = DEFENDER if current_player == ATTACKER else ATTACKER
            
            # Recursive call with switched roles
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, False, next_player)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            # Apply move and capture
            new_board = apply_move(board, move)
            new_board = apply_capture(new_board, move[2], move[3], current_player)
            
            # Switch player for next turn
            next_player = DEFENDER if current_player == ATTACKER else ATTACKER
            
            # Recursive call with switched roles
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, True, next_player)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval, best_move

############################################################
"""
Difficulty Controller
Returns search depth based on difficulty level
"""
def get_difficulty_depth(difficulty):
    if difficulty == "easy":
        return 1
    elif difficulty == "medium":
        return 3
    elif difficulty == "hard":
        return 5
    else:
        return 3  # Default to medium

############################################################
"""
AI Move Selection Function
Returns the best move for the AI player based on difficulty level
"""
def get_ai_move(board, ai_player, difficulty="medium"):
    depth = get_difficulty_depth(difficulty)
    
    # Determine if AI is maximizing or minimizing
    # Defenders want positive scores, Attackers want negative scores
    maximizing = (ai_player == DEFENDER)
    
    # Initial alpha-beta values
    alpha = float('-inf')
    beta = float('inf')
    
    # Get best move using alpha-beta
    best_score, best_move = alpha_beta(board, depth, alpha, beta, maximizing, ai_player)
    
    return best_move
