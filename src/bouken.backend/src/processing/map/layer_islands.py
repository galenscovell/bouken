from typing import List, Optional

import pygame

from src.processing.map.hex import Hex
from src.processing.map.hex_grid import HexGrid
from src.processing.map.island import Island
from src.processing.map.layer_base import BaseLayer
from src.util.constants import island_color


class IslandLayer(HexGrid):
    """
    Defines island layer of a map, detailing separate areas.
    """
    def __init__(self, base_layer: BaseLayer):
        super().__init__(base_layer._pixel_width, base_layer._hex_size, base_layer._pointy)

        # Recreate base layer grid, but replace all water hexes with nones
        # We only want islands to operate on livable land
        self.usable_hexes: List[Hex] = []
        for x in range(self._columns):
            for y in range(self._rows):
                self[x, y] = None
                if base_layer[x, y]:
                    h: Hex = base_layer[x, y].__copy__()
                    if h and (h.is_land() or h.is_coast() or h.is_forest() or h.is_desert()):
                        self[x, y] = h
                        self.usable_hexes.append(h)

        # Set all neighbors
        for x in range(self._columns):
            for y in range(self._rows):
                h: Hex = self[x, y]
                if h:
                    h.direct_neighbors = self._set_direct_neighbors(h)
                    h.secondary_neighbors = self._set_secondary_neighbors(h)

        self.islands: List[Island] = []
        self.current_island: Optional[Island] = None

    def test_draw(self, surface: pygame.Surface):
        for i in self.islands:
            pygame.draw.polygon(surface, island_color, i.get_vertices())

    def discover(self) -> bool:
        """
        Place random island starting hexes.
        Returns True if there is remaining space to discover, False otherwise.
        """
        self.update_hex_states()
        if self.current_island:
            self.expand()
            return True
        else:
            if self.usable_hexes:
                random_h: Hex = self._random.choice(self.usable_hexes)
                if random_h.is_occupied():
                    self.usable_hexes.remove(random_h)
                else:
                    new_island: Island = Island(random_h)
                    self.islands.append(new_island)
                    self.current_island = new_island

                return True
            else:
                return False

    def expand(self):
        """
        Expand island area outward until it can no longer expand.
        """
        if self.current_island.can_expand:
            self.current_island.expand(self.usable_hexes)
        else:
            for h in self.current_island.hexes:
                if h in self.usable_hexes:
                    self.usable_hexes.remove(h)

            self.islands.append(self.current_island)
            self.current_island = None
