import math
import random
from typing import List, Optional, Tuple, Set

import pygame

from backend.processing.exterior.hex import Hex
from backend.state.terraform import Terraform
from backend.util.constants import dryness_color, freshwater_color
from backend.util.hex_utils import HexUtils


class BaseLayer(object):
    """
    The base layer of the map, describing its basic land features.

    Defines a 2D grid of hexes, using Doubled Coordinates as offset.
    Hexes can be either pointy or flat topped - calculations will shift accordingly.
    Allows for both indexed set/get and generator looping of all hexes.
    """
    def __init__(self, pixel_width: int, hex_size: int, initial_land_pct: float, required_land_pct: float,
                 pointy: bool = True):
        self._pixel_width: int = pixel_width
        self._pixel_height: int = round(math.sqrt(1 / 3) * self._pixel_width)
        self.initial_land_pct: float = initial_land_pct
        self.required_land_pct: float = required_land_pct

        width_diameter, height_diameter, horizontal_spacing, vertical_spacing = \
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

        # Init grid as 2D array of None
        self.grid: List[List[Optional[Hex]]] = []
        for x in range(self._columns):
            self.grid.append([])
            for y in range(self._rows):
                self.grid[x].append(None)

        hex_id: int = 0
        # Create even hexagons
        for x in range(0, self._columns, 2):
            for y in range(0, self._rows, 2):
                self[x, y] = Hex(hex_id, x, y)
                hex_id += 1

        # Create odd hexagons
        for x in range(1, self._columns, 2):
            for y in range(1, self._rows, 2):
                self[x, y] = Hex(hex_id, x, y)
                hex_id += 1

        # Set all neighbors
        for x in range(self._columns):
            for y in range(self._rows):
                h: Hex = self[x, y]
                if h:
                    h.direct_neighbors = self._set_direct_neighbors(h)
                    h.secondary_neighbors = self._set_secondary_neighbors(h)

        # Set hex properties
        for h in self.generator():
            h.construct(width_diameter, height_diameter, horizontal_spacing, vertical_spacing)
            h.vertices = HexUtils.calculate_hex_corners(h.pixel_center_x, h.pixel_center_y, hex_size, pointy)

        self._random: random.Random = random.Random()

        self.actual_width: int = round(horizontal_spacing / 2 + horizontal_spacing * self._columns)
        self.actual_height: int = round(vertical_spacing + vertical_spacing * self._rows)

        # Set max possible distance cap. Smaller divisor (larger value) = finer gradient and lower extremes.
        HexUtils.MAX_DISTANCE = (self._columns * self._rows) / 200

        self.randomize()

    def __len__(self) -> int:
        return self._columns * self._rows

    def __setitem__(self, xy: Tuple[int, int], value):
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            self.grid[xy[0]][xy[1]] = value

    def __getitem__(self, xy: Tuple[int, int]) -> Optional[Hex]:
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            return self.grid[xy[0]][xy[1]]
        return None

    def serialize(self) -> dict:
        hexes: dict = {}
        for h in self.generator():
            hexes[str(h.uid)] = h.serialize()

        return hexes

    def debug_render(self, surface: pygame.Surface):
        for h in self.generator():
            if h.is_land() or h.is_coast():
                pygame.draw.polygon(surface, dryness_color, h.vertices)
                # elevation_color = (85 * h.elevation, 139 * h.elevation, 112 * h.elevation)
                # pygame.draw.polygon(surface, elevation_color, h.vertices)
                # dryness_color = (172 * h.dryness, 159 * h.dryness, 112 * h.dryness)
                # pygame.draw.polygon(surface, dryness_color, h.vertices)
            # elif h.is_ocean():
            #     h_color = [(c - (h.depth * c)) for c in ocean_color]
            #     for i in range(len(h_color)):
            #         if h_color[i] > 255:
            #             h_color[i] = 255
            #     pygame.draw.polygon(surface, h_color, h.vertices)
            else:
                h_color = [(c - (h.depth * c)) for c in freshwater_color]
                for i in range(len(h_color)):
                    if h_color[i] > 255:
                        h_color[i] = 255
                pygame.draw.polygon(surface, h_color, h.vertices)

    def total_usable_hexes(self) -> int:
        total: int = 0
        for h in self.generator():
            total += 1

        return total

    def _total_land_hexes(self) -> int:
        total: int = 0
        for h in self.generator():
            if h.is_land():
                total += 1

        return total

    def has_enough_land(self) -> bool:
        """
        Return whether or not the generated map has a reasonable amount of land.
        """
        return self._total_land_hexes() >= (self.total_usable_hexes() * self.required_land_pct)

    def _set_direct_neighbors(self, h: Hex) -> List[Optional[Hex]]:
        """
        Return the 6 direct neighbours of a hex.
        """
        delta: List[Tuple[int, int]] = [(h.x + dx, h.y + dy) for dx, dy in self._direct_neighbors]
        return [self[x, y] for x, y in delta if x > -1 and y > -1 and self[x, y]]

    def _set_secondary_neighbors(self, h: Hex) -> List[Optional[Hex]]:
        """
        Return the 6 secondary neighbours of a hex.
        """
        delta: List[Tuple[int, int]] = [(h.x + dx, h.y + dy) for dx, dy in self._secondary_neighbors]
        return [self[x, y] for x, y in delta if x > -1 and y > -1 and self[x, y]]

    def update_hex_neighbors(self):
        """
        Update the neighbor states for all hexes in the grid.
        """
        [h.set_neighbor_states() for h in self.generator()]

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

    def randomize(self):
        """
        Randomly distribute land hexes across grid.
        """
        for h in self.generator():
            r: float = self._random.uniform(0, 1)
            if r <= self.initial_land_pct:
                h.set_land()
            else:
                h.set_ocean()

    def terraform(self):
        """
        Grow land hexes across grid.
        """
        self.update_hex_neighbors()
        for h in self.generator():
            if not h.is_land() and h.total[Terraform.Land] > 6:
                h.set_land()

    def finalize(self):
        self._remove_stray_land()
        self._enforce_ocean_border()
        self._remove_interior_oceans()

    def _remove_stray_land(self):
        """
        Remove stray patches of land across grid.
        """
        self.update_hex_neighbors()
        for h in self.generator():
            if h.is_land() and h.direct[Terraform.Land] < 4:
                h.set_ocean()

    def _enforce_ocean_border(self):
        """
        Ensure a border of ocean hexes on map.
        """
        xs: List[int] = [0, 1, self._columns, self._columns - 1]
        ys: List[int] = [0, 1, self._rows - 2, self._rows - 3]

        corners: List[Tuple[int, int]] = [
            (2, 2), (2, 4), (3, 3), (4, 2),
            (self._columns - 2, 2), (self._columns - 2, 4), (self._columns - 3, 3), (self._columns - 4, 2),
            (2, self._rows - 5), (3, self._rows - 4),
            (self._columns - 2, self._rows - 5), (self._columns - 3, self._rows - 4)
        ]
        for h in self.generator():
            if h.x in xs or h.y in ys or h.get_tuple_coord() in corners:
                h.set_ocean()

    def _remove_interior_oceans(self):
        """
        Locate any 'interior' oceans, and if present replace them with land.
        """
        usable_hexes: List[Hex] = [h for h in self.generator() if h.is_ocean()]
        found_oceans: List[List[Hex]] = []

        # Pick random ocean hex to start, then expand out until no more ocean to expand to
        start: Hex = self._random.choice(usable_hexes)
        usable_hexes.remove(start)
        ocean_hexes: Set[Hex] = {start}
        expanded: Set[Hex] = {start}
        to_expand: Set[Hex] = set()
        while usable_hexes:
            for h in expanded:
                for n in h.direct_neighbors:
                    if n and n in usable_hexes:
                        to_expand.add(n)
                        ocean_hexes.add(n)
                        usable_hexes.remove(n)

            if not to_expand:
                found_oceans.append(list(ocean_hexes))
                ocean_hexes.clear()
                next_start_hex: Hex = self._random.choice(usable_hexes)
                expanded = {next_start_hex}
                ocean_hexes = {next_start_hex}
                usable_hexes.remove(next_start_hex)
            else:
                expanded = to_expand.copy()
                to_expand.clear()

        if ocean_hexes:
            found_oceans.append(list(ocean_hexes))

        # Turn all 'oceans" smaller than the largest one into land
        if len(found_oceans) > 1:
            found_oceans.sort(key=len, reverse=True)
            for ocean in found_oceans[1:]:
                for h in ocean:
                    h.set_land()
