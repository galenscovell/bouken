from typing import List

from src.processing.interior.cell import Cell


class Corridor(object):
    def __init__(self, start_cell: Cell, end_cell: Cell, cells: List[Cell], end_room_id: int):
        self.start_cell: Cell = start_cell
        self.end_cell: Cell = end_cell
        self.end_room_id: int = end_room_id

        self.cells: List[Cell] = cells
        for c in self.cells:
            c.set_corridor()
