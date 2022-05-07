from typing import List

from backend.processing.interior.cell import Cell
from backend.processing.interior.corridor import Corridor


class Room:
    def __init__(self, room_id: int, center_cell: Cell, width: int, height: int, room_cells: List[Cell], perimeter: List[Cell], corners: List[Cell]) -> None:
        self.room_id: int = room_id
        self.center_cell: Cell = center_cell
        self.width: int = width
        self.height: int = height

        self.room_cells: List[Cell] = room_cells
        self.corridors: List[Corridor] = []

        self._full_perimeter: List[Cell] = perimeter
        self.perimeter: List[Cell] = perimeter.copy()
        self.corner_cells: List[Cell] = corners
        self.perimeter_and_corners: List[Cell] = self.perimeter + self.corner_cells

        for c in self.room_cells:
            c.set_room(self.room_id)
            c.set_floor()

        for c in self.perimeter:
            c.set_room(self.room_id)
            c.set_wall()

        for c in self.corner_cells:
            c.set_room(self.room_id)
            c.set_corner()

    def reset_perimeter(self) -> None:
        corridor_cells: List[Cell] = [c.start_cell for c in self.corridors]
        for c in self._full_perimeter:
            if c in corridor_cells and c in self._full_perimeter:
                self._full_perimeter.remove(c)

        self.perimeter = self._full_perimeter.copy()
