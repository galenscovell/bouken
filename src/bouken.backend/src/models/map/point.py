from __future__ import annotations


class Point(object):
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
