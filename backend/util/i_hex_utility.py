from typing import List, Tuple, Optional

from backend.processing.exterior.hex import Hex

from backend.state.terraform import Terraform


class IHexUtility:
    """Interface for hexagon utility operations."""
    def __init__(self) -> None:
        self.max_distance: float = 0

    def set_max_distance(self, new_value: float) -> None:
        """Max possible distance cap. Smaller divisor (larger value) = finer gradient and lower extremes."""
        pass

    def get_max_distance(self) -> float:
        """Get max possible distance cap."""
        pass

    def distance(self, h: Hex, hex_types: List[Terraform]) -> float:
        """
        Find the hex distance from start hex to any hex of target state.
        """
        pass

    def normalize(self, value: float) -> float:
        """
        Normalize a value to between -1 and 1.
        """
        pass

    def calculate_layout(hex_size: int, pointy: bool) -> Tuple[int, int, int, int]:
        """
        Calculate grid layout values.
        """
        pass

    def calculate_hex_corners(center_x: int, center_y: int, size: int, pointy: bool) -> List[Tuple[int, int]]:
        """
        Calculate the vertices defining a hexes corners.
        """
        pass

    def expand_until_hit(h: Hex, hex_types: List[Terraform]) -> Optional[Hex]:
        """
        Expand from hex until a hex type is hit, returning the last hex before hit.
        """
        pass
