from typing import List, Tuple

import math

from src.models.map.point import Point


class Hex(object):
    """
    Defines a single, flat-topped Hex cell.
    """
    def __init__(self, col: int, row: int, radius: float):
        assert ((col + row) % 2 == 0), f'Hex col and row must sum to an even number (found {col}, {row})'
        self.col: int = col
        self.row: int = row
        self.radius: float = radius

        self.width: float = 2 * self.radius * 2
        self.height: float = math.sqrt(3) * self.radius
        self.horizontal_spacing: float = 0.75 * self.width
        self.vertical_spacing: float = self.height

        self.pixel_center: Point = Point(self.col * self.horizontal_spacing, self.row * self.vertical_spacing)

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
        angle_deg = 60 * i  # - 30 for "pointy top" hexes

        angle_rad = (math.pi / 180) * angle_deg
        vertex_x = self.pixel_center.x + self.radius * math.cos(angle_rad)
        vertex_y = self.pixel_center.y + self.radius * math.sin(angle_rad)

        return vertex_x, vertex_y
