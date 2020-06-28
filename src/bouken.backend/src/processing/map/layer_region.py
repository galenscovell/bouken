from typing import List, Set

import pygame

from src.processing.map.hex import Hex
from src.processing.map.hex_grid import HexGrid
from src.processing.map.layer_base import BaseLayer
from src.processing.map.region import Region
from src.util.constants import region_center_color


class RegionLayer(HexGrid):
    """
    Defines region layer of a map, detailing the political regions on it.
    """
    def __init__(self, base_layer: BaseLayer):
        # Recreate base layer grid, but replacing all water hexes with nones
        # We only want regions to operate on livable land
        super().__init__(base_layer._pixel_width, base_layer._hex_size, base_layer._pointy)

        self.usable_hexes: Set[Hex] = set()
        for x in range(self._columns):
            for y in range(self._rows):
                h: Hex = base_layer[x, y]
                if h and (h.is_land() or h.is_coast() or h.is_forest() or h.is_desert()):
                    self[x, y] = h.__copy__()
                    self[x, y].set_occupied()
                    self[x, y].direct_neighbors = self._set_direct_neighbors(h)
                    self[x, y].secondary_neighbors = self._set_secondary_neighbors(h)
                    self.usable_hexes.add(h)
                else:
                    self[x, y] = None

        self.regions: List[Region] = []
        self.init(10)

    def test_draw(self, surface: pygame.Surface):
        for r in self.regions:
            pygame.draw.polygon(surface, r.color, r.get_vertices())
            pygame.draw.circle(surface, region_center_color, r.get_centroid(), 6)

    def init(self, starters: int):
        """
        Place random region starting hexes with distinct colors.
        """
        usable = list(self.usable_hexes.copy())
        for n in range(starters):
            h: Hex = self._random.choice(usable)
            usable.remove(h)
            region_color = (self._random.randint(0, 255), self._random.randint(0, 255), self._random.randint(0, 255))
            self.regions.append(Region(h, region_color))

    def expand(self):
        """
        Expand region areas outwards from center.
        """
        for r in self.regions:
            self.update_hex_states()
            r.expand(self.usable_hexes)
