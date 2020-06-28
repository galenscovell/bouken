from __future__ import annotations

from typing import List, Tuple

from src.processing.map.hex_state import HexState
from src.util.hex_utils import HexUtils


class Hex(object):
    """
    Defines a single hexagon cell.
    """

    def __init__(self, x: int, y: int, size: int, pointy: bool):
        assert ((x + y) % 2 == 0), f'Hex col and row must sum to an even number (found {x}, {y})'
        self.x: int = x
        self.y: int = y
        self._size: int = size
        self._pointy: bool = pointy

        self._width_diameter, self._height_diameter, self._vertical_spacing, self._horizontal_spacing = \
            HexUtils.calculate_layout(size, pointy)

        self._width_radius: int = int(self._width_diameter / 2)
        self._height_radius: int = int(self._height_diameter / 2)

        self.pixel_center_x: int = self._width_radius + self.x * self._horizontal_spacing
        self.pixel_center_y: int = self._height_radius + self.y * self._vertical_spacing

        # Define points of hex cell, connected in order
        self.vertices: List[Tuple[int, int]] = HexUtils.calculate_hex_corners(
            self.pixel_center_x, self.pixel_center_y, size, pointy)

        self.direct_neighbors: List[Hex] = []
        self.secondary_neighbors: List[Hex] = []
        self.total: List[HexState] = []
        self.direct: List[HexState] = []
        self.secondary: List[HexState] = []

        self._state: HexState = HexState.Water
        self._on_island: bool = False
        self._in_region: bool = False

        self._state_options: List[HexState] = [
            HexState.Land, HexState.Water, HexState.Forest, HexState.Desert, HexState.Coast, HexState.Shallows]

    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __copy__(self) -> Hex:
        cpy: Hex = Hex(self.x, self.y, self._size, self._pointy)
        cpy._state = self._state
        cpy.direct_neighbors = self.direct_neighbors
        cpy.secondary_neighbors = self.secondary_neighbors
        return cpy

    def set_neighbor_states(self):
        self.direct = [0 for s in self._state_options]
        for h in self.direct_neighbors:
            if h:
                self.direct[h._state] += 1

        self.secondary = [0 for s in self._state_options]
        for h in self.secondary_neighbors:
            if h:
                self.secondary[h._state] += 1

        self.total = [self.direct[n] + self.secondary[n] for n in range(len(self._state_options))]

    def set_land(self):
        self._state = HexState.Land

    def set_water(self):
        self._state = HexState.Water

    def set_island(self):
        self._on_island = True

    def unset_island(self):
        self._on_island = False

    def set_region(self):
        self._in_region = True

    def unset_region(self):
        self._in_region = False

    def set_forest(self):
        self._state = HexState.Forest

    def set_desert(self):
        self._state = HexState.Desert

    def set_coast(self):
        self._state = HexState.Coast

    def set_shallows(self):
        self._state = HexState.Shallows

    def is_land(self) -> bool:
        return self._state == HexState.Land

    def is_water(self) -> bool:
        return self._state == HexState.Water

    def is_on_island(self) -> bool:
        return self._on_island is True

    def is_in_region(self) -> bool:
        return self._in_region is True

    def is_forest(self) -> bool:
        return self._state == HexState.Forest

    def is_desert(self) -> bool:
        return self._state == HexState.Desert

    def is_coast(self) -> bool:
        return self._state == HexState.Coast

    def is_shallows(self) -> bool:
        return self._state == HexState.Shallows
