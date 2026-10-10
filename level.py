"""
level.py
OWNER: Member 3 (levels and hazards)
Builds a playable Level (walls, items, traps, enemies) from the ASCII map.
"""

import pygame

from settings import *
from utils import tile_rect, item_rect
from level_data import LEVEL_DATA
from enemies import Walker, Archer, Boss
from hazards import Saw


# --------------------------------------------------------------------------
# Level (built from the ASCII map)
# --------------------------------------------------------------------------
class Level:
    def __init__(self, index):
        self.index = index
        self.data = LEVEL_DATA[index]
        self.theme = self.data["theme"]
        self.t = 0
        self.solid, self.doors = set(), {}
        self.coins, self.potions, self.small_keys, self.powerups = [], [], [], []
        self.spikes, self.toggles, self.plates = [], [], {}
        self.saws, self.enemies, self.projectiles = [], [], []
        self.gate_key = self.exit_rect = self.altar = self.chest = None
        self.start = (1, 1)
        self.has_boss = False
        self.boss_dead = False
        self.cleared = False
        self.puzzle_solved = False
        self.plate_next = 1
        self.plate_lit = set()
        self.on_plate = None

        rows = self.data["map"]
        if len(rows) != ROWS:
            raise ValueError(f"Level {index + 1} needs {ROWS} rows, has {len(rows)}")
        for y, row in enumerate(rows):
            if len(row) != COLS:
                raise ValueError(f"Level {index + 1} row {y} needs {COLS} chars, has {len(row)}")
            for x, ch in enumerate(row):
                self.parse(ch, (x, y))

    def parse(self, ch, pos):
        x, y = pos
        if ch == "#":
            self.solid.add(pos)
        elif ch in "DG":
            self.solid.add(pos)
            self.doors[pos] = ch
        elif ch == "P":
            self.start = pos
        elif ch == "K":
            self.gate_key = item_rect(pos)
        elif ch == "E":
            self.exit_rect = pygame.Rect(x * TILE + 3, y * TILE + 3, 26, 26)
        elif ch == "c":
            self.coins.append(item_rect(pos))
        elif ch == "h":
            self.potions.append(item_rect(pos))
        elif ch == "k":
            self.small_keys.append(item_rect(pos))
        elif ch in "SWB":
            self.powerups.append((item_rect(pos), ch))
        elif ch == "^":
            self.spikes.append(pos)
        elif ch == "s":
            self.toggles.append(pos)
        elif ch == "M":
            self.saws.append(Saw(x, y, "h"))
        elif ch == "V":
            self.saws.append(Saw(x, y, "v"))
        elif ch in "123":
            self.plates[pos] = int(ch)
        elif ch == "e":
            self.enemies.append(Walker(x, y))
        elif ch == "a":
            self.enemies.append(Archer(x, y))
        elif ch == "X":
            self.enemies.append(Boss(x, y))
            self.has_boss = True
        elif ch == "R":
            self.altar = tile_rect(pos)
        elif ch == "T":
            self.chest = tile_rect(pos)

    def open_doors(self, kind):
        for pos in [p for p, c in self.doors.items() if c == kind]:
            self.open_door(pos)

    def open_door(self, pos):
        self.solid.discard(pos)
        self.doors.pop(pos, None)

    # Blinking spikes: safe 1 second, deadly 1 second, warning flicker before.
    def toggle_on(self):
        return (self.t // 60) % 2 == 1

    def toggle_warning(self):
        return (self.t // 60) % 2 == 0 and self.t % 60 >= 40
