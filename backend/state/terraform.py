from enum import IntEnum


class Terraform(IntEnum):
    """
    The possible states of an exterior hex due to terraforming.
    """
    Land = 0
    Coast = 1
    Ocean = 2
    Lake = 3
    River = 4
