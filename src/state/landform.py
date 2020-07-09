from enum import IntEnum


class Landform(IntEnum):
    """
    The landform types for map regions.
    """
    # Can be volcano in bare biome
    Mountain = 0

    # Ice cavern in snow/tundra/taiga
    Cave = 1

    # Swamp in tropical/temperate forests
    # Ice lake in snow/tundra/taiga
    Lake = 2

    # Swamp in tropical/temperate forests
    # Ice river in snow/tundra/taiga
    River = 3

    # Sandy or rocky depending on biome
    Beach = 4

    # Deserts only
    Oasis = 5

    #
    Hill = 6

    # Can be salt flat in temperate desert
    Plain = 7

    # Jungle in tropical forest biome
    Forest = 8
