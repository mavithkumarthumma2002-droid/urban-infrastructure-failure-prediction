import pytest

import main


def test_steps_start_with_exploring_the_data():
    assert list(main.STEPS)[0] == "explore"


def test_unknown_step_stops_with_a_message():
    with pytest.raises(SystemExit, match="Unknown step"):
        main.main(["not_a_step"])
