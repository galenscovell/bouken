import json
import sys
from typing import Optional

from backend.processing.exterior.base_layer import BaseLayer
from backend.processing.exterior.feature_layer import FeatureLayer
from backend.processing.exterior.geography_layer import GeographyLayer
from backend.processing.exterior.island_layer import IslandLayer
from backend.processing.exterior.region_layer import RegionLayer
from backend.state.humidity import Humidity
from backend.state.temperature import Temperature
from backend.util.biome_calculator import BiomeCalculator
from backend.util.compact_json_encoder import CompactJsonEncoder
from backend.util.constants import background_color, update_rate, frame_rate
from backend.util.logger import Logger


class ExteriorMapGenerator:
    """
    Procedurally generates hexagon-based exterior maps composed of land features and regions.
    """
    def __init__(self, logger: Logger) -> None:
        self.logger: Logger = logger
    

    def begin(self, pixel_width: int, hex_size: int, initial_land_pct: float, required_land_pct: float, terraform_iterations: int, min_island_size: int, humidity: Humidity, temperature: Temperature, min_region_expansions: int, max_region_expansions: int, min_region_size_pct: float) -> str:
        # Biome
        self.temperature: Temperature = temperature
        self.humidity: Humidity = humidity
        self.elevation_modifier, self.dryness_modifier, self.min_lakes, self.max_lakes, self.min_lake_expansions, \
            self.max_lake_expansions = BiomeCalculator.calculate_climate_modifiers(temperature, humidity)

        # Base parameters
        self.pixel_width: int = pixel_width
        self.hex_diameter: int = hex_size

        # Terraform parameters
        self.initial_land_pct: float = initial_land_pct
        self.required_land_pct: float = required_land_pct
        self.terraform_iterations: int = terraform_iterations
        self.base_layer: BaseLayer = BaseLayer(self.pixel_width, self.hex_diameter, self.initial_land_pct, self.required_land_pct, False)

        # Island parameters
        self.min_island_size: int = min_island_size
        self.island_layer: Optional[IslandLayer] = None

        # Geography parameters
        self.geography_layer: Optional[GeographyLayer] = None

        # Region parameters
        self.min_region_expansions: int = min_region_expansions
        self.max_region_expansions: int = max_region_expansions
        self.min_region_size_pct: float = min_region_size_pct
        self.region_layer: Optional[RegionLayer] = None

        # Feature parameters
        self.feature_layer: Optional[FeatureLayer] = None

        return self.generate()


    def generate(self) -> str:
        acceptable: bool = False
        while not acceptable:
            self.logger.info('Exterior -> Terraforming')
            for n in range(self.terraform_iterations):
                self.base_layer.terraform()
            self.base_layer.finalize()

            acceptable = self.base_layer.has_enough_land()
            if not acceptable:
                self.base_layer.randomize()

        self.logger.info('Exterior -> Discovering islands')
        self.island_layer = IslandLayer(self.base_layer, self.min_island_size)

        running: bool = True
        while running:
            running = self.island_layer.discover()
        self.island_layer.clean_up(self.base_layer)

        self.logger.info('Exterior -> Calculating geographic details')
        self.geography_layer = GeographyLayer(self.base_layer, self.min_lake_expansions, self.max_lake_expansions, self.min_lakes, self.max_lakes)

        running = True
        while running:
            running = self.geography_layer.place_freshwater()
        self.geography_layer.finalize()

        self.logger.info('Exterior -> Generating regions')
        self.region_layer = RegionLayer(self.island_layer, self.min_region_expansions, self.max_region_expansions, self.min_region_size_pct, self.base_layer.total_usable_hexes(), self.elevation_modifier, self.dryness_modifier)

        running = True
        while running:
            running = self.region_layer.discover(self.island_layer)
        self.region_layer.establish_regions_to_merge()

        self.logger.info('Exterior -> Merging regions')
        running = True
        while running:
            running = self.region_layer.merge(self.island_layer)
        self.region_layer.remove_stray_regions(self.island_layer)

        self.logger.info('Exterior -> Generating features and events')
        self.feature_layer = FeatureLayer(self.region_layer)
        self.feature_layer.construct()

        self.logger.info('Exterior -> Serializing')
        return self.serialize()

    def serialize(self) -> str:
        serialized: dict = {
            'dimensions': (self.base_layer.actual_width, self.base_layer.actual_height),
            'temperature': self.temperature.name,
            'humidity': self.humidity.name,
            'islands': self.island_layer.serialize(),
            'regions': self.region_layer.serialize(),
            'hexes': self.base_layer.serialize()
        }

        return json.dumps(serialized, cls=CompactJsonEncoder, indent=2)

    def debug_render(self) -> None:
        import pygame
        from pygame import freetype

        pygame.init()
        surface: pygame.Surface = pygame.display.set_mode((self.base_layer.actual_width, self.base_layer.actual_height))
        pygame.display.set_caption('Bouken Exterior Map Debug')
        font = freetype.Font('source-code-pro.ttf', 12)

        clock = pygame.time.Clock()
        surface.fill(background_color)

        initial_terraform_iterations: int = self.terraform_iterations
        update_tick = 0
        terraforming = True
        island_filling = False
        placing_freshwater = False
        region_filling = False
        merging = False
        feature_filling = False

        running = True
        while running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False

            update_tick -= 1
            if update_tick <= 0:
                update_tick = update_rate

                if self.terraform_iterations > 0:
                    self.base_layer.terraform()
                    self.terraform_iterations -= 1

                    if self.terraform_iterations == 0:
                        self.base_layer.finalize()

                        if self.base_layer.has_enough_land():
                            self.island_layer = IslandLayer(self.base_layer, self.min_island_size)
                            self.base_layer.debug_render(surface)
                            terraforming = False
                            island_filling = True
                        else:
                            self.base_layer.randomize()
                            self.terraform_iterations = initial_terraform_iterations
                elif island_filling:
                    processing: bool = self.island_layer.discover()
                    if not processing:
                        self.island_layer.clean_up(self.base_layer)
                        self.geography_layer = GeographyLayer(self.base_layer, self.min_lake_expansions, self.max_lake_expansions, self.min_lakes, self.max_lakes)
                        island_filling = False
                        placing_freshwater = True
                elif placing_freshwater:
                    processing: bool = self.geography_layer.place_freshwater()
                    if not processing:
                        self.geography_layer.finalize()
                        self.region_layer = RegionLayer(self.island_layer, self.min_region_expansions, self.max_region_expansions, self.min_region_size_pct, self.base_layer.total_usable_hexes(), self.elevation_modifier, self.dryness_modifier)

                        placing_freshwater = False
                        region_filling = True
                elif region_filling:
                    processing: bool = self.region_layer.discover(self.island_layer)
                    if not processing:
                        self.region_layer.establish_regions_to_merge()
                        region_filling = False
                        merging = True
                elif merging:
                    processing: bool = self.region_layer.merge(self.island_layer)
                    if not processing:
                        self.region_layer.remove_stray_regions(self.island_layer)
                        self.feature_layer = FeatureLayer(self.region_layer)
                        merging = False
                        feature_filling = True
                elif feature_filling:
                    self.feature_layer.construct()

            if terraforming or placing_freshwater:
                self.base_layer.debug_render(surface)
            elif island_filling:
                self.island_layer.debug_render(surface)
            elif region_filling or merging:
                self.base_layer.debug_render(surface)
                self.region_layer.debug_render(surface)
            else:
                self.base_layer.debug_render(surface)
                self.region_layer.debug_render(surface)
                self.feature_layer.debug_render(surface, font)

            pygame.display.flip()
            clock.tick(frame_rate)

        pygame.quit()
        sys.exit(0)
