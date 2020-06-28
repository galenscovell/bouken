from typing import List, Tuple, Set

from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from src.processing.map.hex import Hex


class Region(object):
    """
    Defines a political region of a map, composed of multiple hexes.
    """
    def __init__(self, start_hex: Hex, color: Tuple[int, int, int], expansions: int):
        self.hexes: Set[Hex] = {start_hex}
        self.color: Tuple[int, int, int] = color

        self.expanded_hexes: Set[Hex] = {start_hex}
        self.polygon: Polygon = Polygon(start_hex.vertices)

        self._expansions: int = expansions
        self._can_expand: bool = True

        self.area: float = self.polygon.area

        start_hex.set_region()

    def add_hex(self, h: Hex):
        """
        Add a hex to this region.
        """
        h.set_region()
        self.hexes.add(h)

    def refresh(self):
        """
        Refresh this region's polygon shape and area.
        """
        to_join = [self.polygon]
        for h in self.hexes:
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
        for h in self.expanded_hexes:
            for n in h.direct_neighbors:
                if n and n in usable_hexes and not n.is_in_region():
                    newly_expanded.add(n)

        if not newly_expanded:
            self._can_expand = False
        else:
            self._expansions -= 1
            self.expanded_hexes.clear()
            for h in newly_expanded:
                self.expanded_hexes.add(h)
                self.add_hex(h)

            self.refresh()