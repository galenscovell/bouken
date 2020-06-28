import pygame

from src.processing.map.hex import Hex
from src.processing.map.hex_grid import HexGrid
from src.processing.map.hex_state import HexState
from src.util.constants import land_color, forest_color, coast_color, shallows_color, depths_color


class BaseLayer(HexGrid):
    """
    Defines the base layer of a map, describing its basic land features.
    """
    def __init__(self, pixel_width: int, hex_size: int, pointy: bool = True):
        super().__init__(pixel_width, hex_size, pointy)

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

    def test_draw(self, surface: pygame.Surface):
        for h in self.generator():
            if h.is_land():
                color = land_color
            elif h.is_forest():
                color = forest_color
            elif h.is_desert():
                color = coast_color
            elif h.is_coast():
                color = coast_color
            elif h.is_shallows():
                color = shallows_color
            else:
                color = depths_color

            pygame.draw.polygon(surface, color, h.vertices)

    def init(self):
        """
        Randomly distribute shallow water and land hexes across grid.
        """
        for h in self.generator():
            h.set_shallows()
            r: float = self._random.uniform(0, 100)
            if r >= 71.5:
                h.set_land()

    def terraform_land(self):
        """
        Grow land hexes across grid.
        """
        self.update_hex_states()
        for h in self.generator():
            if not h.is_land() and h.total[HexState.Land] > 6:
                h.set_land()

    def terraform_water(self):
        """
        Grow water hexes across grid.
        """
        self.update_hex_states()
        for h in self.generator():
            if h.is_land() and h.direct[HexState.Land] < 5:
                h.set_shallows()
            elif h.is_depths() and h.direct[HexState.Land] < 0:
                h.set_shallows()

    def cleanup(self):
        self.update_hex_states()
        for h in self.generator():
            if h.is_land():
                if h.direct[HexState.Land] < 3:
                    h.set_depths()
                elif h.direct[HexState.Shallows] > 0:
                    h.set_coast()
            elif h.is_shallows() and h.direct[HexState.Depths] > 5 or h.direct[HexState.Shallows] > 5:
                h.set_depths()
            elif h.is_depths() and h.direct[HexState.Coast] > 0 or h.direct[HexState.Land] > 0:
                h.set_shallows()

    def terraform_forests(self):
        """
        Grow forest patches on land areas.
        """
        for n in range(4):
            self.update_hex_states()
            for h in self.generator():
                if h.is_land() and h.total[HexState.Coast] == 0 and h.total[HexState.Shallows] == 0:
                    if h.direct[HexState.Land] == 6:
                        r: float = self._random.uniform(0, 100)
                        if r >= 95:
                            h.set_forest()
                    elif h.direct[HexState.Forest] > 1:
                        h.set_forest()

        # Clear tiny patches of forest
        self.update_hex_states()
        for h in self.generator():
            if h.is_forest() and h.total[HexState.Forest] < 4:
                h.set_land()
