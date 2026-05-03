import pygame
from MAin_logic import (
    initial_state, get_piece_moves,
    ATTACKER, DEFENDER, KING, EMPTY, BOARD_SIZE,
    CORNERS, THRONE, belongs_to
)

pygame.init()
pygame.font.init()

#  COLOUR PALETTE 
C = {
    # board surface
    "bg":           (12,  13,  18),
    "board_dark":   (28,  32,  42),
    "board_light":  (36,  41,  54),
    "throne":       (55,  38,  22),   # deep amber square
    "corner":       (22,  48,  38),   # deep teal square
    "border":       (58,  66,  88),

    # highlights
    "select":       (180, 140,  60),  # selected piece ring (amber)
    "valid":        ( 60, 160, 120),  # valid-move dot (teal)
    "last_from":    ( 70,  80, 110),
    "last_to":      ( 80,  95, 130),

    # pieces
    "king_body":    (220, 175,  60),
    "king_ring":    (255, 215, 100),
    "king_text":    ( 50,  35,   8),

    "def_body":     (190, 200, 215),
    "def_ring":     (230, 238, 248),
    "def_text":     ( 30,  40,  60),

    "att_body":     ( 90,  38,  38),
    "att_ring":     (150,  55,  55),
    "att_text":     (240, 210, 210),

    # UI
    "panel":        ( 18,  21,  30),
    "panel_border": ( 50,  58,  78),
    "text_main":    (220, 225, 235),
    "text_muted":   (110, 120, 145),
    "text_amber":   (210, 165,  55),
    "text_teal":    ( 75, 185, 145),
    "text_crimson": (190,  75,  75),
    "btn_hover":    ( 45,  52,  70),
    "btn_active":   ( 60,  70,  95),
    "divider":      ( 38,  44,  60),
}

#  LAYOUT CONSTANTS
CELL      = 58
BOARD_PX  = CELL * BOARD_SIZE
MARGIN    = 40
PANEL_W   = 280
GAP       = 20
WIN_W     = MARGIN + BOARD_PX + GAP + PANEL_W + MARGIN
WIN_H     = MARGIN + BOARD_PX + MARGIN
COORD_OFF = 22

PIECE_R   = int(CELL * 0.36)
KING_R    = int(CELL * 0.40)

#  HELPERS
def cell_rect(r, c):
    x = MARGIN + COORD_OFF + c * CELL
    y = MARGIN + COORD_OFF + r * CELL
    return x, y

def cell_center(r, c):
    x, y = cell_rect(r, c)
    return x + CELL // 2, y + CELL // 2

def px_to_cell(px, py):
    c = (px - MARGIN - COORD_OFF) // CELL
    r = (py - MARGIN - COORD_OFF) // CELL
    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        return int(r), int(c)
    return None, None

def is_corner(r, c):
    return (r, c) in CORNERS

def is_throne(r, c):
    return (r, c) == THRONE

def draw_rounded_rect(surf, color, rect, radius=6, width=0):
    pygame.draw.rect(surf, color, rect, width, border_radius=radius)

#  PIECE DRAWING
def draw_piece(surf, piece, r, c):
    """
    Draws a single piece at cell (r, c).
      King     → gold circle with ♔
      Defender → silver-blue circle with D
      Attacker → crimson circle with A
    """
    cx, cy = cell_center(r, c)

    if piece == KING:
        body, ring, txt_c, rad = C["king_body"], C["king_ring"], C["king_text"], KING_R
        label = "♔"
    elif piece == DEFENDER:
        body, ring, txt_c, rad = C["def_body"], C["def_ring"], C["def_text"], PIECE_R
        label = "D"
    else:  # ATTACKER
        body, ring, txt_c, rad = C["att_body"], C["att_ring"], C["att_text"], PIECE_R
        label = "A"

    pygame.draw.circle(surf, ring, (cx, cy), rad + 3)   # outer glow
    pygame.draw.circle(surf, body, (cx, cy), rad)        # body fill

    fsize = rad + 4 if piece == KING else rad - 2
    font  = pygame.font.SysFont("segoeuisymbol,symbola,unifont", fsize, bold=True)
    txt   = font.render(label, True, txt_c)
    surf.blit(txt, txt.get_rect(center=(cx, cy)))

