from typing import List, Tuple

from src.models.map.hex_state import HexState
from src.util.hex_utils import HexUtils


class Hex(object):
    """
    Defines a single, flat-topped Hex cell.
    """
    def __init__(self, x: int, y: int, size: int, pointy: bool):
        assert ((x + y) % 2 == 0), f'Hex col and row must sum to an even number (found {x}, {y})'
        self.x: int = x
        self.y: int = y

        self.width_diameter, self.height_diameter, self.vertical_spacing, self.horizontal_spacing = \
            HexUtils.calculate_layout(size, pointy)

        self.width_radius: int = int(self.width_diameter / 2)
        self.height_radius: int = int(self.height_diameter / 2)

        self.pixel_center_x: int = self.width_radius + self.x * self.horizontal_spacing
        self.pixel_center_y: int = self.height_radius + self.y * self.vertical_spacing

        # Define points of hex cell, connected in order
        self.vertices: List[Tuple[int, int]] = HexUtils.calculate_hex_corners(self.pixel_center_x, self.pixel_center_y, size, pointy)

        self.state: HexState = HexState.Empty

    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self.x == other.x and self.y == other.y
        return False

    def get_connecting_vertex(self, vertex_index: int) -> Tuple[int, int]:
        if vertex_index == len(self.vertices) - 1:
            return self.vertices[0]
        else:
            return self.vertices[vertex_index + 1]

    def set_state(self, state: HexState):
        self.state = state
