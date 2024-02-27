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
        self.pos: Position = pos

    @abstractmethod
    def __hash__(self) -> int:
        """
        Returns the hashcode of this object.

        Returns:
            The hashcode of this object.
        """
        raise NotImplementedError("Every world entity needs its own hash code.")
    
    @abstractmethod
    def reset(self):
        """
        Resets the world entity at the start of a new day.
        """
        raise NotImplementedError("Every entity needs to reset itself at the start of a new day.")
    
    @abstractmethod
    def to_json(self):
        """
        Returns a json serializable form of this world entity.
        """
        raise NotImplementedError("Every entity needs its own way of being transformed into JSON.")
    
    @staticmethod
    @abstractmethod
    def from_json(data: dict):
        """
        Makes a world entity from a json file
        """
        raise NotImplementedError("Every entity must be able to generate itself from JSON.")
