from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_secret_clause_toggles_and_conflicts(monkeypatch, capsys):
    # name, intro->audit (1), toggle secret (5), return audit refresh (auto), then return to intro (1)
    inputs = iter(["Tester", "1", "5",  # go to audit, toggle secret ON
                   "1"])                # after refresh, return to intro

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    # Intro -> Audit
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # First Audit: toggle secret ON (and refresh to audit)
    SCENES["audit"].run(state, io, io)
    assert state.flags.get("secret_clause_active") is True
    assert state.current_scene_id == "audit"

    # Capture output from the second Audit render
    SCENES["audit"].run(state, io, io)
    out = capsys.readouterr().out
    assert "Canal status: BLACK" in out  # conflict banner shown

    # Now return to intro to finish this flow
    assert state.current_scene_id in {"intro", "audit"}
    if state.current_scene_id == "audit":
        # Use the input that returns to intro
        pass  # already queued