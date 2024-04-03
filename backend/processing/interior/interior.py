import pygame

from random import Random
from typing import Tuple, Optional, List, Dict, Set

from processing.interior.cell import Cell
from processing.interior.corridor import Corridor
from processing.interior.room import Room

from util.constants import tropical_forest_color, background_color, tropical_desert_color, taiga_color, bare_color


class Interior:
    def __init__(self,
                 pixel_width: int,
                 pixel_height: int,
                 cell_size: int,
                 number_rooms: int,
                 min_room_size: int,
                 max_room_size: int,
                 min_corridor_length: int,
                 max_corridor_length: int) -> None:
        self._cell_size: int = cell_size
        self._number_rooms: int = number_rooms

        self._min_room_size: int = min_room_size // 2
        self._max_room_size: int = max_room_size // 2
        self._min_corridor_length: int = min_corridor_length
        self._max_corridor_length: int = max_corridor_length

        self._columns: int = pixel_width // cell_size
        self._rows: int = pixel_height // cell_size

        self._room_id_counter: int = 0
        self.room_id_to_room: Dict[int, Room] = dict()

        self._orthogonal_neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))
        self._random: Random = Random()

        # Build grid of cells
        self.grid: List[List[Optional[Cell]]] = []
        cell_id: int = 0
        for x in range(self._columns):
            self.grid.append([])
            for y in range(self._rows):
                # All cells begin as walls
                self.grid[x].append(Cell(cell_id, x, y, self._cell_size))
                cell_id += 1

        # Set cell neighbors
        for x in range(self._columns):
            for y in range(self._rows):
                c: Cell = self[x, y]
                c.neighbors = self._set_neighbors(c)

        col_middle: int = ((self._columns - 1) // 2)
        col_left_offset: int = col_middle - (col_middle // 6)
        col_right_offset: int = col_middle + (col_middle // 6)
        row_middle: int = ((self._rows - 1) // 2)
        row_left_offset: int = row_middle - (row_middle // 6)
        row_right_offset: int = row_middle + (row_middle // 6)

        perimeter_cells: List[Cell] = []
        for c in self.generator():
            if (c.x == 0 or c.x == self._columns - 1
                    or c.y == 0 or c.y == self._rows - 1
                    or (c.y == 0 and col_left_offset < c.x < col_right_offset)
                    or (c.x == 0 and row_left_offset < c.y < row_right_offset)):
                c.set_padding()
                perimeter_cells.append(c)

        # Get random cell from grid's (central) perimeter to begin entry corridor
        corridor_built: bool = False
        while not corridor_built and perimeter_cells:
            self._random.shuffle(perimeter_cells)
            corridor_built = self._build_corridor(perimeter_cells.pop())

    def __len__(self) -> int:
        return self._columns * self._rows

    def __setitem__(self, xy: Tuple[int, int], value):
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            self.grid[xy[0]][xy[1]] = value

    def __getitem__(self, xy: Tuple[int, int]) -> Optional[Cell]:
        if 0 <= xy[0] < self._columns and 0 <= xy[1] < self._rows:
            return self.grid[xy[0]][xy[1]]
        return None

    def serialize(self) -> dict:
        cells: dict = {}
        for c in self.generator():
            cells[str(c.uid)] = c.serialize()

        return cells

    def generator(self) -> Optional[Cell]:
        """
        Iterate through cells in the grid.
        """
        for x in range(self._columns):
            for y in range(self._rows):
                yield self[x, y]

    def construct(self) -> bool:
        """
        Attempt to build a new room branching off of a previously built one.
        Return False when no more rooms can be built or target amount is reached.
        """
        # Pick previously created room to branch off of
        tested_rooms: List[Room] = list(self.room_id_to_room.values())
        if len(tested_rooms) == self._number_rooms:
            return False

        while tested_rooms:
            room: Room = self._random.choice(tested_rooms)
            if not room.perimeter:
                tested_rooms.remove(room)
                room.reset_perimeter()
                continue

            self._random.shuffle(room.perimeter)
            if self._build_corridor(room.perimeter.pop()):
                return True

        return False

    def finalize(self):
        return

    def _build_corridor(self, start_cell: Cell) -> bool:
        """
        Build a corridor out from a cell in the empty direction from it.
        If corridor is viable, build a room at the end of it.
        If room is also viable, return True, otherwise False.
        """
        self._update_neighbors()

        corridor_dir: Tuple[int, int] = (0, 0)
        for dx, dy in self._orthogonal_neighbors:
            c: Cell = self[start_cell.x + dx, start_cell.y + dy]
            if c and (c.is_empty() or c.is_padding()):
                corridor_dir = (dx, dy)

        if corridor_dir == (0, 0):
            return False

        corridor_cells: List[Cell] = [start_cell]
        # - 1 to length to include start cell in total length
        corridor_length: int = self._random.randint(self._min_corridor_length - 1, self._max_corridor_length - 1)
        for n in range(corridor_length):
            start_cell = self[start_cell.x + corridor_dir[0], start_cell.y + corridor_dir[1]]
            if not start_cell or not (start_cell.is_empty() or start_cell.is_padding()):
                return False

            corridor_cells.append(start_cell)

        if corridor_cells:
            end_cell: Cell = corridor_cells[-1]
            room: Room = self._build_room(end_cell, corridor_dir)

            if room:
                end_cell: Cell = corridor_cells[-1]
                new_corridor: Corridor = Corridor(start_cell, end_cell, corridor_cells, room.room_id)
                room.corridors.append(new_corridor)

                return True

    def _build_room(self, corridor_end_cell: Cell, corridor_dir: Tuple[int, int]) -> Optional[Room]:
        """
        Build a room at the end of a corridor.
        If viable return it, otherwise None.
        """
        self._update_neighbors()

        room_width: int = self._random.randint(self._min_room_size, self._max_room_size)
        room_height: int = self._random.randint(self._min_room_size, self._max_room_size)

        room_cells: Set[Cell] = set()
        perimeter: Set[Cell] = set()
        corners: Set[Cell] = set()

        movement_to_room_center: Tuple[int, int] = (corridor_dir[0] * room_width, corridor_dir[1] * room_height)
        center_cell: Cell = self[
            corridor_end_cell.x + movement_to_room_center[0],
            corridor_end_cell.y + movement_to_room_center[1]
        ]

        if not center_cell:
            return None

        for dx in range(-room_width, room_width + 1):
            for dy in range(-room_height, room_height + 1):
                c: Cell = self[center_cell.x + dx, center_cell.y + dy]
                if not c or not c.is_empty():
                    return None

                # Find perimeter
                if dx == -room_width or dx == room_width or dy == -room_height or dy == room_height:
                    # Corner cells, handled differently
                    if ((dx == -room_width and dy == -room_height)
                            or (dx == -room_width and dy == room_height)
                            or (dx == room_width and dy == -room_height)
                            or (dx == room_width and dy == room_height)):
                        corners.add(c)
                    else:
                        perimeter.add(c)
                else:
                    # Floor cells
                    room_cells.add(c)

        room_id: int = self._room_id_counter
        self._room_id_counter += 1

        new_room: Room = Room(
            room_id, center_cell, room_width, room_height, list(room_cells), list(perimeter), list(corners))
        self.room_id_to_room[room_id] = new_room
        self._pad_room(new_room)

        return new_room

    def _pad_room(self, room: Room):
        """
        Add a one cell border of padding around created room so rooms aren't built touching each other.
        """
        self._update_neighbors()
        for c in room.perimeter_and_corners:
            for n in c.neighbors:
                if n.is_empty():
                    n.set_padding()

    def _set_neighbors(self, c: Cell) -> List[Optional[Cell]]:
        """
        Sets the 4 orthogonal neighbours of a cell.
        """
        delta: List[Tuple[int, int]] = [(c.x + dx, c.y + dy) for dx, dy in self._orthogonal_neighbors]
        return [self[x, y] for x, y in delta if x > -1 and y > -1 and self[x, y]]

    def _update_neighbors(self) -> None:
        """
        Update the neighbor states for all cells in the grid.
        """
        [c.set_neighbor_states() for c in self.generator()]

    def debug_render(self, surface: pygame.Surface) -> None:
        for c in self.generator():
            if c.is_floor():
                pygame.draw.rect(surface, tropical_forest_color, c.box)
            elif c.is_wall():
                pygame.draw.rect(surface, taiga_color, c.box)
            elif c.is_corridor():
                pygame.draw.rect(surface, tropical_desert_color, c.box)
            elif c.is_padding():
                # pygame.draw.rect(surface, snow_color, c.box)
                continue
            elif c.is_corner():
                pygame.draw.rect(surface, bare_color, c.box)
            else:
                pygame.draw.rect(surface, background_color, c.box)