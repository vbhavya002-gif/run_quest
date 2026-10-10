"""
game.py
OWNER: Member 1 (Team Lead: game core and flow)
Game rules: state machine, input events, pickups, doors, damage, level changes.
"""

import sys

import pygame

from settings import *
from utils import tile_rect
from player import Player
from enemies import Boss
from level import Level
from puzzle import RunePuzzle, PUZZLE_KEYS
from renderer import RendererMixin


# --------------------------------------------------------------------------
# The game itself
# --------------------------------------------------------------------------
class Game(RendererMixin):
    def __init__(self):
        self.reset_quest()

    # ---- setup ----------------------------------------------------------
    def reset_quest(self):
        self.player = Player()
        self.message, self.msg_timer = "", 0
        self.banner = ""
        self.load_level(0)
        self.state = "intro"

    def load_level(self, index):
        self.level_index = index
        self.level = Level(index)
        self.player.enter_level(self.level.start)
        self.puzzle = RunePuzzle() if self.level.altar else None
        self.say(self.level.data["start_msg"], 300)

    def say(self, text, frames=120):
        self.message, self.msg_timer = text, frames

    def hint(self, text, frames=90):
        if self.msg_timer < 30 or self.message == text:
            self.say(text, frames)

    # ---- events ---------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if self.state == "intro":
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self.state = "play"
            elif key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif self.state == "play":
            if self.puzzle and self.puzzle.active:
                if key == pygame.K_ESCAPE:
                    self.puzzle.active = False
                    self.puzzle.altar_ready = False
                    self.say("You step back from the altar. Step on it again to retry.", 150)
                elif key in PUZZLE_KEYS:
                    if self.puzzle.key(PUZZLE_KEYS[key]) == "solved":
                        self.solve_puzzle()
                return
            if key == pygame.K_SPACE:
                self.player_attack()
            elif key == pygame.K_q:
                p = self.player
                if p.boots > 0 and p.boots_t == 0:
                    p.boots -= 1
                    p.boots_t = 7 * FPS
                    self.say("Speed boots activated!", 90)
                elif p.boots == 0:
                    self.say("You have no speed boots. Find some!", 90)
            elif key == pygame.K_e:
                p = self.player
                if p.shields > 0 and p.shield_t == 0:
                    p.shields -= 1
                    p.shield_t = 6 * FPS
                    self.say("Magic shield up! You are protected.", 90)
                elif p.shields == 0:
                    self.say("You have no magic shields. Find some!", 90)
            elif key == pygame.K_p:
                self.state = "paused"
            elif key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif self.state == "paused":
            if key == pygame.K_p:
                self.state = "play"
            elif key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif self.state in ("won", "lost"):
            if key == pygame.K_r:
                self.reset_quest()
            elif key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # ---- player actions -------------------------------------------------
    def player_attack(self):
        p, lv = self.player, self.level
        if p.attack_cd > 0:
            return
        p.attack_cd = 16
        p.slash_t = 10
        box = p.attack_rect()
        dmg = 1 + p.sword
        for e in lv.enemies[:]:
            if box.colliderect(e.rect):
                e.take_hit(dmg, p.rect.center, lv)
                if e.hp <= 0:
                    lv.enemies.remove(e)
                    p.score += e.points
                    p.coins += 1
                    self.say(f"{e.name} defeated! +{e.points} points", 110)
        for pr in lv.projectiles:           # swords can smash incoming shots
            if box.colliderect(pr.rect):
                pr.alive = False
                p.score += 5

    def hurt(self, text="Ouch! You were hit."):
        p = self.player
        if p.invuln > 0:
            return
        if p.shield_t > 0:
            p.invuln = 20
            self.say("Your shield blocked the hit!", 60)
            return
        p.hp -= 1
        p.invuln = 70
        self.say(text, 80)
        if p.hp <= 0:
            self.state = "lost"

    def solve_puzzle(self):
        p, lv = self.player, self.level
        secs = max(0, self.puzzle.time_left // FPS)
        bonus = 300 + secs * 10
        self.puzzle.active = False
        lv.puzzle_solved = True
        lv.open_doors("G")
        p.score += bonus
        self.say(f"Runes unlocked! The final chamber opens. +{bonus} points", 200)

    # ---- per-frame update ----------------------------------------------
    def update(self):
        if self.msg_timer > 0:
            self.msg_timer -= 1
            if self.msg_timer == 0:
                self.message = ""
        if self.state != "play":
            return
        p, lv = self.player, self.level

        # Level 4 puzzle running: world is frozen, only the timer counts down.
        if self.puzzle and self.puzzle.active:
            if self.puzzle.update() == "failed":
                self.puzzle.active = False
                self.puzzle.altar_ready = False
                p.hp -= 1
                p.invuln = 60
                self.say("Time's up! The runes shock you (-1 heart). Try again!", 180)
                if p.hp <= 0:
                    self.state = "lost"
            return

        p.update(pygame.key.get_pressed(), lv)
        lv.t += 1
        for s in lv.saws:
            s.update(lv)
        for e in lv.enemies:
            e.update(p, lv)
        for pr in lv.projectiles:
            pr.update(lv)
        lv.projectiles = [pr for pr in lv.projectiles if pr.alive]

        self.check_pickups()
        self.check_doors()
        self.check_plates()
        self.check_altar()
        self.check_damage()
        if self.state != "play":
            return
        self.check_events()
        self.check_exit()

    def check_pickups(self):
        p, lv = self.player, self.level
        for c in lv.coins[:]:
            if p.rect.colliderect(c):
                lv.coins.remove(c)
                p.coins += 1
                p.score += 10
                self.say("Coin collected! +10", 50)
        for pt in lv.potions[:]:
            if p.rect.colliderect(pt):
                lv.potions.remove(pt)
                p.hp = min(p.max_hp, p.hp + 2)
                self.say("Health potion: +2 hearts!", 100)
        for k in lv.small_keys[:]:
            if p.rect.colliderect(k):
                lv.small_keys.remove(k)
                p.small_keys += 1
                p.score += 25
                self.say("Door key found! Walk into a locked door to open it.", 140)
        if lv.gate_key and not p.has_key and p.rect.colliderect(lv.gate_key):
            p.has_key = True
            p.score += 50
            self.say("You found the magical key! Reach the castle gate!", 150)
        for entry in lv.powerups[:]:
            rect, kind = entry
            if p.rect.colliderect(rect):
                lv.powerups.remove(entry)
                if kind == "S":
                    p.sword += 1
                    self.say("Sword upgraded! More damage and reach.", 150)
                elif kind == "W":
                    p.shields += 1
                    self.say("Magic shield collected! Press E to use it.", 150)
                else:
                    p.boots += 1
                    self.say("Speed boots collected! Press Q to use them.", 150)

    def check_doors(self):
        p, lv = self.player, self.level
        touch = p.rect.inflate(12, 12)
        for pos, kind in list(lv.doors.items()):
            if not touch.colliderect(tile_rect(pos)):
                continue
            if kind == "D":
                if p.small_keys > 0:
                    p.small_keys -= 1
                    lv.open_door(pos)
                    self.say("Click! The door is unlocked.", 100)
                else:
                    self.hint("This door is locked. Find a key!")
            else:
                if lv.index == 1:
                    self.hint("A magic seal. Try the numbered plates...")
                elif lv.index == 3:
                    self.hint("Sealed by runes. Solve the altar puzzle!")
                else:
                    self.hint("The treasure room is sealed. Defeat the Guardian!")

    def check_plates(self):
        p, lv = self.player, self.level
        if not lv.plates:
            return
        standing = None
        for pos in lv.plates:
            if tile_rect(pos).collidepoint(p.rect.center):
                standing = pos
        if standing == lv.on_plate:
            return
        lv.on_plate = standing
        if standing is None or lv.plate_next > 3:
            return
        n = lv.plates[standing]
        if n == lv.plate_next:
            lv.plate_lit.add(n)
            lv.plate_next += 1
            if lv.plate_next > 3:
                lv.open_doors("G")
                p.score += 100
                self.say("Click! The magic door opens! +100", 150)
            else:
                self.say(f"Plate {n} glows. Next: plate {lv.plate_next}.", 100)
        elif n > lv.plate_next:
            lv.plate_next = 1
            lv.plate_lit.clear()
            self.say("Wrong order! The plates reset. Try 1, 2, 3.", 120)

    def check_altar(self):
        lv = self.level
        if not lv.altar or lv.puzzle_solved:
            return
        if self.player.rect.colliderect(lv.altar):
            if self.puzzle.altar_ready:
                self.puzzle.start()
        else:
            self.puzzle.altar_ready = True

    def check_damage(self):
        p, lv = self.player, self.level
        hb = p.rect.inflate(-6, -6)
        for pos in lv.spikes:
            if hb.colliderect(tile_rect(pos).inflate(-8, -8)):
                self.hurt("Spikes! Watch your step.")
        if lv.toggle_on():
            for pos in lv.toggles:
                if hb.colliderect(tile_rect(pos).inflate(-8, -8)):
                    self.hurt("Spikes shot up!")
        for s in lv.saws:
            if hb.colliderect(s.rect.inflate(-2, -2)):
                self.hurt("The saw blade got you!")
        for e in lv.enemies:
            if hb.colliderect(e.rect):
                self.hurt(f"{e.name} hit you!")
        for pr in lv.projectiles:
            if pr.alive and hb.colliderect(pr.rect):
                pr.alive = False
                self.hurt("You were hit by a magic shot!")
        lv.projectiles = [pr for pr in lv.projectiles if pr.alive]

    def check_events(self):
        p, lv = self.player, self.level
        if lv.index == 2 and not lv.cleared and not lv.enemies:
            lv.cleared = True
            p.score += 300
            self.say("All monsters defeated! The gate is open! +300", 200)
        if lv.has_boss and not lv.boss_dead and not any(isinstance(e, Boss) for e in lv.enemies):
            lv.boss_dead = True
            lv.projectiles.clear()
            lv.enemies.clear()
            lv.open_doors("G")
            self.say("The Guardian falls! The treasure room is open!", 240)
        if lv.chest and lv.boss_dead and lv.chest.collidepoint(p.rect.center):
            p.score += 1000 + p.hp * 100
            self.state = "won"

    def exit_ready(self):
        p, lv = self.player, self.level
        if lv.index == 0:
            return p.has_key
        if lv.index == 2:
            return not lv.enemies
        return True

    def check_exit(self):
        p, lv = self.player, self.level
        if not lv.exit_rect or not lv.exit_rect.collidepoint(p.rect.center):
            return
        if not self.exit_ready():
            if lv.index == 0:
                self.hint("The gate is locked. Find the golden key!")
            else:
                self.hint("The gate is sealed. Defeat every monster!")
            return
        p.score += 200
        self.banner = f"Level {lv.index + 1} complete! +200 points"
        self.load_level(lv.index + 1)
        self.state = "intro"
