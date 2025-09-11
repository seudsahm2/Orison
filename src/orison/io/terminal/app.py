from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from ...engine import GameState, Scene
from ...engine.scene import InputPort, OutputPort
from ...models import Contract, Mark
from ...models.arbiter import TerminalArbiter


@dataclass
class ConsoleIO:
    def write_line(self, text: str) -> None:
        print(text)

    def read_line(self, prompt: str = "") -> str:
        return input(prompt)


# Step 11: centralized input guard (single-shot with safe default)
def _choice_or_default(io_in: InputPort, io_out: OutputPort, prompt: str, valid: set[str], default: str) -> str:
    raw = (io_in.read_line(prompt) or "").strip()
    if not raw:
        return default
    if raw in valid:
        return raw
    io_out.write_line(f"Invalid choice. Using default [{default}].")
    return default


class IntroScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id="intro")

    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        io_out.write_line("Welcome to Orison.")
        if not state.player_name:
            io_out.write_line("What is your name?")
            state.player_name = io_in.read_line("> ").strip() or "Wanderer"
            io_out.write_line(f"Hello, {state.player_name}.")
        
        scribes = state.get_rep("scribes")
        mariners = state.get_rep("mariners")
        io_out.write_line(f"Reputation -- Scribes: {scribes} | Mariners: {mariners}")

        io_out.write_line("")
        io_out.write_line("Main Menu")
        io_out.write_line("1) Begin an audit")
        io_out.write_line("2) Pick up a Witness Mark (demo)")
        io_out.write_line("3) Quit")
        io_out.write_line("4) Save game")
        io_out.write_line("5) Load game")
        io_out.write_line("6) Continue (load last save)")
        choice = _choice_or_default(io_in, io_out, "Choose [1-6]: ", set("123456"), default="3")

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
        elif choice == "4":
            path = io_in.read_line("Save path [save_game/save_orison.json]: ").strip() or "save_game/save_orison.json"
            try:
                state.save_json(path)
                io_out.write_line(f"Saved to {path}")
            except OSError as e:
                io_out.write_line(f"Could not save: {e}")
            state.goto("intro")
        elif choice == "5":
            path = io_in.read_line("Load path [save_game/save_orison.json]: ").strip() or "save_game/save_orison.json"
            try:
                state.load_json_into_self(path)
                io_out.write_line("Loaded. Returning to main menu.")
            except (OSError, ValueError) as e:
                io_out.write_line(f"Could not load: {e}")
            state.goto("intro")
        elif choice == "6":
            default_path = "save_game/save_orison.json"
            try:
                state.load_json_into_self(default_path)
                io_out.write_line("Continuing from last save...")
            except (OSError, ValueError) as e:
                io_out.write_line(f"No save to continue: {e}")
                state.goto("intro")
        else:
            io_out.write_line("I did not understand. Returning to menu.")
            state.goto("intro")         

class AuditScene(Scene):
    """A minimal audit to demonstrate routing and models."""
    def __init__(self) -> None:
        super().__init__(scene_id="audit")
        
    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        public = Contract(
            id="C-001",
            title="Canal Maintenance Oath",
            clauses=["Keep canals clear"],
            is_public=True,
        )

        secret_active = state.flags.get("secret_clause_active", False)
        secret = (
            Contract(
                id="C-SEC-001",
                title="Night Discharge Waiver",
                clauses=["Discharge blackwater at night"],
                is_public=False,
            )
            if secret_active
            else None
        )

        has_witness = any(m.is_witness for m in state.inventory)
        flag_has_witness = state.flags.get("has_witness_mark", False)

        canals_black = False
        if secret is not None and public.conflicts_with(secret):
            canals_black = True
        state.flags["canals_black"] = canals_black

        io_out.write_line("")
        io_out.write_line("Audit: Review Summary")
        io_out.write_line(str(public))
        if secret_active and secret is not None:
            io_out.write_line(str(secret))
        io_out.write_line(
            f"You hold a witness mark: {'yes' if has_witness else 'no'} "
            f"(flag: {'yes' if flag_has_witness else 'no'})"
        )

        io_out.write_line(f"Canal status: {'BLACK' if canals_black else 'CLEAR'}")

        scribes = state.get_rep("scribes")
        mariners = state.get_rep("mariners")
        io_out.write_line(f"Reputation - Scribes: {scribes} | Mariners: {mariners}")

        io_out.write_line("")
        io_out.write_line("What is next?")
        io_out.write_line("1) Return to main menu")
        io_out.write_line("2) Conclude for now")
        io_out.write_line("3) Investigate (check ledger or visit dock)")
        io_out.write_line("4) Visit the Arbiter")
        io_out.write_line("5) Toggle secret clause (reveal/withdraw)")
        io_out.write_line("6) Proceed to decision")
        io_out.write_line("7) Assemble a ritual token")
        choice = _choice_or_default(
            io_in, io_out, "Choose [1-7]: ", set("1234567"), default="1"
        )

        if choice == "1":
            state.goto("intro")
            return
        elif choice == "2":
            state.goto("end")
            return
        elif choice == "3":
            def handle_check_ledger() -> str:
                state.flags["checked_ledger"] = True
                io_out.write_line(
                    "Ledger notes: backlog of repairs and mismatched reports."
                )
                return "intro"

            def handle_visit_dock() -> str:
                state.flags["visited_dock"] = True
                io_out.write_line(
                    "At the docks: faint smell of blackwater and nervous whispers."
                )
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
            sub = _choice_or_default(
                io_in, io_out, "Choose [1-3]: ", set("123"), default="3"
            )

            next_scene = strategies.get(sub, lambda: "intro")()
            state.goto(next_scene)
            return
        elif choice == "4":
            state.goto("arbiter")
            return
        elif choice == "5":
            new_state = not state.flags.get("secret_clause_active", False)
            state.flags["secret_clause_active"] = new_state
            if new_state:
                io_out.write_line(
                    "Secret clause is now ACTIVE (a hidden waiver exists)."
                )
            else:
                io_out.write_line(
                    "Secret clause is now INACTIVE (no hidden waiver)."
                )

            state.goto("audit")
            return
        elif choice == "6":
            state.goto("decision")
            return
        elif choice == "7":
            state.goto("ritual")
            return

        io_out.write_line("Invalid choice. returning to main menu")
        state.goto("intro")
        
class ArbiterScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id="arbiter")
        self.arbiter = TerminalArbiter()
    
    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        io_out.write_line("")
        io_out.write_line("You meet the Arbiter. Offer a memory to receive a hint.")
        memory = io_in.read_line(
            "Type a memory (or just press Enter to skip): "
        ).strip()
        hint = self.arbiter.trade_memory_for_hint(memory)
        io_out.write_line(f"Arbiter's hint: {hint}")
        io_out.write_line("")
        io_out.write_line("1) Return to main menu")
        _ = _choice_or_default(io_in, io_out, "Choose [1]: ", {"1"}, default="1")
        state.goto("intro")
        
class DecisionScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id="decision")
    
    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        secret_active = state.flags.get("secret_clause_active", False)
        current = "SECRET WAIVER ACTIVE" if secret_active else "PUBLIC OATH ONLY"
        io_out.write_line("")
        io_out.write_line("Decision: City Policy")
        io_out.write_line(f"Current stance: {current}")
        io_out.write_line("1) Restore the public oath (disable secret waiver)")
        io_out.write_line("2) Legalize the secret waiver (keep it active)")
        choice = _choice_or_default(
            io_in, io_out, "Choose [1-2]: ", {"1", "2"}, default="1"
        )
        
        if choice == "1":
            state.flags["secret_clause_active"] = False
            state.flags["policy"] = "public"
            state.adjust_rep("scribes", +1)
            state.adjust_rep("mariners", -1)
            io_out.write_line("City response: Relief across districts. Oath restored.")
            state.goto("intro")
        elif choice == "2":
            state.flags["secret_clause_active"] = True
            state.flags["policy"] = "secret"
            state.adjust_rep("scribes", -1)
            state.adjust_rep("mariners", +1)
            io_out.write_line("City response: Uneasy acceptance. Hidden waivers now legal.")
            state.goto("intro")
        else:
            io_out.write_line("No decision made. Returning to main menu.")
            state.goto("intro")

class RitualScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id = "ritual")
    
    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        io_out.write_line("")
        io_out.write_line("Ritual: Assemble the Memory Sigil")
        #  if already forged, short-circuit
        if any(m.kind == "sigil" for m in state.inventory):
            io_out.write_line("You already forged a Memory Sigil.")
            state.goto("audit")
            return
        
        io_out.write_line("Combine two parts. Hint: words tied to your duty.")
        part_a  = io_in.read_line("Enter part A (or blank to cancel): ").strip()
        if not part_a:
            state.goto("audit")
            return
        part_b = io_in.read_line("Enter part B (or blank to cancel): ").strip()
        if not part_b:
            state.goto("audit")
            return
        
        a = part_a.lower()
        b = part_b.lower()
        
        def valid_combo(x:str, y: str) -> bool:
            return {x, y} == {"witness","oath"}
        
        if valid_combo(a, b):
            if not any(m.kind == "sigil" for m in state.inventory):
                state.inventory.append(Mark(id="SIGIL-MEM-1", kind="sigil", is_witness=False))
            state.flags["sigil_for_memory"] = True
            io_out.write_line("Ritual succeeds. A Memory Sigil hums in your hands.")
            state.goto("audit")
        else:
            io_out.write_line("The glyphs sputter. Hint: try combining 'witness' with 'oath'.")
            state.goto("audit")
class EndScene(Scene):
    def __init__(self) -> None:
        super().__init__(scene_id="end")

    def run(self, state: GameState, io_in: InputPort, io_out: OutputPort) -> None:
        io_out.write_line("This is the end of the demo scaffold. Goodbye.")
        state.stop()


SCENES: Dict[str, Scene] = {
    "intro": IntroScene(),
    "audit": AuditScene(),
    "arbiter": ArbiterScene(),
    "decision": DecisionScene(),
    "ritual": RitualScene(),
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
