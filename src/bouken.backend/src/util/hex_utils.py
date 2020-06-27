import math
from typing import List, Tuple


class HexUtils(object):
    @staticmethod
    def calculate_layout(hex_size: int, pointy: bool):
        width_diameter: float = math.sqrt(3) * hex_size if pointy else 2 * hex_size
        height_diameter: float = 2 * hex_size if pointy else math.sqrt(3) * hex_size
        vertical_spacing: float = height_diameter * (3 / 4) if pointy else height_diameter / 2
        horizontal_spacing: float = width_diameter / 2 if pointy else width_diameter * (3 / 4)

        return int(width_diameter), int(height_diameter), int(vertical_spacing), int(horizontal_spacing)

    @staticmethod
    def calculate_hex_corners(center_x: int, center_y: int, size: int, pointy: bool) -> List[Tuple[int, int]]:
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
