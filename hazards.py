"""
hazards.py
OWNER: Member 3 (levels and hazards)
Projectiles (magic shots) and moving saw-blade traps.
"""

import math

import pygame

from settings import *
from entity import Entity


class Projectile:
    def __init__(self, x, y, vx, vy, color=ORANGE, radius=5):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.color, self.r = color, radius
        self.life = 320
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r * 2, self.r * 2)

    def update(self, level):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0 or (int(self.x // TILE), int(self.y // TILE)) in level.solid:
            self.alive = False

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), max(1, self.r - 3))


class Saw(Entity):
    """A spinning saw blade that patrols back and forth (3 tiles each way)."""

    def __init__(self, tx, ty, axis):
        super().__init__(tx, ty, 22)
        self.axis = axis
        self.dir = 1
        self.speed = 1.8
        self.origin = (self.fx, self.fy)
        self.angle = 0

    def update(self, level):
        dx = self.dir * self.speed if self.axis == "h" else 0
        dy = self.dir * self.speed if self.axis == "v" else 0
        hit = self.move(dx, dy, level)
        travelled = abs(self.fx - self.origin[0]) if self.axis == "h" else abs(self.fy - self.origin[1])
        if hit or travelled >= 3 * TILE:
            self.dir *= -1
        self.angle = (self.angle + 14) % 360

    def draw(self):
        cx, cy = self.rect.center
        pygame.draw.circle(screen, GREY, (cx, cy), 11)
        for i in range(8):
            a = math.radians(self.angle + i * 45)
            pygame.draw.line(screen, WHITE, (cx, cy), (cx + math.cos(a) * 14, cy + math.sin(a) * 14), 3)
        pygame.draw.circle(screen, DARK_GREY, (cx, cy), 11, 2)
        pygame.draw.circle(screen, RED, (cx, cy), 3)
