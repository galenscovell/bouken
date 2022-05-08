from state.landform import Landform


class Feature:
    def __init__(self, landform: Landform, name: str) -> None:
        self.landform: Landform = landform
        self.name: str = name
