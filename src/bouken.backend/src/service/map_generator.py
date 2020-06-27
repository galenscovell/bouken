import random

from src.models.map.grid import Grid
from src.models.map.hex import Hex
from src.models.map.hex_state import HexState


class MapGenerator:
    def __init__(self, pixel_width: int, cell_size: int, iterations: int):
        self.pixel_width: int = pixel_width
        self.hex_diameter: int = cell_size
        self.iterations: int = iterations

        self.grid: Grid = Grid(self.pixel_width, self.hex_diameter, True)
        self.rdm: random.Random = random.Random()

        self.test_display()

    def reset(self):
        [h.set_random_state(self.rdm) for h in self.grid.generator()]

    def update_hex_states(self):
        [h.set_neighbor_states() for h in self.grid.generator()]

    def terraform_land(self):
        self.update_hex_states()
        for h in self.grid.generator():
            if not h.is_land() and h.total[HexState.Land] > 6:
                h.set_land()

    def terraform_water(self):
        self.update_hex_states()
        for h in self.grid.generator():
            if h.is_land() and h.direct[HexState.Land] < 5:
                h.set_shallows()
            elif h.is_depths() and h.direct[HexState.Land] < 0:
                h.set_shallows()

    def cleanup(self):
        self.update_hex_states()
        for h in self.grid.generator():
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
        for n in range(4):
            self.update_hex_states()
            for h in self.grid.generator():
                if h.is_land() and h.total[HexState.Coast] == 0 and h.total[HexState.Shallows] == 0:
                    if h.direct[HexState.Land] == 6:
                        r: float = self.grid.rdm.uniform(0, 100)
                        if r >= 95:
                            h.set_forest()
                    elif h.direct[HexState.Forest] > 1:
                        h.set_forest()

        self.update_hex_states()
        for h in self.grid.generator():
            if h.is_forest() and h.total[HexState.Forest] < 4:
                h.set_land()

    def test_display(self):
        import pygame

        frame_rate = 60
        update_rate = 3
        reset_rate = 100
        background_color = (52, 73, 94, 200)

        land_color = (6, 227, 97, 200)
        forest_color = (65, 195, 123, 200)
        coast_color = (255, 255, 42, 200)
        shallows_color = (0, 99, 113, 200)
        depths_color = (0, 89, 114, 200)

        pygame.init()
        screen = pygame.display.set_mode((self.grid.actual_width, self.grid.actual_height))
        pygame.display.set_caption('Bouken Test Display')

        clock = pygame.time.Clock()
        screen.fill(background_color)

        # center: Hex = self.grid[6, 6]
        # center.set_land()
        # [h.set_land() for h in center.neighbors if h]

        terraform_tick = 0
        running = True
        while running:
            pygame.event.poll()

            terraform_tick -= 1
            if self.iterations > 0 and terraform_tick <= 0:
                self.terraform_land()
                terraform_tick = update_rate
                self.iterations -= 1

                if self.iterations == 0:
                    self.terraform_water()
                    self.cleanup()
                    self.terraform_forests()
            elif self.iterations == 0:
                if reset_rate == 0:
                    self.reset()
                    reset_rate = 100
                    self.iterations = 40
                else:
                    reset_rate -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for x in range(self.grid.columns):
                for y in range(self.grid.rows):
                    cell: Hex = self.grid[x, y]
                    if cell:
                        if cell.is_land():
                            color = land_color
                        elif cell.is_forest():
                            color = forest_color
                        elif cell.is_desert():
                            color = coast_color
                        elif cell.is_coast():
                            color = coast_color
                        elif cell.is_shallows():
                            color = shallows_color
                        else:
                            color = depths_color

                        pygame.draw.polygon(screen, color, cell.vertices)
                        # pygame.draw.lines(screen, background_color, True, cell.vertices)

            pygame.display.flip()
            clock.tick(frame_rate)

        pygame.quit()
