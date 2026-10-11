# WarioWare Clone

A fast-paced collection of micro-games made with Python and Pygame. Every round is a different challenge that lasts only a few seconds. Win to score a point, lose and you burn one of your four lives.

**Play it in your browser:** `https://chsaim.itch.io/warioware`



## The games

| Game | Goal | Controls | Time |
|---|---|---|---|
| **Flappy Gap** | Fly through the gaps between the pillars and survive until the clock runs out | `SPACE` to flap | 5 s |
| **Shooting Gallery** | Shoot 3 real targets. Hit a decoy and you lose | Mouse, left click | 6 s |
| **Simon Says** | Watch the arrow sequence, then repeat it from memory | Arrow keys | 9 s |
| **Maze Rush** | Reach the green exit before time runs out | Arrow keys (hold to keep moving) | 10 s |

## Game modes

From the main menu you can either:

- **Pick a single game** to practice it. You keep playing that game until you lose all 4 lives.
- **Play All** for the full mixed-up WarioWare experience, with a random game every round.

Menu controls: `UP` / `DOWN` to move, `ENTER` or `SPACE` to choose. After a game over, press `SPACE` to go back to the menu.

## Run it locally

You need Python 3.10 or newer.

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install pygame-ce
python main.py
```

The project uses `pygame-ce`, the community edition of Pygame. You still `import pygame` as usual.

## Project structure

```
.
├── main.py              # window setup and the main game loop
├── game_manager.py      # menu, rounds, lives, score and game states
└── minigames/
    ├── base.py          # abstract Minigame class every game inherits from
    ├── flappy_gap.py
    ├── shooting_gallery.py
    ├── simon_says.py
    └── maze_rush.py
```

## How it's built

- **One base class, many games.** Every minigame inherits from an abstract `Minigame` class that provides the timer and the win/lose flags and requires four methods: `handle_event`, `update_game`, `on_timeout` and `draw`. The manager only talks to that interface, so it can run any game without knowing which one it is. Adding a new game means writing one new file and adding it to the list.
- **Game states.** The manager is a small state machine (`MENU`, `READY`, `PLAYING`, `RESULT`, `GAME_OVER`), so each screen has its own update and draw logic.
- **Frame-rate independent.** All movement and timers use delta time (`dt`), so the game plays the same on slow and fast machines.
- **Different rules per game.** Running out of time is a loss in most games, but it is a win in Flappy Gap, because surviving is the goal. Each game decides this in its own `on_timeout`.

## Web build

The browser version is built with [pygbag](https://pypi.org/project/pygbag/), which compiles Pygame to WebAssembly.

```bash
pip install pygbag
pygbag --build <folder containing main.py>
```

The game loop in `main.py` is async (`await asyncio.sleep(0)` every frame), which the web build requires. It still runs normally on desktop.

## Roadmap

- [ ] Difficulty scaling: shorter timers and faster objects as the score rises
- [ ] Sound effects and music
- [ ] High score saving
- [ ] More minigames

## License

Released under the MIT License. See the `LICENSE` file for details.
