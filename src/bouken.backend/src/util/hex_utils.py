import math
from typing import List, Tuple, Optional, Set

from src.processing.map.hex import Hex
from src.processing.map.path_find_mode import PathfindMode
from src.processing.map.terraform_state import TerraformState


class HexUtils(object):
    @staticmethod
    def calculate_layout(hex_size: int, pointy: bool):
        """
        Calculate grid layout values.
        """
        width_diameter: float = math.sqrt(3) * hex_size if pointy else 2 * hex_size
        height_diameter: float = 2 * hex_size if pointy else math.sqrt(3) * hex_size
        vertical_spacing: float = height_diameter * (3 / 4) if pointy else height_diameter / 2
        horizontal_spacing: float = width_diameter / 2 if pointy else width_diameter * (3 / 4)

        return int(width_diameter), int(height_diameter), int(horizontal_spacing), int(vertical_spacing)

    @staticmethod
    def calculate_hex_corners(center_x: int, center_y: int, size: int, pointy: bool) -> List[Tuple[int, int]]:
        """
        Calculate the vertices defining a hexes corners.
        """
        vertices: List[Tuple[int, int]] = []
        for i in range(6):
            angle_deg = 60 * i
            if pointy:
                angle_deg -= 30

            angle_rad = (math.pi / 180) * angle_deg
            vertex: Tuple[int, int] = (
                int(center_x + size * math.cos(angle_rad)),
                int(center_y + size * math.sin(angle_rad))
            )
            vertices.append(vertex)

        return vertices

    @staticmethod
    def expand_until_hit(h: Hex, hex_types: List[TerraformState]) -> Optional[Hex]:
        """
        Expand from hex until a hex type is hit, returning the last hex before hit.
        """
        ocean_hit: bool = False
        expanded: Set[Hex] = {h}
        newly_expanded: Set[Hex] = set()
        while not ocean_hit and expanded:
            for h in expanded:
                for n in h.direct_neighbors:
                    if n:
                        if n._state in hex_types:
                            return n
                        else:
                            newly_expanded.add(n)

            expanded = newly_expanded.copy()
            newly_expanded.clear()

        return None

    @staticmethod
    def distance(h: Hex, hex_types: List[TerraformState], path_find_mode: PathfindMode,
                 max_distance: float) -> float:
        """
        Find the hex distance from start hex to any hex of target types.
        """
        shortest_distance: float = float('inf')
        end: Hex = HexUtils.expand_until_hit(h, hex_types)

        dx: float = h.x - end.x
        dy: float = h.y - end.y
        if path_find_mode == PathfindMode.Manhattan:
            distance = max(math.fabs(dx), math.fabs(dy))
        elif path_find_mode == PathfindMode.Euclidean:
            distance = math.sqrt(dx * dx + dy * dy)
        else:
            distance = max(math.fabs(dx), math.fabs(dy))

        if distance < shortest_distance:
            shortest_distance = distance

        return HexUtils.normalize(shortest_distance, max_distance)

    @staticmethod
    def normalize(value: float, max_distance: float) -> float:
        """
        Normalize a value to between 0 and 1, using the total map size.
        """
        normalized: float = value / max_distance
        if normalized > 1:
            normalized = 1

        return normalized
