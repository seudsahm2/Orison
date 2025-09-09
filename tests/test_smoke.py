from orison.engine import GameState
from orison.io.terminal.app import run_terminal_app

def test_imports():
    # Ensure core types import
    state = GameState()
    assert state.current_scene_id == "intro"


def test_terminal_loop_initializes(monkeypatch, capsys):
    # Simulate immediate input for name and continue
    inputs = iter(["Tester", ""])  # name, press enter

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    from orison.io.terminal.app import ConsoleIO, SCENES

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    # Run intro then end
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "end"
