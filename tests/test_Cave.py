import pytest
import test_setup

from Cave import CaveCounter,Cave
from Position import Position
from Agent import AgentCounter, Agent
from ActionSpace import ActionSpace

CaveCounter.reset()
AgentCounter.reset()

@pytest.fixture
def new_cave():
    # Setup
    pos = Position(0, 0)
    max_capacity = 2

    cave = Cave(pos, max_capacity)
    return cave

@pytest.fixture
def aggressive_agent():
    pos = Position(1, 1)
    agent = Agent(pos, aggressiveness=1.0, harvest_percent=0.5, max_memory=5)
    return agent

@pytest.fixture
def peaceful_agent():
    pos = Position(2, 2)
    agent = Agent(pos, aggressiveness=0.0, harvest_percent=0.5, max_memory=5)
    return agent

def test_new_cave(new_cave):
    assert new_cave.pos == Position(0,0), "Position should be 0,0."
    assert new_cave.max_capacity == 2, "Max Capacity should match initializations max capacity."
    assert new_cave.occupants == set(), "Occupants set should be empty."
    assert new_cave.name == "Cave 1", "Cave name should equal 'Cave {#}'"

def test_append_cave_with_aggressive_agent(new_cave, aggressive_agent):
    new_cave.append(aggressive_agent)
    assert aggressive_agent in new_cave.occupants, "Aggressive agent should be added to occupants."
    assert aggressive_agent.action_state == ActionSpace.Sleep, "Aggressive agent's action state should be set to Sleep after entering the cave."

def test_append_cave_with_conflict(new_cave, aggressive_agent, peaceful_agent):
    # First, add a peaceful agent to the cave
    new_cave.append(peaceful_agent)
    # Then, try to add an aggressive agent
    new_cave.append(aggressive_agent)
    # Check the outcome based on the expected behavior
    assert len(new_cave.occupants) <= new_cave.max_capacity, "Cave occupants should not exceed max capacity."
    if aggressive_agent in new_cave.occupants and len(new_cave.occupants) != 2:
        assert peaceful_agent.action_state == ActionSpace.Wander, "Peaceful agent should be wandering if kicked out."
    else:
        assert peaceful_agent in new_cave.occupants, "Peaceful agent should remain if aggressive agent didn't enter."
def test_reset_cave_with_occupants(new_cave, aggressive_agent, peaceful_agent):
    new_cave.append(aggressive_agent)
    new_cave.append(peaceful_agent)
    new_cave.reset()
    assert len(new_cave.occupants) == 0, "Cave should be empty after reset."

def test_cave_memory_interaction(aggressive_agent, peaceful_agent):
    aggressive_agent.interact_agent(peaceful_agent)
    # Check memory addition based on interaction
    assert peaceful_agent in aggressive_agent.memory, "Peaceful agent should be in aggressive agent's memory after interaction."
    assert aggressive_agent in peaceful_agent.memory, "Aggressive agent should be in peaceful agent's memory after interaction."