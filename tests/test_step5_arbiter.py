from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_arbiter_interaction(monkeypatch, capsys):
    # name, intro->audit (1), audit->arbiter (4), offer memory, return
    inputs = iter(["Tester", "1", "4", "I saw the canal", "1"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "arbiter"

    SCENES["arbiter"].run(state, io, io)
    out = capsys.readouterr().out
    assert "canals hide more than water" in out.lower()
    assert state.current_scene_id == "intro"