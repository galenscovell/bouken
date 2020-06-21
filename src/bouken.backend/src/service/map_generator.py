from typing import List, Tuple

import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi

from src.models.map.point import Point
from src.models.map.region import Region


class MapGenerator:
    """
    Map generation tool.
    """
    def generate_overworld(self, width: int, height: int, approx_num_regions: int, smoothing: int):
        points: List[Tuple[float, float]] = []
        for i in range(approx_num_regions * 3):
            x = random.randint(0, width)
            y = random.randint(0, height)
            points.append((x, y))

        vor: Voronoi = self._generate_voronoi(points, smoothing)
        # self._display_voronoi(vor, width, height)

        # Create regions from Voronoi
        regions: List[Region] = []
        for n, reg in enumerate(vor.regions):
            if reg and -1 not in reg:
                region_vertices: List[Point] = []
                for ind in reg:
                    region_vertices.append(Point(vor.vertices[ind][0], vor.vertices[ind][1]))

                center_x = sum([v.x for v in region_vertices]) / len(region_vertices)
                center_y = sum([v.y for v in region_vertices]) / len(region_vertices)
                regions.append(Region(Point(center_x, center_y), region_vertices))

        # Find each region's neighbors
        for region in regions:
            for other in regions:
                if other == region:
                    continue

                shared_vertices = [i for i in region.vertices if i in other.vertices]
                if shared_vertices:
                    region.neighbors.append(other)

    def _generate_voronoi(self, points: List[Tuple[float, float]], iterations: int) -> Voronoi:
        v: Voronoi = Voronoi(points)
        for i in range(iterations):
            points.clear()
            for vertices in v.regions:
                if len(vertices) == 0:
                    continue

                vert_arr = []
                for num in vertices:
                    vert_arr.append(v.vertices[num])

                points.append(self._get_centroid(vert_arr))

            v = Voronoi(points)

        return v

    @staticmethod
    def _display_voronoi(vor: Voronoi, width: int, height: int):
        # vor.ridge_vertices provides indices into the vor.vertices array
        for vpair in vor.ridge_vertices:
            if vpair[0] >= 0 and vpair[1] >= 0:
                v0 = vor.vertices[vpair[0]]
                v1 = vor.vertices[vpair[1]]
                # Draw a line from v0 to v1.
                plt.plot([v0[0], v1[0]], [v0[1], v1[1]], 'k', linewidth=1, alpha=0.6)

        for n, reg in enumerate(vor.regions):
            if reg and -1 not in reg:
                region_vertices = []
                for ind in reg:
                    region_vertices.append(vor.vertices[ind])

                center_x = sum([v[0] for v in region_vertices]) / len(region_vertices)
                center_y = sum([v[1] for v in region_vertices]) / len(region_vertices)
                plt.annotate(f'{n}', xy=(center_x, center_y))

                for v in region_vertices:
                    label_point_x = (v[0] + center_x) / 2
                    label_point_y = (v[1] + center_y) / 2
                    plt.annotate(f'{n}', xy=(label_point_x, label_point_y))

        plt.xlim([0, width]), plt.ylim([0, height])
        plt.show()

    @staticmethod
    def _get_centroid(vertices: List[List[int]]) -> Tuple[float, float]:
        x: float = 0
        y: float = 0
        for i in range(len(vertices)):
            x += vertices[i][0]
            y += vertices[i][1]

        return x / len(vertices), y / len(vertices)
