import pytest
import test_setup

from BerryBush import BerryBush, BushCounter
from Position import Position

# Reset the BushCounter for consistent naming in tests
BushCounter.reset()


@pytest.fixture
def new_berry_bush():
    # Setup
    pos = Position(0, 0)
    max_calories = 100
    bush = BerryBush(pos, max_calories)
    return bush

def test_berry_bush_initialization(new_berry_bush):
    assert new_berry_bush.pos == Position(0, 0), "Position should be (0, 0)"
    assert new_berry_bush.max_calories == 100, "Max calories should be 100"
    assert new_berry_bush.current_calories == 100, "Current calories should be equal to max calories"
    assert new_berry_bush.name.split(' ')[0] == "Bush", "Bush name should follow the counter"

def test_berry_bush_reset(new_berry_bush):
    # Modify current calories
    new_berry_bush.current_calories = 50
    new_berry_bush.reset()
    assert new_berry_bush.current_calories == 100, "Reset should restore calories to max"

def test_berry_bush_harvest(new_berry_bush):
    calories_harvested = new_berry_bush.harvest(0.5)
    assert calories_harvested == 50, "Should harvest 50% of max calories"
    assert new_berry_bush.current_calories == 50, "Current calories should be reduced by harvested amount"

    # Harvest more than available
    calories_harvested = new_berry_bush.harvest(0.6)  # Attempt to harvest 60% of max
    assert calories_harvested == 50, "Should harvest only remaining calories"
    assert new_berry_bush.current_calories == 0, "Bush should now be empty"

def test_berry_bush_to_json(new_berry_bush):
    expected_json = {"max_calories": 100, "x": 0, "y": 0}
    assert new_berry_bush.to_json() == expected_json, "JSON representation should match"

def test_berry_bush_from_json():
    json_data = {"max_calories": 100, "x": 1, "y": 1}
    bush = BerryBush.from_json(json_data)
    assert bush.pos == Position(1, 1), "Position should match JSON data"
    assert bush.max_calories == 100, "Max calories should match JSON data"
    assert isinstance(bush, BerryBush), "Should be an instance of BerryBush"

if __name__ == '__main__':
    pytest.main()
