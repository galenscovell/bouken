import json
from typing import Optional, Tuple

from model.requests import CreateExteriorRequest
from processing.exterior.base_layer import BaseLayer
from processing.exterior.feature_layer import FeatureLayer
from processing.exterior.geography_layer import GeographyLayer
from processing.exterior.island_layer import IslandLayer
from processing.exterior.region_layer import RegionLayer
from util.compact_json_encoder import CompactJsonEncoder
from util.i_biome_calculator import IBiomeCalculator
from util.i_hex_utility import IHexUtility
from util.i_logger import ILogger

from state.humidity import Humidity
from state.temperature import Temperature


class ExteriorMapGenerator:
    """
    Procedurally generates hexagon-based exterior maps composed of land features and regions.
    """
    def __init__(self,
                 logger: ILogger,
                 biome_calculator: IBiomeCalculator,
                 hex_util: IHexUtility) -> None:
        self.logger: ILogger = logger
        self.biome_calculator: IBiomeCalculator = biome_calculator
        self.hex_util: IHexUtility = hex_util

    def generate(self, gen_request: CreateExteriorRequest) -> str:
        # Biome
        temperature: Temperature = gen_request.temperature
        humidity: Humidity = gen_request.humidity

        climate_modifiers: Tuple[float, float, int, int, int, int] = \
            self.biome_calculator.calc_climate_modifiers(temperature, humidity)
        elevation_modifier: float = climate_modifiers[0]
        dryness_modifier: float = climate_modifiers[1]
        min_lakes: int = climate_modifiers[2]
        max_lakes: int = climate_modifiers[3]
        min_lake_expansions: int = climate_modifiers[4]
        max_lake_expansions: int = climate_modifiers[5]

        # Base parameters
        pixel_width: int = gen_request.pixel_width
        hex_diameter: int = gen_request.hex_size

        # Terraform parameters
        initial_land_pct: float = gen_request.initial_land_pct
        required_land_pct: float = gen_request.required_land_pct
        terraform_iterations: int = gen_request.terraform_iterations
        base_layer: Optional[BaseLayer] = BaseLayer(
            self.hex_util,
            pixel_width,
            hex_diameter,
            initial_land_pct,
            required_land_pct,
            False)

        # Island parameters
        min_island_size: int = gen_request.min_island_size

        # Region parameters
        min_region_expansions: int = gen_request.min_region_expansions
        max_region_expansions: int = gen_request.max_region_expansions
        min_region_size_pct: float = gen_request.min_region_size_pct

        acceptable: bool = False
        while not acceptable:
            self.logger.info('Exterior -> Terraforming')
            for n in range(terraform_iterations):
                base_layer.terraform()
            base_layer.finalize()

            acceptable = base_layer.has_enough_land()
            if not acceptable:
                base_layer.randomize()

        self.logger.info('Exterior -> Discovering islands')
        island_layer: IslandLayer = IslandLayer(base_layer, min_island_size)

        running: bool = True
        while running:
            running = island_layer.discover()
        island_layer.clean_up(base_layer)

        self.logger.info('Exterior -> Calculating geographic details')
        geography_layer: GeographyLayer = GeographyLayer(
            self.hex_util,
            base_layer,
            min_lake_expansions,
            max_lake_expansions,
            min_lakes,
            max_lakes)

        running = True
        while running:
            running = geography_layer.place_freshwater()
        geography_layer.finalize()

        self.logger.info('Exterior -> Generating regions')
        region_layer: RegionLayer = RegionLayer(
            self.biome_calculator,
            self.hex_util,
            island_layer,
            min_region_expansions,
            max_region_expansions,
            min_region_size_pct,
            base_layer.total_usable_hexes(),
            elevation_modifier,
            dryness_modifier)

        running = True
        while running:
            running = region_layer.discover(island_layer)
        region_layer.establish_regions_to_merge()

        self.logger.info('Exterior -> Merging regions')
        running = True
        while running:
            running = region_layer.merge(island_layer)
        region_layer.remove_stray_regions(island_layer)

        self.logger.info('Exterior -> Generating features and events')
        feature_layer: FeatureLayer = FeatureLayer(region_layer)
        feature_layer.construct()

        self.logger.info('Exterior -> Serializing')
        serialized: dict = {
            'dimensions': (base_layer.actual_width, base_layer.actual_height),
            'temperature': temperature.name,
            'humidity': humidity.name,
            'islands': island_layer.serialize(),
            'regions': region_layer.serialize(),
            'hexes': base_layer.serialize()
        }

        return json.dumps(serialized, cls=CompactJsonEncoder, indent=2)
