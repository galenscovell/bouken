from typing import Tuple

from state.biome import Biome
from state.humidity import Humidity
from state.temperature import Temperature


class IBiomeCalculator:
    """Biome calculator interface."""
    def calc_climate_modifiers(self, temperature: Temperature, humidity: Humidity) -> Tuple[float, float, int, int, int, int]:
        """Calculate climate modifiers for given temperature and humidity."""
        pass

    def pick_biome(self, elevation: float, dryness: float) -> Biome:
        """Pick a biome for the given elevation and dryness."""
        pass

    def find_biome_color(self, biome: Biome) -> Tuple[int, int, int]:
        """Get the primary color for a given biome type."""
        pass
