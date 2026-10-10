"""
player.py
OWNER: Member 2 (characters and combat)
The knight: movement, sword reach, inventory, drawing.
"""

import pygame

from settings import *
from entity import Entity


class Player(Entity):
    def __init__(self):
        super().__init__(1, 1, 22)
        self.hp = self.max_hp = 5
        self.score = 0
        self.coins = 0
        self.sword = 0        # sword upgrades (each adds damage + reach)
        self.shields = 0      # stored magic shields (press E)
        self.boots = 0        # stored speed boots (press Q)
        self.facing = pygame.math.Vector2(1, 0)
        self.enter_level((1, 1))

    def enter_level(self, start):
        self.place(*start)
        self.has_key = False
        self.small_keys = 0
        self.attack_cd = 0
        self.invuln = 0
        self.shield_t = 0
        self.boots_t = 0
        self.slash_t = 0

    def update(self, keys, level):
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        v = pygame.math.Vector2(dx, dy)
        if v.length_squared() > 0:
            v = v.normalize()
            self.facing = v
            speed = 4.6 if self.boots_t > 0 else 3.0
            self.move(v.x * speed, v.y * speed, level)
        self.attack_cd = max(0, self.attack_cd - 1)
        self.invuln = max(0, self.invuln - 1)
        self.shield_t = max(0, self.shield_t - 1)
        self.boots_t = max(0, self.boots_t - 1)
        self.slash_t = max(0, self.slash_t - 1)

    def attack_rect(self):
        reach = 22 + 4 * self.sword
        size = 34 + 8 * self.sword
        c = pygame.math.Vector2(self.rect.center) + self.facing * reach
        r = pygame.Rect(0, 0, size, size)
        r.center = (round(c.x), round(c.y))
        return r

    def draw(self):
        blink = self.invuln > 0 and (self.invuln // 4) % 2 == 0
        body = WHITE if blink else (BLUE if self.boots_t <= 0 else (110, 210, 255))
        r = self.rect
        pygame.draw.rect(screen, body, r, border_radius=5)
        pygame.draw.rect(screen, DARK_GREY, (r.x + 4, r.y + 3, 14, 7), border_radius=2)
        pygame.draw.circle(screen, GOLD, (r.centerx, r.y + 4), 3)
        tip = pygame.math.Vector2(r.center) + self.facing * (16 + 3 * self.sword)
        pygame.draw.line(screen, WHITE, r.center, (round(tip.x), round(tip.y)), 3)
        if self.boots_t > 0:
            for i in range(3):
                pygame.draw.line(screen, CYAN, (r.x - 4 - i * 4, r.y + 6 + i * 5),
                                 (r.x - 12 - i * 4, r.y + 6 + i * 5), 2)
        if self.shield_t > 0:
            width = 3 if self.shield_t > 90 or (self.shield_t // 6) % 2 == 0 else 1
            pygame.draw.circle(screen, CYAN, r.center, 20, width)
