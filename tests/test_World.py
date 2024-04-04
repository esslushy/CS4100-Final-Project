import pytest
import test_setup

import numpy as np
from unittest.mock import patch, MagicMock
from pathlib import Path
from World import World, checkpoints
from Cave import Cave
from BerryBush import BerryBush
from Agent import Agent
from Position import Position

@pytest.fixture
def basic_world():
    with patch('world.random'), patch('world.np.random.random'), patch('world.Position.get_random_pos', return_value=Position(0, 0)):
        world = World()
    return world

