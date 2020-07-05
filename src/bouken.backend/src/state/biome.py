"""
-------------------------------------------------------------------------------------
Biome                       Vegetation  Life        Description
-------------------------------------------------------------------------------------
TropicalDesert              1           2           Sand, dunes, flat, oasis
TropicalForest              5           5           Jungles, tall tress/dense canopy, fog
TemperateDesert             2           3           Snow and sand (seasonal), salt
TemperateForest             5           5           Mountains, hills, dense canopy, fog
Grassland                   3           4           Prairies, savannas, canyons, sparse vegetation
Taiga                       3           3           Forests (boreal)
Bare                        1           1           Mountains, rocky, caves
Tundra                      2           3           Cold wasteland, permafrost, rocky
Snow                        1           1           Snow, caverns (ice)

At low elevation, lakes become marshes. At high elevation, they become ice.
-------------------------------------------------------------------------------------
Elevation   Dryness     Biome
-------------------------------------------------------------------------------------
1           6           TropicalDesert
1           5           Grassland
1           4           Grassland
1           3           TemperateForest
1           2           TropicalForest
1           1           TropicalForest

2           6           TemperateDesert
2           5           Grassland
2           4           Grassland
2           3           TemperateForest
2           2           TemperateForest
2           1           TropicalForest

3           6           TemperateDesert
3           5           TemperateDesert
3           4           Grassland
3           3           Grassland
3           2           Taiga
3           1           Taiga

4           6           Bare
4           5           Tundra
4           4           Tundra
4           3           Snow
4           2           Snow
4           1           Snow
"""

from enum import IntEnum


class Biome(IntEnum):
    TropicalDesert = 0
    TropicalForest = 1
    TemperateDesert = 2
    TemperateForest = 3
    Grassland = 4
    Taiga = 5
    Bare = 6
    Tundra = 7
    Snow = 8
