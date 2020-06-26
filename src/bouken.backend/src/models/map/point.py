from __future__ import annotations

from typing import Tuple


class Point(object):
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y
