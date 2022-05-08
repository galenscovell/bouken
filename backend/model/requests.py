"""
Defines all request model for the service.
"""

from pydantic import BaseModel
from typing import List, Optional

from state.humidity import Humidity
from state.temperature import Temperature


class CreateExteriorRequest(BaseModel):
    pixel_width: int
    hex_size: int
    initial_land_pct: float
    required_land_pct: float
    terraform_iterations: int
    min_island_size: int
    humidity: Humidity
    temperature: Temperature
    min_region_expansions: int
    max_region_expansions: int
    min_region_size_pct: float


class CreateInteriorRequest(BaseModel):
    pixel_width: int
    pixel_height: int
    cell_size: int
    number_rooms: int
    min_room_size: int
    max_room_size: int
    min_corridor_length: int
    max_corridor_length: int
