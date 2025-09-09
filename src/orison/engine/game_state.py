from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GameState:
    """Holds global game state. UI-agnostic.

    - player_name: simple placeholder now; will expand later
    - current_scene_id: logical scene key
    """

    player_name: str = ""
    current_scene_id: str = "intro"
    running: bool = True
    # later: inventory, flags, reputation, etc.

    def stop(self) -> None:
        self.running = False

    def goto(self, scene_id: str) -> None:
        self.current_scene_id = scene_id
