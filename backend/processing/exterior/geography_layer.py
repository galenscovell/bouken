import random
from typing import List, Set, Tuple, Optional

from backend.processing.exterior.hex import Hex
from backend.processing.exterior.base_layer import BaseLayer
from backend.state.terraform import Terraform
from backend.util.hex_utils import HexUtils


class GeographyLayer(object):
    """
    Defines geographic qualities of map (elevation, depth, dryness, freshwater).
    """
    def __init__(self, base_layer: BaseLayer, min_lake_expansions: int, max_lake_expansions: int,
                 min_lake_amount: int, max_lake_amount: int):
        self._min_lake_expansions: int = min_lake_expansions
        self._max_lake_expansions: int = max_lake_expansions

        self._random: random.Random = random.Random()

        # Get all base hexes
        self.base_layer: BaseLayer = base_layer
        self._usable_hexes: Set[Hex] = set()
        for h in self.base_layer.generator():
            self._usable_hexes.add(h)

        self._lake_amount_target: int = self._random.randint(min_lake_amount, max_lake_amount)
        self._made_lakes: int = 0

        # Set initial elevation using only oceans, so we can utilize it for freshwater placement
        self.set_elevation(include_freshwater=False)

        # Collect a small pool of mid-elevation hexes as our possible lake starters
        mid_elevation_hexes_asc: List[Hex] = sorted(list(self._usable_hexes), key=lambda h: h.elevation)
        start_index: int = round(len(mid_elevation_hexes_asc) // 1.2)
        end_index: int = start_index + (start_index // 24)
        mid_elevation_hexes_asc = mid_elevation_hexes_asc[start_index:end_index]
        self._random.shuffle(mid_elevation_hexes_asc)

        self.possible_lake_starters: List[Hex] = mid_elevation_hexes_asc

    def _expand_lake(self, start_hex: Hex) -> Tuple[List[Hex], List[Hex]]:
        """
        Expand lake from a starting hex a random amount. If lake is not viable, return a tuple of empty lists.
        At each expansion, a random number of hexes continue to expand to prevent uniformity.
        """
        expansions: int = self._random.randint(self._min_lake_expansions, self._max_lake_expansions)
        lake_hexes: Set[Hex] = {start_hex}
        just_expanded: List[Hex] = [start_hex]

        while expansions > 0 and just_expanded:
            newly_expanded: List[Hex] = []
            for h in just_expanded:
                for n in h.direct_neighbors:
                    if n in self._usable_hexes:
                        newly_expanded.append(n)
                        lake_hexes.add(n)

            if not newly_expanded:
                break
            else:
                expansions -= 1
                just_expanded.clear()
                up_to_index: int = int(len(newly_expanded) * self._random.uniform(0.1, 1))
                for n in range(up_to_index):
                    h: Hex = newly_expanded[n]
                    just_expanded.append(h)

        # Find lake exterior
        exterior: List[Hex] = []
        for h in lake_hexes:
            if h.direct[Terraform.Ocean] > 0 or h.direct[Terraform.River] > 0:
                return [], []
            elif h.direct[Terraform.Land] > 0:
                exterior.append(h)

        return list(lake_hexes), exterior

    @staticmethod
    def _path_river(current: Optional[Hex]) -> List[Hex]:
        """
        Plot a river with its hexes flowing down elevation to the ocean.
        """
        river_hexes: List[Hex] = []

        pathing: bool = True
        while pathing:
            river_hexes.append(current)
            neighbors_by_elevation_desc: List[Hex] = sorted(
                current.direct_neighbors, key=lambda h: h.elevation, reverse=True)

            if neighbors_by_elevation_desc:
                next: Hex = neighbors_by_elevation_desc.pop()
                if current.elevation > next.elevation:
                    current: Hex = next
                else:
                    pathing = False

        # Final hex in river should be neighboring ocean
        if river_hexes[-1].direct[Terraform.Ocean] == 0:
            return []
        return list(river_hexes)

    def place_freshwater(self) -> bool:
        """
        Turn a random number of mid-elevation hexes into lakes, expand them, then create rivers flowing
        from them to the ocean. Return False once target reached or pool exhausted.
        """
        if self._made_lakes < self._lake_amount_target and self.possible_lake_starters:
            self.base_layer.update_hex_neighbors()
            lake_hexes, exterior = self._expand_lake(self.possible_lake_starters.pop())
            if exterior:
                exterior.sort(key=lambda h: h.elevation)  # Sort ascending
                while exterior:
                    river_hexes: List[Hex] = self._path_river(exterior.pop())
                    if river_hexes:
                        # If final result was usable, finalize it
                        for h in lake_hexes:
                            h.set_lake()
                            if h in self._usable_hexes:
                                self._usable_hexes.remove(h)

                        for h in river_hexes:
                            h.set_river()
                            if h in self._usable_hexes:
                                self._usable_hexes.remove(h)

                        self._made_lakes += 1
                        return True
            return True
        return False

    def finalize(self):
        self.base_layer.update_hex_neighbors()

        # Set elevation including both ocean and freshwater distances
        self.set_elevation(include_freshwater=True)

        # Set remaining geographic details
        self.set_dryness()
        self.set_depth()

        self.base_layer.update_hex_neighbors()

    def set_elevation(self, include_freshwater: bool):
        """
        Expand out from each hex until water is hit to determine elevation grade.
        Elevation is a land hex's distance from (mostly) ocean and (minorly) freshwater.
        """
        for h in self.base_layer.generator():
            if h.is_land() or h.is_coast():
                ocean_elevation: float = HexUtils.distance(h, [Terraform.Ocean])
                elevation: float = ocean_elevation
                if include_freshwater and self._made_lakes > 0:
                    freshwater_elevation: float = HexUtils.distance(h, [Terraform.Lake, Terraform.River])
                    elevation = (ocean_elevation * 0.6) + (freshwater_elevation * 0.4)

                h.elevation = elevation
            else:
                h.elevation = 0

    def set_dryness(self):
        """
        Expand out from each hex until lake is hit to determine moisture grade.
        Dryness is a land hex's distance from (mostly) freshwater sources and (minorly) ocean.
        """
        for h in self.base_layer.generator():
            if h.is_land() or h.is_coast():
                ocean_distance: float = HexUtils.distance(h, [Terraform.Ocean])
                if self._made_lakes > 0:
                    freshwater_distance = HexUtils.distance(h, [Terraform.Lake, Terraform.River])
                else:
                    freshwater_distance = HexUtils.normalize(HexUtils.MAX_DISTANCE)

                h.dryness = (freshwater_distance * 0.8) + (ocean_distance * 0.2)
            else:
                h.dryness = 0

    def set_depth(self):
        """
        Expand out from each hex until land is hit to determine depth grade.
        Depth is an ocean hex's distance from land.
        """
        for h in self.base_layer.generator():
            if h.is_ocean() or h.is_lake() or h.is_river():
                h.depth = HexUtils.distance(h, [Terraform.Land])
            else:
                h.depth = 0
