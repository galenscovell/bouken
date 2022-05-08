from typing import List

from processing.interior.cell import Cell


class Corridor:
    def __init__(self, start_cell: Cell, end_cell: Cell, cells: List[Cell], end_room_id: int) -> None:
        self.start_cell: Cell = start_cell
        self.end_cell: Cell = end_cell
        self.end_room_id: int = end_room_id

        self.cells: List[Cell] = cells
        for c in self.cells:
            c.set_corridor()
