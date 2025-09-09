# Orison — The City That Remembers (scaffold)

Terminal-first Python OOP learning game with a shared engine and a future Pygame UI.

- Story docs: `game-story-simple.txt` (plain), `game-story.txt` (full)
- OOP roadmap: `python-oop-topics.txt`

## Run (terminal)
```cmd
py -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install -e .[dev]
python -m orison
```

## Optional: Run (Pygame stub)
```cmd
pip install -e .[ui]
python -c "from orison.io.pygame.app import run_pygame_app; run_pygame_app()"
```

## Tests
```cmd
pytest -q
```

## Structure
- `src/orison/engine/`: UI-agnostic logic (GameState, Scene)
- `src/orison/io/terminal/`: terminal app using the shared engine
- `src/orison/io/pygame/`: Pygame UI stub; imports pygame only when run
- `src/orison/models/`: data models (to be added gradually)

Design goal: decouple engine from interfaces so both terminal and Pygame use the same game logic.
