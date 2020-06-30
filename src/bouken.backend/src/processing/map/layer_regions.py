import random
from typing import List, Optional, Dict, KeysView, Tuple

import pygame
from pygame import freetype

from src.processing.map.hex import Hex
from src.processing.map.island import Island
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.region import Region
from src.util.constants import region_center_color, coast_color


class RegionLayer(object):
    """
    Defines region layer of a map, detailing the political regions on it.
    Interactions directly with this object deal with the Regions dict, its primary data.
    """
    def __init__(self, island_layer: IslandLayer, min_region_expansions: int, max_region_expansions: int,
                 min_region_size_pct: float, total_map_size: int):
        self._min_region_expansions: int = min_region_expansions
        self._max_region_expansions: int = max_region_expansions
        self.min_region_size: int = int(min_region_size_pct * total_map_size)
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
            region_center: Tuple[int, int] = region.get_centroid()
            pygame.draw.polygon(surface, region.color, region.get_vertices())
            # pygame.draw.circle(surface, region_center_color, region.get_centroid(), 4)

            label: str = f'{region_key}: '
            if region.is_coastal:
                label += 'C'
            if region.is_bordering_lake:
                label += 'L'
            if region.is_secluded:
                label += 'A'
            if region.is_surrounded:
                label += 'S'

            font.render_to(surface, (region_center[0] - 12, region_center[1]), label, region_center_color)

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

    def update_neighbors(self):
        """
        Find and set the neighboring regions for each region.
        """
        for region_key in self.keys():
            self[region_key].describe()

    def _get_regions_under_threshold(self) -> List[int]:
        """
        Find regions under size threshold.
        """
        to_remove: List[int] = []
        for region_key in self.keys():
            region = self[region_key]
            if len(region.hexes) < self.min_region_size:
                to_remove.append(region_key)

        return to_remove

    def clean_up(self, island_layer: IslandLayer):
        """
        Ensure that final regions are a minimum size.
        If a region is under the threshold either merge it with neighbors or turn it into water.
        """
        self._merge_regions(island_layer)
        self._make_lakes(island_layer)
        self._randomize_edges()
        self.update_neighbors()

    def _merge_regions(self, island_layer: IslandLayer):
        """
        If region is under threshold, merge it with its smallest neighboring region.
        """
        to_remove: List[int] = self._get_regions_under_threshold()
        while len(to_remove) > 0:
            self.update_neighbors()
            region_key: int = to_remove[-1]
            region = self[region_key]
            island_key: int = region.island_id
            island: Island = island_layer[island_key]

            if len(region.neighbor_region_ids) > 0:
                neighbors: List[Region] = [self[rid] for rid in region.neighbor_region_ids]
                smallest_neighbor: Region = neighbors[0]
                for r in neighbors:
                    if not smallest_neighbor or len(r.hexes) < len(smallest_neighbor.hexes):
                        smallest_neighbor = r

                for h in region.hexes:
                    smallest_neighbor.add_hex(h)

                smallest_neighbor.refresh(region.hexes)
                island.region_keys.remove(region_key)
                del self[region_key]

            to_remove.remove(region_key)
        self.update_neighbors()

    def _make_lakes(self, island_layer: IslandLayer):
        """
        Turn random regions into water.
        """
        lakes_num: int = self._random.randint(1, 4)
        for n in range(lakes_num):
            self.update_neighbors()
            region_key: int = self._random.choice(list(self.keys()))
            region = self[region_key]
            island_key: int = region.island_id
            island: Island = island_layer[island_key]

            for h in region.hexes:
                h.unset_region()
                h.unset_island()

                if region.is_coastal:
                    h.set_ocean()
                else:
                    h.set_lake()

            # If island is now empty (no regions), delete it
            island.region_keys.remove(region_key)
            if not island.region_keys:
                del island_layer[island_key]
            else:
                island.refresh()

            del self[region_key]
        self.update_neighbors()

    def _randomize_edges(self):
        """
        Randomize edges of all regions to reduce uniformity.
        """
        for region_key in self.keys():
            self.update_neighbors()
            region = self[region_key]
            region.randomize_edges(self._random, self._region_key_to_region)
