from enum import IntEnum


class TerraformState(IntEnum):
    """
    The possible states of a hex due to terraforming.
    """
    Land = 0
    Ocean = 1
    Lake = 2
