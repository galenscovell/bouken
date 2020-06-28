from enum import IntEnum


class HexState(IntEnum):
    """
    The possible states of a hex.
    """
    # Base Layer
    Land = 0
    Water = 1
    Forest = 2
    Desert = 3
    Coast = 4
    Shallows = 5
