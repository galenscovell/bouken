import random
from typing import List, Optional, Dict, KeysView, Tuple, Set

import pygame
from pygame import freetype

from src.processing.map.hex import Hex
from src.processing.map.island import Island
from src.processing.map.layer_base import BaseLayer
from src.processing.map.layer_islands import IslandLayer
from src.processing.map.region import Region
from src.processing.map.terraform_state import TerraformState
from src.util.constants import region_center_color


class RegionLayer(object):
    """
    Defines region layer of a map, detailing the political regions on it.
    Interactions directly with this object deal with the Regions dict, its primary data.
    """

    def __init__(self, island_layer: IslandLayer, min_region_expansions: int, max_region_expansions: int,
                 min_region_size_pct: float, total_map_size: int):
        self._min_region_expansions: int = min_region_expansions
        self._max_region_expansions: int = max_region_expansions
        self._min_region_size: int = int(min_region_size_pct * total_map_size)

        self._region_key_to_region: Dict[int, Region] = dict()
        self._current_region: Optional[Region] = None
        self._random: random.Random = random.Random()

        # Get all island layer hexes
        self._usable_hexes: Set[Hex] = set()
        for id_key in island_layer.keys():
            island: Island = island_layer[id_key]
            [self._usable_hexes.add(h) for h in island.hexes]

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

    def debug_render(self, surface: pygame.Surface, font: freetype.Font):
        for region_key in self.keys():
            region: Region = self[region_key]
            region_center: Tuple[int, int] = region.get_centroid()

            # pygame.draw.polygon(surface, (region.avg_elevation * 255, 40, 0), region.get_vertices())
            # pygame.draw.polygon(surface, (region.avg_dryness * 255, region.avg_dryness * 255, 40), region.get_vertices())

            pygame.draw.polygon(surface, region_center_color, region.get_vertices(), 4)
            # pygame.draw.circle(surface, region_center_color, region.get_centroid(), 4)
            font.render_to(surface, region_center, str(region_key), region_center_color)

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

    def remove_from_usable_hexes(self, h: Hex):
        if h in self._usable_hexes:
            self._usable_hexes.remove(h)

    def place_freshwater(self, base_layer: BaseLayer):
        """
        Turn a random number of moderate elevation hexes into lakes, expand them, then create rivers flowing
        from them to the ocean.
        """
        # Set initial elevations to ocean only for freshwater placement
        base_layer.set_elevation(include_freshwater=False)

        lakes_num: int = self._random.randint(1, 5)
        lakes_created: int = 0

        high_elevation_hexes_asc: List[Hex] = sorted(list(self._usable_hexes), key=lambda h: h.elevation)
        start_idx: int = len(high_elevation_hexes_asc) // 2
        end_idx: int = start_idx + (start_idx // 2)
        high_elevation_hexes_asc = high_elevation_hexes_asc[start_idx:end_idx]

        while lakes_created < lakes_num and high_elevation_hexes_asc:
            # Expand from a starting hex a random amount
            start_hex: Hex = high_elevation_hexes_asc.pop()
            expansions: int = self._random.randint(1, 5)

            lake_hexes: Set[Hex] = {start_hex}
            latest_expansion: Set[Hex] = set()
            to_expand_from: Set[Hex] = {start_hex}
            while expansions > 0 and to_expand_from:
                for h in to_expand_from:
                    for n in h.direct_neighbors:
                        if n in self._usable_hexes:
                            latest_expansion.add(n)
                            lake_hexes.add(n)

                if latest_expansion:
                    expansions -= 1
                    to_expand_from = latest_expansion.copy()
                    latest_expansion.clear()

            # Find lake exterior
            exterior: List[Hex] = []
            ocean_hit: bool = False
            for h in lake_hexes:
                if h.direct[TerraformState.Ocean] > 0:
                    ocean_hit = True
                elif h.direct[TerraformState.Land] > 0:
                    exterior.append(h)

            if exterior and not ocean_hit:
                # Create river flowing down elevation to the ocean, starting from a random exterior of the lake
                exterior.sort(key=lambda h: h.elevation)
                start_hex: Hex = exterior[0]
                river_hexes: Set[Hex] = set()
                river_choices: List[Hex] = [h for h in start_hex.direct_neighbors
                                            if h.elevation < start_hex.elevation]
                while river_choices:
                    next_hex: Hex = self._random.choice(river_choices)
                    river_hexes.add(next_hex)
                    river_choices = [h for h in next_hex.direct_neighbors
                                     if h.elevation < next_hex.elevation]

                if river_hexes:
                    # If final result was usable, finalize it
                    for h in lake_hexes:
                        h.set_lake()
                        self.remove_from_usable_hexes(h)

                    for h in river_hexes:
                        h.set_river()
                        self.remove_from_usable_hexes(h)

                    lakes_created += 1

        # Set elevation including both ocean and freshwater distances
        base_layer.set_elevation(include_freshwater=True)
        base_layer.set_dryness()
        base_layer.set_depth()

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
            region.set_geographic_details()

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
