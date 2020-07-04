import random
from typing import List, Optional, Dict, KeysView, Set

import pygame

from src.processing.hex import Hex
from src.processing.island import Island
from src.processing.layer_islands import IslandLayer
from src.processing.region import Region
from src.state.terraform import Terraform
from src.util.constants import region_center_color
from src.util.hex_utils import HexUtils


class RegionLayer(object):
    """
    Defines region layer of a map, detailing the political regions on it.
    Interactions directly with this object deal with the Regions dict, its primary data.
    """
    def __init__(self, island_layer: IslandLayer, min_region_expansions: int, max_region_expansions: int,
                 min_region_size_pct: float, total_map_size: int, base_elevation: float, base_dryness: float):
        self._min_region_expansions: int = min_region_expansions
        self._max_region_expansions: int = max_region_expansions
        self._min_region_size: int = int(min_region_size_pct * total_map_size)

        self._base_elevation: float = base_elevation
        self._base_dryness: float = base_dryness

        self._region_key_to_region: Dict[int, Region] = dict()
        self._current_region: Optional[Region] = None
        self._random: random.Random = random.Random()

        # Get all island layer hexes
        self._usable_hexes: Set[Hex] = set()
        for id_key in island_layer.keys():
            island: Island = island_layer[id_key]
            [self._usable_hexes.add(h) for h in island.hexes if h.is_land()]

        self.to_merge: List[int] = []

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

    def values(self) -> List[Region]:
        return list(self._region_key_to_region.values())

    def debug_render(self, surface: pygame.Surface):
        for region_key in self.keys():
            region: Region = self[region_key]
            if region.base_color != (0, 0, 0):
                for h in region.hexes:
                    h_color = [(h.elevation * c * 2) for c in region.base_color]
                    for i in range(len(h_color)):
                        if h_color[i] > 255:
                            h_color[i] = 255
                    pygame.draw.polygon(surface, h_color, h.vertices)

            pygame.draw.polygon(surface, region_center_color, region.get_vertices(), 4)

            # pygame.draw.circle(surface, region_center_color, region.get_centroid(), 4)
            # font.render_to(surface, region_center, str(region_key), region_center_color)

    def serialize(self) -> dict:
        region_map: dict = dict()
        for region_id in self.keys():
            region: Region = self[region_id]
            region_map[str(region_id)] = {
                'island-id': region.island_id,
                'area': region.area,
                'neighboring-region-ids': list(region.neighbor_region_ids),
                'near-lake': region.near_lake,
                'near-river': region.near_river,
                'coastal': region.is_coastal,
                'secluded': region.is_secluded,
                'surrounded': region.is_surrounded,
                'average-dryness': region.avg_dryness,
                'average-elevation': region.avg_elevation,
                'centroid': region.get_centroid(),
                'vertices': region.get_vertices()
            }

        return region_map

    def discover(self, island_layer: IslandLayer) -> bool:
        """
        Place random region starting hexes.
        Returns True if there is remaining space to discover, False otherwise.
        """
        if self._current_region:
            self.expand()
        else:
            if self._usable_hexes:
                random_hex: Hex = self._random.choice(list(self._usable_hexes))
                if random_hex.is_in_region():
                    self._usable_hexes.remove(random_hex)
                else:
                    region_id: int = len(self) + 1
                    new_region: Region = Region(
                        region_id, random_hex.island_id, random_hex,
                        self._random.randint(self._min_region_expansions, self._max_region_expansions))
                    self[region_id] = new_region
                    self._current_region = new_region
                    island_layer[random_hex.island_id].region_keys.add(region_id)
            else:
                return False
        return True

    def expand(self):
        """
        Expand region's area outward until it can no longer expand.
        """
        if self._current_region.can_expand():
            self._current_region.expand(self._usable_hexes)
        else:
            for h in self._current_region.hexes:
                if h in self._usable_hexes:
                    self._usable_hexes.remove(h)

            self._current_region = None

    def _refresh_regions(self):
        """
        Refresh details for each region.
        """
        for region_key in self.keys():
            self[region_key].update_hex_neighbors()

        for region_key in self.keys():
            region: Region = self[region_key]
            region.set_exterior_details()
            region.set_geographic_details(self._base_elevation, self._base_dryness)

    def establish_regions_to_merge(self):
        """
        Determine which regions ought to be merged to reach an appropriate size.
        """
        self.to_merge: Set[int] = set()
        for region_key in self.keys():
            region = self[region_key]
            if len(region.hexes) < self._min_region_size:
                self.to_merge.add(region_key)

    def merge(self, island_layer: IslandLayer) -> bool:
        """
        Merge smaller regions together to make them larger.
        """
        if self.to_merge:
            self._refresh_regions()
            region_key: int = self.to_merge.pop()
            region = self[region_key]
            island: Island = island_layer[region.island_id]

            if region.neighbor_region_ids:
                neighbors: List[Region] = [self[region_id] for region_id in region.neighbor_region_ids]
                neighbors.sort(key=lambda r: len(r.hexes))

                smallest_neighbor: Region = neighbors[0]
                [smallest_neighbor.add_hex(h) for h in region.hexes]
                smallest_neighbor.update_shape(region.hexes)

                island.region_keys.remove(region_key)
                del self[region_key]

            self._refresh_regions()
            return True
        return False

    def remove_stray_regions(self, island_layer: IslandLayer):
        """
        Remove any regions composed of less than 6 hexes post-merge.
        """
        to_remove: List[int] = []
        for region_key in self.keys():
            region = self[region_key]
            if len(region.hexes) < 4:
                to_remove.append(region_key)

        new_ocean_hexes: List[Hex] = []
        for region_key in to_remove:
            region = self[region_key]
            for h in region.hexes:
                h.set_ocean()
                h.unset_island()
                h.unset_region()
                new_ocean_hexes.append(h)

            island: Island = island_layer[region.island_id]
            island.region_keys.remove(region_key)
            del self[region_key]

        # Calculate water depth for the new ocean hexes
        for h in new_ocean_hexes:
            depth: float = HexUtils.distance(h, [Terraform.Land])
            h.depth = depth
