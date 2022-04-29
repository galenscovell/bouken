from typing import Tuple

from backend.state.biome import Biome
from backend.state.humidity import Humidity
from backend.state.temperature import Temperature
from backend.util.constants import tropical_desert_color, tropical_forest_color, temperate_desert_color, \
    temperate_forest_color, grassland_color, taiga_color, bare_color, tundra_color, snow_color


class BiomeCalculator(object):
    @staticmethod
    def calculate_climate_modifiers(temperature: Temperature, humidity: Humidity) \
            -> Tuple[float, float, int, int, int, int]:
        elevation_modifier: float = 0
        if temperature == Temperature.Freezing:
            elevation_modifier += 0.5
        elif temperature == Temperature.Cold:
            elevation_modifier += 0.25
        elif temperature == Temperature.Warm:
            elevation_modifier += -0.25
        elif temperature == Temperature.Hot:
            elevation_modifier += -0.5

        min_lake_expansions: int = 1
        max_lake_expansions: int = 4
        min_lake_amount: int = 2
        max_lake_amount: int = 4
        dryness_modifier: float = 0
        if humidity == Humidity.Barren:
            dryness_modifier += 0.5
            min_lake_expansions -= 1
            max_lake_expansions -= 4
            min_lake_amount -= 2
            max_lake_amount -= 4
        elif humidity == Humidity.Dry:
            dryness_modifier += 0.25
            max_lake_expansions -= 2
            min_lake_amount -= 1
            max_lake_amount -= 2
        elif humidity == Humidity.Wet:
            dryness_modifier += -0.25
            min_lake_expansions += 1
            max_lake_expansions += 1
            min_lake_amount += 1
            max_lake_amount += 1
        elif humidity == Humidity.Drenched:
            dryness_modifier += -0.5
            min_lake_expansions += 1
            max_lake_expansions += 2
            min_lake_amount += 2
            max_lake_amount += 2

        return elevation_modifier, dryness_modifier, min_lake_expansions, max_lake_amount, min_lake_amount, max_lake_amount

    @staticmethod
    def determine_biome(elevation: float, dryness: float) -> Biome:
        elevation *= 4
        dryness *= 6

        if 3 < elevation <= 4:
            if 5 < dryness <= 6:
                return Biome.Bare
            elif 4 < dryness <= 5:
                return Biome.Bare
            elif 3 < dryness <= 4:
                return Biome.Tundra
            elif 2 < dryness <= 3:
                return Biome.Snow
            elif 1 < dryness <= 2:
                return Biome.Snow
            else:
                return Biome.Snow
        elif 2 < elevation <= 3:
            if 5 < dryness <= 6:
                return Biome.TemperateDesert
            elif 4 < dryness <= 5:
                return Biome.TemperateDesert
            elif 3 < dryness <= 4:
                return Biome.Grassland
            elif 2 < dryness <= 3:
                return Biome.Grassland
            elif 1 < dryness <= 2:
                return Biome.Taiga
            else:
                return Biome.Taiga
        elif 1 < elevation <= 2:
            if 5 < dryness <= 6:
                return Biome.TemperateDesert
            elif 4 < dryness <= 5:
                return Biome.Grassland
            elif 3 < dryness <= 4:
                return Biome.Grassland
            elif 2 < dryness <= 3:
                return Biome.TemperateForest
            elif 1 < dryness <= 2:
                return Biome.TemperateForest
            else:
                return Biome.TropicalForest
        else:
            if 5 < dryness <= 6:
                return Biome.TropicalDesert
            elif 4 < dryness <= 5:
                return Biome.Grassland
            elif 3 < dryness <= 4:
                return Biome.TemperateForest
            elif 2 < dryness <= 3:
                return Biome.TemperateForest
            elif 1 < dryness <= 2:
                return Biome.TropicalForest
            else:
                return Biome.TropicalForest

    @staticmethod
    def get_biome_base_color(biome: Biome) -> Tuple[int, int, int]:
        if biome == Biome.TropicalDesert:
            return tropical_desert_color
        elif biome == Biome.TropicalForest:
            return tropical_forest_color
        elif biome == Biome.TemperateDesert:
            return temperate_desert_color
        elif biome == Biome.TemperateForest:
            return temperate_forest_color
        elif biome == Biome.Grassland:
            return grassland_color
        elif biome == Biome.Taiga:
            return taiga_color
        elif biome == Biome.Bare:
            return bare_color
        elif biome == Biome.Tundra:
            return tundra_color
        elif biome == Biome.Snow:
            return snow_color
