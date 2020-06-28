import random
from typing import List, Optional

import pygame

from src.processing.map.hex import Hex
from src.processing.map.island import Island
from src.processing.map.layer_base import BaseLayer
from src.util.constants import island_color


class IslandLayer(object):
    """
    Defines island layer of a map, detailing separate areas.
    """
    def __init__(self, base_layer: BaseLayer, min_island_size: int):
        self.min_island_size: int = min_island_size
        self._random: random.Random = random.Random()

        # Collect all non-water hexes from base layer grid
        self.usable_hexes: List[Hex] = []
        [self.usable_hexes.append(h) for h in base_layer.generator() if h.is_land()]

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
        if self.current_island:
            self.expand()
            return True
        else:
            if self.usable_hexes:
                random_h: Hex = self._random.choice(self.usable_hexes)
                if random_h.is_on_island():
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

            self.current_island = None

    def clean_up(self, base_layer: BaseLayer):
        """
        Ensure that final islands are a minimum size.
        Islands under the threshold have their tiles turned into water.
        """
        to_remove: List[Island] = []
        for i in self.islands:
            if len(i.hexes) < self.min_island_size:
                to_remove.append(i)

        for i in to_remove:
            self.islands.remove(i)
            for h in i.hexes:
                base_layer[h.x, h.y].set_water()
                h.unset_island()
