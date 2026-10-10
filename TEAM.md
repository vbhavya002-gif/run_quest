# Team Guide

Four members, one shared GitHub repository. Each member **only edits their own files**, which avoids merge conflicts.

## Who owns what

### Member 1: Game core and flow (Team Lead)
Files: `main.py`, `settings.py`, `utils.py`, `game.py`
- Game loop, states (intro / play / paused / won / lost), keyboard events
- Pickups, doors, damage rules, level progression, scoring
- Ideas: save high score, sound effects, difficulty setting

### Member 2: Characters and combat
Files: `entity.py`, `player.py`, `enemies.py`
- Knight movement, sword reach, inventory (boots/shields)
- Walker, Archer and Boss behavior
- Ideas: new enemy type, boss phases, dash move

### Member 3: Levels and hazards
Files: `level_data.py`, `level.py`, `hazards.py`
- The five ASCII maps (legend is at the top of `level_data.py`)
- Parsing maps into walls/items/traps, saw blades, projectiles
- Ideas: new map symbols, moving platforms, a bonus level

### Member 4: Puzzles, graphics and UI
Files: `puzzle.py`, `renderer.py`
- Rune puzzle (symbols, number patterns, timer)
- Everything drawn on screen: tiles, traps, HUD, intro screens, overlays
- Ideas: new pattern types, animations, better icons

## How the files connect (keep these working when you change things)
- `Game` (Member 1) calls `Player.update`, `enemy.update(player, level)`, `enemy.draw()`, `enemy.take_hit(...)`.
- Enemies need: `rect`, `hp`, `max_hp`, `points`, `name`, `update(player, level)`, `draw()`, `take_hit(dmg, from_pos, level)`.
- `Level` (Member 3) exposes: `solid`, `doors`, `coins`, `potions`, `small_keys`, `powerups`, `spikes`, `toggles`, `plates`, `saws`, `enemies`, `projectiles`, `exit_rect`, `altar`, `chest`, `start`.
- `RunePuzzle` (Member 4) exposes: `start()`, `key(idx)`, `update()`, `active`, `stage`, `seq`, `entered`, `pattern`, `options`, `time_left`, `TIME_LIMIT`, `message`.
- `renderer.py` reads from `Game`, `Level` and `Player`. If you rename a field, tell the team.
- Import order has no loops: `settings` -> `utils` -> `entity` -> `player / hazards` -> `enemies` -> `level` -> `renderer` -> `game` -> `main`. Do not import `game` from lower files.

## GitHub workflow (Windows PowerShell)

### Member 1 (once): create the repo
1. On github.com create an empty repository, for example `rune-quest`.
2. In the project folder:
```powershell
git init
git add .
git commit -m "Initial project skeleton"
git branch -M main
git remote add origin https://github.com/<member1-username>/rune-quest.git
git push -u origin main
```
3. On GitHub: Settings -> Collaborators -> add Members 2, 3 and 4.

### Members 2, 3, 4: join
```powershell
git clone https://github.com/<member1-username>/rune-quest.git
cd rune-quest
git checkout -b member2-characters      # member3-levels / member4-puzzles-ui
```

### Everyday loop
```powershell
python main.py                           # test your change
git status
git add enemies.py player.py             # only YOUR files
git commit -m "Add dash move for knight"
git push -u origin member2-characters
```
Then open a Pull Request on GitHub into `main`. Member 1 reviews and merges. Everyone runs `git pull origin main` before starting new work.

### Rules
- Only commit your own files. Need a change in someone else's file? Ask them.
- Test with `python main.py` before every push.
- Keep commit messages short and clear.
