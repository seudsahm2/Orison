from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:  # avoid import cycle at runtime
    from .game_state import GameState


class OutputPort(Protocol):
    def write_line(self, text: str) -> None: ...


class InputPort(Protocol):
    def read_line(self, prompt: str = "") -> str: ...


class Scene(ABC):
    """Abstract base class for scenes.

    UI-independent: interacts via InputPort/OutputPort protocols so both
    terminal and pygame UIs can adapt without changing scene logic.
    """

    scene_id: str

    def __init__(self, scene_id: str) -> None:
        self.scene_id = scene_id

    @abstractmethod
    def run(self, state: "GameState", io_in: InputPort, io_out: OutputPort) -> None:
        """Execute one scene frame/loop.

        Concrete scenes decide when to transition state or stop the game.
        """
        raise NotImplementedError
