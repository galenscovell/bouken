import math
import random
from typing import List, Optional, Tuple, Set

import pygame

from src.processing.map.hex import Hex
from src.processing.map.path_find_mode import PathfindMode
from src.processing.map.terraform_state import TerraformState
from src.util.constants import land_color, ocean_color
from src.util.hex_utils import HexUtils


class BaseLayer(object):
    """
    The base layer of the map, describing its basic land features.

    Defines a 2D grid of hexes, using Doubled Coordinates as offset.
    Hexes can be either pointy or flat topped - calculations will shift accordingly.
    Allows for both indexed set/get and generator looping of all hexes.
    """
    def __init__(self, pixel_width: int, hex_size: int, initial_land_pct: float, pointy: bool = True):
        self._pixel_width: int = pixel_width
        self._pixel_height: int = round(math.sqrt(1 / 3) * self._pixel_width)

        self.initial_land_pct: float = initial_land_pct
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

        # Create even hexagons
        for x in range(0, self._columns, 2):
            for y in range(0, self._rows, 2):
                self[x, y] = Hex(x, y, self._hex_size, self._pointy)

        # Create odd hexagons
        for x in range(1, self._columns, 2):
            for y in range(1, self._rows, 2):
                self[x, y] = Hex(x, y, self._hex_size, self._pointy)

        # Set all neighbors
        for x in range(self._columns):
            for y in range(self._rows):
                h: Hex = self[x, y]
                if h:
                    h.direct_neighbors = self._set_direct_neighbors(h)
                    h.secondary_neighbors = self._set_secondary_neighbors(h)

        self.init()

    def __len__(self) -> int:
        return self._columns * self._rows

    def __setitem__(self, xy: Tuple[int, int], value):
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            self.grid[xy[0]][xy[1]] = value

    def __getitem__(self, xy: Tuple[int, int]) -> Optional[Hex]:
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            return self.grid[xy[0]][xy[1]]
        return None

    def test_draw(self, surface: pygame.Surface):
        for h in self.generator():
            if h.is_land():
                color = land_color
            elif h.is_lake():
                color = ocean_color
            else:
                color = ocean_color

            pygame.draw.polygon(surface, color, h.vertices)

            if h.is_land():
                # heat_color: float = h.elevation * 20
                heat_color: float = h.moisture * 5
                if heat_color < 0:
                    heat_color = 0

                # pygame.draw.polygon(surface, (heat_color, 150, 0), h.vertices)
                pygame.draw.polygon(surface, (heat_color, heat_color, 255 - heat_color), h.vertices)

    def total_usable_hexes(self) -> int:
        total: int = 0
        for h in self.generator():
            total += 1

        return total

    def total_land_hexes(self) -> int:
        total: int = 0
        for h in self.generator():
            if h.is_land():
                total += 1

        return total

    def is_acceptable(self) -> bool:
        return self.total_land_hexes() >= (self.total_usable_hexes() * 0.45)

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
        """
        Iterate through non-null hexes in the grid.
        """
        for x in range(self._columns):
            for y in range(self._rows):
                h: Hex = self[x, y]
                if not h:
                    continue

                yield h

    def update_hex_states(self):
        """
        Update the neighbor states for all hexes in the grid.
        """
        [h.set_neighbor_states() for h in self.generator()]

    def init(self):
        """
        Randomly distribute land hexes across grid.
        """
        for h in self.generator():
            r: float = self._random.uniform(0, 1)
            if r <= self.initial_land_pct:
                h.set_land()
            else:
                h.set_ocean()

    def terraform_land(self):
        """
        Grow land hexes across grid.
        """
        self.update_hex_states()
        for h in self.generator():
            if not h.is_land() and h.total[TerraformState.Land] > 6:
                h.set_land()

    @staticmethod
    def _expand_until_hit(h: Hex, hex_type: TerraformState) -> Optional[Hex]:
        """
        Expand from hex until a hex type is hit, returning the last hex before hit.
        """
        ocean_hit: bool = False
        expanded: Set[Hex] = {h}
        newly_expanded: Set[Hex] = set()
        while not ocean_hit:
            for h in expanded:
                for n in h.direct_neighbors:
                    if n:
                        if n._state == hex_type:
                            return n
                        else:
                            newly_expanded.add(n)

            expanded = newly_expanded.copy()
            newly_expanded.clear()

        return None

    def find_distance_to_ocean(self, mode: PathfindMode):
        """
        Expand out from each hex until ocean is hit to determine distance and elevation.
        """
        for h in self.generator():
            shortest_distance: float = float('inf')
            end: Hex = self._expand_until_hit(h, TerraformState.Ocean)

            dx: float = h.x - end.x
            dy: float = h.y - end.y
            if mode == PathfindMode.Manhattan:
                distance = max(math.fabs(dx), math.fabs(dy))
            elif mode == PathfindMode.Euclidean:
                distance = math.sqrt(dx * dx + dy * dy)
            else:
                distance = max(math.fabs(dx), math.fabs(dy))

            if distance < shortest_distance:
                shortest_distance = distance

            h.set_elevation(shortest_distance)

    def find_distance_to_lake(self, mode: PathfindMode):
        """
        Expand out from each hex until lake is hit to determine distance and elevation.
        """
        for h in self.generator():
            shortest_distance: float = float('inf')
            end: Hex = self._expand_until_hit(h, TerraformState.Lake)

            dx: float = h.x - end.x
            dy: float = h.y - end.y
            if mode == PathfindMode.Manhattan:
                distance = max(math.fabs(dx), math.fabs(dy))
            elif mode == PathfindMode.Euclidean:
                distance = math.sqrt(dx * dx + dy * dy)
            else:
                distance = max(math.fabs(dx), math.fabs(dy))

            if distance < shortest_distance:
                shortest_distance = distance

            h.set_moisture(shortest_distance)

    def clean_up(self):
        """
        Remove stray patches of land across grid.
        """
        self.update_hex_states()
        for h in self.generator():
            if h.is_land() and h.direct[TerraformState.Land] < 4:
                h.set_ocean()
