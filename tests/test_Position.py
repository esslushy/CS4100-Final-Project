import pytest
import test_setup

from Position import Position, MAP_SIZE, DISTANCE_PER_STEP

def test_position_initialization():
    # Test that position is limited within the map bounds
    pos_outside = Position(-1, MAP_SIZE + 1)
    assert pos_outside.x == 0 and pos_outside.y == MAP_SIZE, "Position should be adjusted to within map bounds"

def test_position_immutable():
    # Test that position cannot be mutated
    pos = Position(1, 1)
    with pytest.raises(Exception):
        pos.x = 2
    with pytest.raises(Exception):
        pos.y = 2

def test_step_toward():
    start_pos = Position(0, 0)
    end_pos = Position(3, 4) # A position 5 units away (3-4-5 triangle)
    stepped_pos = start_pos.step_toward(end_pos)

    # Assuming DISTANCE_PER_STEP < 5, the stepped position should be closer to end_pos
    dist_after_step = stepped_pos.distance_to(end_pos)
    assert dist_after_step < start_pos.distance_to(end_pos), "Step should move position closer to target"

def test_distance_to():
    pos1 = Position(0, 0)
    pos2 = Position(3, 4) # 3-4-5 triangle
    assert pos1.distance_to(pos2) == 5, "Distance should be calculated correctly"

def test_get_pos_within_radius():
    center_pos = Position(MAP_SIZE / 2, MAP_SIZE / 2)
    radius = 10
    new_pos = center_pos.get_pos_within_radius(radius)

    # Check that the new position is within the specified radius from center_pos
    assert center_pos.distance_to(new_pos) <= radius, "New position should be within radius of center position"

def test_get_random_pos():
    random_pos = Position.get_random_pos()
    # Test that random position is within map bounds
    assert 0 <= random_pos.x <= MAP_SIZE and 0 <= random_pos.y <= MAP_SIZE, "Random position should be within map bounds"

def test_position_equality():
    pos1 = Position(1, 1)
    pos2 = Position(1, 1)
    pos3 = Position(1, 2)
    assert pos1 == pos2, "Identical positions should be equal"
    assert pos1 != pos3, "Different positions should not be equal"
