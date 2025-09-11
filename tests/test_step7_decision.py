from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_decision_restore_public(monkeypatch, capsys):
    # name, intro->audit (1), decision (6), restore public (1)
    inputs = iter(["Tester", "1", "6", "1"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "decision"

    SCENES["decision"].run(state, io, io)
    out = capsys.readouterr().out
    assert state.flags.get("secret_clause_active") is False
    assert state.flags.get("policy") == "public"
    assert "Oath restored" in out

def test_decision_legalize_secret(monkeypatch, capsys):
    # name, intro->audit (1), toggle secret (5), decision (6), legalize secret (2)
    inputs = iter(["Tester", "1", "5", "6", "2"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # Toggle secret ON, then go to decision and choose 'secret'
    SCENES["audit"].run(state, io, io)
    assert state.flags.get("secret_clause_active") is True
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "decision"

    SCENES["decision"].run(state, io, io)
    out = capsys.readouterr().out
    assert state.flags.get("secret_clause_active") is True
    assert state.flags.get("policy") == "secret"
    assert "Hidden waivers now legal" in out