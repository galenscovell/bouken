import math
from typing import List, Tuple

from src.models.map.grid import Grid


class MapGenerator:
    def __init__(self, pixel_width: int, cell_size: int, iterations: int):
        self.pixel_width: int = pixel_width
        self.hex_diameter: int = cell_size
        self.iterations: int = iterations

        self.grid: Grid = Grid(self.pixel_width, self.hex_diameter, True)

        self.grid.test_display()
