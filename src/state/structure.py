from enum import IntEnum


class Structure(IntEnum):
    """
    The structure types for map regions.
    """
    Outpost = 0
    Village = 1
    Ruins = 2
    Traveler = 3

    MonsterCamp = 4
    MonsterDen = 5
