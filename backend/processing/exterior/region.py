from __future__ import annotations

from typing import List, Tuple, Set

from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from processing.exterior.hex import Hex
from state.biome import Biome
from state.terraform import Terraform
from util.i_biome_calculator import IBiomeCalculator


class Region:
    """
    Defines a region of a map, composed of multiple hexes.
    """
    def __init__(self, region_id: int, island_id: int, start_hex: Hex, expansions: int) -> None:
        self.region_id: int = region_id
        self.island_id: int = island_id
        self.hexes: Set[Hex] = {start_hex}

        self.exterior_hexes: Set[Hex] = set()
        self.coast_hexes: Set[Hex] = set()
        self.neighbor_region_ids: Set[int] = set()

        self._expanded_hexes: Set[Hex] = {start_hex}
        self._expansions: int = expansions
        self._can_expand: bool = True

        self.polygon: Polygon = Polygon(start_hex.vertices)
        self.area: float = self.polygon.area

        self.is_coastal: bool = False
        self.is_secluded: bool = False
        self.is_surrounded: bool = False
        self.near_lake: bool = False
        self.near_river: bool = False

        self.avg_elevation: float = 0.0
        self.avg_dryness: float = 0.0
        self.biome: Biome = Biome.Bare
        self.base_color: Tuple[int, int, int] = (0, 0, 0)

        start_hex.set_region(self.region_id)

    def add_hex(self, h: Hex) -> None:
        """
        Add a hex to this region.
        """
        h.set_region(self.region_id)
        self.hexes.add(h)

    def update_shape(self, to_join_hexes=None) -> None:
        """
        Refresh this region's polygon shape and area.
        """
        to_join = [self.polygon]
        if to_join_hexes:
            for h in to_join_hexes:
                to_join.append(Polygon(h.vertices))
        else:
            for h in self.hexes:
                to_join.append(Polygon(h.vertices))

        self.polygon = unary_union(to_join)
        self.area = self.polygon.area

    def get_vertices(self) -> List[Tuple[int, int]]:
        """
        Get this region's exterior vertices defining its shape.
        """
        return [(int(p[0]), int(p[1])) for p in self.polygon.exterior.coords]

    def get_centroid(self) -> Tuple[int, int]:
        """
        Get this regions polygon centroid position.
        """
        p: Point = self.polygon.centroid
        return int(p.x), int(p.y)

    def can_expand(self) -> bool:
        """
        Return whether or not this region can continue to expand.
        """
        return self._can_expand and self._expansions > 0

    def expand(self, usable_hexes: List[Hex]) -> None:
        """
        Expand this region's area outward from its exterior hexes.
        """
        newly_expanded: Set[Hex] = set()
        for h in self._expanded_hexes:
            for n in h.direct_neighbors:
                if n in usable_hexes and not n.is_in_region():
                    newly_expanded.add(n)

        if not newly_expanded:
            self._can_expand = False
        else:
            self._expansions -= 1
            self._expanded_hexes.clear()
            for h in newly_expanded:
                self._expanded_hexes.add(h)
                self.add_hex(h)

            self.update_shape(self._expanded_hexes)

    def update_hex_neighbors(self) -> None:
        """
        Update the neighbor states for all hexes in the region.
        """
        [h.set_neighbor_states() for h in self.hexes]

    def set_exterior_details(self) -> None:
        """
        Set hexes forming exterior perimeter as well as coast and neighboring region ids.
        """
        self.exterior_hexes.clear()
        self.neighbor_region_ids.clear()
        self.coast_hexes.clear()

        for h in self.hexes:
            for n in h.direct_neighbors:
                if n.region_id != self.region_id:
                    if n.is_in_region():
                        self.neighbor_region_ids.add(n.region_id)

                    if n.is_ocean():
                        h.set_coast()
                        self.coast_hexes.add(h)

                    self.exterior_hexes.add(h)

    def set_geographic_details(self, elevation_modifier: float, dryness_modifier: float, biome_calculator: IBiomeCalculator) -> None:
        """
        Find this region's exterior hexes and its overall status geographically.
        """
        self.is_coastal: bool = False
        self.is_secluded: bool = False
        self.is_surrounded: bool = False
        self.near_lake: bool = False
        self.near_river: bool = False

        avg_elevation: float = 0.0
        avg_dryness: float = 0.0
        for h in self.hexes:
            avg_elevation += h.elevation
            avg_dryness += h.dryness
            if h.direct[Terraform.Ocean] > 0:
                self.is_coastal = True
            if h.direct[Terraform.Lake] > 0:
                self.near_lake = True
            if h.direct[Terraform.River] > 0:
                self.near_river = True

        self.is_secluded = len(self.neighbor_region_ids) < 1
        self.is_surrounded = not self.is_coastal and not self.is_secluded

        self.avg_elevation = (avg_elevation / len(self.hexes)) + elevation_modifier
        if self.avg_elevation > 1:
            self.avg_elevation = 1
        elif self.avg_elevation < 0:
            self.avg_elevation = 0

        self.avg_dryness = (avg_dryness / len(self.hexes)) + dryness_modifier
        if self.avg_dryness > 1:
            self.avg_dryness = 1
        elif self.avg_dryness < 0:
            self.avg_dryness = 0

        self.biome = biome_calculator.pick_biome(self.avg_elevation, self.avg_dryness)
        self.base_color = biome_calculator.find_biome_color(self.biome)
