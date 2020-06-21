from __future__ import annotations

import math


class Point(object):
    """
    Defines an x, y coordinate.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Point: {self.x}, {self.y}'

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, list):
            if len(other) == 2:
                return self.x == other[0] and self.y == other[1]
        return False

    def distance_from(self, point: Point):
        dx = self.x - point.x
        dy = self.y - point.y
        return math.sqrt(dx ** 2 + dy ** 2)
