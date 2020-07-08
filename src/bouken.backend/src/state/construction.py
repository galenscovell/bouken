from enum import IntEnum


class Construction(IntEnum):
    """
    The possible states of an interior cell due to construction.
    """
    Floor = 0
    Wall = 1
    Empty = 2
    Padding = 3
    Corridor = 4
    Corner = 5
    Water = 6
