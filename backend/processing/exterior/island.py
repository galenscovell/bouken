from typing import List, Tuple, Set

from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from backend.processing.exterior.hex import Hex


class Island(object):
    """
    Defines an island of a map, composed of multiple hexes.
    """
    def __init__(self, island_id: int, start_hex: Hex):
        self.island_id: int = island_id
        self.hexes: List[Hex] = [start_hex]
        self.region_keys: Set[int] = set()

        self.expanded_hexes: Set[Hex] = {start_hex}
        self.can_expand: bool = True

        self.polygon: Polygon = Polygon(start_hex.vertices)
        self.area: float = self.polygon.area

        start_hex.set_island(self.island_id)

    def add_hex(self, h: Hex):
        """
        Add a hex to this island.
        """
        h.set_island(self.island_id)
        self.hexes.append(h)

    def refresh(self):
        """
        Refresh this island's polygon shape and area.
        """
        to_join = [self.polygon]
        for h in self.expanded_hexes:
            to_join.append(Polygon(h.vertices))

        self.polygon = unary_union(to_join)
        self.area: float = self.polygon.area

    def get_vertices(self) -> List[Tuple[int, int]]:
        """
        Get this island's exterior vertices defining its shape.
        """
        return [(int(p[0]), int(p[1])) for p in self.polygon.exterior.coords]

    def get_centroid(self) -> Tuple[int, int]:
        """
        Get this island's polygon centroid position.
        """
        p: Point = self.polygon.centroid
        return int(p.x), int(p.y)

    def expand(self, usable_hexes: Set[Hex]):
        """
        Expand this island's area outward from its exterior hexes.
        """
        newly_expanded: Set[Hex] = set()
        for h in self.expanded_hexes:
            for n in h.direct_neighbors:
                if n in usable_hexes and not n.is_on_island():
                    newly_expanded.add(n)

        if not newly_expanded:
            self.can_expand = False
        else:
            self.expanded_hexes.clear()
            for h in newly_expanded:
                self.expanded_hexes.add(h)
                self.add_hex(h)

            self.refresh()
