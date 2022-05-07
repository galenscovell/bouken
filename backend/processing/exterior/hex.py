from __future__ import annotations

from typing import List, Tuple

from backend.state.terraform import Terraform


class Hex:
    """
    Defines a single hexagon cell.
    """
    def __init__(self, uid: int, x: int, y: int) -> None:
        assert ((x + y) % 2 == 0), f'Hex col and row must sum to an even number (found {x}, {y})'
        self.x: int = x
        self.y: int = y
        self.uid: int = uid

        self.pixel_center_x: int = 0
        self.pixel_center_y: int = 0

        # Define points of hex cell, connected in order
        self.vertices: List[Tuple[int, int]] = []

        self.direct_neighbors: List[Hex] = []
        self.secondary_neighbors: List[Hex] = []
        self.total: List[Terraform] = []
        self.direct: List[Terraform] = []
        self.secondary: List[Terraform] = []

        self._state: Terraform = Terraform.Ocean
        self._on_island: bool = False
        self._in_region: bool = False

        self._state_options: List[Terraform] = [
            Terraform.Land,
            Terraform.Coast,
            Terraform.Ocean,
            Terraform.Lake,
            Terraform.River]

        self.island_id: int = -1
        self.region_id: int = -1
        self.elevation: float = 0
        self.dryness: float = 0
        self.depth: float = 0

    def construct(self, width_diameter: int, height_diameter: int, horizontal_spacing: int, vertical_spacing: int) -> None:
        width_radius: int = int(width_diameter / 2)
        height_radius: int = int(height_diameter / 2)

        self.pixel_center_x = width_radius + self.x * horizontal_spacing
        self.pixel_center_y = height_radius + self.y * vertical_spacing

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self.uid == other.uid
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def serialize(self) -> dict:
        return {
            'type': self._state.name,
            'elevation': self.elevation,
            'dryness': self.dryness,
            'depth': self.depth,
            'vertices': self.vertices
        }

    def get_tuple_coord(self) -> Tuple[int, int]:
        return self.x, self.y

    def set_neighbor_states(self) -> None:
        self.direct = [0 for s in self._state_options]
        for h in self.direct_neighbors:
            self.direct[h._state] += 1

        self.secondary = [0 for s in self._state_options]
        for h in self.secondary_neighbors:
            self.secondary[h._state] += 1

        self.total = [self.direct[n] + self.secondary[n] for n in range(len(self._state_options))]

    def set_land(self) -> None:
        self._state = Terraform.Land

    def set_coast(self) -> None:
        self._state = Terraform.Coast

    def set_ocean(self) -> None:
        self._state = Terraform.Ocean

    def set_lake(self) -> None:
        self._state = Terraform.Lake

    def set_river(self) -> None:
        self._state = Terraform.River

    def is_land(self) -> bool:
        return self._state == Terraform.Land

    def is_coast(self) -> bool:
        return self._state == Terraform.Coast

    def is_ocean(self) -> bool:
        return self._state == Terraform.Ocean

    def is_lake(self) -> bool:
        return self._state == Terraform.Lake

    def is_river(self) -> bool:
        return self._state == Terraform.River

    def set_island(self, island_id: int) -> None:
        self._on_island = True
        self.island_id = island_id

    def set_region(self, region_id: int) -> None:
        self._in_region = True
        self.region_id = region_id

    def unset_island(self) -> None:
        self._on_island = False
        self.island_id = -1

    def unset_region(self) -> None:
        self._in_region = False
        self.region_id = -1

    def is_on_island(self) -> bool:
        return self._on_island is True

    def is_in_region(self) -> bool:
        return self._in_region is True
