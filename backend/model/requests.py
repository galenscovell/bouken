"""
Defines all request model for the service.
"""

from pydantic import BaseModel
from typing import List, Optional

from backend.state.humidity import Humidity
from backend.state.temperature import Temperature


class JobCreateRequest(BaseModel):
    appId: str
    accountId: str
    userId: str
    inputs: List


class ExteriorGenerateRequest(BaseModel):
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
