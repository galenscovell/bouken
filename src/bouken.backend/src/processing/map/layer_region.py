from typing import List

import pygame

from src.processing.map.hex import Hex
from src.processing.map.hex_grid import HexGrid
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.region import Region
from src.util.constants import region_center_color


class RegionLayer(HexGrid):
    """
    Defines region layer of a map, detailing the political regions on it.
    """
    def __init__(self, island_layer: IslandLayer):
        super().__init__(island_layer._pixel_width, island_layer._hex_size, island_layer._pointy)

        # Recreate island layer grid
        self.usable_hexes: List[Hex] = []
        for x in range(self._columns):
            for y in range(self._rows):
                self[x, y] = None
                if island_layer[x, y]:
                    h: Hex = island_layer[x, y].__copy__()
                    if h:
                        h.set_unoccupied()
                        self[x, y] = h
                        self.usable_hexes.append(h)

        # Set all neighbors
        for x in range(self._columns):
            for y in range(self._rows):
                h: Hex = self[x, y]
                if h:
                    h.direct_neighbors = self._set_direct_neighbors(h)
                    h.secondary_neighbors = self._set_secondary_neighbors(h)

        self.regions: List[Region] = []
        self.init(10)

    def test_draw(self, surface: pygame.Surface):
        for r in self.regions:
            pygame.draw.polygon(surface, r.color, r.get_vertices())
            pygame.draw.circle(surface, region_center_color, r.get_centroid(), 4)

    def init(self, starters: int):
        """
        Place random region starting hexes with distinct colors.
        """
        for n in range(starters):
            h: Hex = self._random.choice(self.usable_hexes)
            self.usable_hexes.remove(h)
            region_color = (self._random.randint(0, 255), self._random.randint(0, 255), self._random.randint(0, 255))
            self.regions.append(Region(h, region_color))

    def expand(self):
        """
        Expand region areas outwards from center.
        """
        for r in self.regions:
            self.update_hex_states()
            r.expand(self.usable_hexes)
