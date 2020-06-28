from typing import List, Optional

import pygame

from src.processing.map.hex import Hex
from src.processing.map.hex_grid import HexGrid
from src.processing.map.layer_base import BaseLayer
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.region import Region
from src.util.constants import region_center_color


class RegionLayer(HexGrid):
    """
    Defines region layer of a map, detailing the political regions on it.
    """
    def __init__(self, island_layer: IslandLayer,
                 min_region_expansions: int, max_region_expansions: int, min_region_size: int):
        super().__init__(island_layer._pixel_width, island_layer._hex_size, island_layer._pointy)

        self.min_region_expansions: int = min_region_expansions
        self.max_region_expansions: int = max_region_expansions
        self.min_region_size: int = min_region_size

        # Get all island layer hexes
        self.usable_hexes: List[Hex] = []
        for island in island_layer.islands:
            [self.usable_hexes.append(h) for h in island.hexes]

        self.regions: List[Region] = []
        self.current_region: Optional[Region] = None

    def test_draw(self, surface: pygame.Surface):
        for r in self.regions:
            pygame.draw.polygon(surface, r.color, r.get_vertices())
            pygame.draw.circle(surface, region_center_color, r.get_centroid(), 4)

    def discover(self) -> bool:
        """
        Place random region starting hexes.
        Returns True if there is remaining space to discover, False otherwise.
        """
        self.update_hex_states()
        if self.current_region:
            self.expand()
        else:
            if self.usable_hexes:
                random_h: Hex = self._random.choice(self.usable_hexes)
                if random_h.is_in_region():
                    self.usable_hexes.remove(random_h)
                else:
                    region_color = (
                        self._random.randint(0, 255), self._random.randint(0, 255), self._random.randint(0, 255))
                    region_expansions: int = self._random.randint(self.min_region_expansions, self.max_region_expansions)
                    new_region: Region = Region(random_h, region_color, region_expansions)
                    self.regions.append(new_region)
                    self.current_region = new_region
            else:
                return False
        return True

    def expand(self):
        """
        Expand regions area outward until they can no longer expand.
        """
        if self.current_region.can_expand():
            self.current_region.expand(self.usable_hexes)
        else:
            for h in self.current_region.hexes:
                if h in self.usable_hexes:
                    self.usable_hexes.remove(h)

                self.current_region = None

    def clean_up(self, base_layer: BaseLayer):
        """
        Ensure that final islands are a minimum size.
        Regions under the threshold have their tiles turned into water.
        """
        to_remove: List[Region] = []
        for r in self.regions:
            if len(r.hexes) < self.min_region_size:
                to_remove.append(r)

        for r in to_remove:
            self.regions.remove(r)
            for h in r.hexes:
                base_layer[h.x, h.y].set_water()
                h.unset_region()
