from enum import Enum


class RegionFlag(Enum):
    """
    The possible flags a region can have.
    """
    Tiny = 0
    Small = 1
    Medium = 2
    Large = 3
    Enormous = 4

    Coastal = 5
    Secluded = 6
    Surrounded = 7
