from typing import Dict, List

import pygame
from pygame import freetype

from src.processing.map.feature import Feature
from src.processing.map.island import Island
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.layer_regions import RegionLayer
from src.processing.map.region import Region


class FeatureLayer(object):
    """
    Defines feature layer of a map, detailing its landscape/biome features.
    """
    def __init__(self, island_layer: IslandLayer, region_layer: RegionLayer):
        self.islands: Dict[int, Island] = {}
        for island_id in island_layer.keys():
            self.islands[island_id] = island_layer[island_id]

        self.regions: Dict[int, Region] = {}
        for region_id in region_layer.keys():
            self.regions[region_id] = region_layer[region_id]

        self.features: Dict[str, List[Feature]] = dict()

    def debug_render(self, surface: pygame.Surface, font: freetype.Font):
        # label: str = f'{region_key}: '
        # if region.is_coastal:
        #     label += 'C'
        # if region.is_bordering_lake:
        #     label += 'L'
        # if region.is_secluded:
        #     label += 'A'
        # if region.is_surrounded:
        #     label += 'S'
        # font.render_to(surface, (region_center[0] - 48, region_center[1] + 12), label, region_center_color)
        return

    def construct(self):
        self._place_mountains()
        self._place_biome_elements()
        self._place_caves()
        self._place_structures()
        self._place_events()

    def _place_mountains(self):
        """
        Place mountain features in areas of high elevation hexes.
        """
        return

    def _place_biome_elements(self):
        """
        Place biome-related elements (snow, marsh, forest, grassland, etc.).
        Elevation   Dryness     Biome       Description
        High        High        Scorched    Mountains, sand, barren, caves, reduced life
        High        Moderate    Tundra      Frozen, permafrost, patchy vegetation, caverns, reduced life
        High        Low         Snow        Snow, ice lakes, ice caverns, reduced life
        Moderate    High        Cold Desert Snow, sand, reduced life
        Moderate    Moderate    Deciduous   Forests, marshes, life
        Moderate    Low         Taiga       Boreal forests, life
        Low         High        Hot Desert  Sand, reduced life
        Low         Moderate    Grassland   Prairies, life
        Low         Low         Tropical    Jungles, life
        """
        return

    def _place_caves(self):
        """
        Place cave features randomly.
        """
        return

    def _place_structures(self):
        """
        Place structure features in areas of low elevation and low dryness.
        """
        return

    def _place_events(self):
        """
        Add events to each placed feature.
        """
        return
