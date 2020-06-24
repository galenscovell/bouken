import math
import random
from typing import List, Tuple

import matplotlib.pyplot as plt

from src.models.map.hex import Hex


class Grid(object):
    """
    Defines a grid of flat-topped Hex cells, using Doubled Coordinates as offset.

    Example:
    [0, 4]	[2, 4]	[4, 4]
        [1, 3]	[3, 3]
    [0, 2]	[2, 2]	[4, 2]
        [1, 1]	[3, 1]
    [0, 0]	[2, 0]	[4, 0]
    """
    _corners = ((1, 1), (0, 2), (-1, 1), (-1, -1), (0, -2), (1, -1))
    _neighbours = ((2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1))

    def __init__(self, pixel_width: int, pixel_height: int, hex_diameter: int):
        self.pixel_width: int = pixel_width
        self.pixel_height: int = pixel_height
        self.rows: int = self.pixel_width // hex_diameter
        self.columns: int = self.pixel_height // hex_diameter
        self.hex_radius: float = hex_diameter / 2

        self.rdm: random.Random = random.Random()

        # Init grid as 2D array of None
        self.grid: List[List[Hex]] = []
        for col in range(self.columns):
            self.grid.append([])
            for row in range(self.rows):
                self.grid[col].append(None)

        # Create even column Hexagons
        for col in range(0, self.columns, 2):
            for row in range(0, self.rows, 2):
                self.grid[col][row] = Hex(row, col, self.hex_radius)

        # Create odd column Hexagons
        for col in range(1, self.columns, 2):
            for row in range(1, self.rows, 2):
                self.grid[col][row] = Hex(row, col, self.hex_radius)

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
        for col in range(self.columns - 1, -1, -1):
            print()
            for row in range(self.rows):
                cell: Hex = self.grid[col][row]
                if cell:
                    print(self.grid[col][row], end='')
                    plt.plot(cell.pixel_center.x, cell.pixel_center.y, 'ko', ms=1, color='teal', alpha=0.8)
                    plt.annotate(xy=[cell.pixel_center.x, cell.pixel_center.y], s=str(cell))

                    for n in range(len(cell.vertices)):
                        v1: Tuple[float, float] = cell.vertices[n]
                        v2: Tuple[float, float] = cell.get_connecting_vertex(n)
                        plt.plot([v1[0], v2[0]], [v1[1], v2[1]], 'k', linewidth=1, alpha=0.6)
                else:
                    print('\t', end='')

        # plt.xlim([-self.hex_radius * 2, self.pixel_width - self.hex_radius * 4])
        # plt.ylim([-self.hex_radius * 2, self.pixel_height - self.hex_radius * 2])
        plt.show()
        print('debug')
