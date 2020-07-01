import sys
from typing import Optional

from src.processing.map.layer_base import BaseLayer
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.layer_regions import RegionLayer
from src.processing.map.path_find_mode import PathfindMode
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

        self.base_layer: BaseLayer = BaseLayer(self.pixel_width, self.hex_diameter, self.initial_land_pct, True)
        self.island_layer: Optional[IslandLayer] = None
        self.region_layer: Optional[RegionLayer] = None

        # self.generate()
        self.test_display(realtime=True)
        # self.test_display()

    def generate(self):
        acceptable: bool = False
        while not acceptable:
            for n in range(self.terraform_iterations):
                self.base_layer.terraform_land()
            self.base_layer.clean_up()

            if not self.base_layer.is_acceptable():
                self.base_layer.init()
                continue

            self.island_layer = IslandLayer(self.base_layer, self.min_island_size)

            filling_islands: bool = True
            while filling_islands:
                filling_islands = self.island_layer.discover()
            self.island_layer.clean_up(self.base_layer)

        self.region_layer = RegionLayer(
            self.island_layer,
            self.min_region_expansions,
            self.max_region_expansions,
            self.min_region_size_pct,
            self.base_layer.total_usable_hexes()
        )

        filling_regions: bool = True
        while filling_regions:
            filling_regions = self.region_layer.discover(self.island_layer)
        self.region_layer.clean_up(self.island_layer)

        self.base_layer.find_distance_to_ocean(PathfindMode.Manhattan)
        self.base_layer.find_distance_to_lake(PathfindMode.Manhattan)

    def serialize(self) -> str:
        # Serialize Islands: type, polygon coordinates + area, regions
        # Regions: type, polygon coordinates + area, centroid xy, distance from coast, elevation
        return ''

    def test_display(self, realtime=False):
        import pygame
        from pygame import freetype

        pygame.init()
        surface: pygame.Surface = pygame.display.set_mode((self.base_layer.actual_width, self.base_layer.actual_height))
        pygame.display.set_caption('Bouken Map Generation Debug')
        font = freetype.Font('source-code-pro.ttf', 12)

        clock = pygame.time.Clock()
        surface.fill(background_color)

        initial_terraform_iterations: int = self.terraform_iterations
        terraform_tick = 0
        island_tick = 0
        region_tick = 0
        terraforming = True
        island_filling = False
        region_filling = False

        if not realtime:
            self.generate()

        running = True
        while running:
            if realtime:
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    running = False

                if self.terraform_iterations > 0:
                    terraform_tick -= 1
                    if terraform_tick <= 0:
                        self.base_layer.terraform_land()
                        terraform_tick = update_rate
                        self.terraform_iterations -= 1

                        if self.terraform_iterations == 0:
                            self.base_layer.clean_up()

                            if self.base_layer.is_acceptable():
                                self.island_layer = IslandLayer(self.base_layer, self.min_island_size)
                                self.base_layer.test_draw(surface)
                                terraforming = False
                                island_filling = True
                            else:
                                self.base_layer.init()
                                self.terraform_iterations = initial_terraform_iterations
                elif island_filling:
                    island_tick -= 1
                    if island_tick <= 0:
                        remaining: bool = self.island_layer.discover()
                        if not remaining:
                            self.island_layer.clean_up(self.base_layer)
                            self.base_layer.test_draw(surface)
                            self.island_layer.test_draw(surface)
                            island_filling = False
                            region_filling = True
                        else:
                            island_tick = update_rate

                        if not island_filling:
                            self.region_layer = RegionLayer(
                                self.island_layer,
                                self.min_region_expansions,
                                self.max_region_expansions,
                                self.min_region_size_pct,
                                self.base_layer.total_usable_hexes()
                            )
                elif region_filling:
                    region_tick -= 1
                    if region_tick <= 0:
                        remaining: bool = self.region_layer.discover(self.island_layer)
                        if not remaining:
                            self.region_layer.clean_up(self.island_layer)
                            self.base_layer.find_distance_to_ocean(PathfindMode.Manhattan)
                            self.base_layer.find_distance_to_lake(PathfindMode.Manhattan)
                            self.base_layer.test_draw(surface)
                            self.region_layer.test_draw(surface, font)
                            region_filling = False
                        else:
                            region_tick = update_rate

                if terraforming:
                    self.base_layer.test_draw(surface)
                elif island_filling:
                    self.island_layer.test_draw(surface)
                elif region_filling:
                    self.region_layer.test_draw(surface, font)
                else:
                    self.base_layer.test_draw(surface)

                pygame.display.flip()
                clock.tick(frame_rate)
            else:
                self.base_layer.test_draw(surface)
                self.island_layer.test_draw(surface)
                self.region_layer.test_draw(surface, font)
                self.base_layer.test_draw(surface)
                pygame.display.flip()
                clock.tick(frame_rate)

        pygame.quit()
        sys.exit(0)
