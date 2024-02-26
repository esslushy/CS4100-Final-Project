from Agent import Agent, ActionSpace
import numpy as np
from typing import Set
from WorldEntity import WorldEntity
from Counter import Counter
from Position import Position

CaveCounter = Counter()

class Cave(WorldEntity):
    """
    Represents a cave with a limited capacity
    """
    def __init__(self, pos: Position, max_capacity: int) -> None:
        """
        Initializes a cave with a max capacity

        Args:
            max_capacity: The maximum number of entities in a cave
        """
        super().__init__(pos)
        self.max_capacity = max_capacity
        self.occupants: Set[Agent] = {}
        self.name = f"Cave {CaveCounter.get_next()}"

    def append(self, agent: Agent):
        """
        Does the process for an agent entering a cave

        Args:
            agent: The agent entering the cave
        """
        if not self.is_full:
            self.occupants.add(agent)
            agent.action_state = ActionSpace.Sleep
            agent.pos = self.pos
        else:
            rival: Agent = np.random.choice(list(self.occupants))
            # Interact and maybe chuck out rival
            if agent.is_aggressive(rival) and not rival.is_aggressive(agent):
                # Agent successfully kicks out rival
                self.occupants.remove(rival)
                rival.action_state = ActionSpace.Wander
                self.occupants.add(agent)
                agent.action_state = ActionSpace.Sleep
                agent.pos = self.pos

    @property
    def is_full(self):
        return len(self.occupants) == self.max_capacity
    
    def reset(self):
        self.occupants = {}

    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def to_json(self):
        return {
            "x": self.pos.x,
            "y" : self.pos.y,
            "max_capacity": self.max_capacity
        }
    
    @staticmethod
    def from_json(data: dict):
        return Cave(Position(data["x"], data["y"]), data["max_capacity"])
