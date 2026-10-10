"""
settings.py
OWNER: Member 1 (Team Lead: game core and flow)
Window setup, constants, colors and fonts. Everyone imports from here.
"""

import pygame

pygame.init()
pygame.display.set_caption("Rune Quest: The Lost Kingdom")

# --------------------------------------------------------------------------
# Window / constants
# --------------------------------------------------------------------------
TILE = 32
COLS, ROWS = 25, 16
HUD = 88
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + HUD
FPS = 60
def _make_icon():
    """Tiny knight icon drawn in code (no image file needed)."""
    s = pygame.Surface((32, 32))
    s.fill((28, 66, 48))
    pygame.draw.rect(s, (74, 164, 226), (8, 8, 16, 18), border_radius=4)
    pygame.draw.rect(s, (49, 55, 68), (10, 11, 12, 6), border_radius=2)
    pygame.draw.circle(s, (245, 194, 55), (16, 8), 3)
    pygame.draw.line(s, (242, 241, 232), (16, 18), (28, 4), 3)
    return s


pygame.display.set_icon(_make_icon())

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 20)
SMALL = pygame.font.SysFont("arial", 16)
TINY = pygame.font.SysFont("arial", 13)
BIG = pygame.font.SysFont("arial", 38)
HUGE = pygame.font.SysFont("arial", 52, bold=True)

# Colors
BLACK = (18, 20, 28)
WHITE = (242, 241, 232)
GOLD = (245, 194, 55)
BLUE = (74, 164, 226)
CYAN = (90, 220, 240)
RED = (210, 65, 68)
ORANGE = (240, 140, 50)
PURPLE = (150, 95, 210)
GREEN = (70, 190, 100)
HEART = (238, 75, 94)
GREY = (150, 155, 165)
DARK_GREY = (70, 74, 86)
BROWN = (120, 78, 44)
RUNE_COLORS = [(90, 200, 255), (120, 230, 130), (255, 200, 80), (240, 120, 200)]
