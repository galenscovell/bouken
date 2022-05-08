"""
Entrypoint for Bouken API.

@author GalenS <galen.scovell@gmail.com>
"""

import os
import sys

# This line is required for absolute imports to work throughout the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from model.requests import CreateExteriorRequest, CreateInteriorRequest
from model.responses import StatusResponse
from service.cache.i_cache_service import ICacheService
from service.cache.redis_service import RedisService
from service.database.i_db_service import IDbService
from service.database.sqlite_service import SqliteService
from service.generator.i_map_generator import IMapGenerator
from service.generator.exterior_map_generator import ExteriorMapGenerator
from service.generator.interior_map_generator import InteriorMapGenerator
from util.i_biome_calculator import IBiomeCalculator
from util.biome_calculator import BiomeCalculator
from util.i_hex_utility import IHexUtility
from util.hex_utils import HexUtils
from util.i_logger import ILogger
from util.logger import Logger

_logger: ILogger = Logger()
_biome_calculator: IBiomeCalculator = BiomeCalculator()
_cache_service: ICacheService = RedisService(_logger, 'localhost')
_db_service: IDbService = SqliteService(_logger)
_hex_util: IHexUtility = HexUtils()

app = FastAPI(
    title='Bouken API',
    description='',
    version='0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5050", "localhost:5050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def cache_dependency() -> ICacheService:
    global _cache_service
    if not _cache_service:
        _cache_service = None
    return _cache_service


def db_dependency() -> IDbService:
    global _db_service
    if not _db_service:
        _db_service = None
    return _db_service


def _generate_response(status_code: int, contents: dict) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=jsonable_encoder(contents))


@app.get(
    path='/status',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Status',
    description='Get service and dependencies status'
)
async def status(cache: ICacheService = Depends(cache_dependency),
                 db: IDbService = Depends(db_dependency)) -> JSONResponse:
    try:
        cache.ping()
        db.ping()
        return _generate_response(200, {'status': 200})
    except Exception as ex:
        msg = {'message': 'Error checking service health'}
        _logger.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.post(
    path='/exterior',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Generate an exterior map',
    description='Generate an exterior map'
)
async def create_exterior(req: CreateExteriorRequest,
                          cache: ICacheService = Depends(cache_dependency),
                          db: IDbService = Depends(db_dependency)) -> JSONResponse:
    try:
        generator: ExteriorMapGenerator = ExteriorMapGenerator(
            _logger, _biome_calculator, _hex_util, req)
        return _generate_response(200, {'map_guid': ''})
    except Exception as ex:
        msg = {'message': 'Error generating exterior map'}
        _logger.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.get(
    path='/exterior/{user_guid}/{map_guid}',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Get an exterior map',
    description='Get an exterior map'
)
async def get_exterior(user_guid: str,
                       map_guid: str,
                       cache: ICacheService = Depends(cache_dependency),
                       db: IDbService = Depends(db_dependency)) -> JSONResponse:
    pass


@app.post(
    path='/interior',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Generate an interior map',
    description='Generate an interior map'
)
async def create_interior(req: CreateInteriorRequest,
                          cache: ICacheService = Depends(cache_dependency),
                          db: IDbService = Depends(db_dependency)) -> JSONResponse:
    try:
        # interior_map: str = _interior_map_generator.begin(
        #     pixel_width=900,
        #     pixel_height=720,
        #     cell_size=20,
        #     number_rooms=8,
        #     min_room_size=4,
        #     max_room_size=10,
        #     min_corridor_length=2,
        #     max_corridor_length=6,
        # )
        generator: IMapGenerator = InteriorMapGenerator(_logger)
        return _generate_response(200, {'map_guid': ''})
    except Exception as ex:
        msg = {'message': 'Error generating interior map'}
        _logger.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.get(
    path='/interior/{user_guid}/{map_guid}',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Get an interior map',
    description='Get an interior map'
)
async def get_interior(user_guid: str,
                       map_guid: str,
                       cache: ICacheService = Depends(cache_dependency),
                       db: IDbService = Depends(db_dependency)) -> JSONResponse:
    pass


@app.on_event('shutdown')
def shutdown_event() -> None:
    _logger.info('Service shutdown')


@app.on_event('startup')
def startup_event() -> None:
    _logger.info('Service startup')
