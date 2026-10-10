"""
enemies.py
OWNER: Member 2 (characters and combat)
Monsters: Walker (melee), Archer (ranged) and the final Boss.
"""

import math
import random

import pygame

from settings import *
from entity import Entity
from hazards import Projectile


class Enemy(Entity):
    points = 100
    name = "Monster"
    knock_dist = 18
    contact = True

    def __init__(self, tx, ty, size, hp):
        super().__init__(tx, ty, size)
        self.hp = self.max_hp = hp
        self.flash = 0
        self.stun = 0

    def take_hit(self, dmg, from_pos, level):
        self.hp -= dmg
        self.flash = 8
        if self.knock_dist:
            self.stun = 12
            d = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(from_pos)
            if d.length() > 0:
                d.scale_to_length(self.knock_dist / 4)
                for _ in range(4):
                    self.move(d.x, d.y, level)

    def draw_eyes(self, color=BLACK):
        r = self.rect
        for ex in (r.x + 7, r.right - 7):
            pygame.draw.circle(screen, WHITE, (ex, r.y + 8), 3)
            pygame.draw.circle(screen, color, (ex, r.y + 8), 1)


class Walker(Enemy):
    """Melee monster: patrols, then chases when the player gets close."""
    name = "Monster"
    points = 100

    def __init__(self, tx, ty):
        super().__init__(tx, ty, 22, 2)
        self.speed = 1.05
        self.dir = random.choice((-1, 1))
        self.patrol = 0

    def update(self, player, level):
        self.flash = max(0, self.flash - 1)
        if self.stun > 0:
            self.stun -= 1
            return
        d = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        if 0 < d.length() < 170:
            d.scale_to_length(self.speed)
            self.move(d.x, d.y, level)
        else:
            if self.move(self.dir * self.speed * 0.7, 0, level):
                self.dir *= -1
            self.patrol += 1
            if self.patrol > 120:
                self.dir *= -1
                self.patrol = 0

    def draw(self):
        color = WHITE if self.flash else RED
        pygame.draw.rect(screen, color, self.rect, border_radius=7)
        pygame.draw.polygon(screen, color, [(self.rect.x + 3, self.rect.y + 2), (self.rect.x + 6, self.rect.y - 4),
                                            (self.rect.x + 9, self.rect.y + 2)])
        pygame.draw.polygon(screen, color, [(self.rect.right - 9, self.rect.y + 2), (self.rect.right - 6, self.rect.y - 4),
                                            (self.rect.right - 3, self.rect.y + 2)])
        self.draw_eyes()


