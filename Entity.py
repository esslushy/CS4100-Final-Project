from ProjectParameters import AGGRESSIVE_BOUNDS, HARVEST_BOUNDS, MEMORY_BOUNDS
from enum import Enum

ActionSpace = Enum("ActionSpace", [
    "Wander",
    "GoTo",
    "Interact"
])

class Entity():
    """
    Represents an entity in the world with a set of genetics
    """
    memory = []
    current_pos = ()
    goal_pos = ()
    action_state = 
    
    def __init__(self, aggressiveness: float, harvest_percent: float, max_memory: int) -> None:
        pass

    def _check_well_bounded(self, aggressiveness: float, harvest_percent: float, max_memory: int) -> bool:
        return (AGGRESSIVE_BOUNDS[0] <= aggressiveness and aggressiveness <= AGGRESSIVE_BOUNDS[1]) \
            and (HARVEST_BOUNDS[0] <= harvest_percent and harvest_percent <= HARVEST_BOUNDS[1]) \
            and (MEMORY_BOUNDS[0] <= max_memory and max_memory <= MEMORY_BOUNDS[1]) 
    
    def act(self, view):
        """
        
        Args:
            view: A list of all items in the 
        """

    @staticmethod
    def from_parents(parent1, parent2):
        return Entity()

    def compute_base_calorie_expenditure(self):
        pass