from __future__ import annotations

from typing import List, Tuple

from src.processing.map.terraform_state import TerraformState
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
        self.total: List[TerraformState] = []
        self.direct: List[TerraformState] = []
        self.secondary: List[TerraformState] = []

        self._state: TerraformState = TerraformState.Ocean
        self._on_island: bool = False
        self._in_region: bool = False

        self._state_options: List[TerraformState] = [TerraformState.Land, TerraformState.Ocean, TerraformState.Lake]

        self.island_id: int = -1
        self.region_id: int = -1
        self.elevation: float = 0
        self.moisture: float = 0

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

    def set_elevation(self, elevation: float):
        self.elevation = elevation

    def set_moisture(self, moisture: float):
        self.moisture = moisture

    def set_land(self):
        self._state = TerraformState.Land

    def set_ocean(self):
        self._state = TerraformState.Ocean

    def set_lake(self):
        self._state = TerraformState.Lake

    def set_island(self, island_id: int):
        self._on_island = True
        self.island_id = island_id

    def set_region(self, region_id: int):
        self._in_region = True
        self.region_id = region_id

    def unset_island(self):
        self._on_island = False
        self.island_id = -1

    def unset_region(self):
        self._in_region = False
        self.region_id = -1

    def is_land(self) -> bool:
        return self._state == TerraformState.Land

    def is_ocean(self) -> bool:
        return self._state == TerraformState.Ocean

    def is_lake(self) -> bool:
        return self._state == TerraformState.Lake

    def is_on_island(self) -> bool:
        return self._on_island is True

    def is_in_region(self) -> bool:
        return self._in_region is True
