from ProjectParameters import (STEPS_PER_DAY, INIT_NUM_AGENTS, INIT_NUM_BUSHES, 
                               INIT_NUM_CAVES, INIT_CAVE_CAP, INIT_BUSH_CAP,
                               DAYS_PER_CHECKPOINT)
import json
from typing import List, Optional
from Cave import Cave
from BerryBush import BerryBush
from Agent import Agent
import itertools
from matplotlib.pyplot import subplots
from Position import Position
import numpy as np
from pathlib import Path

checkpoints = Path("checkpoints/")

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
        checkpoints.mkdir(exist_ok=True)
        # Will be used to show entities, and histograms of genes
        self.fig, self.axes = subplots(2, 2)
        self.caves = caves
        self.bushes = bushes
        self.agents = agents
        # Add caves and bushes and agents if they are empty
        if len(caves) == 0:
            for _ in range(INIT_NUM_CAVES):
                self.caves.append(Cave(Position.get_random_pos(), np.random.randint(3, )))

    @staticmethod
    def from_json(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)

    def to_json(self):
        return {
            "caves": [cave.to_json() for cave in self.caves]
        }

    def step(self, timestep: int):
        """
        Represents a single step in the world.

        Args:
            timestep: The timestep of this action
        """
        current_day = (timestep // STEPS_PER_DAY) + 1
        timestep %= STEPS_PER_DAY
        
        if timestep == 0:
            # Make new children if there is space available
            # Reset all entities
            for entity in itertools.chain(self.caves, self.bushes, self.agents):
                entity.reset()
            # If current day is at checkpoint
            if current_day % DAYS_PER_CHECKPOINT == 0:
                with open(checkpoints.joinpath(f"checkpoint_{current_day}.json"), "wt+") as f:
                    json.dump(self.to_json, f)