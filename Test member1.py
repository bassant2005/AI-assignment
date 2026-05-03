from MAin_logic import *
###########################################################
# HELPER
############################################################
def section(title):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)

passed = 0
failed = 0

def check(name, result, expected):
    global passed, failed
    if result == expected:
        passed += 1
        print(f"  [PASS] {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name}")
        print(f"         got={result!r}, expected={expected!r}")

############################################################
# 1. is_valid_move
############################################################
section("is_valid_move — No Jumping Rule")

board = initial_state()

check("clear slide left",           is_valid_move(board, 1, 5, 1, 3),  True)
check("adjacent move",              is_valid_move(board, 1, 5, 1, 4),  True)
check("diagonal rejected",          is_valid_move(board, 1, 5, 2, 6),  False)
check("destination occupied",       is_valid_move(board, 0, 3, 0, 4),  False)
check("out of bounds",              is_valid_move(board, 0, 5, -1, 5), False)
check("cannot jump over piece",     is_valid_move(board, 0, 3, 0, 9),  False)
check("cannot move to own cell",    is_valid_move(board, 0, 3, 0, 3),  False)

############################################################
# 2. evaluate_board
############################################################
section("evaluate_board — Scoring System")

board = initial_state()
score = evaluate_board(board)
print(f"  [INFO] Initial score: {score}  (negative = attackers outnumber defenders 24 vs 12)")
check("returns an int",                     isinstance(score, int),  True)

# Remove all attackers → score must rise
board_no_atk = [row[:] for row in board]
for r in range(BOARD_SIZE):
    for c in range(BOARD_SIZE):
        if board_no_atk[r][c] == ATTACKER:
            board_no_atk[r][c] = EMPTY
check("no attackers → higher score",        evaluate_board(board_no_atk) > score, True)

# King threatened → score must drop
board_threat = initial_state()
kr, kc = find_king(board_threat)
board_threat[kr+1][kc] = ATTACKER
board_threat[kr-1][kc] = ATTACKER
check("king threatened → lower score",      evaluate_board(board_threat) < score, True)

# King gone → -9999
board_noking = initial_state()
kr, kc = find_king(board_noking)
board_noking[kr][kc] = EMPTY
check("king gone → -9999",                  evaluate_board(board_noking), -9999)

############################################################
# 3. is_winner
############################################################
section("is_winner — Win Conditions")

# Fresh board → no winner
board = initial_state()
check("fresh board → None",                 is_winner(board), None)

# King removed → Attacker wins
board_noking = initial_state()
kr, kc = find_king(board_noking)
board_noking[kr][kc] = EMPTY
check("king removed → ATTACKER",            is_winner(board_noking), "ATTACKER")

# King at corner → Defender wins
board_escape = initial_state()
kr, kc = find_king(board_escape)
board_escape[kr][kc] = EMPTY
board_escape[0][0] = KING
check("king at corner (0,0) → DEFENDER",    is_winner(board_escape), "DEFENDER")

# CASE 1: King in center, surrounded on all 4 sides
board_c1 = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
board_c1[5][5] = KING
board_c1[4][5] = ATTACKER
board_c1[6][5] = ATTACKER
board_c1[5][4] = ATTACKER
board_c1[5][6] = ATTACKER
check("center: 4 attackers → ATTACKER",     is_winner(board_c1), "ATTACKER")

# CASE 1: center, only 3 attackers → not enough
board_c1b = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
board_c1b[5][5] = KING
board_c1b[4][5] = ATTACKER
board_c1b[6][5] = ATTACKER
board_c1b[5][4] = ATTACKER
check("center: 3 attackers → None",         is_winner(board_c1b), None)

# CASE 2: King on edge, wall + 2 attackers = 3 blocked
board_c2 = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
board_c2[0][5] = KING
board_c2[1][5] = ATTACKER
board_c2[0][4] = ATTACKER
board_c2[0][6] = ATTACKER
check("edge: wall + 2 attackers → ATTACKER", is_winner(board_c2), "ATTACKER")

# CASE 2: King on edge, only 1 attacker → not enough
board_c2b = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
board_c2b[0][5] = KING
board_c2b[1][5] = ATTACKER
check("edge: wall + 1 attacker → None",     is_winner(board_c2b), None)

############################################################
# SUMMARY
############################################################
print("\n" + "=" * 55)
print(f"  RESULT: {passed} passed, {failed} failed")
print("=" * 55)