from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_ritual_success(monkeypatch, capsys):
    # name, intro->audit (1), audit->ritual (7), enter valid parts
    inputs = iter(["Tester", "1", "7", "witness", "oath"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]
    state = GameState()

    # Intro -> Audit
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # Audit -> Ritual
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "ritual"

    # Ritual run (success) -> back to Audit
    SCENES["ritual"].run(state, io, io)
    out = capsys.readouterr().out
    assert "Ritual succeeds" in out
    assert state.current_scene_id == "audit"
    assert state.flags.get("sigil_for_memory") is True
    assert any(m.kind == "sigil" for m in state.inventory)

def test_ritual_failure(monkeypatch, capsys):
    # name, intro->audit (1), audit->ritual (7), enter invalid parts
    inputs = iter(["Tester", "1", "7", "x", "y"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]
    state = GameState()

    # Intro -> Audit
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # Audit -> Ritual
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "ritual"

    # Ritual run (failure) -> hint -> back to Audit
    SCENES["ritual"].run(state, io, io)
    out = capsys.readouterr().out
    assert "sputter" in out or "Hint" in out
    assert state.current_scene_id == "audit"
    assert not any(m.kind == "sigil" for m in state.inventory)
    assert not state.flags.get("sigil_for_memory", False)