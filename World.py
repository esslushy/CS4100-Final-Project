from ProjectParameters import STEPS_PER_DAY
import json
from typing import List, Optional
from Cave import Cave
from BerryBush import BerryBush
from Agent import Agent
import itertools

class World:
    def __init__(self, caves: Optional[List[Cave]] = list(), bushes: Optional[List[BerryBush]] = list(), 
                 agents: Optional[List[Agent]] = list()) -> None:
        """
        Initializes a random world if all parameters are none

        Args:
            caves: The list of caves to initialize with
            bushes: The list of bushes to initialize with
            agents: The list of agents to initialize with
        """
        self.caves = caves
        self.bushes = bushes
        self.agents = agents

    @staticmethod
    def from_json(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)

    def step(self, timestep):
        """
        Represents a single step in the world.
        """
        if timestep % STEPS_PER_DAY == 0:
            # Start of a new day
            for entity in itertools.chain(self.caves, self.bushes, self.agents):
                entity.reset()