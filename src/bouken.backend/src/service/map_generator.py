import json
import sys
from typing import Optional

from src.processing.map.layer_base import BaseLayer
from src.processing.map.layer_feature import FeatureLayer
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.layer_regions import RegionLayer
from src.util.compact_json_encoder import CompactJsonEncoder
from src.util.constants import background_color, update_rate, frame_rate


class MapGenerator:
    """
    Procedurally generates hexagon-based maps composed of land features and political regions.
    """
    def __init__(self, pixel_width: int, hex_size: int, initial_land_pct: float, terraform_iterations: int,
                 min_island_size: int, min_region_expansions: int, max_region_expansions: int,
                 min_region_size_pct: float):
        self.pixel_width: int = pixel_width
        self.hex_diameter: int = hex_size
        self.initial_land_pct: float = initial_land_pct
        self.terraform_iterations: int = terraform_iterations

        self.min_island_size: int = min_island_size
        self.min_region_expansions: int = min_region_expansions
        self.max_region_expansions: int = max_region_expansions
        self.min_region_size_pct: float = min_region_size_pct

        self.base_layer: BaseLayer = BaseLayer(self.pixel_width, self.hex_diameter, self.initial_land_pct, False)
        self.island_layer: Optional[IslandLayer] = None
        self.region_layer: Optional[RegionLayer] = None
        self.feature_layer: Optional[FeatureLayer] = None

        # self.generate()
        self.debug_render(realtime=True)

    def generate(self):
        acceptable: bool = False
        while not acceptable:
            print('Generating base layer...')
            for n in range(self.terraform_iterations):
                self.base_layer.terraform()
            self.base_layer.finalize()

            acceptable = self.base_layer.has_enough_land()
            if not acceptable:
                self.base_layer.randomize()
                continue

            print('Generating island layer...')
            self.island_layer = IslandLayer(self.base_layer, self.min_island_size)

            filling_islands: bool = True
            while filling_islands:
                filling_islands = self.island_layer.discover()
            self.island_layer.clean_up(self.base_layer)

        print('Generating region layer...')
        self.region_layer = RegionLayer(
            self.island_layer,
            self.min_region_expansions,
            self.max_region_expansions,
            self.min_region_size_pct,
            self.base_layer.total_usable_hexes()
        )

        print('Placing freshwater...')
        self.region_layer.place_freshwater(self.base_layer)

        filling_regions: bool = True
        while filling_regions:
            filling_regions = self.region_layer.discover(self.island_layer)
        self.region_layer.establish_regions_to_merge()

        merging: bool = True
        while merging:
            merging = self.region_layer.merge(self.island_layer)

        print('Serializing...')
        # self.serialize()

    def serialize(self) -> str:
        serialized: dict = {
            'dimensions': (self.base_layer.actual_width, self.base_layer.actual_height),
            'islands': self.island_layer.serialize(),
            'regions': self.region_layer.serialize(),
            'hexes': self.base_layer.serialize()
        }

        string: str = json.dumps(serialized, cls=CompactJsonEncoder, indent=2)
        return string

    def debug_render(self, realtime=False):
        import pygame
        from pygame import freetype

        pygame.init()
        surface: pygame.Surface = pygame.display.set_mode((self.base_layer.actual_width, self.base_layer.actual_height))
        pygame.display.set_caption('Bouken Map Generation Debug')
        font = freetype.Font('source-code-pro.ttf', 12)

        clock = pygame.time.Clock()
        surface.fill(background_color)

        initial_terraform_iterations: int = self.terraform_iterations
        update_tick = 0
        terraforming = True
        island_filling = False
        region_filling = False
        merging = False
        feature_filling = False

        if not realtime:
            self.generate()

        running = True
        while running:
            if realtime:
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
                        remaining: bool = self.island_layer.discover()
                        if not remaining:
                            self.island_layer.clean_up(self.base_layer)
                            island_filling = False
                            region_filling = True

                        if not island_filling:
                            self.region_layer = RegionLayer(
                                self.island_layer,
                                self.min_region_expansions,
                                self.max_region_expansions,
                                self.min_region_size_pct,
                                self.base_layer.total_usable_hexes()
                            )

                            self.region_layer.place_freshwater(self.base_layer)
                    elif region_filling:
                        discovering: bool = self.region_layer.discover(self.island_layer)
                        if not discovering:
                            self.region_layer.establish_regions_to_merge()
                            region_filling = False
                            merging = True
                    elif merging:
                        merging: bool = self.region_layer.merge(self.island_layer)
                        if not merging:
                            self.feature_layer = FeatureLayer(self.island_layer, self.region_layer)
                            merging = False
                            feature_filling = True
                    elif feature_filling:
                        self.feature_layer.construct()

                if terraforming:
                    self.base_layer.debug_render(surface)
                elif island_filling:
                    self.island_layer.debug_render(surface)
                elif region_filling or merging:
                    self.base_layer.debug_render(surface)
                    self.region_layer.debug_render(surface, font)
                else:
                    self.base_layer.debug_render(surface)
                    # self.region_layer.debug_render(surface, font)
                    self.feature_layer.debug_render(surface, font)

                pygame.display.flip()
                clock.tick(frame_rate)
            else:
                self.base_layer.debug_render(surface)
                self.island_layer.debug_render(surface)
                self.base_layer.debug_render(surface)
                self.region_layer.debug_render(surface, font)
                self.feature_layer.debug_render(surface, font)
                pygame.display.flip()
                clock.tick(frame_rate)

        pygame.quit()
        sys.exit(0)
