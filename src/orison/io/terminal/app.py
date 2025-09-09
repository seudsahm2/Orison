from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from ...engine import GameState, Scene
from ...engine.scene import InputPort, OutputPort
from ...models import Contract, Mark


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
        io_out.write_line("Welcome to Orison.")
        if not state.player_name:
            io_out.write_line("What is your name?")
            state.player_name = io_in.read_line("> ").strip() or "Wanderer"
            io_out.write_line(f"Hello, {state.player_name}.")
        
        io_out.write_line("")
        io_out.write_line("Main Menu")
        io_out.write_line("1) Begin an audit")
        io_out.write_line("2) Quit")
        choice = io_in.read_line("Choose [1-2]: ").strip()
        
        if choice == "1":
            state.goto("audit")
        elif choice == "2":
            state.goto("end")
        else:
            io_out.write_line("I did not understand returning to menu.")
            state.goto("intro")
            

class AuditScene(Scene):
    """A minimal audit to demonstrate routing and models."""
    def __init__(self) -> None:
        super().__init__(scene_id="audit")
        
    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        # Create some example data (not yet stored on GameState; that’s Step 3)
        contract = Contract(
            id="C-001",
            title="Canal Maintainance Oath",
            clauses=["Kep canals clear"],
            is_public=True
        )
        mark = Mark(id="M-WIT-01", kind="witness", is_witness=True)
        
        io_out.write_line("")
        io_out.write_line("Audit: Review Summary")
        io_out.write_line(str(contract))
        io_out.write_line(str(mark))
        
        io_out.write_line("")
        io_out.write_line("What is next?")
        io_out.write_line("1) Return to main menu")
        io_out.write_line("2) Conclude for now")
        choice = io_in.read_line("Choose [1-2]: ").strip()
        
        if choice == "1":
            state.goto("intro")
        elif choice =="2":
            state.goto("end")
        else:
            io_out.write_line("Invalid choice. returning to main menu")
            state.goto("intro")
        

class EndScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id="end")

    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        io_out.write_line("This is the end of the demo scaffold. Goodbye.")
        state.stop()


SCENES: Dict[str, Scene] = {
    "intro": IntroScene(),
    "audit": AuditScene(),
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
