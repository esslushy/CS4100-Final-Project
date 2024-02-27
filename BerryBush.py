from Position import Position
from WorldEntity import WorldEntity
from Counter import Counter

BushCounter = Counter()

class BerryBush(WorldEntity):
    """
    Represents a berry bush in the world
    """
    def __init__(self, pos: Position, max_calories: int) -> None:
        """
        Initializes a new berry bush

        Args:
            pos: The position to put the berry bush.
            max_calories: The maximum amount of calories this berry bush has.
        """
        super().__init__(pos)
        self.max_calories = max_calories
        self.current_calories = max_calories
        self.name = f"Bush {BushCounter.get_next()}"

    def reset(self):
        """
        Resets the berry bush for a new day.
        """
        self.current_calories = self.max_calories

    def harvest(self, harvest_percent: float) -> int:
        """
        Harvest a certain percentage of the max calories from the bush.
        Capped by current remaining calories.

        Args:
            harvest_percent: How much of the max calories this bush holds to take in a harvest.

        Returns:
            The number of calories harvested from this bush.
        """
        # Either percentage of max or all that remain.
        calories_gotten = min(int(self.max_calories * harvest_percent), self.current_calories)
        self.current_calories -= calories_gotten
        return calories_gotten
    
    def __hash__(self) -> int:
        return self.name.__hash__() 
    
    def to_json(self):
        """
        Returns a JSON serializable form of this BerryBush.

        Returns:
            A dictionary of information on this BerryBush.
        """
        return {
            "max_calories": self.max_calories,
            "x": self.pos.x,
            "y": self.pos.y
        }
    
    @staticmethod
    def from_json(data: dict):
        """
        Creates a BerryBush from data.

        Args:
            data: The data to make a berry bush from.
        
        Returns:
            A berry bush matched with the data.
        """
        return BerryBush(Position(data["x"], data["y"]), data["max_calories"])