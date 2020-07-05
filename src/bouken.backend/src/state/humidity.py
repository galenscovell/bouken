from enum import IntEnum


class Humidity(IntEnum):
    """
    The general humidity types for a map.
    """
    Barren = 0
    Dry = 1
    Average = 2
    Wet = 3
    Drenched = 4
