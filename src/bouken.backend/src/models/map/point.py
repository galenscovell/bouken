"""
Defines an x, y coordinate.
"""

from __future__ import annotations

import math


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Point: {self.x}, {self.y}'

    def distance_from(self, point: Point):
        dx = self.x - point.x
        dy = self.y - point.y
        return math.sqrt(dx ** 2 + dy ** 2)
