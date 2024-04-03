from typing import List, Tuple

from state.construction import Construction


class Cell:
    def __init__(self, uid: int, x: int, y: int, size: int) -> None:
        self.uid: int = uid
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.box: Tuple[int, int, int, int] = (self.x * self.size, self.y * self.size, self.size, self.size)

        self._state: Construction = Construction.Empty
        self._state_options: List[Construction] = [
            Construction.Floor,
            Construction.Wall,
            Construction.Empty,
            Construction.Padding,
            Construction.Corridor,
            Construction.Corner,
            Construction.Water]

        self.room_id: int = -1
        self._in_room: bool = False

        self.neighbors: List[Cell] = []

    def __eq__(self, other) -> bool:
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def serialize(self) -> dict:
        return {
            'type': self._state.name
        }

    def get_tuple_coord(self) -> Tuple[int, int]:
        return self.x, self.y

    def set_neighbor_states(self) -> None:
        self.direct = [0 for s in self._state_options]
        for c in self.neighbors:
            self.direct[c._state] += 1

    def set_floor(self) -> None:
        self._state = Construction.Floor

    def set_wall(self) -> None:
        self._state = Construction.Wall

    def set_empty(self) -> None:
        self._state = Construction.Empty

    def set_padding(self) -> None:
        self._state = Construction.Padding

    def set_corridor(self) -> None:
        self._state = Construction.Corridor

    def set_corner(self) -> None:
        self._state = Construction.Corner

    def set_water(self) -> None:
        self._state = Construction.Water

    def is_floor(self) -> bool:
        return self._state == Construction.Floor

    def is_wall(self) -> bool:
        return self._state == Construction.Wall

    def is_empty(self) -> bool:
        return self._state == Construction.Empty

    def is_padding(self) -> bool:
        return self._state == Construction.Padding

    def is_corridor(self) -> bool:
        return self._state == Construction.Corridor

    def is_corner(self) -> bool:
        return self._state == Construction.Corner

    def is_water(self) -> bool:
        return self._state == Construction.Water

    def set_room(self, room_id: int) -> None:
        self._in_room = True
        self.room_id = room_id

    def unset_room(self) -> None:
        self._in_room = False
        self.room_id = -1

    def is_in_room(self) -> bool:
        return self._in_room is True
