from Agent import Agent, ActionSpace
import numpy as np
from typing import Set
from WorldEntity import WorldEntity

class Cave(WorldEntity):
    """
    Represents a cave with a limited capacity
    """
    def __init__(self, max_capacity: int) -> None:
        """
        Initializes a cave with a max capacity

        Args:
            max_capacity: The maximum number of entities in a cave
        """
        self.max_capacity = max_capacity
        self.occupants: Set[Agent] = {}
        self.pos = ()

    def append(self, agent: Agent):
        """
        Does the process for an agent entering a cave

        Args:
            agent: The agent entering the cave
        """
        if not self.is_full:
            self.occupants.append(agent)
            agent.action_state = ActionSpace.Sleep
        else:
            rival: Agent = np.random.choice(list(self.occupants))
            # Interact and maybe chuck out rival
            if agent.is_aggressive(rival) and not rival.is_aggressive(agent):
                # Agent successfully kicks out rival
                self.occupants.remove(rival)

    @property
    def is_full(self):
        return len(self.occupants) == self.max_capacity
