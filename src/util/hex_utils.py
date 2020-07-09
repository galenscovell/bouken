import math
from typing import List, Tuple, Optional, Set

from src.processing.exterior.hex import Hex
from src.state.pathfinding import Pathfinding
from src.state.terraform import Terraform
from src.util.constants import path_find_mode


class HexUtils(object):
    # Max possible distance cap. Smaller divisor (larger value) = finer gradient and lower extremes.
    MAX_DISTANCE: float = 0

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
    def expand_until_hit(h: Hex, hex_types: List[Terraform]) -> Optional[Hex]:
        """
        Expand from hex until a hex type is hit, returning the last hex before hit.
        """
        seen: Set[Hex] = set()
        expanded: Set[Hex] = {h}
        newly_expanded: Set[Hex] = set()
        while expanded:
            for h in expanded:
                seen.add(h)
                for n in h.direct_neighbors:
                    if n._state in hex_types:
                        return n
                    else:
                        if n not in seen:
                            newly_expanded.add(n)

            expanded = newly_expanded.copy()
            newly_expanded.clear()

        return None

    @staticmethod
    def distance(h: Hex, hex_types: List[Terraform]) -> float:
        """
        Find the hex distance from start hex to any hex of target state.
        """
        shortest_distance: float = float('inf')
        end: Hex = HexUtils.expand_until_hit(h, hex_types)
        if not end:
            return 1

        dx: float = h.x - end.x
        dy: float = h.y - end.y
        if path_find_mode == Pathfinding.Manhattan:
            distance = max(math.fabs(dx), math.fabs(dy))
        elif path_find_mode == Pathfinding.Euclidean:
            distance = math.sqrt(dx * dx + dy * dy)
        else:
            distance = max(math.fabs(dx), math.fabs(dy))

        if distance < shortest_distance:
            shortest_distance = distance

        return HexUtils.normalize(shortest_distance)

    @staticmethod
    def normalize(value: float) -> float:
        """
        Normalize a value to between -1 and 1.
        """
        normalized: float = value / HexUtils.MAX_DISTANCE
        if normalized > 1:
            normalized = 1
        elif normalized < -1:
            normalized = -1

        return normalized
