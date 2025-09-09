from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_pickup_mark_then_audit(capsys):
    # name, pick up mark (2), go to audit (1), then return (1)
    inputs = iter(["Tester", "2", "1", "1"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    # First intro: name + choose 2 (pickup)
    SCENES["intro"].run(state, io, io)
    assert state.flags.get("has_witness_mark", False) is True
    assert any(m.is_witness for m in state.inventory)
    assert state.current_scene_id == "intro"

    # Second intro: choose 1 (audit)
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # Audit: choose 1 (return to main)
    SCENES["audit"].run(state, io, io)
    out = capsys.readouterr().out
    assert "You hold a witness mark: yes" in out
    assert state.current_scene_id == "intro"