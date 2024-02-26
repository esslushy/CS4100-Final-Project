from ProjectParameters import AGGRESSIVE_BOUNDS, HARVEST_BOUNDS, MEMORY_BOUNDS, STEPS_PER_DAY
from enum import Enum
from WorldEntity import WorldEntity
from Position import Position
from typing import Set, List
import numpy as np
from collections import OrderedDict
from BerryBush import BerryBush

ActionSpace = Enum("ActionSpace", [
    "Wander",
    "GoTo",
    "Sleep"
])

class Agent(WorldEntity):
    """
    Represents an agent in the world with a set of genes, goals, location, and actions
    """
    memory: OrderedDict = OrderedDict() 
    current_pos: Position = None
    goal_pos: WorldEntity = None
    action_state = ActionSpace.Wander
    seen_today: Set[WorldEntity] = set()
    calories: int = 0
    
    def __init__(self, aggressiveness: float, harvest_percent: float, max_memory: int) -> None:
        self.aggressiveness = aggressiveness
        self.harvest_percent = harvest_percent
        self.max_memory = max_memory

    def _check_well_bounded(self, aggressiveness: float, harvest_percent: float, max_memory: int) -> bool:
        return (AGGRESSIVE_BOUNDS[0] <= aggressiveness and aggressiveness <= AGGRESSIVE_BOUNDS[1]) \
            and (HARVEST_BOUNDS[0] <= harvest_percent and harvest_percent <= HARVEST_BOUNDS[1]) \
            and (MEMORY_BOUNDS[0] <= max_memory and max_memory <= MEMORY_BOUNDS[1]) 
    
    def act(self, view, interact, timestep):
        """
        Make the entity act at a certain timestep

        Args:
            view: A list of all items in the 
        """
        # Do something based on current state

        # Update state
        if timestep % STEPS_PER_DAY < (STEPS_PER_DAY * 0.1):
            # Start of day, wander or go to bushes and collect.
            interact = filter(lambda entity: type(entity) == BerryBush, interact)
            if len(interact) > 0:
                # Interact with a berry bush
                self.calories += next(iter(interact))

        elif timestep % STEPS_PER_DAY > (STEPS_PER_DAY * 0.9):
            # Try to find a cave.
            pass
        else:
            # Can collect from berry bushes or interact with others.
            pass

    def reset(self):
        """
        Resets this entity for the start of a new day.
        """
        self.calories = 0
        self.action_state = ActionSpace.Wander
        self.goal_pos = None
        self.seen_today = {}

    @staticmethod
    def from_parents(parent1, parent2):
        return None

    @property
    def calorie_expenditure(self) -> float:
        """
        Formula for base calories expenditure from genes
        """
        return (self.aggressiveness * 200) + (self.harvest_percent * 100) + (self.max_memory * 50)
    
    @property
    def survived(self) -> bool:
        """
        Tells if this entity survived a day, should be called at end of day.
        True if it is sleeping in a cave, and covered enough calories
        """
        return self.action_state == ActionSpace.Sleep and self.calorie_expenditure < self.calories
    
    def is_aggressive(self, other: Agent) -> bool:
        """
        Determines if this entity will act aggressively.
        """
        return np.random.random() < self.aggressiveness