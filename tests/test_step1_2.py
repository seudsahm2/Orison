from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES
from orison.models import Mark, Contract


def test_models_str():
    c = Contract(id="C-1", title="Test", clauses=["a", "b"], is_public=False)
    m = Mark(id="M-1", kind="witness", is_witness=True)
    s = str(c)
    t = str(m)
    assert "Test" in s and "secret" in s and "a; b" in s
    assert "witness" in t and "Mark[M-1]" in t


def test_routing_intro_to_audit_and_back(monkeypatch):
    # Inputs: name, choose audit, then in audit choose back to intro
    inputs = iter(["Tester", "1", "1"])  # name, intro->audit, audit->intro

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "intro"


def test_quit_from_intro(monkeypatch):
    inputs = iter(["Tester", "3"])  # name, choose quit

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001
        return next(inputs)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]

    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "end"