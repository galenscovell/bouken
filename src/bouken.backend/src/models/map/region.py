from __future__ import annotations

from typing import List

from src.models.map.point import Point


class Region(object):
    """
    Defines a region of a map.
    """
    def __init__(self, center: Point, vertices: List[Point]):
        self.center: Point = center
        self.vertices: List[Point] = vertices  # In order by connection (0->1, 1->2, ... n->0)
        self.area: float = self.get_area()
        self.neighbors: List[Region] = []

    def get_area(self) -> float:
        """
        Calculate area of this Region using the Shoelace method.
        :return: area as float
        """
        n = len(self.vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i].x * self.vertices[j].y
            area -= self.vertices[j].x * self.vertices[i].y

        return abs(area) / 2.0
