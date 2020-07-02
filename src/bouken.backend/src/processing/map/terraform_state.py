from enum import IntEnum


class TerraformState(IntEnum):
    """
    The possible states of a hex due to terraforming.
    """
    Land = 0
    Coast = 1
    Ocean = 2
    Lake = 3
    River = 4
