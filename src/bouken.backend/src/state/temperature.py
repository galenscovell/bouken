from enum import IntEnum


class Temperature(IntEnum):
    """
    The general temperature types for a map.
    """
    Freezing = 0
    Cold = 1
    Temperate = 2
    Warm = 3
    Hot = 4
