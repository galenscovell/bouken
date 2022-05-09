"""
Separate listener process which works through queue to generate results.

@author GalenS <galen.scovell@gmail.com>
"""


from service.generator.exterior_map_generator import ExteriorMapGenerator
from service.generator.interior_map_generator import InteriorMapGenerator
from service.queue.i_queue import IQueue
from service.queue.gcp_queue import GCPQueue
from service.read_thru_cache.i_read_thru_cache import IReadThruCache
from service.read_thru_cache.gcp_read_thru_cache import GCPReadThruCache
from util.i_biome_calculator import IBiomeCalculator
from util.biome_calculator import BiomeCalculator
from util.i_hex_utility import IHexUtility
from util.hex_utils import HexUtils
from util.i_logger import ILogger
from util.logger import Logger


_logger: ILogger = Logger()
_biome_calculator: IBiomeCalculator = BiomeCalculator()
_hex_util: IHexUtility = HexUtils()

_cache: IReadThruCache = GCPReadThruCache(_logger)
_queue: IQueue = GCPQueue(_logger)

_exterior_generator: ExteriorMapGenerator = ExteriorMapGenerator(
    _logger, _biome_calculator, _hex_util)
_interior_map_generator: InteriorMapGenerator = InteriorMapGenerator(_logger)

if __name__ == '__main__':
    pass
