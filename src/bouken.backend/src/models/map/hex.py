from __future__ import annotations

from random import Random
from typing import List, Tuple

from src.models.map.hex_state import HexState
from src.util.hex_utils import HexUtils


class Hex(object):
    """
    Defines a single hexagon cell.
    """
    def __init__(self, x: int, y: int, size: int, pointy: bool):
        assert ((x + y) % 2 == 0), f'Hex col and row must sum to an even number (found {x}, {y})'
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.pointy: bool = pointy

        self.width_diameter, self.height_diameter, self.vertical_spacing, self.horizontal_spacing = \
            HexUtils.calculate_layout(size, pointy)

        self.width_radius: int = int(self.width_diameter / 2)
        self.height_radius: int = int(self.height_diameter / 2)

        self.pixel_center_x: int = self.width_radius + self.x * self.horizontal_spacing
        self.pixel_center_y: int = self.height_radius + self.y * self.vertical_spacing

        # Define points of hex cell, connected in order
        self.vertices: List[Tuple[int, int]] = HexUtils.calculate_hex_corners(
            self.pixel_center_x, self.pixel_center_y, size, pointy)

        self.direct_neighbors: List[Hex] = []
        self.secondary_neighbors: List[Hex] = []
        self.total: List[HexState] = []
        self.direct: List[HexState] = []
        self.secondary: List[HexState] = []

        self.state: HexState = HexState.Land

        self.state_options: List[HexState] = [
            HexState.Land, HexState.Forest, HexState.Desert,
            HexState.Coast, HexState.Shallows, HexState.Depths,
            HexState.Unoccupied, HexState.Occupied]

    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __copy__(self) -> Hex:
        cpy: Hex = Hex(self.x, self.y, self.size, self.pointy)
        return cpy

    def get_connecting_vertex(self, vertex_index: int) -> Tuple[int, int]:
        if vertex_index == len(self.vertices) - 1:
            return self.vertices[0]
        else:
            return self.vertices[vertex_index + 1]

    def set_random_land(self, rdm: Random):
        self.set_shallows()
        r: float = rdm.uniform(0, 100)
        if r >= 71.5:
            self.set_land()

    def set_neighbor_states(self):
        self.direct = [0 for s in self.state_options]
        for h in self.direct_neighbors:
            if h:
                self.direct[h.state] += 1

        self.secondary = [0 for s in self.state_options]
        for h in self.secondary_neighbors:
            if h:
                self.secondary[h.state] += 1

        self.total = [self.direct[n] + self.secondary[n] for n in range(len(self.state_options))]

    def set_land(self):
        self.state = HexState.Land

    def set_forest(self):
        self.state = HexState.Forest

    def set_desert(self):
        self.state = HexState.Desert

    def set_coast(self):
        self.state = HexState.Coast

    def set_shallows(self):
        self.state = HexState.Shallows

    def set_depths(self):
        self.state = HexState.Depths

    def set_unoccupied(self):
        self.state = HexState.Unoccupied

    def set_occupied(self):
        self.state = HexState.Occupied

    def is_land(self) -> bool:
        return self.state == HexState.Land

    def is_forest(self) -> bool:
        return self.state == HexState.Forest

    def is_desert(self) -> bool:
        return self.state == HexState.Desert

    def is_coast(self) -> bool:
        return self.state == HexState.Coast

    def is_shallows(self) -> bool:
        return self.state == HexState.Shallows

    def is_depths(self) -> bool:
        return self.state == HexState.Depths

    def is_occupied(self):
        return self.state == HexState.Occupied
