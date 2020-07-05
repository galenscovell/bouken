from typing import Dict, List, Tuple

import pygame
from pygame import freetype

from src.processing.layer_regions import RegionLayer
from src.processing.region import Region
from src.util.constants import text_color


class FeatureLayer(object):
    """
    Defines feature layer of a map, detailing its landscape features and events.
    """
    def __init__(self, region_layer: RegionLayer):
        self.regions: Dict[int, Region] = dict()
        for region_id in region_layer.keys():
            self.regions[region_id] = region_layer[region_id]

    def debug_render(self, surface: pygame.Surface, font: freetype.Font):
        return
        # for region_key in self.regions.keys():
        #     region: Region = self.regions[region_key]
        #     center: Tuple[int, int] = region.get_centroid()
        #     font.render_to(surface, (center[0] - 32, center[1] + 12), str(region.biome.name), text_color)

    def construct(self):
        """
        Details we have for each region:
            Biome, coastal, near-lake, near-river, secluded, surrounded, neighbor regions, island,
            elevation (avg and per hex), dryness (avg and per hex), area.
        """
        return

    def _handle_bare_biome(self):
        """
        Vegetation  Life        Features
        1           1           Mountains, rocky, caves
        """
        return

    def _handle_snow_biome(self):
        """
        Vegetation  Life        Features
        1           1           Snow, caverns (ice)
        """
        return

    def _handle_tundra_biome(self):
        """
        Vegetation  Life        Features
        2           3           Cold wasteland, permafrost, rocky
        """
        return

    def _handle_temperate_desert_biome(self):
        """
        Vegetation  Life        Features
        2           3           Snow and sand (seasonal), salt
        """
        return

    def _handle_temperate_forest(self):
        """
        Vegetation  Life        Features
        5           5           Mountains, hills, dense canopy, fog
        """
        return

    def _handle_taiga_biome(self):
        """
        Vegetation  Life        Features
        3           3           Forests (boreal)
        """
        return

    def _handle_tropical_desert_biome(self):
        """
        Vegetation  Life        Features
        1           2           Sand, dunes, flat, oasis
        """
        return

    def _handle_grassland_biome(self):
        """
        Vegetation  Life        Features
        3           4           Prairies, savannas, canyons, sparse vegetation
        """
        return

    def _handle_tropical_forest(self):
        """
        Vegetation  Life        Features
        5           5           Jungles, tall tress/dense canopy, fog
        """
        return

    def _place_mountains(self):
        """
        Place mountain/canyon/cliff/peak features.
        High elevation regions
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
        Place structure/temple/town/fortress/outposts/village/ruins features.
        """
        return

    def _generate_events(self):
        """
        Add events to each placed feature.
        """
        return
