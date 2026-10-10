"""
utils.py
OWNER: Member 1 (Team Lead: game core and flow)
Shared helper functions: text, hearts, rune symbols, tile maths and wall collision.
"""

import pygame

from settings import *

# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def draw_text(text, x, y, color=WHITE, font=FONT, center=False):
    img = font.render(text, True, color)
    if center:
        x = x - img.get_width() // 2
    screen.blit(img, (x, y))
    return img.get_width()


def wrap_text(text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_heart(x, y, size, filled):
    r = size // 4
    color = HEART if filled else (72, 52, 64)
    pygame.draw.circle(screen, color, (x + r, y + r), r)
    pygame.draw.circle(screen, color, (x + 3 * r, y + r), r)
    pygame.draw.polygon(screen, color, [(x, y + r + 1), (x + 4 * r, y + r + 1), (x + 2 * r, y + 4 * r)])


def draw_symbol(idx, center, size, color):
    """Rune symbols: 0 circle, 1 triangle, 2 square, 3 diamond."""
    cx, cy = center
    h = size // 2
    if idx == 0:
        pygame.draw.circle(screen, color, center, h)
    elif idx == 1:
        pygame.draw.polygon(screen, color, [(cx, cy - h), (cx - h, cy + h), (cx + h, cy + h)])
    elif idx == 2:
        pygame.draw.rect(screen, color, (cx - h, cy - h, size, size))
    else:
        pygame.draw.polygon(screen, color, [(cx, cy - h), (cx + h, cy), (cx, cy + h), (cx - h, cy)])


def tile_rect(pos):
    return pygame.Rect(pos[0] * TILE, pos[1] * TILE, TILE, TILE)


def item_rect(pos):
    return pygame.Rect(pos[0] * TILE + 6, pos[1] * TILE + 6, 20, 20)


def blocked(rect, level):
    """True if the rectangle overlaps any solid tile (walls, closed doors)."""
    x0, x1 = max(0, rect.left // TILE), min(COLS - 1, (rect.right - 1) // TILE)
    y0, y1 = max(0, rect.top // TILE), min(ROWS - 1, (rect.bottom - 1) // TILE)
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            if (tx, ty) in level.solid:
                return True
    return False
