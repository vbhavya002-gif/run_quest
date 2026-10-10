"""
main.py
OWNER: Member 1 (Team Lead: game core and flow)
Entry point. Run with:  python main.py   (or double-click run_game.bat)
"""

import os
import sys
import traceback

import pygame

from settings import clock, FPS
from game import Game


def main():
    game = Game()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            game.handle_event(event)
        game.update()
        game.draw()


def app_folder():
    """Folder next to the .exe (when packaged) or next to this file."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def run():
    """Run the game; if it crashes, save the error to crash_log.txt."""
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        log = os.path.join(app_folder(), "crash_log.txt")
        with open(log, "w") as f:
            traceback.print_exc(file=f)
        traceback.print_exc()
        try:  # friendly pop-up on Windows
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0, f"Rune Quest crashed.\nDetails saved to:\n{log}", "Rune Quest", 0x10)
        except Exception:
            pass
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    run()
