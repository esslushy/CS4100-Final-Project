from enum import Enum

class ActionSpace(Enum):
    """
    Represents all the actions an Agent can do. 

    {Wander, GoTo, Sleep}
    """
    Wander = 1
    GoTo = 2
    Sleep = 3