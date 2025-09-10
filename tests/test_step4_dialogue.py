from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_investigate_check_ledger(monkeypatch, capsys):
    # name, intro->audit (1), audit->investigate (3), investigate->check ledger (1)
    inputs = iter(["Tester", "1", "3", "1"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    out = capsys.readouterr().out
    assert state.current_scene_id == "intro"
    assert state.flags.get("checked_ledger") is True
    assert "Ledger notes" in out

def test_investigate_visit_dock(monkeypatch, capsys):
    # name, intro->audit (1), audit->investigate (3), investigate->visit dock (2)
    inputs = iter(["Tester", "1", "3", "2"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    out = capsys.readouterr().out
    assert state.current_scene_id == "intro"
    assert state.flags.get("visited_dock") is True
    assert "docks" in out.lower()