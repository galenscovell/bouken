import random
from typing import List, Optional, Dict, KeysView

import pygame
from pygame import freetype

from src.processing.map.hex import Hex
from src.processing.map.island import Island
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.region import Region
from src.util.constants import region_center_color


class RegionLayer(object):
    """
    Defines region layer of a map, detailing the political regions on it.
    Interactions directly with this object deal with the Regions dict, its primary data.
    """
    def __init__(self, island_layer: IslandLayer, min_region_expansions: int, max_region_expansions: int,
                 min_region_area_pct: float, min_lake_area_pct: float):
        self._min_region_expansions: int = min_region_expansions
        self._max_region_expansions: int = max_region_expansions
        self._min_region_area_pct: float = min_region_area_pct
        self._min_lake_area_pct: float = min_lake_area_pct
        self._random: random.Random = random.Random()

        # Get all island layer hexes
        self._usable_hexes: List[Hex] = []
        for id_key in island_layer.keys():
            island: Island = island_layer[id_key]
            [self._usable_hexes.append(h) for h in island.hexes]

        self._region_key_to_region: Dict[int, Region] = {}
        self._current_region: Optional[Region] = None

    def __len__(self) -> int:
        return len(self._region_key_to_region)

    def __setitem__(self, id_key: int, value: Region):
        self._region_key_to_region[id_key] = value

    def __getitem__(self, id_key: int) -> Optional[Region]:
        if id_key in self._region_key_to_region:
            return self._region_key_to_region[id_key]
        return None

    def __delitem__(self, key):
        if key in self._region_key_to_region:
            del self._region_key_to_region[key]

    def keys(self) -> KeysView[int]:
        return self._region_key_to_region.keys()

    def test_draw(self, surface: pygame.Surface, font: freetype.Font):
        for region_key in self.keys():
            region: Region = self._region_key_to_region[region_key]
            pygame.draw.polygon(surface, region.color, region.get_vertices())
            # pygame.draw.circle(surface, region_center_color, region.get_centroid(), 4)
            font.render_to(surface, region.get_centroid(), str(region_key), region_center_color)

    def discover(self, island_layer: IslandLayer) -> bool:
        """
        Place random region starting hexes.
        Returns True if there is remaining space to discover, False otherwise.
        """
        if self._current_region:
            self.expand()
        else:
            if self._usable_hexes:
                random_hex: Hex = self._random.choice(self._usable_hexes)
                if random_hex.is_in_region():
                    self._usable_hexes.remove(random_hex)
                else:
                    region_id: int = len(self) + 1
                    new_region: Region = Region(
                        region_id, random_hex.island_id, random_hex,
                        (self._random.randint(0, 255), self._random.randint(0, 255), self._random.randint(0, 255)),
                        self._random.randint(self._min_region_expansions, self._max_region_expansions))
                    self._region_key_to_region[region_id] = new_region
                    self._current_region = new_region
                    island_layer[random_hex.island_id].region_keys.add(region_id)
            else:
                return False
        return True

    def expand(self):
        """
        Expand regions area outward until they can no longer expand.
        """
        if self._current_region.can_expand():
            self._current_region.expand(self._usable_hexes)
        else:
            for h in self._current_region.hexes:
                if h in self._usable_hexes:
                    self._usable_hexes.remove(h)

                self._current_region = None

    def clean_up(self, island_layer: IslandLayer):
        """
        Ensure that final regions are a minimum size - any under threshold have tiles become water.
        Also add lakes to particularly large regions.
        """
        # Determine which regions to entirely remove
        to_remove: List[int] = []
        for region_key in self.keys():
            region = self[region_key]
            island_threshold: float = island_layer[region.island_id].area * self._min_region_area_pct
            if region.area <= island_threshold:
                to_remove.append(region_key)

        # Remove them from islands. If island is then empty, delete it
        for region_key in to_remove:
            region = self[region_key]
            del self[region_key]
            for h in region.hexes:
                h.set_ocean()
                h.unset_region()
                h.unset_island()

            island_key: int = region.island_id
            island: Island = island_layer[island_key]
            island.region_keys.remove(region_key)
            if not island.region_keys:
                del island_layer[island_key]
            else:
                island.refresh()

        # Determine which regions to add lakes to, then do so
        # for region_key in self.keys():
        #     region = self[region_key]
        #     island_threshold: float = island_layer[region.island_id].area * self._min_lake_area_pct
        #     if region.area > island_threshold:
        #         lake_hex: List[Hex] = region.create_lake(self._random)
        #         for h in lake_hex:
        #             h.set_lake()
        #             h.unset_region()
        #             h.unset_island()
