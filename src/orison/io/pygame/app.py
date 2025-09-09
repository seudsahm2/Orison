from __future__ import annotations
"""Pygame UI stub.

This module intentionally avoids importing pygame until run_pygame_app() is called,
so the project installs and runs terminal mode without requiring pygame.
"""

from typing import Any, cast

from ...engine import GameState, Scene
from ...engine.scene import InputPort, OutputPort


class PygameIO:
    def __init__(self, screen):
        self.screen = screen

    # Minimal adapters to satisfy protocols; will be fleshed out later
    def write_line(self, text: str) -> None:  # type: ignore[override]
        # Placeholder: render text later
        pass

    def read_line(self, prompt: str = "") -> str:  # type: ignore[override]
        # Placeholder: open text input UI later
        return ""


def run_pygame_app() -> None:
    import importlib

    try:
        pygame = cast(Any, importlib.import_module("pygame"))  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - UI-only path
        print("Pygame is not installed. Install with: pip install .[ui]")
        return

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Orison (Pygame Stub)")

    io = PygameIO(screen)
    state = GameState()

    clock = pygame.time.Clock()
    running = True
    while running and state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                state.stop()
        # For now, just clear the screen
        screen.fill((10, 10, 20))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
