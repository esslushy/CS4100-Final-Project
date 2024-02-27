from ProjectParameters import AGGRESSIVE_BOUNDS, HARVEST_BOUNDS, MEMORY_BOUNDS, \
    STEPS_PER_DAY, CAL_PER_MEM, MAX_AGGR_CAL, MAX_HARVEST_CAL, CHANCE_TO_REMEMBER_BUSH, \
    CHANCE_TO_REMEMBER_CAVE, CHANCE_TO_USE_MEMORY, VISION_RADIUS, INTERACTION_RADIUS, \
    MORNING_PERCENT, EVENING_PERCENT
from ActionSpace import ActionSpace
from WorldEntity import WorldEntity
from Position import Position
from typing import Set
import numpy as np
from collections import OrderedDict
from BerryBush import BerryBush
from Counter import Counter
from Cave import Cave

AgentCounter = Counter()

class Agent(WorldEntity):
    """
    Represents an agent in the world with a set of genes, goals, location, and actions
    """
    goal: WorldEntity = None
    action_state = ActionSpace.Wander
    seen_today: Set[WorldEntity] = set()
    calories: int = 0
    wander_spot: Position = None
    
    def __init__(self, pos: Position, aggressiveness: float, harvest_percent: float, max_memory: int, memory: OrderedDict = OrderedDict()) -> None:
        super().__init__(pos)
        if not self.is_well_bounded(aggressiveness, harvest_percent, max_memory):
            raise ValueError("Genetics are not within proper range.")
        self.aggressiveness = aggressiveness
        self.harvest_percent = harvest_percent
        self.max_memory = max_memory
        self.memory: OrderedDict = memory
        self.name = f"Agent {AgentCounter.get_next()}"

    def is_well_bounded(self, aggressiveness: float, harvest_percent: float, max_memory: int) -> bool:
        return (AGGRESSIVE_BOUNDS[0] <= aggressiveness and aggressiveness <= AGGRESSIVE_BOUNDS[1]) \
            and (HARVEST_BOUNDS[0] <= harvest_percent and harvest_percent <= HARVEST_BOUNDS[1]) \
            and (MEMORY_BOUNDS[0] <= max_memory and max_memory <= MEMORY_BOUNDS[1]) 
    
    def act(self, view: Set[WorldEntity], interact: Set[WorldEntity], timestep: int):
        """
        Make the entity act at a certain timestep

        Args:
            view: A set of all entities in the viewing radius of the entity
            interact: A set of all entities in the interaction raidus of the entity
            timestep: The current timestep for the day
        """
        # Figure out everything we know about (see and remember), filter out what we've already gone to.
        possible_goals = view.copy()
        # Some small chance to include memory
        if np.random.random() < CHANCE_TO_USE_MEMORY:
            possible_goals.update(self.memory.keys())
        possible_goals = filter(lambda e: e not in self.seen_today, possible_goals)
        # Do action based on current state
        if self.action_state == ActionSpace.GoTo:
            # If we are at our goal that we are going to
            if self.goal in interact:
                # Interact with goal
                if type(self.goal) == Cave:
                    self.interact_cave(self.goal)
                elif type(self.goal) == BerryBush:
                    self.interact_bush(self.goal)
                else:
                    self.interact_agent(self.goal)
                if self.action_state != ActionSpace.Sleep:
                    # If didn't go to sleep in a cave
                    self.action_state = ActionSpace.Wander
                self.goal = None
            else:
                # Continue going toward goal
                self.pos = self.pos.step_toward(self.goal.pos)
        elif self.action_state == ActionSpace.Wander:
            if self.wander_spot is None:
                self.wander_spot = self.pos.get_pos_within_radius(VISION_RADIUS)
            # Wander toward picked spot
            self.pos = self.pos.step_toward(self.wander_spot)
            # If near spot, reset
            if self.pos.distance_to(self.wander_spot) < INTERACTION_RADIUS:
                self.wander_spot = None
                # Set up goal for next action
                if timestep % STEPS_PER_DAY < (STEPS_PER_DAY * MORNING_PERCENT):
                    # Morning, go to any berry bushes you see or know, otherwise keep wandering
                    bushes = list(filter(lambda e: type(e) == BerryBush, possible_goals))
                    if len(bushes) > 0:
                        self.action_state = ActionSpace.GoTo
                        self.goal = np.random.choice(bushes)
                elif timestep % STEPS_PER_DAY > (STEPS_PER_DAY * (1-EVENING_PERCENT)):
                    # Evening, go to any cave you see or know, otherwise keep ing
                    caves = list(filter(lambda e: type(e) == Cave, possible_goals))
                    if len(caves) > 0:
                        self.action_state = ActionSpace.GoTo
                        self.goal = np.random.choice(caves)
                else:
                    # Midday, go to any bushes or entities you see or know, otherwise keep wandering
                    bushes_and_agents = list(filter(lambda e: type(e) == BerryBush or type(e) == Agent, possible_goals))
                    if len(bushes_and_agents) > 0:
                        self.action_state = ActionSpace.GoTo
                        self.goal = np.random.choice(bushes_and_agents)
        # If neither of these actions, we are sleeping which is no change.

    def interact_bush(self, bush: BerryBush):
        self.calories += bush.harvest(self.harvest_percent)
        self.seen_today.add(bush)
        if np.random.random() < CHANCE_TO_REMEMBER_BUSH:
            self.add_memory(bush)

    def interact_cave(self, cave: Cave):
        cave.append(self)
        self.seen_today.add(cave)
        if np.random.random() < CHANCE_TO_REMEMBER_CAVE:
            self.add_memory(cave)

    def interact_agent(self, other):
        """
        Interacts with another agent
        """
        self_agg = self.is_aggressive(other)
        other_agg = other.is_aggressive(self)
        total_calories = self.calories + other.calories
        if self_agg == other_agg:
            # both share or both steal
            calorie_split = total_calories // 2
            self.calories = calorie_split
            other.calories = calorie_split
        else:
            self.calories = total_calories if self_agg else 0
            other.calories = total_calories if other_agg else 0
        # Add to short term memory
        self.seen_today.add(other)
        other.seen_today.add(self)
        # Add to long term memory
        self.add_memory(other, "steal" if other_agg else "share")
        other.add_memory(self, "steal" if self_agg else "share")

    def add_memory(self, entity: WorldEntity, val: str = ""):
        self.memory[entity] = val
        if len(self.memory) > self.max_memory:
            # Remove oldest item in memory.
            self.memory.popitem(False)

    def reset(self):
        """
        Resets this entity for the start of a new day.
        """
        self.calories = 0
        self.action_state = ActionSpace.Wander
        self.goal = None
        self.seen_today = set()

    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def to_json(self):
        return {
            # Permenant Genes
            "max_memory": self.max_memory,
            "aggressiveness": self.aggressiveness,
            "harvest_percent": self.harvest_percent,
            # Semipermenant state
            "memory": self.memory,
            "x": self.pos.x,
            "y": self.pos.y
        }
    
    @staticmethod
    def from_json(data: dict):
        return Agent(Position(data["x"], data["y"]), data["aggressiveness"], 
                     data["harvest_percent"], data["max_memory"], OrderedDict(data["memory"]))

    @staticmethod
    def from_parents(parent1, parent2):
        # New genes are average
        new_aggressiveness = (parent1.aggressiveness + parent2.aggressiveness) / 2
        new_harvest_percent = (parent1.harvest_percent + parent2.harvest_percent) / 2
        new_max_memory = (parent1.max_memory + parent2.max_memory) // 2
        # Apply mutation
        new_aggressiveness += (np.random.random() - 0.5) / 5
        new_harvest_percent += (np.random.random() - 0.5) / 5
        new_max_memory += np.random.randint(-2, 3)
        # Share memory
        parent_memory = list(parent1.memory.items()) + list(parent2.memory.items())
        np.random.shuffle(parent_memory)
        new_memory = OrderedDict(parent_memory[0:new_max_memory])
        return Agent(parent1.pos, new_aggressiveness, new_harvest_percent, new_max_memory, new_memory)

    @property
    def calorie_expenditure(self) -> float:
        """
        Formula for base calories expenditure from genes
        """
        return (self.aggressiveness * MAX_AGGR_CAL) + \
                (self.harvest_percent * MAX_HARVEST_CAL) + \
                (self.max_memory * CAL_PER_MEM)
    
    @property
    def survived(self) -> bool:
        """
        Tells if this entity survived a day, should be called at end of day.
        True if it is sleeping in a cave, and covered enough calories
        """
        return self.action_state == ActionSpace.Sleep and self.calorie_expenditure < self.calories
    
    def is_aggressive(self, other) -> bool:
        """
        Determines if this entity will act aggressively.
        """
        modifier = 0
        if other in self.memory:
            # Double if the other stole from you, half if they shared
            modifier = 2 if self.memory[other] == "steal" else 0.5
        return np.random.random() < (self.aggressiveness * modifier)