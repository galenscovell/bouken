from typing import List, Tuple, Set

from shapely.geometry import Polygon
from shapely.ops import cascaded_union

from src.processing.map.hex import Hex
from src.processing.map.island_type import IslandType


class Island(object):
    """
    Defines an island of a map, composed of multiple hexes.
    """
    def __init__(self, start_hex: Hex):
        self.hexes: Set[Hex] = {start_hex}

        self.expanded_hexes: Set[Hex] = {start_hex}
        self.can_expand: bool = True
        self.polygon: Polygon = Polygon(start_hex.vertices)

        self.type: IslandType = IslandType.Grassland
        self.area: float = self.polygon.area

        start_hex.set_occupied()

    def add_hex(self, h: Hex):
        """
        Add a hex to this island, refreshing its polygon shape and area.
        """
        h.set_occupied()
        self.hexes.add(h)
        self.polygon = cascaded_union([self.polygon, Polygon(h.vertices)])
        self.area: float = self.polygon.area

    def get_vertices(self) -> List[Tuple[int, int]]:
        """
        Get this island's exterior vertices defining its shape.
        """
        return [(p[0], p[1]) for p in self.polygon.exterior.coords]

    def expand(self, usable_hexes: List[Hex]):
        """
        Expand this island's area outward from its exterior hexes.
        """
        newly_expanded: Set[Hex] = set()
        for h in self.expanded_hexes:
            for n in h.direct_neighbors:
                if n and n in usable_hexes and not n.is_occupied():
                    newly_expanded.add(n)

        if not newly_expanded:
            self.can_expand = False
        else:
            self.expanded_hexes.clear()
            for h in newly_expanded:
                self.expanded_hexes.add(h)
                self.add_hex(h)
