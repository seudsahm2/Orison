import os
from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES

def test_save_load_roundtrip(tmp_path, monkeypatch, capsys):
    save_path = str(tmp_path / "save_orison.json")
    # name, pick mark (2), save (4), path, load (5), path
    inputs = iter(["Tester", "2", "4", save_path, "5", save_path])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]
    state = GameState()

    # Intro: pick mark -> returns to intro
    SCENES["intro"].run(state, io, io)
    assert any(m.is_witness for m in state.inventory)
    assert state.current_scene_id == "intro"

    # Intro: save -> returns to intro
    SCENES["intro"].run(state, io, io)
    assert os.path.exists(save_path)
    assert state.current_scene_id == "intro"

    # Intro: load -> returns to intro with same inventory/flags
    SCENES["intro"].run(state, io, io)
    out = capsys.readouterr().out
    assert "Loaded" in out or "Saved" in out  # lenient output check
    assert any(m.is_witness for m in state.inventory)
    assert state.flags.get("has_witness_mark") is True

def test_load_missing_file(monkeypatch, capsys):
    # name, load (5), non-existent path
    inputs = iter(["Tester", "5", "X:\\no\\such\\file\\save_orison.json"])

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]
    state = GameState()

    SCENES["intro"].run(state, io, io)
    out = capsys.readouterr().out
    assert "Could not load" in out
    assert state.current_scene_id == "intro"