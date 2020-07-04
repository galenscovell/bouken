from enum import IntEnum


class BiomeType(IntEnum):
    """
    Elevation   Dryness     Biome       Vegetation      Life        Features

    High        High        Scorched    Limited         Limited     Mountains, rocky, caves
    High        Moderate    Tundra      Reduced         Reduced     Permafrost, caverns
    High        Low         Snow        Limited         Reduced     Snow, ice lakes, ice caverns
    Moderate    High        Cold Desert Limited         Limited     Snow, sand
    Moderate    Moderate    Deciduous   High            High        Forests, marshes
    Moderate    Low         Taiga       High            High        Boreal forests
    Low         High        Hot Desert  Limited         Limited     Sand, dunes
    Low         Moderate    Grassland   High            High        Prairies, canyons
    Low         Low         Tropical    High            High        Jungles
    """
    Scorched = 0
    Tundra = 1
    Snow = 2
    ColdDesert = 3
    Deciduous = 4
    Taiga = 5
    HotDesert = 6
    Grassland = 7
    Tropical = 8
