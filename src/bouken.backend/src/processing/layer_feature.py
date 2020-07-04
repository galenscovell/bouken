from typing import Dict, List

import pygame
from pygame import freetype

from src.processing.feature import Feature
from src.processing.island import Island
from src.processing.layer_islands import IslandLayer
from src.processing.layer_regions import RegionLayer
from src.processing.region import Region


class FeatureLayer(object):
    """
    Defines feature layer of a map, detailing its landscape features and events.
    """
    def __init__(self, island_layer: IslandLayer, region_layer: RegionLayer):
        self.islands: Dict[int, Island] = dict()
        for island_id in island_layer.keys():
            self.islands[island_id] = island_layer[island_id]

        self.regions: Dict[int, Region] = dict()
        for region_id in region_layer.keys():
            self.regions[region_id] = region_layer[region_id]

        self.features: Dict[str, List[Feature]] = dict()

    def debug_render(self, surface: pygame.Surface, font: freetype.Font):
        # font.render_to(surface, (region_center[0] - 48, region_center[1] + 12), label, region_center_color)
        return

    def construct(self):
        """
        Details we have for each region:
            Biome, coastal, near-lake, near-river, secluded, surrounded, neighbor regions, island,
            elevation (avg and per hex), dryness (avg and per hex), area.
        """
        self._place_mountains()
        self._place_forests()
        self._place_open_areas()
        self._place_caves()
        self._place_structures()
        self._generate_events()

    def _place_mountains(self):
        """
        Place mountain/canyon/cliff/peak features.
        """
        return

    def _place_forests(self):
        """
        Place forest/jungle/woodland/marsh/thicket/grove features.
        """
        return

    def _place_open_areas(self):
        """
        Place meadow/prairie/savanna/plain features.
        """
        return

    def _place_caves(self):
        """
        Place cave/cavern/grotto/den features.
        """
        return

    def _place_structures(self):
        """
        Place structure/temple/town/fortress/ruins features.
        """
        return

    def _generate_events(self):
        """
        Add events to each placed feature.
        """
        return
