from ActionSpace import ActionSpace
import numpy as np
from typing import Set
from WorldEntity import WorldEntity
from Counter import Counter
from Position import Position
from src.ProjectParameters import FIGHT_CAL_COST

CaveCounter = Counter()

class Cave(WorldEntity):
    """
    Represents a cave with a limited capacity
    """
    def __init__(self, pos: Position, max_capacity: int) -> None:
        """
        Initializes a cave with a max capacity.

        Args:
            pos: The position of this cave.
            max_capacity: The maximum number of entities in a cave.
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
            if agent_agg:
                agent.calories_for_exercise += FIGHT_CAL_COST
            if rival_agg:
                rival.calories_for_exercise += FIGHT_CAL_COST
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
        """
        Says if the cave can't take another occupant.
        """
        return len(self.occupants) == self.max_capacity
    
    def reset(self):
        """
        Resets the cave to empty at the start of a new day.
        """
        self.occupants = set()

    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def to_json(self):
        """
        Returns a JSON serializable form of this Cave.

        Returns:
            A dictionary of information about this Cave
        """
        return {
            "x": self.pos.x,
            "y" : self.pos.y,
            "max_capacity": self.max_capacity
        }
    
    @staticmethod
    def from_json(data: dict):
        """
        Produces a Cave object from json data.

        Args:
            data: The JSON data to make the cave from.

        Returns:
            A new Cave based on the provided data.
        """
        return Cave(Position(data["x"], data["y"]), data["max_capacity"])
