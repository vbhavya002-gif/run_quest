"""
level_data.py
OWNER: Member 3 (levels and hazards)
The 5 level maps, story text and themes. Edit the ASCII maps to design levels.
"""

from settings import *

# --------------------------------------------------------------------------
# Level data
#
# Map legend (every row must be exactly 25 characters, 16 rows total):
#   #  wall / trees            .  floor              P  player start
#   K  magic gate key          E  castle gate/exit   c  coin
#   h  health potion           k  small door key     D  locked door (needs k)
#   G  magic door (opens by puzzle / boss defeat)
#   ^  spike trap              s  blinking spike trap
#   M  saw blade (left-right)  V  saw blade (up-down)
#   1 2 3  numbered floor plates (step on them in order)
#   e  monster (melee)         a  archer           X  final boss
#   S  sword upgrade           W  magic shield     B  speed boots
#   R  rune altar              T  treasure chest
# --------------------------------------------------------------------------
LEVEL_DATA = [
    # ---------------------------------------------------------------- 1
    {
        "name": "The Forgotten Forest",
        "story": "Your knight enters an abandoned forest to find the entrance to a lost kingdom.",
        "bullets": ["Move around using the keyboard.",
                    "Collect coins and a magical key.",
                    "Avoid traps and reach the castle gate."],
        "goal": "Find the key to unlock the next level.",
        "hud_goal": "Goal: Find the key, reach the castle gate",
        "tip": "Spike traps hurt! Walk around them.",
        "start_msg": "Find the golden key, then reach the gate!",
        "theme": {"floor": ((62, 126, 73), (50, 108, 62)), "wall": (28, 66, 48),
                  "edge": (18, 44, 32), "magic": PURPLE, "tree": True},
        "map": [
            "#########################",
            "#P.....#....c.....#...K.#",
            "#......#..........#.....#",
            "#..c...#...^......#..c..#",
            "#.......................#",
            "#.##..^....##....^...##.#",
            "#.##.......##........##.#",
            "#.......c.......c.......#",
            "#.^.......##.##.......^.#",
            "#.........#.c.#.........#",
            "#..c......#####......c..#",
            "#...........^...........#",
            "#.##.............#...##.#",
            "#h.#..c..........#...##.#",
            "#...........c..........E#",
            "#########################",
        ],
    },
    # ---------------------------------------------------------------- 2
    {
        "name": "The Ancient Dungeon",
        "story": "Inside the castle, you discover a maze filled with locked doors and hidden treasures.",
        "bullets": ["Find keys to unlock doors.",
                    "Solve simple puzzles.",
                    "Avoid spikes and moving traps.",
                    "Collect health potions."],
        "goal": "Find the exit while keeping your health above zero.",
        "hud_goal": "Goal: Reach the exit alive",
        "tip": "Walk into a locked door while holding a key. Behind one is a treasure room! Step on plates 1, 2, 3 in order to open the magic door.",
        "start_msg": "Find keys to open the locked doors.",
        "theme": {"floor": ((72, 74, 90), (62, 64, 80)), "wall": (38, 40, 54),
                  "edge": (22, 23, 34), "magic": PURPLE, "tree": False},
        "map": [
            "#########################",
            "#P....#.....#.S...#....c#",
            "#.....#..k..#.....#.....#",
            "#..h..#.....#..c..#..^..#",
            "#.....#..^..#.....#.....#",
            "#.....#.....#...V.#.....#",
            "##.#####.#####D#####.####",
            "#....^.....^....s.......#",
            "#.........M.............#",
            "##.########D##########G##",
            "#.....#...........#.....#",
            "#.c.h.#..1.....3..#..c..#",
            "#.....#..^..2..^..#.....#",
            "#..k..#.s.......s.#.....#",
            "#.....#....M......#....E#",
            "#########################",
        ],
    },
    # ---------------------------------------------------------------- 3
    {
        "name": "The Monster's Territory",
        "story": "Monsters guard the path to the kingdom's treasure.",
        "bullets": ["Fight enemies using a sword.",
                    "Dodge enemy attacks.",
                    "Earn points for defeating monsters.",
                    "Collect power-ups to improve your abilities."],
        "goal": "Defeat the enemies and survive.",
        "hud_goal": "Goal: Defeat all enemies and survive",
        "tip": "SPACE swings your sword (it also smashes arrows). Q = speed boots, E = magic shield.",
        "start_msg": "Defeat every monster to open the gate!",
        "theme": {"floor": ((98, 72, 64), (86, 62, 56)), "wall": (54, 36, 40),
                  "edge": (34, 22, 26), "magic": ORANGE, "tree": False},
        "map": [
            "#########################",
            "#P..........c...........#",
            "#...##.......e.....##..c#",
            "#...##.............##...#",
            "#.......................#",
            "#...c.......a.......c...#",
            "#.........###...........#",
            "#.e..W....###......B...e#",
            "#.........###...........#",
            "#.......................#",
            "#...c...S.....h.....c...#",
            "#.......................#",
            "#...##.....e.......##...#",
            "#h..##.............##...#",
            "#...................a..E#",
            "#########################",
        ],
    },
    # ---------------------------------------------------------------- 4
    {
        "name": "The Chamber of Runes",
        "story": "You discover a magical door protected by ancient symbols.",
        "bullets": ["Match symbols in the correct order.",
                    "Solve a number or pattern puzzle.",
                    "Complete the challenge before the timer ends."],
        "goal": "Unlock the final chamber.",
        "hud_goal": "Goal: Unlock the final chamber",
        "tip": "Step onto the glowing altar in the middle chamber. Press 1-4 to choose runes and answers.",
        "start_msg": "Find the rune altar in the middle chamber.",
        "theme": {"floor": ((54, 54, 98), (46, 46, 88)), "wall": (30, 28, 66),
                  "edge": (18, 16, 44), "magic": CYAN, "tree": False},
        "map": [
            "#########################",
            "#P.....#.........#.....c#",
            "#......#...^.....#......#",
            "#..c...#....M....#......#",
            "#......#....c....#......#",
            "#......#.........#...c..#",
            "#..^...#.........#......#",
            "#...........R....G......#",
            "#......#.........#......#",
            "#...h..#...^.....#......#",
            "#......#.........#...c..#",
            "#..c...#....^....#......#",
            "#......#.........#......#",
            "#......#....c....#....E.#",
            "#......#.........#......#",
            "#########################",
        ],
    },
    # ---------------------------------------------------------------- 5
    {
        "name": "The Lost King's Treasure",
        "story": "A powerful guardian protects the treasure. You must defeat it to restore the lost kingdom.",
        "bullets": ["Fight the final boss.",
                    "Dodge powerful attacks.",
                    "Use collected power-ups strategically.",
                    "Unlock the treasure room after winning."],
        "goal": "Defeat the guardian and complete the quest!",
        "hud_goal": "Goal: Defeat the guardian, claim the treasure",
        "tip": "The guardian glows before each attack. Dodge, then strike while it is dizzy!",
        "start_msg": "The Guardian awakens... use your power-ups wisely!",
        "theme": {"floor": ((114, 94, 60), (102, 84, 52)), "wall": (62, 46, 28),
                  "edge": (38, 28, 16), "magic": GOLD, "tree": False},
        "map": [
            "#########################",
            "#P..................#..c#",
            "#..................h#...#",
            "#....##........##...#...#",
            "#....##....X...##...#...#",
            "#...................#...#",
            "#...................#...#",
            "#...................G.T.#",
            "#...................#...#",
            "#...................#...#",
            "#....##........##...#...#",
            "#....##........##...#...#",
            "#.h.................#..c#",
            "#...................#...#",
            "#..B..........W.....#...#",
            "#########################",
        ],
    },
]
