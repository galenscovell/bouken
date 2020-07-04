from typing import Dict, List, Tuple

import pygame
from pygame import freetype

from src.processing.layer_regions import RegionLayer
from src.processing.region import Region
from src.util.constants import region_center_color


class FeatureLayer(object):
    """
    Defines feature layer of a map, detailing its landscape features and events.
    """
    def __init__(self, region_layer: RegionLayer):
        self.regions: Dict[int, Region] = dict()
        for region_id in region_layer.keys():
            self.regions[region_id] = region_layer[region_id]

    def debug_render(self, surface: pygame.Surface, font: freetype.Font):
        for region_key in self.regions.keys():
            region: Region = self.regions[region_key]
            center: Tuple[int, int] = region.get_centroid()

            label: str = f'{region.region_id}'
            if region.is_coastal:
                label += 'C'
            if region.near_lake:
                label += 'L'
            if region.near_river:
                label += 'R'
            if region.is_secluded:
                label += 'A'
            if region.is_surrounded:
                label += 'S'

            font.render_to(surface, (center[0] - 12, center[1]), label, region_center_color)

    def construct(self):
        """
        Details we have for each region:
            Biome, coastal, near-lake, near-river, secluded, surrounded, neighbor regions, island,
            elevation (avg and per hex), dryness (avg and per hex), area.
        """
        return

    def _handle_scorched_biome(self):
        """
        Vegetation  Life        Features
        Limited     Limited     Mountains, rocky, caves
        """
        return

    def _handle_tundra_biome(self):
        """
        Vegetation  Life        Features
        Reduced     Reduced     Permafrost, caverns
        """
        return

    def _handle_snow_biome(self):
        """
        Vegetation  Life        Features
        Limited     Reduced     Snow, ice lakes, ice caverns
        """
        return

    def _handle_cold_desert_biome(self):
        """
        Vegetation  Life        Features
        Limited     Limited     Snow, sand
        """
        return

    def _handle_deciduous_biome(self):
        """
        Vegetation  Life        Features
        High        High        Forests, marshes
        """
        return

    def _handle_taiga_biome(self):
        """
        Vegetation  Life        Features
        High        High        Boreal forests
        """
        return

    def _handle_hot_desert_biome(self):
        """
        Vegetation  Life        Features
        Limited     Limited     Sand, dunes
        """
        return

    def _handle_grassland_biome(self):
        """
        Vegetation  Life        Features
        High        High        Prairies, canyons
        """
        return

    def _handle_tropical_biome(self):
        """
        Vegetation  Life        Features
        High        High        Jungles
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
        Place structure/temple/town/fortress/ruins features.
        """
        return

    def _generate_events(self):
        """
        Add events to each placed feature.
        """
        return
