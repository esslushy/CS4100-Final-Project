from abc import ABC, abstractmethod
from Position import Position

class WorldEntity(ABC):
    """
    Represents an entity in the world with a given position
    """
    def __init__(self, pos: Position) -> None:
        """
        Initializes world entity with a position

        Args:
            pos: The position to start with
        """
        super().__init__()
        self.pos = pos

    @abstractmethod
    def __hash__(self) -> int:
        """
        All world entities need a hash code for speed up using sets to work.
        """
        raise NotImplementedError("Every world entity needs its own hash code.")
    
    @abstractmethod
    def reset(self):
        """
        Resets the world entity at the start of a new day.
        """
        raise NotImplementedError("Every entity needs to reset itself at the start of a new day.")