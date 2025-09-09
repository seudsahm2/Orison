from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Mark


@dataclass
class GameState:
    """Holds global game state. UI-agnostic.

    - player_name: simple placeholder now; will expand later
    - current_scene_id: logical scene key
    - inventory: player's tokens/marks (Step 3)
    - flags: world/story booleans (Step 3)
    """

    player_name: str = ""
    current_scene_id: str = "intro"
    running: bool = True
    inventory: list["Mark"] = field(default_factory=list)
    flags: dict[str, bool] = field(default_factory=dict)

    def stop(self) -> None:
        self.running = False

    def goto(self, scene_id: str) -> None:
        self.current_scene_id = scene_id
