from typing import Tuple

from src.state.biome import Biome
from src.state.landform import Landform


class Feature(object):
    def __init__(self, landform: Landform, name: str):
        self.landform: Landform = landform
        self.name: str = name
