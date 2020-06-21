"""
Map generation tool.
"""

from typing import List, Tuple

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d


class MapGenerator:
    def generate_overworld(self, width: int, height: int, approx_num_regions: int, smoothing: int):
        points = []
        for i in range(approx_num_regions * 3):
            x = random.randint(0, width)
            y = random.randint(0, height)
            points.append((x, y))

        vor = self._lloyd_relaxation(Voronoi(points), smoothing)

        # TODO: Get root_point and vertices for each region
        # Find neighbors for each region
        # Assemble internal Map with Regions

        # Mark the vertices
        plt.plot(vor.vertices[:, 0], vor.vertices[:, 1], 'ko', ms=4, color='orange', alpha=0.8)

        # vor.ridge_vertices provides indices into the vor.vertices array
        for vpair in vor.ridge_vertices:
            if vpair[0] >= 0 and vpair[1] >= 0:
                v0 = vor.vertices[vpair[0]]
                v1 = vor.vertices[vpair[1]]
                # Draw a line from v0 to v1.
                plt.plot([v0[0], v1[0]], [v0[1], v1[1]], 'k', linewidth=1, color='blue', alpha=0.8)

        for n in range(len(vor.regions)):
            region = vor.regions[n]
            if region and -1 not in region:
                polygon_x = [vor.vertices[i][0] for i in region]
                polygon_y = [vor.vertices[i][1] for i in region]
                center_x = sum(polygon_x) / len(polygon_x)
                center_y = sum(polygon_y) / len(polygon_y)
                plt.annotate(f'{n}', xy=(center_x, center_y))

        plt.xlim([0, width]), plt.ylim([0, height])
        plt.show()

        for n in range(len(vor.regions)):
            if n in vor.point_region:
                region_idx = np.where(vor.point_region == n)[0][0]
                region_vertices = vor.regions[region_idx]

                print(region_vertices)

        # voronoi_plot_2d(vor, show_vertices=False, line_width=2, line_alpha=0.4, point_size=2)
        # plt.show()

    def _lloyd_relaxation(self, v: Voronoi, iterations: int):
        for i in range(iterations):
            relaxed_points = []
            for vertices in v.regions:
                if len(vertices) == 0:
                    continue

                vert_arr = []
                for num in vertices:
                    vert_arr.append(v.vertices[num])

                relaxed_points.append(self._get_centroid(vert_arr))

            v = Voronoi(relaxed_points)

        return v

    @staticmethod
    def _get_centroid(vertices: List[List[int]]) -> Tuple[float, float]:
        x, y = 0, 0
        for i in range(len(vertices)):
            x += vertices[i][0]
            y += vertices[i][1]

        return x / len(vertices), y / len(vertices)
