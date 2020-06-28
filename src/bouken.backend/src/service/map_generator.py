from typing import Optional

from pygame.surface import Surface

from src.models.map.layer_base import BaseLayer
from src.models.map.layer_region import RegionLayer
from src.util.constants import background_color, update_rate, frame_rate


class MapGenerator:
    """
    Procedurally generates hexagon-based maps composed of land formations and political regions.
    """
    def __init__(self, pixel_width: int, cell_size: int, terraform_iterations: int, political_iterations: int):
        self.pixel_width: int = pixel_width
        self.hex_diameter: int = cell_size
        self.terraform_iterations: int = terraform_iterations
        self.political_iterations: int = political_iterations

        self.base_layer: BaseLayer = BaseLayer(self.pixel_width, self.hex_diameter, True)
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
        political_tick = 0
        while pygame.event.poll().type != pygame.QUIT:
            if self.terraform_iterations > 0:
                terraform_tick -= 1
                if terraform_tick <= 0:
                    self.base_layer.terraform_land()
                    terraform_tick = update_rate
                    self.terraform_iterations -= 1

                    if self.terraform_iterations == 0:
                        self.base_layer.terraform_water()
                        self.base_layer.cleanup()
                        self.base_layer.terraform_forests()
                        self.region_layer = RegionLayer(self.base_layer)

            elif self.political_iterations > 0:
                political_tick -= 1
                if political_tick <= 0:
                    self.region_layer.expand()

            self.base_layer.test_draw(surface)

            if self.terraform_iterations == 0:
                self.region_layer.test_draw(surface)

            pygame.display.flip()
            clock.tick(frame_rate)

        pygame.quit()
