from datetime import datetime
import pprint
from ProjectParameters import (MAP_SIZE, NUM_DAYS, STEPS_PER_DAY, INIT_NUM_AGENTS, INIT_NUM_BUSHES, 
                               INIT_NUM_CAVES, INIT_CAVE_CAP, INIT_BUSH_CAP,
                               DAYS_PER_CHECKPOINT, MEMORY_BOUNDS, NUM_BINS,
                               INTERACTION_RADIUS, VISION_RADIUS, VISUALIZE,
                               AGGRESSIVE_BOUNDS, HARVEST_BOUNDS, AS_MP4
                               )
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
import statistics as st

class World:
    def __init__(self, 
                 project: Path,
                 caves: List[Cave] = list(), 
                 bushes: List[BerryBush] = list(), 
                 agents: List[Agent] = list()) -> None:
        """
        Initializes a random world if all parameters are none

        Args:
            caves: The list of caves to initialize with
            bushes: The list of bushes to initialize with
            agents: The list of agents to initialize with
        """
        self.project = project
        self.project.mkdir(exist_ok=True)
        self.checkpoints = self.project.joinpath("checkpoints/")
        self.checkpoints.mkdir(exist_ok=True)
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
                self.agents.append(
                    Agent(
                        Position.get_random_pos(),
                        np.random.random(),
                        np.random.random(),
                        np.random.randint(MEMORY_BOUNDS[0], MEMORY_BOUNDS[1] + 1),
                    )
                )
        # Initial checkpoint
        with open(self.checkpoints.joinpath(f"checkpoint_0.json"), "wt+") as f:
            json.dump(self.to_json(), f, indent=2)
        if VISUALIZE:
            self.make_plot()

        # create zones
        zones = []
        for i in range((MAP_SIZE // VISION_RADIUS)+1):
            row = []
            for i2 in range((MAP_SIZE // VISION_RADIUS)+1):
                j_list = []
                for j in itertools.chain(self.caves, self.bushes):
                    jx = j.pos.x // VISION_RADIUS
                    jy = j.pos.y // VISION_RADIUS
                    if (jx == i or jx == i+1 or jx == i-1) and (jy == i2 or jy == i2+1 or jy == i2-1):
                        j_list.append(j)
                row.append(j_list)
            zones.append(row)
        self.zones = zones

    def make_plot(self):
        """
        Makes the plot of the map and the histograms of genes.
        """
        if AS_MP4:
            self.fig, map = plt.subplots(figsize=(8, 8), tight_layout=True)
        else:
            # Make plot
            self.fig, ((map, self.memory_bar_chart), (self.agg_hist, self.harvest_hist)) = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)
            # Set title and axis
            self.memory_bar_chart.set_title("Max Memory")
            self.memory_bar_chart.set_ylabel("Num Agents")
            self.memory_bar_chart.set_xlabel("Max Memory")
            self.agg_hist.set_title("Aggressiveness")
            self.agg_hist.set_ylabel("Num Agents")
            self.agg_hist.set_xlabel("Aggressiveness")
            self.harvest_hist.set_title("Harvest Percent")
            self.harvest_hist.set_ylabel("Num Agents")
            self.harvest_hist.set_xlabel("Harvest Percent")
            # Add mutable
            memory, aggression, harvest = self.get_agent_data()
            self.memory_bar_chart.hist(memory, bins=MEMORY_BOUNDS[1], range=MEMORY_BOUNDS)
            self.agg_hist.hist(aggression, bins=NUM_BINS, range=AGGRESSIVE_BOUNDS)
            self.harvest_hist.hist(harvest, bins=NUM_BINS, range=HARVEST_BOUNDS)

        # Map stuff
        map.set_title("Map")
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
        agent_x, agent_y = self.get_agent_pos()
        self.agent_loc = map.scatter(agent_x, agent_y, c="black", marker="o")

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
        bushes = [BerryBush.from_json(c) for c in data["bushes"]]
        agents = [Agent.from_json(c) for c in data["agents"]]
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

        # create zones of agents
        agent_zones = []
        for i in range((MAP_SIZE // VISION_RADIUS) + 1):
            row = []
            for i2 in range((MAP_SIZE // VISION_RADIUS) + 1):
                j_list = []
                for j in self.agents:
                    jx = j.pos.x // VISION_RADIUS
                    jy = j.pos.y // VISION_RADIUS
                    if (jx == i or jx == i + 1 or jx == i - 1) and (
                        jy == i2 or jy == i2 + 1 or jy == i2 - 1
                    ):
                        j_list.append(j)
                row.append(j_list)
            agent_zones.append(row)

        for agent in self.agents:
            view, interact = set(), set()
            for entity in itertools.chain(self.zones[int(agent.pos.x / VISION_RADIUS)][int(agent.pos.y / VISION_RADIUS)],agent_zones[int(agent.pos.x / VISION_RADIUS)][int(agent.pos.y / VISION_RADIUS)]):
            # for entity in itertools.chain(self.caves, self.bushes, self.agents):

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
                cave.occupants = set(filter(lambda agent: agent.survived, cave.occupants))
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
            if VISUALIZE and not AS_MP4:
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
                with open(self.checkpoints.joinpath(f"checkpoint_{current_day}.json"), "wt+") as f:
                    json.dump(self.to_json(), f, indent=2)

                # print(f"completed day {current_day} of {NUM_DAYS} (Population: {len(self.agents)})")


    def get_agg_plot(self, file_name):
        mean_agg = [] # list of mean aggressiveness values per checkpoint
        std_agg = [] # list of std aggressiveness values per checkpoint 
        max_agg = [] # list of max aggressiveness values per checkpoint 
        min_agg = [] # list of min aggressiveness values per checkpoint

        # obtains max aggressiveness, min aggressiveness, mean aggressiveness and std aggressivness for each checkpoint
        for day in range(NUM_DAYS):
            aggressive_vals = []
            with open(self.checkpoints.joinpath(f"checkpoint_{day}.json"), "r") as f:
                data = json.load(f)
                for i in range(len(data["agents"])):
                    aggressive_vals.append(data["agents"][i]["aggressiveness"])
                mean_agg.append(st.mean(aggressive_vals))
                std_agg.append(st.stdev(aggressive_vals))
                max_agg.append(max(aggressive_vals))
                min_agg.append(min(aggressive_vals))
            f.close()

        m_agg = np.array(mean_agg)
        s_agg = np.array(std_agg)
        mx_agg = np.array(max_agg)
        mn_agg = np.array(min_agg)

        plt.plot(np.array(range(NUM_DAYS)), m_agg, label="mean aggressiveness", color="yellow")
        plt.plot(np.array(range(NUM_DAYS)), mx_agg, label="max aggressiveness", color="red")
        plt.plot(np.array(range(NUM_DAYS)), mn_agg, label="min aggressiveness", color="purple")
        plt.legend()
        plt.fill_between(np.array(range(NUM_DAYS)), m_agg - s_agg, m_agg + s_agg, alpha=0.5)
        plt.xlabel("Checkpoint Day")
        plt.ylabel("Aggressiveness Value")
        plt.title("Evolution of Aggressiveness via Mean")
        plt.savefig(self.project.joinpath(file_name), format="pdf")
        plt.close()

    def get_mem_plot(self, file_name):
        mean_mem = [] # list of mean memory values per checkpoint
        std_mem = [] # list of std memory values per checkpoint
        max_mem = [] # list of maximum max memory values per checkpoint 
        min_mem = [] # list of minimum max memory values per checkpoint

        # obtains maximum of max memory, minimum of max memory, mean of max memory and std of max memory for each checkpoint
        for day in range(NUM_DAYS):
            mem_vals = []
            with open(self.checkpoints.joinpath(f"checkpoint_{day}.json"), "r") as f:
                data = json.load(f)
                for i in range(len(data["agents"])):
                    mem_vals.append(data["agents"][i]["max_memory"])
                mean_mem.append(st.mean(mem_vals))
                std_mem.append(st.stdev(mem_vals))
                max_mem.append(max(mem_vals))
                min_mem.append(min(mem_vals))
            f.close() 

        m_mem = np.array(mean_mem)
        s_mem = np.array(std_mem)
        mx_mem = np.array(max_mem)
        mn_mem = np.array(min_mem)

        plt.plot(np.array(range(NUM_DAYS)), m_mem, label="mean max memory", color="yellow")
        plt.plot(np.array(range(NUM_DAYS)), mx_mem, label="maximum of max memory", color="red")
        plt.plot(np.array(range(NUM_DAYS)), mn_mem, label="minumum of max percentage", color="purple")
        plt.legend()
        plt.fill_between(np.array(range(NUM_DAYS)), m_mem - s_mem, m_mem + s_mem, alpha=0.5)
        plt.xlabel("Checkpoint Day")
        plt.ylabel("Memory Value")
        plt.title("Evolution of Memory via Mean")
        plt.savefig(self.project.joinpath(file_name), format="pdf")
        plt.close()

    def get_hvst_plot(self, file_name):
        mean_hvst = [] # list of mean harvest values per checkpoint
        std_hvst = [] # list of std harvest values per checkpoint 
        max_hvst = [] # list of max harvest values per checkpoint 
        min_hvst = [] # list of min harvest values per checkpoint

         # obtains max hvst, min hvst, mean hvst and std hvst for each checkpoint
        for day in range(NUM_DAYS):
            hvst_vals = []
            with open(self.checkpoints.joinpath(f"checkpoint_{day}.json"), "r") as f:
                data = json.load(f)
                for i in range(len(data["agents"])):
                    hvst_vals.append(data["agents"][i]["harvest_percent"])
                mean_hvst.append(st.mean(hvst_vals))
                std_hvst.append(st.stdev(hvst_vals))
                max_hvst.append(max(hvst_vals))
                min_hvst.append(min(hvst_vals))
            f.close() 

        m_hvst = np.array(mean_hvst)
        s_hvst = np.array(std_hvst)
        mx_hvst = np.array(max_hvst)
        mn_hvst = np.array(min_hvst)

        plt.plot(np.array(range(NUM_DAYS)), m_hvst, label="mean harvest percentage", color="yellow")
        plt.plot(np.array(range(NUM_DAYS)), mx_hvst, label="max harvest percentage", color="red")
        plt.plot(np.array(range(NUM_DAYS)), mn_hvst, label="min harvest percentage", color="purple")
        plt.legend()
        plt.fill_between(np.array(range(NUM_DAYS)), m_hvst - s_hvst, m_hvst + s_hvst, alpha=0.5)
        plt.xlabel("Checkpoint Day")
        plt.ylabel("Harvest Percentage")
        plt.title("Evolution of Harvest Percentage via Mean")
        plt.savefig(self.project.joinpath(file_name), format="pdf")
        plt.close()

    def plot_population(self, file_name):
        pop_val = [] # stores populations at each checkpoint 
        for day in range(NUM_DAYS):
            with open(self.checkpoints.joinpath(f"checkpoint_{day}.json"), "r") as f:
                data = json.load(f)
                pop_val.append(len(data["agents"]))
            f.close() 

        p_vals = np.array(pop_val)
        plt.plot(np.array(range(NUM_DAYS)), p_vals)
        plt.xlabel("Checkpoint Day")
        plt.ylabel("Total Population")
        plt.title("Total Population across Checkpoints")
        plt.savefig(self.project.joinpath(file_name), format="pdf")
        plt.close()
