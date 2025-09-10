from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
import time
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
        io_out.write_line("2) Pick up a Witness Mark (demo)")
        io_out.write_line("3) Quit")
        choice = io_in.read_line("Choose [1-3]: ").strip()
        choice = choice or "3"  # Enter defaults to Quit (for test_smoke)

        if choice == "1":
            state.goto("audit")
        elif choice == "2":
            has_witness = any(m.is_witness for m in state.inventory)
            if not has_witness:
                state.inventory.append(Mark(id="M-WIT-DEMO", kind="witness", is_witness=True))
                state.flags["has_witness_mark"] = True
                io_out.write_line("You received a Witness Mark.")
            else:
                io_out.write_line("You already carry a Witness Mark.")
            state.goto("intro")
        elif choice == "3":
            state.goto("end")
        else:
            io_out.write_line("I did not understand. Returning to menu.")
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
        
        has_witness = any(m.is_witness for m in state.inventory)
        flag_has_witness = state.flags.get("has_witness_mark", False)
        
        io_out.write_line("")
        io_out.write_line("Audit: Review Summary")
        io_out.write_line(str(contract))
        io_out.write_line(f"You hold a witness mark: {'yes' if has_witness else 'no'} "
                          f"(flag: {'yes' if flag_has_witness else 'no'})")
        
        io_out.write_line("")
        io_out.write_line("What is next?")
        io_out.write_line("1) Return to main menu")
        io_out.write_line("2) Conclude for now")
        io_out.write_line("3) Investigate (chck ledger or visit dock)")
        choice = io_in.read_line("Choose [1-3]: ").strip()
        choice = choice or "1"
        
        if choice == "1":
            state.goto("intro")
            return
        elif choice == "2":
            state.goto("end")
            return
        elif choice == "3":
            def handle_check_ledger() -> str:
                state.flags["checked_ledger"] = True
                io_out.write_line("Ledger notes: backlog of repairs and mismatched reports.")
                return "intro"
            
            def handle_visit_dock() -> str:
                state.flags["visited_dock"] = True
                io_out.write_line("At the docks: faint smell of blackwater and nervous whispers.")
                return "intro"
            
            strategies = {
                "1": handle_check_ledger,
                "2": handle_visit_dock,
                "3": lambda: "intro",
            }
            
            io_out.write_line("")
            io_out.write_line("Investigation")
            io_out.write_line("1) Check ledger")
            io_out.write_line("2) Visit dock")
            io_out.write_line("3) Back")
            sub = io_in.read_line("Choose [1-3]: ").strip() or "3"
            
            next_scene = strategies.get(sub, lambda: "intro")()
            state.goto(next_scene)
            return
        
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
