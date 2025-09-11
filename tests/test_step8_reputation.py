from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_decision_influences_reputation_public(monkeypatch):
    # name, intro->audit (1), decision (6), choose public (1)
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
    assert state.flags.get("policy") == "public"
    assert state.get_rep("scribes") == 1
    assert state.get_rep("mariners") == -1

def test_decision_influences_reputation_secret(monkeypatch):
    # name, intro->audit (1), toggle secret (5), decision (6), choose secret (2)
    inputs = iter(["Tester", "1", "5", "6", "2"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # Toggle secret active
    SCENES["audit"].run(state, io, io)
    assert state.flags.get("secret_clause_active") is True
    assert state.current_scene_id == "audit"

    # Go to decision and choose secret
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "decision"

    SCENES["decision"].run(state, io, io)
    assert state.flags.get("policy") == "secret"
    assert state.get_rep("scribes") == -1
    assert state.get_rep("mariners") == 1