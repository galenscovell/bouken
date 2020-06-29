from random import Random
from typing import List, Tuple, Set

from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from src.processing.map.hex import Hex
from src.processing.map.terraform_state import TerraformState


class Region(object):
    """
    Defines a political region of a map, composed of multiple hexes.
    """
    def __init__(self, region_id: int, island_id: int, start_hex: Hex, color: Tuple[int, int, int], expansions: int):
        self.region_id: int = region_id
        self.island_id: int = island_id
        self.start_hex: Hex = start_hex
        self.hexes: Set[Hex] = {start_hex}
        self.color: Tuple[int, int, int] = color

        self._expanded_hexes: Set[Hex] = {start_hex}
        self._expansions: int = expansions
        self._can_expand: bool = True

        self.polygon: Polygon = Polygon(start_hex.vertices)
        self.area: float = self.polygon.area

        start_hex.set_region(self.region_id)

    def add_hex(self, h: Hex):
        """
        Add a hex to this region.
        """
        h.set_region(self.region_id)
        self.hexes.add(h)

    def refresh(self, to_join_hexes):
        """
        Refresh this region's polygon shape and area.
        """
        to_join = [self.polygon]
        for h in to_join_hexes:
            to_join.append(Polygon(h.vertices))

        self.polygon = unary_union(to_join)
        self.area: float = self.polygon.area

    def get_vertices(self) -> List[Tuple[int, int]]:
        """
        Get this region's exterior vertices defining its shape.
        """
        return [(p[0], p[1]) for p in self.polygon.exterior.coords]

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

    def create_lake(self, random: Random) -> List[Hex]:
        """
        Create a lake at a random location with a random number of expansions.
        """
        lake_hex: Set[Hex] = set()

        self.start_hex.set_lake()
        self.hexes.remove(self.start_hex)
        newly_expanded: Set[Hex] = {self.start_hex}
        next_to_expand: Set[Hex] = set()
        for x in range(random.randint(1, 3)):
            for h in newly_expanded:
                for n in h.direct_neighbors:
                    if n in self.hexes and n.direct[TerraformState.Ocean] == 0:
                        self.hexes.remove(n)
                        lake_hex.add(n)
                        next_to_expand.add(n)

            newly_expanded = next_to_expand.copy()
            next_to_expand.clear()

            self.refresh(newly_expanded)

        return list(lake_hex)

    def expand(self, usable_hexes: List[Hex]):
        """
        Expand this region's area outward from its exterior hexes.
        """
        newly_expanded: Set[Hex] = set()
        for h in self._expanded_hexes:
            for n in h.direct_neighbors:
                if n and n in usable_hexes and not n.is_in_region():
                    newly_expanded.add(n)

        if not newly_expanded:
            self._can_expand = False
        else:
            self._expansions -= 1
            self._expanded_hexes.clear()
            for h in newly_expanded:
                self._expanded_hexes.add(h)
                self.add_hex(h)

            self.refresh(self._expanded_hexes)
