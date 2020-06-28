from typing import List, Tuple, Set

from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union

from src.models.map.hex import Hex
from src.models.map.region_state import RegionState


class Region(object):
    """
    Defines a political region of a map, composed of multiple base hexes.
    """
    def __init__(self, start_hex: Hex, color: Tuple[int, int, int]):
        self.hexes: Set[Hex] = {start_hex}
        self.color: Tuple[int, int, int] = color

        self.expanded_hexes: Set[Hex] = {start_hex}
        self.polygon: Polygon = Polygon(start_hex.vertices)

        self.state: RegionState = RegionState.Grassland
        self.area: float = self.polygon.area

    def add_hex(self, h: Hex):
        h.set_occupied()
        self.hexes.add(h)
        self.polygon = cascaded_union([self.polygon, Polygon(h.vertices)])
        self.area: float = self.polygon.area

    def get_vertices(self) -> List[Tuple[int, int]]:
        return [(p[0], p[1]) for p in self.polygon.exterior.coords]

    def get_centroid(self) -> Tuple[int, int]:
        p: Point = self.polygon.centroid
        return int(p.x), int(p.y)

    def expand(self, usable_hexes: Set[Hex]):
        newly_expanded: Set[Hex] = set()
        for h in self.expanded_hexes:
            for n in h.direct_neighbors:
                if n and n in usable_hexes and not n.is_occupied():
                    newly_expanded.add(n)

        self.expanded_hexes.clear()
        for h in newly_expanded:
            self.expanded_hexes.add(h)
            self.add_hex(h)
