from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from ...engine import GameState, Scene
from ...engine.scene import InputPort, OutputPort


@dataclass
class ConsoleIO:
    def write_line(self, text: str) -> None:
        print(text)

    def read_line(self, prompt: str = "") -> str:
        return input(prompt)


class IntroScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id="intro")

    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        io_out.write_line("Welcome to Orison. What is your name?")
        if not state.player_name:
            state.player_name = io_in.read_line("> ")
            io_out.write_line(f"Hello, {state.player_name}.")
        io_out.write_line("Press Enter to begin your first audit.")
        io_in.read_line("")
        state.goto("end")


class EndScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id="end")

    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        io_out.write_line("This is the end of the demo scaffold. Goodbye.")
        state.stop()


SCENES: Dict[str, Scene] = {
    "intro": IntroScene(),
    "end": EndScene(),
}


def run_terminal_app() -> None:
    state = GameState()
    io = ConsoleIO()
    while state.running:
        scene = SCENES.get(state.current_scene_id)
        if not scene:
            io.write_line(f"Unknown scene: {state.current_scene_id}")
            break
        scene.run(state, io, io)
