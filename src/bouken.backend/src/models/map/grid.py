import math
import random

import pygame

from typing import List, Optional

from src.models.map.hex_state import HexState
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
        self.width_diameter, self.height_diameter, self.vertical_spacing, self.horizontal_spacing = \
            HexUtils.calculate_layout(hex_size, pointy)

        self.columns: int = int(self.pixel_width // (self.width_diameter / 2))
        self.rows: int = int(self.pixel_height // (self.height_diameter / 2))

        self.neighbours = ((2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1))

        # Swap grid dimensions if flat-topped hexes
        if not pointy:
            self.rows, self.columns = self.columns, self.rows
            self.neighbours = ((0, 2), (1, 1), (-1, 1), (0, -2), (-1, -1), (1, -1))

        self.grid: List[List[Hex]] = self._construct_grid()

        final_cell = self.get_hex(self.columns - 1, self.rows - 1)
        self.actual_width: int = round(final_cell.pixel_center_x + self.width_diameter)
        self.actual_height: int = round(final_cell.pixel_center_y + self.height_diameter)

        self.rdm: random.Random = random.Random()

    def _construct_grid(self) -> List[List[Hex]]:
        # Init grid as 2D array of None
        grid: List[List[Hex]] = []
        for x in range(self.columns):
            grid.append([])
            for y in range(self.rows):
                grid[x].append(None)

        # Create even Hexagons
        for x in range(0, self.columns, 2):
            for y in range(0, self.rows, 2):
                grid[x][y] = Hex(x, y, self.hex_size, self.pointy)

        # Create odd Hexagons
        for x in range(1, self.columns, 2):
            for y in range(1, self.rows, 2):
                grid[x][y] = Hex(x, y, self.hex_size, self.pointy)

        return grid

    @staticmethod
    def distance(h1: Hex, h2: Hex) -> int:
        """
        Distance in number of hexagon steps between two hexes.
        Direct neighbours of a hex have distance 1.
        """
        dx = abs(h1.x - h2.x)
        dy = abs(h1.y - h2.y)
        return dy + max(0, (dx - dy) // 2)

    def get_neighbours(self, h: Hex) -> List[Hex]:
        """
        Return the 6 direct neighbours of a hex.
        """
        return [self.get_hex(h.x + dx, h.y + dy) for dx, dy in self.neighbours]

    def random_neighbour(self, h: Hex) -> Optional[Hex]:
        """
        Return a random neighbour of a hex.
        """
        dx, dy = self.rdm.choice(self.neighbours)
        return self.get_hex(h.x + dx, h.y + dy)

    def get_hex(self, x: int, y: int) -> Optional[Hex]:
        """
        Get the Hex at given col, row coordinates.
        """
        if 0 <= x < self.columns and 0 <= y < self.rows:
            return self.grid[x][y]
        return None

    def test_display(self):
        frame_rate = 60
        input_rate = 6
        background_color = (52, 73, 94)
        empty_color = (44, 62, 80)
        selected_color = (241, 196, 15)
        land_color = (39, 174, 96)
        water_color = (52, 152, 219)

        pygame.init()
        screen = pygame.display.set_mode((self.actual_width, self.actual_height))
        pygame.display.set_caption('Bouken Test Display')

        clock = pygame.time.Clock()
        screen.fill(background_color)

        selected_hex: Hex = self.get_hex(0, 0)
        selected_hex.state = HexState.Selected
        selection_tick = 0
        last_y = 1
        running = True
        while running:
            pygame.event.poll()

            selection_tick -= 1
            if selection_tick <= 0:
                pressed = pygame.key.get_pressed()
                selection_tick = input_rate
                new_hex: Optional[Hex] = None
                if pressed[pygame.K_LEFT]:
                    last_y = -last_y
                    new_hex: Hex = self.get_hex(selected_hex.x - 1, selected_hex.y - last_y)
                elif pressed[pygame.K_RIGHT]:
                    last_y = -last_y
                    new_hex: Hex = self.get_hex(selected_hex.x + 1, selected_hex.y + last_y)
                elif pressed[pygame.K_UP]:
                    new_hex: Hex = self.get_hex(selected_hex.x, selected_hex.y - 2)
                elif pressed[pygame.K_DOWN]:
                    new_hex: Hex = self.get_hex(selected_hex.x, selected_hex.y + 2)

                if new_hex:
                    selected_hex.state = HexState.Empty
                    [h.set_state(HexState.Empty) for h in self.get_neighbours(selected_hex) if h]
                    selected_hex = new_hex
                    new_hex.state = HexState.Selected
                    [h.set_state(HexState.Land) for h in self.get_neighbours(selected_hex) if h]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for x in range(self.columns):
                for y in range(self.rows):
                    cell: Hex = self.get_hex(x, y)
                    if cell:
                        if cell.state == HexState.Selected:
                            color = selected_color
                        elif cell.state == HexState.Land:
                            color = land_color
                        elif cell.state == HexState.Water:
                            color = water_color
                        else:
                            color = empty_color

                        pygame.draw.polygon(screen, color, cell.vertices)
                        pygame.draw.lines(screen, background_color, True, cell.vertices)

            pygame.display.flip()
            clock.tick(frame_rate)

        pygame.quit()
