from typing import Optional

from pygame.surface import Surface

from src.processing.map.layer_base import BaseLayer
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.layer_region import RegionLayer
from src.util.constants import background_color, update_rate, frame_rate


class MapGenerator:
    """
    Procedurally generates hexagon-based maps composed of land formations and political regions.
    """
    def __init__(self, pixel_width: int, cell_size: int, terraform_iterations: int):
        self.pixel_width: int = pixel_width
        self.hex_diameter: int = cell_size
        self.terraform_iterations: int = terraform_iterations

        self.base_layer: BaseLayer = BaseLayer(self.pixel_width, self.hex_diameter, True)
        self.island_layer: Optional[IslandLayer] = None
        self.region_layer: Optional[RegionLayer] = None

        self.test_display()

    def test_display(self):
        import pygame

        pygame.init()
        surface: Surface = pygame.display.set_mode((self.base_layer.actual_width, self.base_layer.actual_height))
        pygame.display.set_caption('Bouken Test Display')

        clock = pygame.time.Clock()
        surface.fill(background_color)

        terraform_tick = 0
        island_tick = 0
        region_tick = 0
        terraforming = True
        island_filling = False
        region_filling = False

        running = True
        while running:
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
                        self.base_layer.clear_stray_land()
                        self.island_layer = IslandLayer(self.base_layer)
                        self.base_layer.test_draw(surface)
                        terraforming = False
                        island_filling = True
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
                        self.region_layer = RegionLayer(self.island_layer)
            elif region_filling:
                region_tick -= 1
                if region_tick <= 0:
                    remaining: bool = self.region_layer.discover()
                    if not remaining:
                        self.region_layer.clean_up(self.base_layer)
                        self.base_layer.test_draw(surface)
                        self.region_layer.test_draw(surface)
                        region_filling = False
                    else:
                        region_tick = update_rate

            if terraforming:
                self.base_layer.test_draw(surface)
            elif island_filling:
                self.island_layer.test_draw(surface)
            elif region_filling:
                self.region_layer.test_draw(surface)

            pygame.display.flip()
            clock.tick(frame_rate)

        pygame.quit()
