# Copilot instructions for this repository

Purpose: Make AI helpers productive and aligned with this project’s learning goals. Keep this doc short, concrete, and updated as code lands.

Repository status (2025-09-09)
- Project: “The City That Remembers” — an OOP learning game. Terminal-first, later UI with Pygame.
- Current source is not yet created; design docs exist:
  - `game-story-simple.txt` (plain-language canon), `game-story.txt` (full lore)
  - `python-oop-topics.txt` (ordered OOP roadmap)

Working agreement (how AI should help)
- Each step, propose a tiny goal (1 feature or scene), list changed files, then deliver minimal code + a 4-part note:
  1) What changed (2–4 bullets)
  2) How to run (Windows cmd, copy/paste)
  3) OOP mapping: reference items from `python-oop-topics.txt` by number/name
  4) Next step suggestion (1–2 options)
- Keep explanations brief and concrete; avoid theory unless tied to the current change.
- Pause after touching 3–5 files or introducing a new concept; checkpoint and await confirmation.

Architecture baseline (no code yet)
- Layout: `src/orison/` with `models/` (Characters, Contracts, Marks, Arbiters), `engine/` (GameState, Scenes, Actions), `io/terminal/` (menu, input loop), later `io/pygame/`.
- Tests in `tests/` (pytest). Entry point via `python -m orison`.
- Data seeds in `assets/` or `src/orison/data/` (JSON or simple text).

Conventions
- Python 3.11+, `pyproject.toml` (hatch/poetry), Ruff + Black, type hints where helpful.
- Prefer composition; use inheritance for clear hierarchies (e.g., Arbiters). Use `@dataclass` for plain data.
- No heavy deps at MVP; later add `pygame` for UI.

Iteration order (story × learning)
- Start with Season 1 MVP: audit → interview → caverns → parley → reveal → decision.
- Map features to topics: e.g., Contracts + Marks (Levels 1–3), Arbiters as interfaces/ABCs (Level 2), Scenes via strategy/state (Levels 5, 14), simple descriptors later.

Deliverables per increment
- Code + short comments, tiny smoke test or script, and a “Learning Notes” block linking to `python-oop-topics.txt`.
- Update this file with newly established patterns (keep within 20–50 lines).

Common commands (Windows cmd)
```cmd
py -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install -e .[dev]
pytest -q
ruff check . && ruff format --check .
```

Review checklist before completing a step
- Build/lint/tests pass; entry point runs a small demo.
- Explanations include the OOP mapping and next step.
- Story alignment: changes reference a Season 1 scene and named characters/places from `game-story-simple.txt`.
