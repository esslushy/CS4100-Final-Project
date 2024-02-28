from ProjectParameters import (STEPS_PER_DAY, INIT_NUM_AGENTS, INIT_NUM_BUSHES, 
                               INIT_NUM_CAVES, INIT_CAVE_CAP, INIT_BUSH_CAP,
                               DAYS_PER_CHECKPOINT, MEMORY_BOUNDS, NUM_BINS,
                               INTERACTION_RADIUS, VISION_RADIUS, VISUALIZE,
                               AGGRESSIVE_BOUNDS, HARVEST_BOUNDS)
import json
from typing import List
from Cave import Cave
from BerryBush import BerryBush
from Agent import Agent
import itertools
import matplotlib.pyplot as plt
from Position import Position
import numpy as np
from pathlib import Path
import random

checkpoints = Path("checkpoints/")

class World:
    def __init__(self, caves: List[Cave] = list(), bushes: List[BerryBush] = list(), 
                 agents: List[Agent] = list()) -> None:
        """
        Initializes a random world if all parameters are none

        Args:
            caves: The list of caves to initialize with
            bushes: The list of bushes to initialize with
            agents: The list of agents to initialize with
        """
        checkpoints.mkdir(exist_ok=True)
        self.caves = caves
        self.bushes = bushes
        self.agents = agents
        # Add caves and bushes and agents if they are empty
        if len(self.caves) == 0:
            for _ in range(INIT_NUM_CAVES):
                self.caves.append(Cave(Position.get_random_pos(), 
                                       random.randint(INIT_CAVE_CAP[0], INIT_CAVE_CAP[1])))
        if len(self.bushes) == 0:
            for _ in range(INIT_NUM_BUSHES):
                self.bushes.append(BerryBush(Position.get_random_pos(), 
                                             random.randrange(INIT_BUSH_CAP[0], INIT_BUSH_CAP[1]+1, 50)))
        if len(self.agents) == 0:
            for _ in range(INIT_NUM_AGENTS):
                self.agents.append(Agent(Position.get_random_pos(), np.random.random(), 
                                         np.random.random(), np.random.randint(MEMORY_BOUNDS[0], MEMORY_BOUNDS[1]+1)))
        # Initial checkpoint
        with open(checkpoints.joinpath(f"checkpoint_0.json"), "wt+") as f:
            json.dump(self.to_json(), f, indent=4)
        if VISUALIZE:
            self.make_plot()

    def make_plot(self):
        """
        Makes the plot of the map and the histograms of genes.
        """
        # Make plot
        self.fig, ((map, self.memory_bar_chart), (self.agg_hist, self.harvest_hist)) = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)
        # Set title and axis
        map.set_title("Map")
        self.memory_bar_chart.set_title("Max Memory")
        self.memory_bar_chart.set_ylabel("Num Agents")
        self.memory_bar_chart.set_xlabel("Max Memory")
        self.agg_hist.set_title("Aggressiveness")
        self.agg_hist.set_ylabel("Num Agents")
        self.agg_hist.set_xlabel("Aggressiveness")
        self.harvest_hist.set_title("Harvest Percent")
        self.harvest_hist.set_ylabel("Num Agents")
        self.harvest_hist.set_xlabel("Harvest Percent")
        # Add non mutable
        cave_x, cave_y = [], []
        for cave in self.caves:
            cave_x.append(cave.pos.x)
            cave_y.append(cave.pos.y)
        map.scatter(cave_x, cave_y, c="grey", marker="^")
        bush_x, bush_y = [], []
        for bush in self.bushes:
            bush_x.append(bush.pos.x)
            bush_y.append(bush.pos.y)
        map.scatter(bush_x, bush_y, c="green", marker="p")
        # Add mutable
        agent_x, agent_y = self.get_agent_pos()
        memory, aggression, harvest = self.get_agent_data()
        self.agent_loc = map.scatter(agent_x, agent_y, c="black", marker="o")
        self.memory_bar_chart.hist(memory, bins=MEMORY_BOUNDS[1], range=MEMORY_BOUNDS)
        self.agg_hist.hist(aggression, bins=NUM_BINS, range=AGGRESSIVE_BOUNDS)
        self.harvest_hist.hist(harvest, bins=NUM_BINS, range=HARVEST_BOUNDS)

    def get_agent_pos(self):
        """
        Returns the X and Y coordinates of all agents
        """
        agent_x, agent_y = [], []
        for agent in self.agents:
            agent_x.append(agent.pos.x)
            agent_y.append(agent.pos.y)
        return agent_x, agent_y

    def get_agent_data(self):
        """
        Returns the memory, aggression, and harvest genes of all agents.
        """
        memory, aggression, harvest = [], [], []
        for agent in self.agents:
            memory.append(agent.max_memory)
            aggression.append(agent.aggressiveness)
            harvest.append(agent.harvest_percent)
        return memory, aggression, harvest

    @staticmethod
    def from_json(data: dict):
        """
        Creates a world from JSON data. Used to rebuild the world from a saved initial condition.
        Do not use checkpoints that are not initial saves as it does not restore the same memory in 
        agents.
        """
        caves = [Cave.from_json(c) for c in data["caves"]]
        bushes = [BerryBush.from_json(c) for c in data["caves"]]
        agents = [Agent.from_json(c) for c in data["caves"]]
        return World(caves, bushes, agents)

    def to_json(self):
        """
        Returns a JSON serializable form of this object.
        """
        return {
            "caves": [cave.to_json() for cave in self.caves],
            "bushes": [bush.to_json() for bush in self.bushes],
            "agents": [agent.to_json() for agent in self.agents]
        }

    def step(self, timestep: int):
        """
        Represents a single step in the world.

        Args:
            timestep: The timestep of this action
        """
        current_day = (timestep // STEPS_PER_DAY) + 1
        timestep %= STEPS_PER_DAY
        for agent in self.agents:
            view, interact = set(), set()
            for entity in itertools.chain(self.caves, self.bushes, self.agents):
                if entity is not agent:
                    dis = agent.pos.distance_to(entity.pos)
                    if dis < VISION_RADIUS:
                        view.add(entity)
                    if dis < INTERACTION_RADIUS:
                        interact.add(entity)
            agent.act(view, interact, timestep)
        
        if VISUALIZE:
            # Update map:
            agent_x, agent_y = self.get_agent_pos()
            self.agent_loc.set_offsets(np.array(list(zip(agent_x, agent_y))))

        if timestep == STEPS_PER_DAY - 1:
            # Purge all who fail to survive
            self.agents = list(filter(lambda agent: agent.survived, self.agents))
            # Make new children if there is space available
            for cave in self.caves:
                if len(cave.occupants) >= 2:
                    parents = list(itertools.combinations(cave.occupants, 2))
                    while not cave.is_full:
                        # Breed
                        parent1, parent2 = random.choice(parents)
                        child = Agent.from_parents(parent1, parent2)
                        cave.append(child)
                        self.agents.append(child)
            # Reset all entities
            for entity in itertools.chain(self.caves, self.bushes, self.agents):
                entity.reset()
            # Update graphs
            if VISUALIZE:
                memory, aggression, harvest = self.get_agent_data()
                for count, rect in zip(np.histogram(memory, MEMORY_BOUNDS[1], range=MEMORY_BOUNDS)[0], self.memory_bar_chart.patches):
                    rect.set_height(count)
                for count, rect in zip(np.histogram(aggression, NUM_BINS, range=AGGRESSIVE_BOUNDS)[0], self.agg_hist.patches):
                    rect.set_height(count)
                for count, rect in zip(np.histogram(harvest, NUM_BINS, range=HARVEST_BOUNDS)[0], self.harvest_hist.patches):
                    rect.set_height(count)
                # Allow scaling
                self.memory_bar_chart.relim()
                self.memory_bar_chart.autoscale()
                self.agg_hist.relim()
                self.agg_hist.autoscale()
                self.harvest_hist.relim()
                self.harvest_hist.autoscale()
            # If current day is at checkpoint. 
            if current_day % DAYS_PER_CHECKPOINT == 0:
                with open(checkpoints.joinpath(f"checkpoint_{current_day}.json"), "wt+") as f:
                    json.dump(self.to_json(), f, indent=4)