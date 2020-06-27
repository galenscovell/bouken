import math
import random

from typing import List, Optional, Tuple

from src.models.map.hex import Hex
from src.util.hex_utils import HexUtils


class Grid(object):
    """
    Defines a grid of Hex cells, using Doubled Coordinates as offset.
    They can be either pointy or flat topped - calculations will shift accordingly.
    """
    def __init__(self, pixel_width: int, hex_size: int, pointy: bool):
        self.pixel_width: int = pixel_width
        self.pixel_height: int = round(math.sqrt(1 / 3) * self.pixel_width)

        self.pointy: bool = pointy
        self.hex_size: int = hex_size
        width_diameter, height_diameter, vertical_spacing, horizontal_spacing = \
            HexUtils.calculate_layout(hex_size, pointy)

        self.columns: int = int(self.pixel_width // (width_diameter / 2))
        self.rows: int = int(self.pixel_height // (height_diameter / 2))

        self.direct_neighbors = ((1, 1), (-1, -1), (1, -1), (-1, 1), (2, 0), (-2, 0))
        self.secondary_neighbors = ((0, 2), (0, -2), (3, 1), (-3, 1), (-3, -1), (3, -1))

        # Swap grid dimensions if flat-topped hexes
        if not pointy:
            self.rows, self.columns = self.columns, self.rows
            self.direct_neighbors = ((1, 1), (-1, -1), (1, -1), (-1, 1), (0, 2), (0, -2))
            self.secondary_neighbors = ((2, 0), (-2, 0), (1, 3), (-1, 3), (1, -3), (-1, -3))

        self.actual_width: int = round(horizontal_spacing / 2 + horizontal_spacing * self.columns)
        self.actual_height: int = round(vertical_spacing + vertical_spacing * self.rows)

        self.rdm: random.Random = random.Random()

        # Init grid as 2D array of None
        self.grid: List[List[Hex]] = []
        for x in range(self.columns):
            self.grid.append([])
            for y in range(self.rows):
                self.grid[x].append(None)

        # Create even hexagons
        for x in range(0, self.columns, 2):
            for y in range(0, self.rows, 2):
                self[x, y] = Hex(x, y, self.hex_size, self.pointy)

        # Create odd hexagons
        for x in range(1, self.columns, 2):
            for y in range(1, self.rows, 2):
                self[x, y] = Hex(x, y, self.hex_size, self.pointy)

        # Set all neighbors
        for x in range(self.columns):
            for y in range(self.rows):
                h: Hex = self[x, y]
                if h:
                    h.direct_neighbors = self._set_direct_neighbors(h)
                    h.secondary_neighbors = self._set_secondary_neighbors(h)
                    # h.set_water()
                    h.set_random_state(self.rdm)

    def __len__(self) -> int:
        return self.columns * self.rows

    def __setitem__(self, xy: Tuple[int, int], value):
        if 0 <= xy[0] < self.columns and 0 <= xy[1] < self.rows:
            self.grid[xy[0]][xy[1]] = value

    def __getitem__(self, xy: Tuple[int, int]) -> Optional[Hex]:
        if 0 <= xy[0] < self.columns and 0 <= xy[1] < self.rows:
            return self.grid[xy[0]][xy[1]]
        return None

    def _set_direct_neighbors(self, h: Hex) -> List[Hex]:
        """
        Return the 6 direct neighbours of a hex.
        """
        return [self[h.x + dx, h.y + dy] for dx, dy in self.direct_neighbors]

    def _set_secondary_neighbors(self, h: Hex) -> List[Hex]:
        """
        Return the 6 secondary neighbours of a hex.
        """
        return [self[h.x + dx, h.y + dy] for dx, dy in self.secondary_neighbors]

    def generator(self):
        for x in range(self.columns):
            for y in range(self.rows):
                h: Hex = self[x, y]
                if not h:
                    continue

                yield h

    def random_neighbour(self, h: Hex) -> Optional[Hex]:
        """
        Return a random neighbour of a hex.
        """
        return self.rdm.choice(h.direct_neighbors)

    @staticmethod
    def distance(h1: Hex, h2: Hex) -> int:
        """
        Distance in number of hexagon steps between two hexes.
        Direct neighbours of a hex have distance 1.
        """
        dx = abs(h1.x - h2.x)
        dy = abs(h1.y - h2.y)
        return dy + max(0, (dx - dy) // 2)
