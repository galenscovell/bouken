import random
from typing import List, Optional, Dict, KeysView

import pygame

from src.processing.map.hex import Hex
from src.processing.map.island import Island
from src.processing.map.layer_base import BaseLayer
from src.util.constants import island_color


class IslandLayer(object):
    """
    Defines island layer of a map, detailing separate areas.
    Interactions directly with this object deal with the Islands dict, its primary data.
    """
    def __init__(self, base_layer: BaseLayer, min_island_size: int):
        self._min_island_size: int = min_island_size
        self._random: random.Random = random.Random()

        # Collect all non-water hexes from base layer grid
        self._usable_hexes: List[Hex] = []
        [self._usable_hexes.append(h) for h in base_layer.generator() if h.is_land()]

        self._island_key_to_island: Dict[int, Island] = {}
        self._current_island: Optional[Island] = None

    def __len__(self) -> int:
        return len(self._island_key_to_island)

    def __setitem__(self, island_key: int, value: Island):
        self._island_key_to_island[island_key] = value

    def __getitem__(self, island_key: int) -> Optional[Island]:
        if island_key in self._island_key_to_island:
            return self._island_key_to_island[island_key]
        return None

    def __delitem__(self, island_key: int):
        if island_key in self._island_key_to_island:
            del self._island_key_to_island[island_key]

    def keys(self) -> KeysView[int]:
        return self._island_key_to_island.keys()

    def values(self) -> List[Island]:
        return list(self._island_key_to_island.values())

    def debug_render(self, surface: pygame.Surface):
        for island_key in self.keys():
            island: Island = self._island_key_to_island[island_key]
            pygame.draw.polygon(surface, island_color, island.get_vertices())

    def serialize(self) -> dict:
        island_map: dict = {}
        for island_id in self.keys():
            island: Island = self[island_id]
            island_map[str(island_id)] = {
                'region-ids': list(island.region_keys),
                'area': island.area,
                'centroid': island.get_centroid(),
                'vertices': island.get_vertices(),
            }

        return island_map

    def discover(self) -> bool:
        """
        Place random island starting hexes.
        Returns True if there is remaining space to discover, False otherwise.
        """
        if self._current_island:
            self.expand()
            return True
        else:
            if self._usable_hexes:
                random_h: Hex = self._random.choice(self._usable_hexes)
                if random_h.is_on_island():
                    self._usable_hexes.remove(random_h)
                else:
                    island_id: int = len(self) + 1
                    new_island: Island = Island(island_id, random_h)
                    self._island_key_to_island[island_id] = new_island
                    self._current_island = new_island

                return True
            else:
                return False

    def expand(self):
        """
        Expand island area outward until it can no longer expand.
        """
        if self._current_island.can_expand:
            self._current_island.expand(self._usable_hexes)
        else:
            for h in self._current_island.hexes:
                if h in self._usable_hexes:
                    self._usable_hexes.remove(h)

            self._current_island = None

    def clean_up(self, base_layer: BaseLayer):
        """
        Ensure that final islands are a minimum size.
        Islands under the threshold have their tiles turned into water.
        """
        to_remove: List[int] = []
        for island_key in self.keys():
            island: Island = self[island_key]
            if len(island.hexes) < self._min_island_size:
                to_remove.append(island_key)

        for island_key in to_remove:
            island: Island = self[island_key]
            for h in island.hexes:
                base_layer[h.x, h.y].set_ocean()
                h.unset_island()

            del self[island_key]
