import math
import random
from typing import List, Tuple, Optional

from src.models.map.hex import Hex
from src.util.hex_utils import HexUtils


class HexGrid(object):
    """
    Defines a 2D grid of hexes, using Doubled Coordinates as offset.
    Hexes can be either pointy or flat topped - calculations will shift accordingly.
    Allows for both indexed set/get and generator looping of all hexes.
    All map layers inherit from this class.
    """
    def __init__(self, pixel_width: int, hex_size: int, pointy: bool = True):
        self._pixel_width: int = pixel_width
        self._pixel_height: int = round(math.sqrt(1 / 3) * self._pixel_width)

        self._pointy: bool = pointy
        self._hex_size: int = hex_size
        width_diameter, height_diameter, vertical_spacing, horizontal_spacing = \
            HexUtils.calculate_layout(hex_size, pointy)

        self._columns: int = int(self._pixel_width // (width_diameter / 2))
        self._rows: int = int(self._pixel_height // (height_diameter / 2))

        self._direct_neighbors = ((1, 1), (-1, -1), (1, -1), (-1, 1), (2, 0), (-2, 0))
        self._secondary_neighbors = ((0, 2), (0, -2), (3, 1), (-3, 1), (-3, -1), (3, -1))

        # We assume pointy hexes - swap grid dimensions and modify neighbors if flat-topped instead
        if not pointy:
            self._rows, self._columns = self._columns, self._rows
            self._direct_neighbors = ((1, 1), (-1, -1), (1, -1), (-1, 1), (0, 2), (0, -2))
            self._secondary_neighbors = ((2, 0), (-2, 0), (1, 3), (-1, 3), (1, -3), (-1, -3))

        self._random: random.Random = random.Random()

        # Init grid as 2D array of None
        self.grid: List[List[Optional[Hex]]] = []
        for x in range(self._columns):
            self.grid.append([])
            for y in range(self._rows):
                self.grid[x].append(None)

        self.actual_width: int = round(horizontal_spacing / 2 + horizontal_spacing * self._columns)
        self.actual_height: int = round(vertical_spacing + vertical_spacing * self._rows)

    def __len__(self) -> int:
        return self._columns * self._rows

    def __setitem__(self, xy: Tuple[int, int], value):
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            self.grid[xy[0]][xy[1]] = value

    def __getitem__(self, xy: Tuple[int, int]) -> Optional[Hex]:
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            return self.grid[xy[0]][xy[1]]
        return None

    def _set_direct_neighbors(self, h: Hex) -> List[Optional[Hex]]:
        """
        Return the 6 direct neighbours of a hex.
        """
        return [self[h.x + dx, h.y + dy] for dx, dy in self._direct_neighbors]

    def _set_secondary_neighbors(self, h: Hex) -> List[Optional[Hex]]:
        """
        Return the 6 secondary neighbours of a hex.
        """
        return [self[h.x + dx, h.y + dy] for dx, dy in self._secondary_neighbors]

    def generator(self):
        for x in range(self._columns):
            for y in range(self._rows):
                h: Hex = self[x, y]
                if not h:
                    continue

                yield h

    def update_hex_states(self):
        [h.set_neighbor_states() for h in self.generator()]
