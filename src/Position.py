from ProjectParameters import MAP_SIZE, DISTANCE_PER_STEP
import numpy as np

class Position:
    """
    Represents a position within a world map. Automatically binds any position to within the world map
    """
    def __init__(self, x: float, y: float) -> None:
        """
        Initializes a new position. Automatically limits to within the map.

        Args:
            x: The x-coord
            y: The y-coord
        """
        self._x = max(min(x, MAP_SIZE), 0)
        self._y = max(min(y, MAP_SIZE), 0)

    @property
    def x(self):
        """
        X coordinate of the position
        """
        return self._x
    
    @x.setter
    def x(self, value):
        raise Exception("Position is not mutable")
    
    @property
    def y(self):
        """
        Y coordinate of the position
        """
        return self._y
    
    @y.setter
    def y(self, value):
        raise Exception("Position is not mutable")

    def step_toward(self, pos):
        """
        Takes a step from this position toward the next position.

        Args:
            pos: The position to step toward.

        Returns:
            The new position that is being stepped toward.
        """
        # Computer displacement
        dx = pos.x - self.x
        dy = pos.y - self.y
        # Scale to direction and step distance
        mag = np.sqrt((dx**2) + (dy**2)) + 1e-4
        dx *= (DISTANCE_PER_STEP/mag)
        dy *= (DISTANCE_PER_STEP/mag)
        return Position(self.x + dx, self.y + dy)

    def distance_to(self, pos) -> int:
        """
        Gets the l2 distance between this position and another position.

        Args:
            pos: The other position to compute distance to.

        Returns:
            The l2 distance between the positions.
        """
        return np.sqrt((self.x - pos.x)**2 + (self.y - pos.y)**2)
    
    def get_pos_within_radius(self, radius):
        """
        Gets a random position within a radius of this position.

        Args:
            radius: The radius to look within.

        Returns:
            The new position within a radius of this position.
        """
        # Get random radius value
        r = np.random.random() * radius
        # Get random value between 0 and 2pi
        theta = np.random.random() * 2 * np.pi
        # Compute displacement
        dx = r * np.cos(theta)
        dy = r * np.sin(theta)
        # Return new position with displacment
        return Position(self.x + dx, self.y + dy)
    
    @staticmethod
    def get_random_pos():
        """
        Returns a random position in the map.
        """
        return Position(np.random.random() * MAP_SIZE, np.random.random() * MAP_SIZE)
    
    def __eq__(self,other):
        return other.x == self.x and other.y == self.y