import json
import sys

from backend.processing.interior.interior import Interior
from backend.util.compact_json_encoder import CompactJsonEncoder
from backend.util.constants import frame_rate, update_rate, background_color
from backend.util.logger import Logger


class InteriorMapGenerator(object):
    """
    Procedurally generates square-based interior maps composed of rooms and events.
    """
    def __init__(self, logger: Logger) -> None:
        self.logger: Logger = logger


    def begin(self, pixel_width: int, pixel_height: int, cell_size: int, number_rooms: int, min_room_size: int, max_room_size: int, min_corridor_length: int, max_corridor_length: int) -> None:
        self.pixel_width: int = pixel_width
        self.pixel_height: int = pixel_height
        self.cell_size: int = cell_size
        self.number_rooms: int = number_rooms
        self.min_room_size: int = min_room_size
        self.max_room_size: int = max_room_size
        self.min_corridor_length: int = min_corridor_length
        self.max_corridor_length: int = max_corridor_length

        self.interior: Interior = Interior(self.pixel_width, self.pixel_height, self.cell_size, self.number_rooms, self.min_room_size, self.max_room_size, self.min_corridor_length, self.max_corridor_length)

        # self.debug_render()

    def generate(self) -> str:
        self.logger.info('Interior -> Serializing')
        return self.serialize()

    def serialize(self) -> str:
        serialized: dict = {}

        return json.dumps(serialized, cls=CompactJsonEncoder, indent=2)

    def debug_render(self) -> None:
        import pygame
        from pygame import freetype

        pygame.init()
        surface: pygame.Surface = pygame.display.set_mode((self.pixel_width, self.pixel_height))
        pygame.display.set_caption('Bouken Interior Map Debug')

        clock = pygame.time.Clock()
        surface.fill(background_color)

        update_tick = 0
        terraforming = True

        running = True
        while running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False

            update_tick -= 1
            if update_tick <= 0:
                update_tick = update_rate

                if terraforming:
                    constructing: bool = self.interior.construct()
                    if not constructing:
                        self.interior.finalize()
                        terraforming = False

            self.interior.debug_render(surface)

            pygame.display.flip()
            clock.tick(frame_rate)

        pygame.quit()
        sys.exit(0)
