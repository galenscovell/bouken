"""
Defines the core map.
"""

from typing import List

from src.models.map.region import Region


class Map(object):
    def __init__(self, width: int, height: int, regions: List[Region]):
        self.width: int = width
        self.height: int = height
        self.num_regions: int = len(regions)
        self.regions = regions

    def merge_regions(self, target_region: Region, other_region: Region):
        """
        Merge this Region with another, resulting in a single expanded Region.
        :param target_region: Region to maintain
        :param other_region: Region to merge into target-region
        :return: Region
        """
        # find vertices between regions, delete them
        # add all remaining vertices of other_region to target_region, as well as new neighbors
        # recalculate area
        print('todo')
