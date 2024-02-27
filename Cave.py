from ActionSpace import ActionSpace
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
        self.occupants: Set = set()
        self.name = f"Cave {CaveCounter.get_next()}"

    def append(self, agent):
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
            rival = np.random.choice(list(self.occupants))
            # Interact and maybe chuck out rival
            agent_agg = agent.is_aggressive(rival)
            rival_agg = rival.is_aggressive(agent)
            if agent_agg and not rival_agg:
                # Agent successfully kicks out rival
                self.occupants.remove(rival)
                rival.action_state = ActionSpace.Wander
                self.occupants.add(agent)
                agent.action_state = ActionSpace.Sleep
                agent.pos = self.pos
            # Add to memory
            agent.add_memory(rival, "steal" if rival_agg else "share")
            rival.add_memory(agent, "steal" if agent_agg else "share")

    @property
    def is_full(self):
        return len(self.occupants) == self.max_capacity
    
    def reset(self):
        self.occupants = set()

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
