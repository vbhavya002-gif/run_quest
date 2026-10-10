"""
entity.py
OWNER: Member 2 (characters and combat)
Base class for anything that moves (float positions + wall collision).
"""

import pygame

from settings import TILE
from utils import blocked


class Entity:
    """Anything that moves. Uses float positions so slow speeds still work."""

    def __init__(self, tx, ty, size):
        self.size = size
        self.place(tx, ty)

    def place(self, tx, ty):
        self.fx = tx * TILE + (TILE - self.size) / 2
        self.fy = ty * TILE + (TILE - self.size) / 2
        self.rect = pygame.Rect(round(self.fx), round(self.fy), self.size, self.size)

    def move(self, dx, dy, level):
        """Move with wall collision. Returns True if a wall was hit."""
        hit = False
        if dx:
            self.fx += dx
            self.rect.x = round(self.fx)
            if blocked(self.rect, level):
                self.fx -= dx
                self.rect.x = round(self.fx)
                hit = True
        if dy:
            self.fy += dy
            self.rect.y = round(self.fy)
            if blocked(self.rect, level):
                self.fy -= dy
                self.rect.y = round(self.fy)
                hit = True
        return hit
