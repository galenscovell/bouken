import math
from typing import List, Tuple, Optional, Set

from processing.exterior.hex import Hex
from util.i_hex_utility import IHexUtility

from state.pathfinding import Pathfinding
from state.terraform import Terraform

from util.constants import path_find_mode


class HexUtils(IHexUtility):
    def __init__(self) -> None:
        self.max_distance: float = 0
        
    def set_max_distance(self, new_value: float) -> None:
        self.max_distance = new_value

    def get_max_distance(self) -> float:
        return self.max_distance

    def distance(self, h: Hex, hex_types: List[Terraform]) -> float:
        shortest_distance: float = float('inf')
        end: Hex = self.expand_until_hit(h, hex_types)
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

        return self.normalize(shortest_distance)

    def normalize(self, value: float) -> float:
        normalized: float = value / self.max_distance
        if normalized > 1:
            normalized = 1
        elif normalized < -1:
            normalized = -1

        return normalized

    def calculate_layout(self, hex_size: int, pointy: bool) -> Tuple[int, int, int, int]:
        width_diameter: float = (math.sqrt(3) * hex_size if pointy else 2 * hex_size)
        height_diameter: float = (2 * hex_size if pointy else math.sqrt(3) * hex_size)
        vertical_spacing: float = (height_diameter * (3 / 4) if pointy else height_diameter / 2)
        horizontal_spacing: float = (width_diameter / 2 if pointy else width_diameter * (3 / 4))

        return int(width_diameter), int(height_diameter), int(horizontal_spacing), int(vertical_spacing)

    def calculate_hex_corners(self, center_x: int, center_y: int, size: int, pointy: bool) -> List[Tuple[int, int]]:
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

    def expand_until_hit(self, h: Hex, hex_types: List[Terraform]) -> Optional[Hex]:
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
