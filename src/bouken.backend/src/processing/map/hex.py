from __future__ import annotations

from typing import List, Tuple

from src.processing.map.terraform_state import TerraformState
from src.util.hex_utils import HexUtils


class Hex(object):
    """
    Defines a single hexagon cell.
    """
    def __init__(self, uuid: int, x: int, y: int, size: int, pointy: bool):
        assert ((x + y) % 2 == 0), f'Hex col and row must sum to an even number (found {x}, {y})'
        self.x: int = x
        self.y: int = y
        self.uuid: int = uuid
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

        self._state_options: List[TerraformState] = [
            TerraformState.Land, TerraformState.Coast, TerraformState.Ocean, TerraformState.Lake, TerraformState.River]

        self.island_id: int = -1
        self.region_id: int = -1
        self.elevation: float = 0.0
        self.depth: float = 0.0
        self.dryness: float = 0.0

    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def serialize(self):
        type_str: str = ''
        if self.is_land():
            type_str = 'land'
        elif self.is_ocean():
            type_str = 'ocean'
        elif self.is_lake():
            type_str = 'lake'
        elif self.is_coast():
            type_str = 'coast'
        elif self.is_river():
            type_str = 'river'

        return {
            'type': type_str,
            'elevation': self.elevation,
            'depth': self.depth,
            'dryness': self.dryness,
            'vertices': self.vertices
        }

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

    def set_depth(self, depth: float):
        self.depth = depth

    def set_dryness(self, moisture: float):
        self.dryness = moisture

    def set_land(self):
        self._state = TerraformState.Land

    def set_coast(self):
        self._state = TerraformState.Coast

    def set_ocean(self):
        self._state = TerraformState.Ocean

    def set_lake(self):
        self._state = TerraformState.Lake

    def set_river(self):
        self._state = TerraformState.River

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

    def is_coast(self) -> bool:
        return self._state == TerraformState.Coast

    def is_ocean(self) -> bool:
        return self._state == TerraformState.Ocean

    def is_lake(self) -> bool:
        return self._state == TerraformState.Lake

    def is_river(self) -> bool:
        return self._state == TerraformState.River

    def is_on_island(self) -> bool:
        return self._on_island is True

    def is_in_region(self) -> bool:
        return self._in_region is True
