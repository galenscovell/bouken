import json
import sys

from src.processing.interior.interior import Interior
from src.util.compact_json_encoder import CompactJsonEncoder
from src.util.constants import frame_rate, update_rate, background_color


class InteriorMapGenerator(object):
    """
    Procedurally generates square-based interior maps composed of rooms and events.
    """
    def __init__(self, pixel_width: int, pixel_height: int, cell_size: int, number_rooms: int,
                 min_room_size: int, max_room_size: int, min_corridor_length: int, max_corridor_length: int):
        self.pixel_width: int = pixel_width
        self.pixel_height: int = pixel_height
        self.cell_size: int = cell_size
        self.number_rooms: int = number_rooms
        self.min_room_size: int = min_room_size
        self.max_room_size: int = max_room_size
        self.min_corridor_length: int = min_corridor_length
        self.max_corridor_length: int = max_corridor_length

        self.interior: Interior = Interior(self.pixel_width, self.pixel_height, self.cell_size, self.number_rooms,
                                           self.min_room_size, self.max_room_size, self.min_corridor_length,
                                           self.max_corridor_length)

        self.debug_render()

    def generate(self):
        print(' -> Serializing')
        # self.serialize()

    def serialize(self) -> str:
        serialized: dict = {}

        string: str = json.dumps(serialized, cls=CompactJsonEncoder, indent=2)
        return string

    def debug_render(self):
        import pygame
        from pygame import freetype

        pygame.init()
        surface: pygame.Surface = pygame.display.set_mode((self.pixel_width, self.pixel_height))
        pygame.display.set_caption('Bouken Interior Map Debug')
        font = freetype.Font('res/source-code-pro.ttf', 12)

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
