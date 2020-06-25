from typing import List, Tuple

import math

from src.models.map.point import Point


class Hex(object):
    """
    Defines a single, flat-topped Hex cell.
    """
    def __init__(self, col: int, row: int, size: float, pointy: bool):
        assert ((col + row) % 2 == 0), f'Hex col and row must sum to an even number (found {col}, {row})'
        self.col: int = col
        self.row: int = row
        self.size: float = size
        self.pointy: bool = pointy

        self.width_diameter: float = math.sqrt(3) * self.size if self.pointy else 2 * self.size
        self.width_radius: float = self.width_diameter / 2

        self.height_diameter: float = 2 * self.size if self.pointy else math.sqrt(3) * self.size
        self.height_radius: float = self.height_diameter / 2

        self.vertical_spacing: float = self.height_diameter * (3/4) if self.pointy else self.height_diameter / 2
        self.horizontal_spacing: float = self.width_diameter / 2 if self.pointy else self.width_diameter * (3 / 4)

        self.pixel_center: Point = Point(
            self.width_radius + self.col * self.horizontal_spacing,
            self.height_radius + self.row * self.vertical_spacing
        )

        # Define points of hex cell, connected in order
        self.vertices: List[Tuple[float, float]] = [self._calculate_hex_corner(i) for i in range(6)]

    def __str__(self) -> str:
        return f'[{self.col}, {self.row}]'

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self.col == other.col and self.row == other.row
        return False

    def get_connecting_vertex(self, vertex_index: int) -> Tuple[float, float]:
        if vertex_index == len(self.vertices) - 1:
            return self.vertices[0]
        else:
            return self.vertices[vertex_index + 1]

    def _calculate_hex_corner(self, i) -> Tuple[float, float]:
        angle_deg = 60 * i - 30  # for "pointy top" hexes

        angle_rad = (math.pi / 180) * angle_deg
        vertex_x = self.pixel_center.x + self.size * math.cos(angle_rad)
        vertex_y = self.pixel_center.y + self.size * math.sin(angle_rad)

        return vertex_x, vertex_y
