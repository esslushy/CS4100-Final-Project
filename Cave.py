from Entity import Entity
import numpy as np

class Cave():
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
        self.occupants = []
        self.pos = ()

    def append(self, entity: Entity):
        """
        Does the process for an entity entering a cave

        Args:
            entity: The entity entering the cave
        """
        if len(self.occupants) < self.max_capacity:
            self.occupants.append(entity)
            return True
        else:
            rival = np.random.choice(self.occupants)
            # Interact and maybe chuck out rival
