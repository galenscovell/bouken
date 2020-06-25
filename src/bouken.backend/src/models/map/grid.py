import math
import random
from typing import List, Tuple

import matplotlib.pyplot as plt

from src.models.map.hex import Hex


class Grid(object):
    """
    Defines a grid of Hex cells, using Doubled Coordinates as offset.
    They can be either pointy or flat topped - calculations will shift accordingly.
    """
    _corners = ((1, 1), (0, 2), (-1, 1), (-1, -1), (0, -2), (1, -1))
    _neighbours = ((2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1))

    def __init__(self, pixel_width: int, pixel_height: int, hex_size: int, pointy: bool):
        self.pixel_width: int = pixel_width
        self.pixel_height: int = round(math.sqrt(1 / 3) * self.pixel_width)
        self.pointy: bool = pointy

        self.hex_size: float = hex_size
        self.width_diameter: float = math.sqrt(3) * self.hex_size if self.pointy else 2 * self.hex_size
        self.height_diameter: float = 2 * self.hex_size if self.pointy else math.sqrt(3) * self.hex_size
        self.vertical_spacing: float = self.height_diameter * (3 / 4) if self.pointy else self.height_diameter / 2
        self.horizontal_spacing: float = self.width_diameter / 2 if self.pointy else self.width_diameter * (3 / 4)

        self.rows: int = int(self.pixel_width // (self.width_diameter / 2))
        self.columns: int = int(self.pixel_height // (self.height_diameter / 2))

        self.rdm: random.Random = random.Random()

        # Init grid as 2D array of None
        self.grid: List[List[Hex]] = []
        for col in range(self.columns):
            self.grid.append([])
            for row in range(self.rows):
                self.grid[col].append(None)

        # Create even Hexagons
        for col in range(0, self.columns, 2):
            for row in range(0, self.rows, 2):
                self.grid[col][row] = Hex(row, col, self.hex_size, self.pointy)

        # Create odd Hexagons
        for col in range(1, self.columns, 2):
            for row in range(1, self.rows, 2):
                self.grid[col][row] = Hex(row, col, self.hex_size, self.pointy)

    def corners(self, h: Hex):
        """
        Get the 6 corners (in pixel coordinates) of the hex.
        """
        x0, y0 = h
        y0 *= 3
        return [(self.rows * (x + x0), self.columns * (y + y0)) for x, y in self._corners]

    def distance(self, h1: Hex, h2: Hex) -> float:
        """
        Distance in number of hexagon steps between two hexes.
        Direct neighbours of a hex have distance 1.
        """
        dx = abs(h1.col - h2.col)
        dy = abs(h1.row - h2.row)
        return dy + max(0, (dx - dy) // 2)

    def neighbours(self, h: Hex) -> List[Hex]:
        """
        Return the 6 direct neighbours of a hex.
        """
        return [self.grid[h.col + dx][h.row + dy] for dx, dy in self._neighbours]

    def random_neighbour(self, h: Hex) -> Hex:
        """
        Return a random neighbour of a hex.
        """
        dx, dy = self.rdm.choice(self._neighbours)
        return self.grid[h.col + dx][h.row + dy]

    def display(self):
        for col in range(self.columns):
            for row in range(self.rows):
                cell: Hex = self.grid[col][row]
                if cell:
                    plt.plot(cell.pixel_center.x, cell.pixel_center.y, 'go', ms=3, alpha=0.6)
                    # plt.annotate(xy=[cell.pixel_center.x, cell.pixel_center.y], s=str(cell))

                    for n in range(len(cell.vertices)):
                        v1: Tuple[float, float] = cell.vertices[n]
                        v2: Tuple[float, float] = cell.get_connecting_vertex(n)
                        plt.plot([v1[0], v2[0]], [v1[1], v2[1]], '--b', linewidth=1, alpha=0.6)

        # plt.xlim([0, self.pixel_width])
        # plt.ylim([0, self.pixel_height])
        plt.show()
        print('debug')
