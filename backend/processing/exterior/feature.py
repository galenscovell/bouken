from typing import Tuple

from backend.state.biome import Biome
from backend.state.landform import Landform


class Feature(object):
    def __init__(self, landform: Landform, name: str) -> None:
        self.landform: Landform = landform
        self.name: str = name
