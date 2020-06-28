from enum import IntEnum


class IslandType(IntEnum):
    """
    The possible types of an island.
    """
    Grassland = 0
    Mountainous = 1
    Tundra = 2
    Tropical = 3
    Desert = 4
