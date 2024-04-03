import pytest
from ProjectParameters import FIGHT_CAL_COST, WALK_CAL_COST
import test_setup

from collections import OrderedDict
from Position import Position
import Agent as _Agent
from Agent import Agent, AgentCounter
from ActionSpace import ActionSpace
from BerryBush import BerryBush
from Cave import Cave
import numpy as np

AgentCounter.reset()


@pytest.fixture
def basic_agent():
    pos = Position(0, 0)
    aggressiveness = 0.5
    harvest_percent = 0.5
    max_memory = 5
    agent = Agent(
        pos,
        aggressiveness,
        harvest_percent,
        max_memory,
    )
    return agent


def test_agent_initialization(basic_agent):
    assert basic_agent.pos == Position(0 ,0), "Agent's position should be initialized correctly."
    assert 0 <= basic_agent.aggressiveness <= 1, "Agent's aggressiveness should be within range."
    assert 0 <= basic_agent.harvest_percent <= 1, "Agent's harvest_percent should be within range."
    assert isinstance(basic_agent.max_memory, int) and basic_agent.max_memory > 0, "Agent's max_memory should be a positive integer."
    assert basic_agent.name.startswith("Agent"), "Agent should have a name starting with 'Agent'."

def test_is_well_bounded(basic_agent):
    assert basic_agent.is_well_bounded(0.5, 0.5, 5) is True, "Agent genetics should be well bounded."
    assert basic_agent.is_well_bounded(1.1,0.5,5) is False, "Agent aggressiveness genetics should be well bounded."
    assert basic_agent.is_well_bounded(0.5,1.1,5) is False, "Agent harvest genetics should be well bounded."
    assert basic_agent.is_well_bounded(0.5,0.5,21) is False, "Agent memory genetics should be well bounded."

def test_agent_action_state_transition(basic_agent):
    basic_agent.act(set(), set(), 1)
    assert basic_agent.action_state == ActionSpace.Wander, "Agent should start in a wandering state."

@pytest.mark.parametrize("entity,expected_memory_len", [
    (BerryBush(Position(1, 1), 100), 1),
    (Cave(Position(2, 2),100), 2)
])
def test_agent_add_memory(basic_agent, entity, expected_memory_len):
    basic_agent.add_memory(entity)
    assert len(basic_agent.memory) == expected_memory_len, "Agent should remember entities encountered."

def test_agent_memory_limit(basic_agent):
    for i in range(10):
        basic_agent.add_memory(BerryBush(Position(i, i), 100))
    assert len(basic_agent.memory) <= basic_agent.max_memory, "Agent memory should not exceed the maximum limit."

def test_agent_json_serialization(basic_agent):
    json_data = basic_agent.to_json()
    assert "max_memory" in json_data and "aggressiveness" in json_data and "harvest_percent" in json_data, "Agent JSON should contain all necessary properties."

def test_agent_json_deserialization():
    json_data = {
        "x": 0,
        "y": 0,
        "aggressiveness": 0.5,
        "harvest_percent": 0.5,
        "max_memory": 5
    }
    agent = Agent.from_json(json_data)
    assert agent.pos == Position(0,0), "Deserialized agent should have correct position."
    assert agent.aggressiveness == 0.5, "Deserialized agent should have correct aggressiveness."
    assert agent.harvest_percent == 0.5, "Deserialized agent should have correct harvest percent."
    assert agent.max_memory == 5, "Deserialized agent should have correct max memory."

if __name__ == "__main__":
    pytest.main()
