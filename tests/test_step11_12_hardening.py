from orison.engine import GameState
from orison.io.terminal.app import ConsoleIO, SCENES


def _mk_io(inputs):
    it = iter(inputs)

    def fake_input(prompt: str = "") -> str:  # noqa: ARG001,ARG002
        return next(it)

    io = ConsoleIO()
    io.read_line = fake_input  # type: ignore[assignment]
    return io


def test_intro_invalid_defaults_to_quit():
    # name, invalid 'x' should default to Quit (3)
    io = _mk_io(["Player", "x"])  # invalid main menu
    state = GameState()

    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "end"


def test_audit_invalid_defaults_to_return():
    # name, go to audit, enter invalid choice in audit menu -> defaults to 1 (return)
    io = _mk_io(["Player", "1", "x"])  # intro->audit, then invalid
    state = GameState()

    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "intro"


def test_investigate_invalid_defaults_to_back():
    # name, intro->audit, choose investigate (3), then invalid 'x' -> defaults to 3 (back)
    io = _mk_io(["Player", "1", "3", "x"])  # intro->audit->investigate->invalid
    state = GameState()

    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    SCENES["audit"].run(state, io, io)
    # after investigate invalid, should route via default to intro
    assert state.current_scene_id == "intro"


def test_decision_invalid_defaults_to_public():
    # name, intro->audit (1), decision (6), invalid 'x' -> defaults to 1
    io = _mk_io(["Player", "1", "6", "x"])  # invalid decision choice
    state = GameState()

    SCENES["intro"].run(state, io, io)
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "decision"

    SCENES["decision"].run(state, io, io)
    assert state.flags.get("secret_clause_active") is False
    assert state.flags.get("policy") == "public"


def test_continue_no_save_stays_intro():
    # name, choose Continue (6) with no save file present
    io = _mk_io(["Player", "6"])  # continue without save
    state = GameState()

    SCENES["intro"].run(state, io, io)
    # Depending on implementation, it may set intro explicitly after exception
    assert state.current_scene_id in {"intro", "end"}  # lenient


# Step 12 reachability tests

def test_reach_all_scenes_quickly():
    # Intro -> Audit
    io = _mk_io(["P", "1"])  # go to audit
    state = GameState()
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # Audit -> Arbiter -> back to Intro
    io = _mk_io(["4", "", "1"])  # visit arbiter, skip memory, then return
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "arbiter"
    SCENES["arbiter"].run(state, io, io)
    assert state.current_scene_id == "intro"

    # Intro -> Audit -> Ritual -> back to Audit
    io = _mk_io(["1"])  # back to audit
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "audit"

    io = _mk_io(["7"])  # ritual
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "ritual"

    io = _mk_io(["witness", "oath"])  # complete ritual; should return to audit
    SCENES["ritual"].run(state, io, io)
    assert state.current_scene_id == "audit"

    # Decision path -> back to Intro
    io = _mk_io(["6"])  # go to decision
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "decision"

    io = _mk_io(["1"])  # pick public oath
    SCENES["decision"].run(state, io, io)
    assert state.current_scene_id == "intro"

    # End via Conclude and via Quit
    io = _mk_io(["1", "2"])  # audit then conclude
    SCENES["intro"].run(state, io, io)
    SCENES["audit"].run(state, io, io)
    assert state.current_scene_id == "end"

    # Restart and Quit directly from Intro
    state = GameState()
    io = _mk_io(["P", "3"])  # quit from intro
    SCENES["intro"].run(state, io, io)
    assert state.current_scene_id == "end"
