# Rune Quest: The Lost Kingdom

A small 2D fantasy adventure game made with Python and Pygame. It uses simple shapes for art, so you do not need any image or sound files.

## Features
- Five levels: forest, dungeon, monster territory, rune chamber, and final guardian
- Keyboard movement, walls, collision detection
- Coins, magic key, door keys, health potions, hearts
- Traps: spikes, blinking spikes, moving saw blades
- Sword combat, patrolling/chasing monsters, archers, and a boss fight
- Power-ups: sword upgrades, speed boots, magic shields
- Plate puzzle (Level 2) and a timed rune + number-pattern puzzle (Level 4)
- Win/lose screens, restart with `R`

## Requirements
- Python 3.10 or newer recommended
- Pygame 2.1 or newer

## Easiest ways to play

1. **Double-click `run_game.bat`** (Windows). It installs pygame if needed and starts the game. Python must be installed first (python.org, tick "Add python.exe to PATH").
2. **Build a standalone `RuneQuest.exe`** that runs on any Windows PC with no Python: double-click `build_exe.bat`. The finished file appears in `dist\RuneQuest.exe`.
3. **Let GitHub build the .exe**: push the project, open the repo's **Actions** tab, choose **Build Windows app**, click **Run workflow**, then download `RuneQuest-windows` from the finished run.
4. macOS/Linux: `sh run_game.sh`

If the game ever crashes, it writes the error to `crash_log.txt` next to the game.

## Run manually on Windows
```bash
python -m pip install -r requirements.txt
python main.py
```
If `python` is not recognized, use `py -m pip install -r requirements.txt` and `py main.py`.

## Controls
- Move: `W A S D` or arrow keys
- Sword: `SPACE`  |  Speed boots: `Q`  |  Magic shield: `E`
- Rune puzzle (Level 4): `1`-`4`
- Pause: `P`  |  Quit / close puzzle: `ESC`  |  Restart after win or defeat: `R`

## Project structure
| File | What it does | Owner |
|------|--------------|-------|
| `main.py` | Entry point and game loop | Member 1 |
| `settings.py` | Window, constants, colors, fonts | Member 1 |
| `utils.py` | Shared drawing helpers and wall collision | Member 1 |
| `game.py` | Game rules: events, pickups, doors, damage, level changes | Member 1 |
| `entity.py` | Base class for moving things | Member 2 |
| `player.py` | The knight | Member 2 |
| `enemies.py` | Walker, Archer, and Boss | Member 2 |
| `level_data.py` | The 5 ASCII maps, story text, themes | Member 3 |
| `level.py` | Builds a playable level from a map | Member 3 |
| `hazards.py` | Magic shots and saw blades | Member 3 |
| `run_game.bat`, `build_exe.bat`, `run_game.sh`, `.github/` | One-click launcher, .exe builder, GitHub build | Member 1 |
| `puzzle.py` | Rune puzzle logic and timer | Member 4 |
| `renderer.py` | All drawing: world, HUD, intro, puzzle UI | Member 4 |

See `TEAM.md` for who does what and the GitHub workflow.

## Troubleshooting
- `ModuleNotFoundError: No module named 'pygame'` -> run `python -m pip install pygame`.
- Window opens and closes immediately -> run it from the VS Code terminal to read the error.
- Always run from inside the project folder (`python main.py`), because the files import each other.
