"""
renderer.py
OWNER: Member 4 (puzzles, graphics and UI)
Everything drawn on screen: world, traps, HUD, intro screen, puzzle UI, overlays.
"""

import math

import pygame

from settings import *
from utils import draw_text, wrap_text, draw_heart, draw_symbol, tile_rect
from enemies import Boss


class RendererMixin:
    """Drawing methods that the Game class inherits."""

    # ---- drawing --------------------------------------------------------
    def draw(self):
        if self.state == "intro":
            self.draw_intro()
        else:
            self.draw_world()
            self.draw_hud()
            if self.puzzle and self.puzzle.active:
                self.draw_puzzle()
            if self.state == "paused":
                self.overlay("PAUSED", "Press P to resume or ESC to quit.", GOLD)
            elif self.state == "won":
                self.overlay("KINGDOM RESTORED!",
                             f"The Guardian is defeated. Final score: {self.player.score}   Coins: {self.player.coins}",
                             GOLD, "Press R to play again or ESC to quit.")
            elif self.state == "lost":
                self.overlay("QUEST FAILED", f"Score: {self.player.score}   Coins: {self.player.coins}",
                             RED, "Press R to restart the quest or ESC to quit.")
        pygame.display.flip()

    def overlay(self, title, line1, color, line2=""):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((8, 12, 20, 215))
        screen.blit(shade, (0, 0))
        draw_text(title, WIDTH // 2, 190, color, HUGE if len(title) < 16 else BIG, center=True)
        draw_text(line1, WIDTH // 2, 270, WHITE, FONT, center=True)
        if line2:
            draw_text(line2, WIDTH // 2, 315, GREY, FONT, center=True)

    def draw_intro(self):
        lv = self.level
        d = lv.data
        screen.fill(BLACK)
        a, b = lv.theme["floor"]
        panel = pygame.Rect(50, 30, WIDTH - 100, HEIGHT - 60)
        pygame.draw.rect(screen, tuple(max(0, c - 40) for c in a), panel, border_radius=14)
        pygame.draw.rect(screen, GOLD, panel, 3, border_radius=14)
        y = 52
        if lv.index == 0:
            draw_text("RUNE QUEST: THE LOST KINGDOM", WIDTH // 2, y, GOLD, FONT, center=True)
            y += 28
        elif self.banner:
            draw_text(self.banner, WIDTH // 2, y, GREEN, FONT, center=True)
            y += 28
        draw_text(f"LEVEL {lv.index + 1}", WIDTH // 2, y + 6, GOLD, FONT, center=True)
        draw_text(d["name"], WIDTH // 2, y + 34, WHITE, BIG, center=True)
        y += 100
        for line in wrap_text(d["story"], FONT, panel.width - 80):
            draw_text(line, panel.x + 40, y, WHITE)
            y += 26
        y += 12
        for b_text in d["bullets"]:
            pygame.draw.circle(screen, GOLD, (panel.x + 48, y + 11), 4)
            draw_text(b_text, panel.x + 62, y, WHITE)
            y += 27
        y += 12
        for line in wrap_text("Goal: " + d["goal"], FONT, panel.width - 80):
            draw_text(line, panel.x + 40, y, GOLD)
            y += 26
        y += 6
        for line in wrap_text("Tip: " + d["tip"], SMALL, panel.width - 80):
            draw_text(line, panel.x + 40, y, CYAN, SMALL)
            y += 21
        draw_text("Move: WASD/Arrows   Sword: SPACE   Boots: Q   Shield: E   Pause: P",
                  WIDTH // 2, panel.bottom - 70, GREY, SMALL, center=True)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            draw_text("Press SPACE to begin", WIDTH // 2, panel.bottom - 40, WHITE, FONT, center=True)

    def draw_world(self):
        lv, p = self.level, self.player
        th = lv.theme
        # floor
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(screen, th["floor"][(x + y) % 2], (x * TILE, y * TILE, TILE, TILE))
        # walls
        for (x, y) in lv.solid:
            if (x, y) in lv.doors:
                continue
            r = tile_rect((x, y))
            pygame.draw.rect(screen, th["wall"], r)
            if th["tree"]:
                pygame.draw.circle(screen, tuple(min(255, c + 22) for c in th["wall"]), r.center, 13)
                pygame.draw.circle(screen, th["edge"], r.center, 13, 2)
            else:
                pygame.draw.rect(screen, th["edge"], r, 2)
                pygame.draw.line(screen, th["edge"], (r.x, r.centery), (r.right, r.centery), 1)
                off = 8 if (y % 2) else 22
                pygame.draw.line(screen, th["edge"], (r.x + off, r.y), (r.x + off, r.centery), 1)
                pygame.draw.line(screen, th["edge"], (r.x + 30 - off, r.centery), (r.x + 30 - off, r.bottom), 1)
        self.draw_doors()
        self.draw_plates()
        self.draw_traps()
        self.draw_altar_and_chest()
        self.draw_exit()
        self.draw_items()
        for s in lv.saws:
            s.draw()
        for e in lv.enemies:
            e.draw()
        for pr in lv.projectiles:
            pr.draw()
        p.draw()
        if p.slash_t > 0:
            ang = math.atan2(p.facing.y, p.facing.x)
            reach = 28 + 5 * p.sword
            pts = []
            for i in range(9):
                a = ang + math.radians(-60 + 15 * i)
                pts.append((p.rect.centerx + math.cos(a) * reach, p.rect.centery + math.sin(a) * reach))
            pygame.draw.lines(screen, WHITE, False, pts, 4 if p.slash_t > 4 else 2)
        # boss health bar
        for e in lv.enemies:
            if isinstance(e, Boss):
                bar = pygame.Rect(WIDTH // 2 - 160, 9, 320, 14)
                pygame.draw.rect(screen, BLACK, bar.inflate(4, 4), border_radius=4)
                pygame.draw.rect(screen, (90, 30, 40), bar)
                pygame.draw.rect(screen, RED if e.enraged else PURPLE,
                                 (bar.x, bar.y, int(bar.w * max(0, e.hp) / e.max_hp), bar.h))
                draw_text("THE GUARDIAN", WIDTH // 2, 7, WHITE, TINY, center=True)

    def draw_doors(self):
        lv = self.level
        t = lv.t
        for pos, kind in lv.doors.items():
            r = tile_rect(pos)
            if kind == "D":
                pygame.draw.rect(screen, BROWN, r)
                pygame.draw.rect(screen, (70, 44, 24), r, 3)
                pygame.draw.circle(screen, GOLD, r.center, 5)
                pygame.draw.rect(screen, GOLD, (r.centerx - 1, r.centery, 3, 8))
            else:
                glow = 140 + int(60 * math.sin(t / 10))
                col = lv.theme["magic"]
                pygame.draw.rect(screen, tuple(min(255, int(c * glow / 255)) for c in col), r)
                pygame.draw.rect(screen, WHITE, r, 2)
                pygame.draw.circle(screen, WHITE, r.center, 7, 2)
                pygame.draw.line(screen, WHITE, (r.x + 6, r.centery), (r.right - 6, r.centery), 2)

    def draw_plates(self):
        lv = self.level
        for pos, n in lv.plates.items():
            r = tile_rect(pos)
            lit = n in lv.plate_lit
            pygame.draw.rect(screen, (60, 190, 100) if lit else DARK_GREY, r.inflate(-6, -6), border_radius=6)
            pygame.draw.rect(screen, WHITE, r.inflate(-6, -6), 2, border_radius=6)
            draw_text(str(n), r.centerx, r.y + 5, WHITE if not lit else BLACK, FONT, center=True)

    def draw_traps(self):
        lv = self.level
        for pos in lv.spikes:
            self.draw_spikes(tile_rect(pos), 1.0)
        for pos in lv.toggles:
            r = tile_rect(pos)
            if lv.toggle_on():
                self.draw_spikes(r, 1.0)
            elif lv.toggle_warning() and (lv.t // 4) % 2 == 0:
                self.draw_spikes(r, 0.45, GOLD)
            else:
                for dx in (9, 23):
                    for dy in (9, 23):
                        pygame.draw.circle(screen, (30, 30, 40), (r.x + dx, r.y + dy), 2)

    def draw_spikes(self, r, scale, color=GREY):
        pygame.draw.rect(screen, (40, 40, 52), r.inflate(-4, -4))
        h = int(20 * scale)
        for i in range(3):
            x = r.x + 6 + i * 9
            pygame.draw.polygon(screen, color, [(x - 4, r.bottom - 5), (x + 4, r.bottom - 5), (x, r.bottom - 5 - h)])
            if scale >= 1.0:
                pygame.draw.circle(screen, RED, (x, r.bottom - 5 - h), 2)

    def draw_altar_and_chest(self):
        lv = self.level
        if lv.altar:
            r = lv.altar
            pulse = 3 + int(2 * math.sin(pygame.time.get_ticks() / 250))
            col = (80, 80, 110) if lv.puzzle_solved else CYAN
            pygame.draw.circle(screen, (30, 30, 70), r.center, 15)
            pygame.draw.circle(screen, col, r.center, 13 + pulse, 2)
            draw_symbol(3, r.center, 12, col)
        if lv.chest:
            r = lv.chest.inflate(-6, -10)
            ready = lv.boss_dead
            pygame.draw.rect(screen, BROWN, r, border_radius=4)
            pygame.draw.rect(screen, GOLD, (r.x, r.y + 4, r.w, 4))
            pygame.draw.rect(screen, GOLD, (r.centerx - 3, r.y + 3, 6, 9))
            pygame.draw.rect(screen, BLACK, r, 2, border_radius=4)
            if ready:
                for i in range(3):
                    a = pygame.time.get_ticks() / 300 + i * 2.1
                    pygame.draw.circle(screen, WHITE, (int(r.centerx + math.cos(a) * 17), int(r.centery + math.sin(a) * 12)), 2)

    def draw_exit(self):
        lv = self.level
        if not lv.exit_rect:
            return
        r = lv.exit_rect
        ready = self.exit_ready()
        color = GOLD if ready else DARK_GREY
        pygame.draw.rect(screen, color, r, border_top_left_radius=13, border_top_right_radius=13)
        pygame.draw.rect(screen, WHITE, r, 2, border_top_left_radius=13, border_top_right_radius=13)
        inner = pygame.Rect(r.x + 6, r.y + 8, r.w - 12, r.h - 8)
        pygame.draw.rect(screen, (255, 235, 150) if ready else BLACK, inner, border_top_left_radius=7,
                         border_top_right_radius=7)
        if not ready:
            pygame.draw.rect(screen, GOLD, (r.centerx - 4, r.centery, 8, 7))
            pygame.draw.circle(screen, GOLD, (r.centerx, r.centery), 4, 2)

    def draw_items(self):
        lv = self.level
        t = pygame.time.get_ticks()
        for c in lv.coins:
            w = max(3, int(abs(math.cos(t / 250 + c.x)) * 7))
            pygame.draw.ellipse(screen, GOLD, (c.centerx - w, c.centery - 7, w * 2, 14))
            pygame.draw.ellipse(screen, WHITE, (c.centerx - w, c.centery - 7, w * 2, 14), 1)
        for p in lv.potions:
            pygame.draw.rect(screen, RED, (p.x + 3, p.y + 6, 14, 13), border_radius=5)
            pygame.draw.rect(screen, WHITE, (p.x + 7, p.y + 1, 6, 6))
            pygame.draw.circle(screen, WHITE, (p.x + 7, p.y + 11), 2)
        if lv.gate_key and not self.player.has_key:
            k = lv.gate_key
            bob = int(math.sin(t / 200) * 2)
            pygame.draw.circle(screen, GOLD, (k.centerx - 3, k.centery + bob), 7, 3)
            pygame.draw.rect(screen, GOLD, (k.centerx + 2, k.centery - 2 + bob, 9, 4))
            pygame.draw.circle(screen, WHITE, (k.centerx - 3, k.centery + bob), 12, 1)
        for k in lv.small_keys:
            pygame.draw.circle(screen, (200, 225, 255), (k.centerx - 3, k.centery), 5, 2)
            pygame.draw.rect(screen, (200, 225, 255), (k.centerx + 1, k.centery - 1, 8, 3))
        for rect, kind in lv.powerups:
            bob = int(math.sin(t / 220 + rect.x) * 2)
            col = {"S": ORANGE, "W": CYAN, "B": GREEN}[kind]
            pygame.draw.circle(screen, col, (rect.centerx, rect.centery + bob), 11)
            pygame.draw.circle(screen, WHITE, (rect.centerx, rect.centery + bob), 11, 2)
            draw_text(kind, rect.centerx, rect.centery - 9 + bob, BLACK, SMALL, center=True)

    def draw_hud(self):
        p, lv = self.player, self.level
        y0 = ROWS * TILE
        pygame.draw.rect(screen, BLACK, (0, y0, WIDTH, HUD))
        pygame.draw.line(screen, GOLD, (0, y0), (WIDTH, y0), 2)
        draw_text(f"LEVEL {lv.index + 1}/5: {lv.data['name']}", 14, y0 + 6, GOLD)
        draw_text(lv.data["hud_goal"], 790 - SMALL.size(lv.data["hud_goal"])[0], y0 + 9, WHITE, SMALL)
        for i in range(p.max_hp):
            draw_heart(14 + i * 26, y0 + 36, 20, i < p.hp)
        x = 160
        x += draw_text(f"Score: {p.score}", x, y0 + 36) + 24
        x += draw_text(f"Coins: {p.coins}", x, y0 + 36) + 24
        if lv.gate_key or lv.index == 0:
            draw_text(f"Magic key: {'YES' if p.has_key else 'NO'}", x, y0 + 36, GOLD if p.has_key else WHITE)
        elif lv.index == 1:
            draw_text(f"Door keys: {p.small_keys}", x, y0 + 36, (200, 225, 255))
        inv = f"[Q] Boots x{p.boots}   [E] Shield x{p.shields}   Sword Lv {1 + p.sword}"
        draw_text(inv, 14, y0 + 64, WHITE, SMALL)
        if p.boots_t > 0:
            draw_text(f"SPEED {p.boots_t // FPS + 1}s", 300, y0 + 64, GREEN, SMALL)
        if p.shield_t > 0:
            draw_text(f"SHIELD {p.shield_t // FPS + 1}s", 300 if p.boots_t == 0 else 385, y0 + 64, CYAN, SMALL)
        if self.message:
            font = SMALL if SMALL.size(self.message)[0] <= 400 else TINY
            draw_text(self.message, 790 - font.size(self.message)[0], y0 + 64, GOLD, font)

    def draw_puzzle(self):
        pz = self.puzzle
        shade = pygame.Surface((WIDTH, ROWS * TILE), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 195))
        screen.blit(shade, (0, 0))
        box = pygame.Rect(110, 50, 580, 410)
        pygame.draw.rect(screen, (30, 30, 70), box, border_radius=14)
        pygame.draw.rect(screen, CYAN, box, 3, border_radius=14)
        draw_text("CHAMBER OF RUNES", WIDTH // 2, box.y + 12, CYAN, BIG, center=True)

        # timer bar
        frac = max(0.0, pz.time_left / pz.TIME_LIMIT)
        bar = pygame.Rect(box.x + 30, box.y + 70, box.w - 130, 16)
        pygame.draw.rect(screen, BLACK, bar, border_radius=6)
        col = GREEN if frac > 0.5 else (GOLD if frac > 0.25 else RED)
        pygame.draw.rect(screen, col, (bar.x, bar.y, int(bar.w * frac), bar.h), border_radius=6)
        draw_text(f"{max(0, pz.time_left) // FPS + 1}s", bar.right + 14, bar.y - 4, col)

        cy = box.y + 170
        if pz.stage == "memorize":
            draw_text("Memorize the rune order!", WIDTH // 2, box.y + 105, WHITE, FONT, center=True)
            for i, s in enumerate(pz.seq):
                cx = WIDTH // 2 + (i - 1.5) * 100
                pygame.draw.rect(screen, (50, 50, 100), (cx - 38, cy - 38, 76, 76), border_radius=10)
                draw_symbol(s, (int(cx), cy), 40, RUNE_COLORS[s])
                draw_text(str(i + 1), cx, cy - 62, GREY, SMALL, center=True)
            draw_text(f"Hiding in {pz.show_timer // FPS + 1}...", WIDTH // 2, cy + 60, GREY, SMALL, center=True)
        elif pz.stage == "sequence":
            draw_text("Enter the runes in the same order", WIDTH // 2, box.y + 105, WHITE, FONT, center=True)
            for i in range(4):
                cx = WIDTH // 2 + (i - 1.5) * 100
                pygame.draw.rect(screen, (50, 50, 100), (cx - 38, cy - 38, 76, 76), border_radius=10)
                pygame.draw.rect(screen, GREY, (cx - 38, cy - 38, 76, 76), 2, border_radius=10)
                if i < len(pz.entered):
                    draw_symbol(pz.entered[i], (int(cx), cy), 40, RUNE_COLORS[pz.entered[i]])
        else:  # pattern stage
            draw_text("What number comes next?", WIDTH // 2, box.y + 105, WHITE, FONT, center=True)
            text = ",  ".join(str(n) for n in pz.pattern) + ",  ?"
            draw_text(text, WIDTH // 2, cy - 22, GOLD, BIG, center=True)
            for i, opt in enumerate(pz.options):
                cx = WIDTH // 2 + (i - 1.5) * 120
                rr = pygame.Rect(int(cx) - 48, cy + 50, 96, 70)
                pygame.draw.rect(screen, (50, 50, 100), rr, border_radius=10)
                pygame.draw.rect(screen, CYAN, rr, 2, border_radius=10)
                draw_text(f"{i + 1}", rr.x + 8, rr.y + 4, GREY, SMALL)
                draw_text(str(opt), rr.centerx, rr.y + 28, WHITE, FONT, center=True)

        if pz.stage in ("memorize", "sequence"):
            draw_text("Rune keys:", box.x + 40, box.y + 295, GREY, SMALL)
            for i in range(4):
                cx = box.x + 190 + i * 100
                draw_text(str(i + 1), cx - 28, box.y + 290, WHITE, FONT)
                draw_symbol(i, (cx + 6, box.y + 303), 22, RUNE_COLORS[i])
        if pz.message:
            draw_text(pz.message, WIDTH // 2, box.y + 335, GOLD, SMALL, center=True)
        draw_text("Press 1-4 to answer.  ESC to step back (no penalty).", WIDTH // 2, box.bottom - 30, GREY, TINY, center=True)
