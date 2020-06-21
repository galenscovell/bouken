"""
Defines a region of a map.
"""

from __future__ import annotations

from typing import List

from src.models.map.point import Point


class Region(object):
    def __init__(self, center: Point, vertices: List[Point], neighbors: List[Region]):
        self.root_point: Point = center
        self.vertices: List[Point] = vertices
        self.neighbors = neighbors
        self.area = self.get_area()

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
