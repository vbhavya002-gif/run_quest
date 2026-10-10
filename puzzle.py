"""
puzzle.py
OWNER: Member 4 (puzzles, graphics and UI)
Level 4 rune puzzle: symbol order, number pattern and the countdown timer.
"""

import random

import pygame

from settings import FPS


# --------------------------------------------------------------------------
# Level 4 rune puzzle
# --------------------------------------------------------------------------
PATTERNS = [([2, 4, 8, 16], 32), ([3, 6, 9, 12], 15), ([1, 4, 9, 16], 25), ([2, 6, 18, 54], 162),
            ([5, 10, 20, 40], 80), ([1, 1, 2, 3, 5], 8), ([100, 90, 80, 70], 60), ([1, 3, 6, 10], 15)]


class RunePuzzle:
    TIME_LIMIT = 45 * FPS          # 45 seconds for the whole challenge
    PENALTY = 5 * FPS              # wrong answers cost 5 seconds

    def __init__(self):
        self.active = False
        self.altar_ready = True    # must step off the altar before it re-triggers
        self.stage = "idle"
        self.message = ""

    def start(self):
        self.active = True
        self.time_left = self.TIME_LIMIT
        self.seq = [random.randrange(4) for _ in range(4)]
        self.entered = []
        self.stage = "memorize"
        self.show_timer = 4 * FPS
        self.message = ""
        nums, answer = random.choice(PATTERNS)
        self.pattern, self.answer = nums, answer
        wrong = {answer + 2, answer - 2, answer + 5, answer - 5, answer * 2, max(1, answer // 2), answer + 10}
        wrong.discard(answer)
        wrong = [w for w in wrong if w > 0]
        self.options = random.sample(wrong, 3) + [answer]
        random.shuffle(self.options)

    def key(self, idx):
        """idx is 0-3 (keys 1-4). Returns 'solved' when everything is complete."""
        if self.stage == "sequence":
            self.entered.append(idx)
            if self.entered != self.seq[:len(self.entered)]:
                self.time_left -= self.PENALTY
                self.entered = []
                self.stage = "memorize"
                self.show_timer = 2 * FPS
                self.message = "Wrong rune! -5 seconds. Look again!"
            elif len(self.entered) == len(self.seq):
                self.stage = "pattern"
                self.message = "Runes matched! Now solve the number pattern."
        elif self.stage == "pattern":
            if self.options[idx] == self.answer:
                return "solved"
            self.time_left -= self.PENALTY
            self.message = "Wrong answer! -5 seconds."
        return None

    def update(self):
        self.time_left -= 1
        if self.stage == "memorize":
            self.show_timer -= 1
            if self.show_timer <= 0:
                self.stage = "sequence"
                self.message = "Enter the runes in the same order."
        if self.time_left <= 0:
            return "failed"
        return None


PUZZLE_KEYS = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
               pygame.K_KP1: 0, pygame.K_KP2: 1, pygame.K_KP3: 2, pygame.K_KP4: 3}
