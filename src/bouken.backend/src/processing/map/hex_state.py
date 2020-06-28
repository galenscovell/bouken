from enum import IntEnum


class HexState(IntEnum):
    """
    The possible states of a hex.
    """
    # Base Layer
    Land = 0
    Forest = 1
    Desert = 2
    Coast = 3
    Shallows = 4
    Depths = 5

    # Region Layer
    Unoccupied = 6
    Occupied = 7
