from random import Random
from typing import Dict, List

from processing.exterior.region_layer import RegionLayer
from processing.exterior.region import Region

from state.biome import Biome
from state.landform import Landform
from state.structure import Structure


class FeatureLayer:
    """
    Defines feature layer of a map, detailing its landscape features and events.
    """
    def __init__(self, region_layer: RegionLayer) -> None:
        self.regions: List[Region] = []
        for region_id in region_layer.keys():
            self.regions.append(region_layer[region_id])

        self._random: Random = Random()

        self.biome_to_base_landform_possibilities: Dict[Biome, Dict[float, Landform]] = {
            Biome.Grassland: {
                0.4: Landform.Hill,
                0.6: Landform.Plain
            },
            Biome.TropicalDesert: {
                0.1: Landform.Oasis,
                0.9: Landform.Plain
            },
            Biome.TropicalForest: {
                1.0: Landform.Forest
            }
        }

        self.biome_to_base_structure_possibilities: Dict[Biome, Dict[float, Structure]] = {}

    def construct(self) -> None:
        """
        Details we have for each region:
            Biome, coastal, near-lake, near-river, secluded, surrounded, neighbor regions, island,
            elevation (avg and per hex), dryness (avg and per hex), area.
        """
        for region in self.regions:
            if region.biome == Biome.Bare:
                self._handle_bare_biome(region)

    def _handle_bare_biome(self, region: Region) -> None:
        """
        Mountainous and rocky with little flora or fauna.
        There are less chances of running into anyone friendly here, and more chances to find enemies.
        Life is generally harder here and events are more dangerous.

        Landscape: Deep caves, mountains
        Locations: Ruins, monster dens, outposts
        Dangers: Falling (strong winds), starving, avalanches
        """
        return

    def _handle_snow_biome(self, region: Region) -> None:
        """
        Freezing, either flat or mountainous, and have little flora or fauna.
        There are less chances of running into anyone friendly here, and more chances to find enemies.
        Life is generally harder here and events are more dangerous.

        Landscape: Ice caverns/lakes/rivers
        Locations: Ruins, monster dens, outposts
        Dangers: Freezing, starving, falling (ice breaking/slipping), avalanches
        """
        return

    def _handle_tundra_biome(self, region: Region) -> None:
        """
        Cold wastelands (permafrost), with sparse flora and moderate amounts of fauna.
        Friendly encounters are either fellow travellers or small outposts.

        Landscape: Permafrost caverns/lakes/rivers
        Locations: Ruins, monster dens, outposts
        Dangers: Freezing, starving
        """
        return

    def _handle_temperate_desert_biome(self, region: Region) -> None:
        """
        Generally flat and sparse of flora with moderate amounts of fauna that thrive seasonally.
        Friendly encounters are either fellow travellers or small outposts.

        Landscape: Snow and sand depending on elevation, salt deposits
        Locations: Ruins, monster dens, outposts
        Dangers: Freezing or burning, starving
        """
        return

    def _handle_temperate_forest_biome(self, region: Region) -> None:
        """
        Dense flora (tree canopies) and fauna across hills and mountains with high amounts of fog.
        Friendly encounters are more frequent and vary in size.

        Landscape: Fog, mountains, hills, forests
        Locations: Ruins, monster dens, outposts, villages
        Dangers: Sight impacted (vegetation and fog), poison
        """
        return

    def _handle_taiga_biome(self, region: Region) -> None:
        """
        Boreal forests with moderate amounts of both flora and fauna.
        Friendly encounters are more frequent and vary in size.

        Landscape: Forests, hills
        Locations: Ruins, monster dens, outposts, villages
        Dangers:
        """
        return

    def _handle_grassland_biome(self, region: Region) -> None:
        """
        Sparse but thriving flora and fauna in stretched out flats of land and rolling hills.
        Friendly encounters are more frequent and vary in size.

        Landscape: Prairies, savannas, canyons
        Locations: Ruins, monster dens, outposts, villages
        Dangers:
        """
        return

    def _handle_tropical_desert_biome(self, region: Region) -> None:
        """
        Hot flats that become freezing at night. Sand dunes and sometimes a rare oasis. Little flora or fauna.
        There are less chances of running into anyone friendly here, and more chances to find enemies.
        Life is generally harder here and events are more dangerous.

        Landscape: Sand, dunes, oasis
        Locations: Ruins, monster dens, outposts
        Dangers: Burning, freezing, starving
        """
        return

    def _handle_tropical_forest_biome(self, region: Region) -> None:
        """
        Dense flora and fauna with high humidity and temperature.

        Landscape: Fog, mountains, hills, jungles
        Locations: Ruins, monster dens, outposts
        Dangers: Sight impacted (vegetation and fog), poison
        """
        return

    def _generate_events(self) -> None:
        """
        Add events to each placed feature.
        """
        return