#  VALID-MOVE DOT
def draw_valid_dot(surf, r, c):
    """Small teal dot marking a valid destination square."""
    cx, cy = cell_center(r, c)
    pygame.draw.circle(surf, C["valid"], (cx, cy), 8)
    pygame.draw.circle(surf, (30, 90, 70), (cx, cy), 8, 2)

#  BOARD
def draw_board(surf, board, selected, valid_moves, last_move, hover_cell):
    """
    Draws the full 11x11 board:
      - Checkerboard cells (dark / light)
      - Throne square highlighted in amber
      - Corner squares highlighted in teal
      - Last-move tint on origin and destination cells
      - Hover tint on empty cells when nothing is selected
      - Selected piece amber border
      - Teal dots for all valid move destinations
      - All pieces (King, Defenders, Attackers)
      - Row / column coordinate labels
    """
    board_x = MARGIN + COORD_OFF
    board_y = MARGIN + COORD_OFF

    # border frame
    bg_rect = (board_x - 4, board_y - 4, BOARD_PX + 8, BOARD_PX + 8)
    draw_rounded_rect(surf, C["border"], bg_rect, radius=4)

    # draw each cell
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            x, y = cell_rect(r, c)
            rect  = (x, y, CELL, CELL)

            # base colour — corner / throne / checkerboard
            if is_corner(r, c):
                col = C["corner"]
            elif is_throne(r, c):
                col = C["throne"]
            elif (r + c) % 2 == 0:
                col = C["board_dark"]
            else:
                col = C["board_light"]

            pygame.draw.rect(surf, col, rect)

            # last-move tint
            if last_move:
                r1, c1, r2, c2 = last_move
                if (r, c) == (r1, c1):
                    s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                    s.fill((*C["last_from"], 80))
                    surf.blit(s, (x, y))
                elif (r, c) == (r2, c2):
                    s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                    s.fill((*C["last_to"], 80))
                    surf.blit(s, (x, y))

            # hover tint (only when nothing is selected)
            if hover_cell == (r, c) and selected is None:
                s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                s.fill((255, 255, 255, 12))
                surf.blit(s, (x, y))

            # selected piece highlight — amber border
            if selected == (r, c):
                pygame.draw.rect(surf, C["select"], rect, 3)

            # thin grid line
            pygame.draw.rect(surf, C["bg"], rect, 1)

    # valid-move dots drawn before pieces (so dots appear underneath pieces)
    for (vr, vc) in valid_moves:
        if board[vr][vc] == EMPTY:
            draw_valid_dot(surf, vr, vc)

    # draw all pieces
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board[r][c]
            if p != EMPTY:
                draw_piece(surf, p, r, c)

    # coordinate labels — columns on top, rows on left
    coord_font = pygame.font.SysFont("consolas,monospace", 11)
    for i in range(BOARD_SIZE):
        lbl = coord_font.render(str(i), True, C["text_muted"])
        surf.blit(lbl, (board_x + i * CELL + CELL // 2 - lbl.get_width() // 2,
                        MARGIN + COORD_OFF - 18))
        surf.blit(lbl, (MARGIN + COORD_OFF - 18,
                        board_y + i * CELL + CELL // 2 - lbl.get_height() // 2))

#  SIDE PANEL
def draw_panel(surf, state):
    px = MARGIN + COORD_OFF + BOARD_PX + GAP
    py = MARGIN
    pw = PANEL_W
    ph = BOARD_PX + COORD_OFF

    draw_rounded_rect(surf, C["panel"], (px, py, pw, ph), radius=10)
    draw_rounded_rect(surf, C["panel_border"], (px, py, pw, ph), radius=10, width=1)

    y  = py + 20
    cx = px + pw // 2

    title_font = pygame.font.SysFont("georgia,palatino,serif", 22, bold=True)
    t = title_font.render("HNEFATAFL", True, C["text_amber"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 30

    sub_font = pygame.font.SysFont("consolas,monospace", 10)
    t = sub_font.render("VIKING CHESS", True, C["text_muted"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 24

    pygame.draw.line(surf, C["divider"], (px + 16, y), (px + pw - 16, y)); y += 16

    label_font = pygame.font.SysFont("consolas,monospace", 11)
    val_font   = pygame.font.SysFont("consolas,monospace", 13, bold=True)

    t = label_font.render("GAME STATUS", True, C["text_muted"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 16

    player = state["current_player"]
    pcol   = C["text_crimson"] if player == ATTACKER else C["text_teal"]
    pname  = "ATTACKER" if player == ATTACKER else "DEFENDER"
    t = val_font.render(pname, True, pcol)
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 22

    pygame.draw.line(surf, C["divider"], (px + 16, y), (px + pw - 16, y)); y += 16

    t = label_font.render("PIECES REMAINING", True, C["text_muted"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 18

    board     = state["board"]
    att_count = sum(row.count(ATTACKER) for row in board)
    def_count = sum(row.count(DEFENDER) for row in board)
    bar_w = pw - 48
    bar_x = px + 24

    t = label_font.render(f"Attackers  {att_count}/24", True, C["text_crimson"])
    surf.blit(t, (bar_x, y)); y += 14
    fill = int(bar_w * att_count / 24)
    pygame.draw.rect(surf, C["divider"],  (bar_x, y, bar_w, 7), border_radius=3)
    pygame.draw.rect(surf, C["att_body"], (bar_x, y, fill,  7), border_radius=3)
    y += 16

    t = label_font.render(f"Defenders  {def_count}/12", True, C["text_teal"])
    surf.blit(t, (bar_x, y)); y += 14
    fill = int(bar_w * def_count / 12)
    pygame.draw.rect(surf, C["divider"],  (bar_x, y, bar_w, 7), border_radius=3)
    pygame.draw.rect(surf, C["def_body"], (bar_x, y, fill,  7), border_radius=3)
    y += 20

    pygame.draw.line(surf, C["divider"], (px + 16, y), (px + pw - 16, y)); y += 16

    t = label_font.render(f"TURN  {state['turn_count']}", True, C["text_muted"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 20

    pygame.draw.line(surf, C["divider"], (px + 16, y), (px + pw - 16, y)); y += 16

    t = label_font.render("LEGEND", True, C["text_muted"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 16

    legend = [
        ("♔", C["king_body"],  "King — escape to corner"),
        ("D",  C["def_body"],  "Defender — protect King"),
        ("A",  C["att_body"],  "Attacker — capture King"),
        ("◆",  C["text_teal"], "Corner — escape goal"),
        ("✦",  C["text_amber"],"Throne — King's start"),
    ]
    lf = pygame.font.SysFont("segoeuisymbol,symbola,unifont", 13, bold=True)
    df = pygame.font.SysFont("consolas,monospace", 10)
    for sym, sc, desc in legend:
        s = lf.render(sym, True, sc)
        surf.blit(s, (bar_x, y))
        d = df.render(desc, True, C["text_muted"])
        surf.blit(d, (bar_x + 20, y + 2))
        y += 18

    pygame.draw.line(surf, C["divider"], (px + 16, y), (px + pw - 16, y)); y += 16

    controls = ["Click piece to select",
                "Click highlight to move",
                "R — reset   ESC — quit"]
    for line in controls:
        t = df.render(line, True, C["text_muted"])
        surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 14

#  START SCREEN 
def draw_start_screen(surf):
    """
    Draws the opening screen with a START GAME button.
    Returns the pygame.Rect of the button so the caller can detect clicks.
    """
    surf.fill(C["bg"])

    # decorative dot grid background
    for row in range(0, WIN_H, 40):
        for col in range(0, WIN_W, 40):
            pygame.draw.circle(surf, C["board_light"], (col, row), 1)

    cx = WIN_W // 2
    y  = WIN_H // 2 - 130

    title_font = pygame.font.SysFont("georgia,palatino,serif", 52, bold=True)
    sub_font   = pygame.font.SysFont("consolas,monospace", 13)
    btn_font   = pygame.font.SysFont("consolas,monospace", 15, bold=True)

    # title
    t = title_font.render("HNEFATAFL", True, C["text_amber"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 64

    t = sub_font.render("THE ANCIENT NORSE STRATEGY GAME", True, C["text_muted"])
    surf.blit(t, t.get_rect(centerx=cx, top=y)); y += 50

    pygame.draw.line(surf, C["divider"], (cx - 100, y), (cx + 100, y)); y += 36

    # START button
    bw, bh  = 220, 52
    bx      = cx - bw // 2
    rect    = pygame.Rect(bx, y, bw, bh)

    mx, my  = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mx, my)
    bg      = C["btn_hover"] if hovered else C["panel"]

    draw_rounded_rect(surf, bg, rect, radius=10)
    draw_rounded_rect(surf,
                      C["text_amber"] if hovered else C["panel_border"],
                      rect, radius=10, width=2 if hovered else 1)

    tc = C["text_amber"] if hovered else C["text_main"]
    t  = btn_font.render("START GAME", True, tc)
    surf.blit(t, t.get_rect(center=rect.center))

    y += bh + 28
    hint_font = pygame.font.SysFont("consolas,monospace", 10)
    t = hint_font.render("Human vs Human  |  R — reset  |  ESC — quit", True, C["text_muted"])
    surf.blit(t, t.get_rect(centerx=cx, top=y))

    return rect   # caller uses this for click detection

#  WINNER OVERLAY
def draw_winner_overlay(surf, winner):
    overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
    overlay.fill((8, 10, 16, 210))
    surf.blit(overlay, (0, 0))

    cx, cy = WIN_W // 2, WIN_H // 2
    big   = pygame.font.SysFont("georgia,palatino,serif", 52, bold=True)
    small = pygame.font.SysFont("consolas,monospace", 15)

    if winner == "DEFENDER":
        col, msg = C["text_teal"],    "DEFENDERS TRIUMPH!"
        sub = "The King reaches freedom."
    else:
        col, msg = C["text_crimson"], "ATTACKERS VICTORIOUS!"
        sub = "The King is captured."

    t = big.render(msg, True, col)
    surf.blit(t, t.get_rect(center=(cx, cy - 30)))
    t = small.render(sub, True, C["text_muted"])
    surf.blit(t, t.get_rect(center=(cx, cy + 28)))
    t = small.render("Press R to restart  |  ESC to quit", True, C["text_muted"])
    surf.blit(t, t.get_rect(center=(cx, cy + 56)))

#  GAME STATE
def make_state():
    return {
        "board":          initial_state(),
        "current_player": ATTACKER,        # attackers move first
        "selected":       None,
        "valid_moves":    [],
        "last_move":      None,
        "winner":         None,
        "turn_count":     1,
    }

#  CLICK / MOVE LOGIC
def handle_click(state, pos):
    r, c = px_to_cell(*pos)
    if r is None:
        return

    board  = state["board"]
    player = state["current_player"]

    if state["selected"]:
        sr, sc = state["selected"]

        if (r, c) in state["valid_moves"]:
            return

        if belongs_to(board[r][c], player):
            state["selected"]    = (r, c)
            state["valid_moves"] = get_piece_moves(board, r, c, player)
            return

        state["selected"]    = None
        state["valid_moves"] = []
        return

    if belongs_to(board[r][c], player):
        state["selected"]    = (r, c)
        state["valid_moves"] = get_piece_moves(board, r, c, player)

#  MAIN
def test_gui():
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Hnefatafl")
    clock  = pygame.time.Clock()

    phase     = "start"   # "start" | "game"
    state     = None
    start_btn = None
    hover     = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); return
                # R resets back to start screen from anywhere
                if event.key == pygame.K_r:
                    phase     = "start"
                    state     = None
                    start_btn = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if phase == "start":
                    if start_btn and start_btn.collidepoint(event.pos):
                        state = make_state()
                        phase = "game"
                elif phase == "game" and state["winner"] is None:
                    handle_click(state, event.pos)

        # render
        if phase == "start":
            start_btn = draw_start_screen(screen)

        elif phase == "game":
            screen.fill(C["bg"])

            hover = None
            if state["winner"] is None:
                mx, my = pygame.mouse.get_pos()
                hr, hc = px_to_cell(mx, my)
                if hr is not None:
                    hover = (hr, hc)

            draw_board(screen, state["board"], state["selected"],
                       state["valid_moves"], state["last_move"], hover)
            draw_panel(screen, state)

            if state["winner"]:
                draw_winner_overlay(screen, state["winner"])

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    test_gui()