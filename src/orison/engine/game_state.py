from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
import json
from pathlib import Path

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
    reputation: dict[str, int] = field(default_factory=dict)

    def stop(self) -> None:
        self.running = False

    def goto(self, scene_id: str) -> None:
        self.current_scene_id = scene_id
        
    def adjust_rep(self, faction: str, delta: int) -> None:
        self.reputation[faction] = self.reputation.get(faction, 0) + delta
    
    def get_rep(self, faction: str) -> int:
        return self.reputation.get(faction,0)
    
    def to_dict(self) -> dict:
        return {
            "player_name": self.player_name,
            "current_scene_id": self.current_scene_id,
            "running": [
                {"id": m.id,"kind":m.kind, "is_witness": m.is_witness} for m in self.inventory
            ],
            "flags": dict(self.flags),
            "reputation": dict(self.reputation),
        }
        
    @classmethod
    def from_dict(cls, data:dict) -> "GameState":
        from ..models import Mark
        gs = cls()
        gs.player_name = data.get("player_name","")
        gs.current_scene_id = data.get("current_scene_id","intro")
        gs.running = bool(data.get("running",True))
        gs.inventory = [
            Mark(
                id=item.get("id",""),
                kind=item.get("kind",""),
                is_witness=bool(item.get("is_witness",False)),
            )
            for item in data.get("inventory",[])
        ]
        gs.flags = dict(data.get("flags",{}))
        gs.reputation = dict(data.get("reputation",{}))
        return gs
    
    def _apply(self, other: "GameState") -> None:
        self.player_name = other.player_name
        self.current_scene_id = other.current_scene_id
        self.running = other.running
        self.inventory = list(other.inventory)
        self.flags = dict(other.flags)
        self.reputation = dict(other.reputation)
        
    def save_json(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w",encoding="utf-8") as f:
            json.dump(self.to_dict(),f,ensure_ascii=False,indent=2)
    
    def load_json_into_self(self, path: str | Path) -> None:
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        loaded = GameState.from_dict(data)
        self._apply(loaded)
