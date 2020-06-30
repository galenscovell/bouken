from typing import List, Tuple, Set

from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from src.processing.map.hex import Hex


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

        self.neighbor_region_ids: Set[int] = set()
        self.is_coastal: bool = False
        self.is_bordering_lake: bool = False
        self.is_secluded: bool = False
        self.is_surrounded: bool = False

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

    def find_neighbors(self):
        """
        Find all regions connected to this region.
        """
        self.neighbor_region_ids.clear()
        self.is_coastal: bool = False
        self.is_bordering_lake: bool = False
        self.is_secluded: bool = False
        self.is_surrounded: bool = False

        for h in self.hexes:
            for n in h.direct_neighbors:
                if n:
                    if n.is_in_region() and n.region_id != self.region_id:
                        self.neighbor_region_ids.add(n.region_id)
                    elif n.is_ocean():
                        self.is_coastal = True
                    elif n.is_lake():
                        self.is_bordering_lake = True

        self.is_secluded = len(self.neighbor_region_ids) < 1
        self.is_surrounded = not self.is_coastal and not self.is_secluded