class Archer(Enemy):
    """Ranged monster: winds up (flashes yellow), then fires an arrow orb."""
    name = "Archer"
    points = 150

    def __init__(self, tx, ty):
        super().__init__(tx, ty, 22, 2)
        self.cooldown = random.randint(60, 120)
        self.windup = 0

    def update(self, player, level):
        self.flash = max(0, self.flash - 1)
        if self.stun > 0:
            self.stun -= 1
            return
        d = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        dist = d.length()
        if self.windup > 0:
            self.windup -= 1
            if self.windup == 0:
                self.shoot(d, level)
        else:
            self.cooldown -= 1
            if self.cooldown <= 0:
                if dist < 360:
                    self.windup = 24
                    self.cooldown = random.randint(110, 160)
                else:
                    self.cooldown = 30
        if 0 < dist < 90 and self.windup == 0:     # backs away from the player
            away = -d
            away.scale_to_length(0.8)
            self.move(away.x, away.y, level)

    def shoot(self, d, level):
        if d.length() == 0:
            return
        d.scale_to_length(3.4)
        level.projectiles.append(Projectile(self.rect.centerx, self.rect.centery, d.x, d.y, ORANGE))

    def draw(self):
        color = WHITE if self.flash else (GOLD if self.windup > 0 and (self.windup // 3) % 2 == 0 else (60, 150, 120))
        pygame.draw.rect(screen, color, self.rect, border_radius=9)
        pygame.draw.rect(screen, (30, 80, 64), (self.rect.x + 3, self.rect.y + 1, 16, 8), border_radius=4)
        self.draw_eyes()
        pygame.draw.arc(screen, BROWN, self.rect.inflate(10, 6), -1.2, 1.2, 3)


class Boss(Enemy):
    """The Guardian. Cycles through chase, wind-up, attack and dizzy states."""
    name = "The Guardian"
    points = 1000
    knock_dist = 0

    def __init__(self, tx, ty):
        super().__init__(tx, ty, 40, 24)
        self.state = "chase"
        self.timer = 80
        self.attack = "burst"
        self.dir = pygame.math.Vector2(1, 0)

    @property
    def enraged(self):
        return self.hp <= self.max_hp // 2

    def update(self, player, level):
        self.flash = max(0, self.flash - 1)
        to_p = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        if self.state == "chase":
            if to_p.length() > 1:
                d = to_p.normalize() * (1.5 if self.enraged else 1.0)
                self.move(d.x, d.y, level)
            self.timer -= 1
            if self.timer <= 0:
                choices = ["burst", "volley", "charge"] + (["burst", "volley"] if self.enraged else [])
                self.attack = random.choice(choices)
                self.state = "windup"
                self.timer = 36 if self.enraged else 48
        elif self.state == "windup":
            self.timer -= 1
            if self.timer <= 0:
                if self.attack == "burst":
                    self.fire_burst(level)
                elif self.attack == "volley":
                    self.fire_volley(to_p, level)
                else:
                    self.dir = to_p.normalize() if to_p.length() > 0 else pygame.math.Vector2(1, 0)
                    self.state, self.timer = "charge", 34
                    return
                self.state = "chase"
                self.timer = random.randint(55, 85) if self.enraged else random.randint(80, 120)
        elif self.state == "charge":
            self.timer -= 1
            hit = self.move(self.dir.x * 7, self.dir.y * 7, level)
            if hit or self.timer <= 0:
                self.state, self.timer = "recover", 60      # dizzy: a great time to strike!
        elif self.state == "recover":
            self.timer -= 1
            if self.timer <= 0:
                self.state, self.timer = "chase", 50

    def fire_burst(self, level):
        n = 12 if self.enraged else 8
        offset = random.random() * math.tau
        for i in range(n):
            a = offset + i * math.tau / n
            level.projectiles.append(Projectile(self.rect.centerx, self.rect.centery,
                                                math.cos(a) * 2.6, math.sin(a) * 2.6, PURPLE, 6))

    def fire_volley(self, to_p, level):
        base = math.atan2(to_p.y, to_p.x)
        count = 5 if self.enraged else 3
        for i in range(count):
            a = base + (i - count // 2) * 0.24
            level.projectiles.append(Projectile(self.rect.centerx, self.rect.centery,
                                                math.cos(a) * 3.6, math.sin(a) * 3.6, RED, 6))

    def draw(self):
        r = self.rect
        winding = self.state == "windup"
        if self.flash:
            color = WHITE
        elif winding and (self.timer // 4) % 2 == 0:
            color = GOLD
        elif self.state == "recover":
            color = (120, 100, 160)
        else:
            color = (200, 60, 90) if self.enraged else PURPLE
        pygame.draw.rect(screen, color, r, border_radius=10)
        pygame.draw.rect(screen, BLACK, r, 3, border_radius=10)
        # crown
        for i in range(3):
            x = r.x + 6 + i * 13
            pygame.draw.polygon(screen, GOLD, [(x, r.y + 1), (x + 4, r.y - 9), (x + 8, r.y + 1)])
        for ex in (r.x + 12, r.right - 12):
            pygame.draw.circle(screen, WHITE, (ex, r.y + 16), 6)
            pygame.draw.circle(screen, RED if not self.state == "recover" else BLACK, (ex, r.y + 16), 3)
        if self.state == "recover":      # dizzy stars
            for i in range(3):
                a = self.timer / 6 + i * 2.1
                pygame.draw.circle(screen, GOLD, (int(r.centerx + math.cos(a) * 18), int(r.y - 12 + math.sin(a) * 4)), 3)
        if winding and self.attack == "charge":
            pygame.draw.line(screen, RED, r.center, (r.centerx + self.dir.x * 90, r.centery + self.dir.y * 90), 2)
